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

function Add-WorkflowEvidence {
    param(
        [Parameter(Mandatory = $true)][object]$State,
        [Parameter(Mandatory = $true)][string]$Id,
        [Parameter(Mandatory = $true)][string]$Reference,
        [string]$RecordedAt = (Get-Date -Format "yyyy-MM-dd")
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
        [string[]]$EvidenceArguments
    )

    foreach ($item in @($EvidenceArguments)) {
        if ($item -notmatch "^([a-z][a-z0-9_]*)=(.+)$") {
            throw "Workflow evidence must use id=reference, got '$item'."
        }
        Add-WorkflowEvidence -State $State -Id $Matches[1] -Reference $Matches[2]
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
