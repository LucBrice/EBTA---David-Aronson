function Get-WorkflowContract {
    param(
        [Parameter(Mandatory = $true)][string]$RepoRoot,
        [Parameter(Mandatory = $true)][string]$WorkflowId,
        [switch]$RequireActive
    )

    if ($WorkflowId -notmatch "^[a-z][a-z0-9-]*$") {
        throw "Invalid workflow id: '$WorkflowId'."
    }
    $path = Join-Path $RepoRoot ".ai/workflows/$WorkflowId/WORKFLOW.json"
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Workflow contract not found: $path"
    }
    $contract = Get-Content -Raw -LiteralPath $path | ConvertFrom-Json
    Assert-WorkflowContract -Contract $contract -ExpectedId $WorkflowId
    if ($RequireActive -and $contract.status -ne "ACTIVE") {
        throw "Workflow '$WorkflowId' is '$($contract.status)', not ACTIVE."
    }
    return $contract
}

function Assert-WorkflowContract {
    param(
        [Parameter(Mandatory = $true)][object]$Contract,
        [string]$ExpectedId
    )

    if ($ExpectedId -and $Contract.workflow_id -ne $ExpectedId) {
        throw "Workflow id mismatch: expected '$ExpectedId', got '$($Contract.workflow_id)'."
    }
    $stageIds = @($Contract.stages | ForEach-Object { [string]$_.id })
    if ($stageIds.Count -eq 0 -or @($stageIds | Select-Object -Unique).Count -ne $stageIds.Count) {
        throw "Workflow '$($Contract.workflow_id)' has missing or duplicate stages."
    }
    if ($Contract.initial_stage -notin $stageIds) {
        throw "Workflow '$($Contract.workflow_id)' initial stage '$($Contract.initial_stage)' is undeclared."
    }
    foreach ($terminal in @($Contract.terminal_stages)) {
        if ($terminal -notin $stageIds) {
            throw "Workflow '$($Contract.workflow_id)' terminal stage '$terminal' is undeclared."
        }
        $declared = @($Contract.stages | Where-Object { $_.id -eq $terminal })
        if ($declared.Count -ne 1 -or -not $declared[0].terminal) {
            throw "Workflow '$($Contract.workflow_id)' terminal stage '$terminal' is not marked terminal."
        }
    }
    foreach ($stage in @($Contract.stages)) {
        $listedTerminal = $stage.id -in @($Contract.terminal_stages)
        if ([bool]$stage.terminal -ne $listedTerminal) {
            throw "Workflow '$($Contract.workflow_id)' stage '$($stage.id)' has an inconsistent terminal marker."
        }
    }
    $initial = @($Contract.stages | Where-Object { $_.id -eq $Contract.initial_stage })[0]
    if ($Contract.status -eq "ACTIVE" -and $initial.terminal) {
        throw "ACTIVE workflow '$($Contract.workflow_id)' cannot start in a terminal stage."
    }
    if ($Contract.status -eq "PLANNED" -and @($Contract.transitions).Count -gt 0) {
        throw "PLANNED workflow '$($Contract.workflow_id)' cannot declare executable transitions."
    }

    $transitionKeys = New-Object System.Collections.Generic.List[string]
    foreach ($transition in @($Contract.transitions)) {
        if ($transition.from -notin $stageIds -or $transition.to -notin $stageIds) {
            throw "Workflow '$($Contract.workflow_id)' transition '$($transition.action)' references an undeclared stage."
        }
        if ($transition.from -in @($Contract.terminal_stages)) {
            throw "Workflow '$($Contract.workflow_id)' defines an outbound transition from terminal stage '$($transition.from)'."
        }
        $key = "$($transition.from)|$($transition.action)"
        if ($key -in $transitionKeys) {
            throw "Workflow '$($Contract.workflow_id)' has duplicate transition '$key'."
        }
        $requiredEvidence = @($transition.required_evidence)
        if (@($requiredEvidence | Select-Object -Unique).Count -ne $requiredEvidence.Count) {
            throw "Workflow '$($Contract.workflow_id)' transition '$key' repeats a required evidence id."
        }
        $transitionKeys.Add($key)
    }
}

function Assert-WorkflowState {
    param(
        [Parameter(Mandatory = $true)][object]$Contract,
        [Parameter(Mandatory = $true)][object]$State
    )

    if ($State.id -ne $Contract.workflow_id -or $State.contract_version -ne $Contract.contract_version) {
        throw "Workflow state contract mismatch for '$($State.id)'."
    }
    if (@($Contract.stages | Where-Object { $_.id -eq $State.stage }).Count -ne 1) {
        throw "Workflow '$($State.id)' state references undeclared stage '$($State.stage)'."
    }
    $evidenceIds = New-Object System.Collections.Generic.List[string]
    foreach ($entry in @($State.evidence)) {
        if ($entry.id -notmatch "^[a-z][a-z0-9_]*$" -or [string]::IsNullOrWhiteSpace([string]$entry.reference)) {
            throw "Workflow '$($State.id)' contains malformed evidence."
        }
        if ($entry.recorded_at -notmatch "^\d{4}-\d{2}-\d{2}$") {
            throw "Workflow '$($State.id)' evidence '$($entry.id)' has an invalid recorded_at date."
        }
        if ($entry.id -in $evidenceIds) {
            throw "Workflow '$($State.id)' repeats evidence id '$($entry.id)'."
        }
        $evidenceIds.Add([string]$entry.id)
    }
}

function New-WorkflowState {
    param([Parameter(Mandatory = $true)][object]$Contract)

    return [pscustomobject][ordered]@{
        id = [string]$Contract.workflow_id
        contract_version = [string]$Contract.contract_version
        stage = [string]$Contract.initial_stage
        evidence = @()
    }
}

function Get-SubstantiatedEvidenceIds {
    # IDs d'evidence dont la reference doit pointer vers un artefact reel du
    # depot (fichier existant, ancre Markdown verifiee si fournie), au lieu
    # d'accepter n'importe quelle chaine non vide. Cible exactement le risque
    # identifie par l'audit robustesse 2026-08-07 (recommandation 1) : ces
    # trois IDs sont les preuves exigees par la transition "ready" du
    # workflow core-engine avant /close. Ne pas etendre a intake_audit/
    # plan_audit/baseline_commit/legacy_import, dont les formats (SHA,
    # phrase libre) ne sont pas des chemins de fichier. Fonction plutot que
    # variable de script : evite toute ambiguite de portee sous
    # dot-sourcing repete (ce fichier est source par plan.ps1 et par le
    # harnais de test).
    return @("bug_hunter", "adversarial_tester", "plan_conformance")
}

function ConvertTo-HeadingSlug {
    # Approxime (best-effort) l'algorithme de slug d'ancre Markdown de
    # GitHub : minuscule, retrait de la ponctuation hors espace/tiret,
    # espaces -> tirets, tirets multiples reduits. Ne gere pas les suffixes
    # de doublon ("-1", "-2") ni une translitteration fine des caracteres
    # accentues : caveat documente, pas une garantie d'exactitude totale.
    param([Parameter(Mandatory = $true)][string]$Text)

    $slug = $Text.ToLowerInvariant()
    $slug = ($slug -replace "[^a-z0-9\s\-]", "")
    $slug = ($slug -replace "\s+", "-")
    $slug = ($slug -replace "-{2,}", "-")
    return $slug.Trim("-")
}

function Test-EvidenceReferenceSubstance {
    # Valide qu'une reference d'evidence pointe vers un artefact reel :
    # decoupe "chemin#ancre", exige un chemin relatif au depot (pas de
    # racine absolue, pas de "..") qui existe comme fichier, et, si une
    # ancre est fournie, verifie (best-effort) qu'elle correspond a un titre
    # Markdown du fichier. Leve une erreur descriptive sinon. N'evalue
    # jamais le contenu semantique de l'artefact : preuve d'existence
    # uniquement, pas preuve de contenu.
    param(
        [Parameter(Mandatory = $true)][string]$RepoRoot,
        [Parameter(Mandatory = $true)][string]$Id,
        [Parameter(Mandatory = $true)][string]$Reference
    )

    $hashIndex = $Reference.IndexOf("#")
    if ($hashIndex -ge 0) {
        $relativePath = $Reference.Substring(0, $hashIndex)
        $anchor = $Reference.Substring($hashIndex + 1)
    } else {
        $relativePath = $Reference
        $anchor = $null
    }

    if ([string]::IsNullOrWhiteSpace($relativePath)) {
        throw "Workflow evidence '$Id' reference must include a file path before any '#' anchor: '$Reference'."
    }
    if ([System.IO.Path]::IsPathRooted($relativePath) -or $relativePath -match "\.\.") {
        throw "Workflow evidence '$Id' reference must be a repo-relative path without '..' traversal: '$Reference'."
    }

    if ($hashIndex -ge 0 -and [string]::IsNullOrWhiteSpace($anchor)) {
        # A trailing "#" with nothing after it signals an anchor was
        # intended but left empty. Silently treating this like "no anchor"
        # would accept a malformed reference instead of rejecting it -
        # reject explicitly rather than fall back.
        throw "Workflow evidence '$Id' reference has a '#' with no anchor text after it: '$Reference'."
    }

    $fullPath = Join-Path $RepoRoot ($relativePath -replace "/", "\")
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        throw "Workflow evidence '$Id' reference does not point to an existing file: '$relativePath' (from '$Reference')."
    }

    if (-not [string]::IsNullOrWhiteSpace($anchor)) {
        $content = Get-Content -Raw -LiteralPath $fullPath
        $targetSlug = (ConvertTo-HeadingSlug $anchor)
        $found = $false
        $validSlugs = New-Object System.Collections.Generic.List[string]
        foreach ($line in ($content -split "`r?`n")) {
            if ($line -match "^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$") {
                $headingSlug = (ConvertTo-HeadingSlug $Matches[1])
                if (-not [string]::IsNullOrWhiteSpace($headingSlug)) {
                    $validSlugs.Add($headingSlug)
                }
                if ($headingSlug -eq $targetSlug) {
                    $found = $true
                    break
                }
            }
        }
        if (-not $found) {
            $sortedValidSlugs = @($validSlugs | Sort-Object -Unique)
            $validSlugSummary = if ($sortedValidSlugs.Count -gt 0) {
                $sortedValidSlugs -join ", "
            } else {
                "<none>"
            }
            throw ("Workflow evidence '$Id' reference anchor '#$anchor' " +
                "(requested slug: '$targetSlug') was not found among Markdown headings of " +
                "'$relativePath'. Valid heading slugs: $validSlugSummary.")
        }
    }
}

function Add-WorkflowEvidence {
    param(
        [Parameter(Mandatory = $true)][object]$State,
        [Parameter(Mandatory = $true)][string]$Id,
        [Parameter(Mandatory = $true)][string]$Reference,
        [string]$RecordedAt = (Get-Date -Format "yyyy-MM-dd"),
        [string]$RepoRoot
    )

    if ($Id -notmatch "^[a-z][a-z0-9_]*$") {
        throw "Invalid workflow evidence id: '$Id'."
    }
    if ([string]::IsNullOrWhiteSpace($Reference)) {
        throw "Workflow evidence '$Id' requires a non-empty reference."
    }
    if (@($State.evidence | Where-Object { $_.id -eq $Id }).Count -gt 0) {
        throw "Workflow evidence id '$Id' is already recorded."
    }
    if ($Id -in (Get-SubstantiatedEvidenceIds)) {
        if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
            throw "Workflow evidence '$Id' requires -RepoRoot to validate that its reference points to a real artifact."
        }
        Test-EvidenceReferenceSubstance -RepoRoot $RepoRoot -Id $Id -Reference $Reference
    }
    $entry = [pscustomobject][ordered]@{
        id = $Id
        reference = $Reference
        recorded_at = $RecordedAt
    }
    $State.evidence = @($State.evidence) + @($entry)
}

function Add-WorkflowEvidenceArguments {
    param(
        [Parameter(Mandatory = $true)][object]$State,
        [string[]]$EvidenceArguments,
        [string]$RepoRoot
    )

    foreach ($item in @($EvidenceArguments)) {
        if ($item -notmatch "^([a-z][a-z0-9_]*)=(.+)$") {
            throw "Workflow evidence must use id=reference, got '$item'."
        }
        Add-WorkflowEvidence -State $State -Id $Matches[1] -Reference $Matches[2] -RepoRoot $RepoRoot
    }
}

function Move-WorkflowStage {
    param(
        [Parameter(Mandatory = $true)][object]$Contract,
        [Parameter(Mandatory = $true)][object]$State,
        [Parameter(Mandatory = $true)][string]$Action
    )

    Assert-WorkflowState -Contract $Contract -State $State
    $matches = @($Contract.transitions | Where-Object {
        $_.from -eq $State.stage -and $_.action -eq $Action
    })
    if ($matches.Count -ne 1) {
        throw "Workflow '$($State.id)' forbids action '$Action' from stage '$($State.stage)'."
    }
    $available = @($State.evidence | ForEach-Object { [string]$_.id })
    $missing = @($matches[0].required_evidence | Where-Object { $_ -notin $available })
    if ($missing.Count -gt 0) {
        throw "Workflow '$($State.id)' action '$Action' lacks evidence: $($missing -join ', ')."
    }
    $State.stage = [string]$matches[0].to
}

function Get-LegacyWorkflowId {
    param([Parameter(Mandatory = $true)][string]$Classification)

    if ($Classification -in @("IMPLEMENTATION_DETAIL", "CONTRACT_ENCODING", "TEST_FIXTURE", "ADAPTER_MAPPING")) {
        return "core-engine"
    }
    return "common"
}

function Get-LegacyWorkflowStage {
    param([Parameter(Mandatory = $true)][object]$Workstream)

    if ($Workstream.lifecycle -in @("DONE", "BLOCKED", "REJECTED", "SUPERSEDED")) {
        return [string]$Workstream.lifecycle
    }
    if ($Workstream.lifecycle -eq "ACTIVE" -or $Workstream.status -eq "ACTIVE") {
        return "ACTIVE"
    }
    return "TRIAGED"
}
