$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
. (Join-Path $repoRoot ".ai/tools/workflow_state.ps1")

function Assert-Equal {
    param([object]$Actual, [object]$Expected, [string]$Message)
    if ($Actual -ne $Expected) {
        throw "$Message Expected '$Expected', got '$Actual'."
    }
}

function Assert-Throws {
    param([scriptblock]$Action, [string]$Message)
    $threw = $false
    try {
        & $Action
    } catch {
        $threw = $true
    }
    if (-not $threw) {
        throw "$Message Expected a terminating error."
    }
}

function Assert-ThrowsMessage {
    param([scriptblock]$Action, [string]$ExpectedMessage, [string]$Message)
    $actualMessage = $null
    try {
        & $Action
    } catch {
        $actualMessage = $_.Exception.Message
    }
    if ($null -eq $actualMessage) {
        throw "$Message Expected a terminating error."
    }
    Assert-Equal $actualMessage $ExpectedMessage $Message
}

function Invoke-Git {
    param([string[]]$Arguments)
    & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Arguments -join ' ') failed with exit code $LASTEXITCODE."
    }
}

# Unit contract and transition checks.
$common = Get-WorkflowContract -RepoRoot $repoRoot -WorkflowId "common" -RequireActive
$state = New-WorkflowState -Contract $common
Add-WorkflowEvidence -State $state -Id "intake_audit" -Reference "unit:intake"
Move-WorkflowStage -Contract $common -State $state -Action "start"
Assert-Equal $state.stage "TRIAGED" "start transition failed."
Assert-Throws { Move-WorkflowStage -Contract $common -State $state -Action "continue" } "continue bypassed baseline."
Assert-Throws { Add-WorkflowEvidence -State $state -Id "intake_audit" -Reference "duplicate" } "duplicate evidence was accepted."
Add-WorkflowEvidence -State $state -Id "plan_audit" -Reference "unit:plan"
Add-WorkflowEvidence -State $state -Id "baseline_commit" -Reference "0123456789abcdef"
Move-WorkflowStage -Contract $common -State $state -Action "baseline"
Move-WorkflowStage -Contract $common -State $state -Action "continue"
Assert-Throws { Move-WorkflowStage -Contract $common -State $state -Action "ready" } "ready bypassed required evidence."
Add-WorkflowEvidence -State $state -Id "plan_conformance" -Reference ".ai/tools/tests/test_workflow_state_machine.ps1" -RepoRoot $repoRoot
Move-WorkflowStage -Contract $common -State $state -Action "ready"
Move-WorkflowStage -Contract $common -State $state -Action "close_done"
Assert-Equal $state.stage "DONE" "close transition failed."
Assert-Throws { Move-WorkflowStage -Contract $common -State $state -Action "continue" } "terminal state allowed an outbound transition."
Assert-Throws { Get-WorkflowContract -RepoRoot $repoRoot -WorkflowId "interface" -RequireActive } "PLANNED interface workflow was executable."

# Negative proof: a substantiated evidence id (bug_hunter / adversarial_tester /
# plan_conformance) must reject a reference that does not point to a real
# artifact of the repository, even if the string itself is non-empty and
# well-formed. This is Exit criteria condition (4) of
# EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE and Exit criteria condition (3) of
# PLAN_SUBSTANTIATION_PREUVES_WORKFLOW_READY: this case must fail on the code
# predating that lot, and pass afterward.
$coreEngine = Get-WorkflowContract -RepoRoot $repoRoot -WorkflowId "core-engine" -RequireActive
$substanceState = New-WorkflowState -Contract $coreEngine
Assert-Throws {
    Add-WorkflowEvidence -State $substanceState -Id "bug_hunter" -Reference "chaine_arbitraire_sans_artefact" -RepoRoot $repoRoot
} "bug_hunter accepted a reference that does not point to a real artifact."
Assert-Throws {
    Add-WorkflowEvidence -State $substanceState -Id "adversarial_tester" -Reference "unit:fake" -RepoRoot $repoRoot
} "adversarial_tester accepted a reference that does not point to a real artifact."
Assert-Throws {
    Add-WorkflowEvidence -State $substanceState -Id "plan_conformance" -Reference "unit:fake"
} "plan_conformance was accepted without -RepoRoot (fail-closed expected)."
Assert-ThrowsMessage {
    Add-WorkflowEvidence -State $substanceState -Id "plan_conformance" `
        -Reference ".ai/workflows/common/WORKFLOW.json#section-inexistante" -RepoRoot $repoRoot
} "Workflow evidence 'plan_conformance' reference anchor '#section-inexistante' (requested slug: 'section-inexistante') was not found among Markdown headings of '.ai/workflows/common/WORKFLOW.json'. Valid heading slugs: <none>." `
    "plan_conformance non-existent anchor diagnostic changed or did not fail closed."
Assert-Throws {
    Add-WorkflowEvidence -State $substanceState -Id "plan_conformance" `
        -Reference ".ai/tools/tests/test_workflow_state_machine.ps1#" -RepoRoot $repoRoot
} "plan_conformance accepted a reference with a trailing '#' and no anchor text (silent fallback to no-anchor)."
# A substantiated id with a real, existing file reference must still be accepted.
Add-WorkflowEvidence -State $substanceState -Id "bug_hunter" -Reference ".ai/tools/tests/test_workflow_state_machine.ps1" -RepoRoot $repoRoot
Assert-Equal (@($substanceState.evidence | Where-Object { $_.id -eq "bug_hunter" }).Count) 1 "valid substantiated evidence was not recorded."
# A real Markdown anchor must remain accepted after enriching the negative
# diagnostic. This also proves that valid heading discovery does not turn into
# an unconditional rejection path.
Add-WorkflowEvidence -State $substanceState -Id "adversarial_tester" -Reference ".ai/README.md#roles" -RepoRoot $repoRoot
Assert-Equal (@($substanceState.evidence | Where-Object { $_.id -eq "adversarial_tester" }).Count) 1 "valid anchored evidence was not recorded."
# A Markdown file with headings must expose normalized, sorted choices while
# keeping the requested missing anchor rejected.
$diagnosticState = New-WorkflowState -Contract $coreEngine
$diagnosticMessage = $null
try {
    Add-WorkflowEvidence -State $diagnosticState -Id "plan_conformance" `
        -Reference ".ai/README.md#section-inexistante" -RepoRoot $repoRoot
} catch {
    $diagnosticMessage = $_.Exception.Message
}
if ($null -eq $diagnosticMessage) {
    throw "missing Markdown anchor was accepted instead of producing suggestions."
}
if ($diagnosticMessage -notmatch [regex]::Escape("requested slug: 'section-inexistante'")) {
    throw "missing-anchor diagnostic omitted the requested normalized slug."
}
if ($diagnosticMessage -notmatch [regex]::Escape("Valid heading slugs: ")) {
    throw "missing-anchor diagnostic omitted valid heading slugs."
}
if ($diagnosticMessage -notmatch "Valid heading slugs: [^.]*cockpit-ia-ebta[^.]*roles") {
    throw "missing-anchor diagnostic did not expose sorted known heading slugs."
}
# Non-substantiated ids remain unaffected by the new check (no RepoRoot required).
Add-WorkflowEvidence -State $substanceState -Id "intake_audit" -Reference "unit:intake"

$malformed = Get-Content -Raw (Join-Path $repoRoot ".ai/workflows/common/WORKFLOW.json") | ConvertFrom-Json
$malformed.stages = @($malformed.stages) + @($malformed.stages[0])
Assert-Throws { Assert-WorkflowContract -Contract $malformed -ExpectedId "common" } "duplicate contract stage was accepted."
$corruptState = New-WorkflowState -Contract $common
$corruptState.evidence = @(
    [pscustomobject]@{ id = "intake_audit"; reference = "first"; recorded_at = "2026-07-30" },
    [pscustomobject]@{ id = "intake_audit"; reference = "second"; recorded_at = "2026-07-30" }
)
Assert-Throws { Move-WorkflowStage -Contract $common -State $corruptState -Action "start" } "duplicate persisted evidence was accepted."

# Generated Mermaid must be stable and derived from the JSON contracts.
$generator = Join-Path $repoRoot ".ai/tools/generate_workflow_mermaid.ps1"
& $generator
$firstHashes = @{}
foreach ($path in Get-ChildItem (Join-Path $repoRoot ".ai/workflows") -Recurse -Filter "WORKFLOW.mmd") {
    $firstHashes[$path.FullName] = (Get-FileHash -Algorithm SHA256 -LiteralPath $path.FullName).Hash
}
& $generator
foreach ($path in Get-ChildItem (Join-Path $repoRoot ".ai/workflows") -Recurse -Filter "WORKFLOW.mmd") {
    Assert-Equal (Get-FileHash -Algorithm SHA256 -LiteralPath $path.FullName).Hash $firstHashes[$path.FullName] "Mermaid generation drifted for '$($path.FullName)'."
}

# Backend integration in an isolated disposable Git repository.
$tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
$tempRepo = [System.IO.Path]::Combine($tempBase, "ebta-workflow-test-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tempRepo | Out-Null
try {
    New-Item -ItemType Directory -Force -Path (Join-Path $tempRepo ".ai/tools") | Out-Null
    New-Item -ItemType Directory -Force -Path (Join-Path $tempRepo ".ai/workflows") | Out-Null
    New-Item -ItemType Directory -Force -Path (Join-Path $tempRepo ".ai/backlog/annexes") | Out-Null
    New-Item -ItemType Directory -Force -Path (Join-Path $tempRepo "0 - HUMAN START HERE") | Out-Null
    Copy-Item -LiteralPath (Join-Path $repoRoot ".ai/tools/plan.ps1") -Destination (Join-Path $tempRepo ".ai/tools/plan.ps1")
    Copy-Item -LiteralPath (Join-Path $repoRoot ".ai/tools/workflow_state.ps1") -Destination (Join-Path $tempRepo ".ai/tools/workflow_state.ps1")
    Copy-Item -LiteralPath (Join-Path $repoRoot ".ai/workflows/common") -Destination (Join-Path $tempRepo ".ai/workflows/common") -Recurse
    Copy-Item -LiteralPath (Join-Path $repoRoot ".ai/workflows/core-engine") -Destination (Join-Path $tempRepo ".ai/workflows/core-engine") -Recurse
    Copy-Item -LiteralPath (Join-Path $repoRoot ".ai/workflows/interface") -Destination (Join-Path $tempRepo ".ai/workflows/interface") -Recurse

    @'
{
  "schema_version": "1.2.0",
  "updated_at": "2026-07-30",
  "active_workstream_id": null,
  "workstreams": [
    {
      "id": "LEGACY_DONE",
      "classification": "GOVERNANCE",
      "status": "DONE",
      "lifecycle": "DONE",
      "source_path": ".ai/archive/legacy.md"
    }
  ]
}
'@ | Set-Content -Encoding UTF8 (Join-Path $tempRepo ".ai/checkpoint.json")

    $planText = @'
# Test plan

## Bandeau de statut
Cold start.
## Carte d'execution IA
Bounded execution.
## Triage
| Field | Value |
|---|---|
| Track | annexe |
| Lifecycle | TRIAGED |
| Type de chantier | SINGLE |
| Scope | isolated test |
| Non-goals | production |
| Source | test |
| Exit criteria | state DONE |
## Contexte obligatoire
Read the local contract.
## Etat des lieux
No competing authority.
## Decision d'architecture
Use the JSON contract.
## Decoupage en phases
One integration phase.
## NO GO
No protocol change.
## Verification a chaque etape
Run this test.
## Journal des decisions humaines
Test fixture only.
## Definition of Done
- [ ] State reaches DONE.
'@
    $draftPath = Join-Path $tempRepo "0 - HUMAN START HERE/draft.md"
    $rewrittenPath = Join-Path $tempRepo ".ai/backlog/annexes/PLAN_TEST.md"
    "raw draft" | Set-Content -Encoding UTF8 $draftPath
    $planText | Set-Content -Encoding UTF8 $rewrittenPath

    Push-Location $tempRepo
    try {
        Invoke-Git @("init", "-q")
        Invoke-Git @("config", "user.email", "workflow-test@example.invalid")
        Invoke-Git @("config", "user.name", "Workflow Test")
        $planBackend = Join-Path $tempRepo ".ai/tools/plan.ps1"

        & $planBackend migrate-workflows
        $checkpoint = Get-Content -Raw ".ai/checkpoint.json" | ConvertFrom-Json
        Assert-Equal $checkpoint.schema_version "1.3.0" "migration did not bump checkpoint schema."
        Assert-Equal $checkpoint.workstreams[0].workflow.stage "DONE" "legacy terminal stage was not preserved."
        Assert-Equal $checkpoint.workstreams[0].workflow.evidence[0].id "legacy_import" "migration evidence is missing."

        Assert-Throws {
            & $planBackend start -Path $draftPath -RewrittenPath $rewrittenPath -Id "PLAN_TEST" `
                -Classification IMPLEMENTATION_DETAIL -Workflow common -Audited `
                -IntakeAuditPasses 2 -IntakeAuditEvidence "test:intake"
        } "backend accepted a classification/workflow mismatch."
        & $planBackend start -Path $draftPath -RewrittenPath $rewrittenPath -Id "PLAN_TEST" -Audited -IntakeAuditPasses 2 -IntakeAuditEvidence "test:intake"
        Assert-Throws { & $planBackend continue -Id "PLAN_TEST" } "backend continue bypassed baseline."

        Invoke-Git @("add", "-A")
        Invoke-Git @("commit", "-q", "-m", "test: baseline")
        $baselineCommit = (& git rev-parse HEAD).Trim()
        if ($LASTEXITCODE -ne 0) {
            throw "Unable to resolve test baseline commit."
        }
        Assert-Throws {
            & $planBackend baseline -Id "PLAN_TEST" -PlanAuditPasses 2 `
                -PlanAuditEvidence "test:plan" -BaselineCommit "HEAD"
        } "backend accepted a non-SHA baseline reference."
        & $planBackend baseline -Id "PLAN_TEST" -PlanAuditPasses 2 -PlanAuditEvidence "test:plan" -BaselineCommit $baselineCommit
        & $planBackend continue -Id "PLAN_TEST"
        Assert-Throws { & $planBackend close -Id "PLAN_TEST" -Outcome DONE } "backend close bypassed READY_TO_CLOSE."
        Assert-Throws { & $planBackend ready -Id "PLAN_TEST" } "backend ready bypassed conformance evidence."
        Assert-Throws {
            & $planBackend ready -Id "PLAN_TEST" -Evidence "plan_conformance=test:report"
        } "backend ready accepted a plan_conformance reference that does not point to a real artifact."
        & $planBackend ready -Id "PLAN_TEST" -Evidence "plan_conformance=.ai/backlog/annexes/PLAN_TEST.md"
        & $planBackend close -Id "PLAN_TEST" -Outcome DONE -Reason "integration test complete"

        $checkpoint = Get-Content -Raw ".ai/checkpoint.json" | ConvertFrom-Json
        $completed = @($checkpoint.workstreams | Where-Object { $_.id -eq "PLAN_TEST" })[0]
        Assert-Equal $completed.workflow.stage "DONE" "backend did not persist terminal workflow state."
        Assert-Equal $completed.lifecycle "DONE" "backend did not preserve lifecycle compatibility."
    } finally {
        Pop-Location
    }
} finally {
    $resolvedTempRepo = [System.IO.Path]::GetFullPath($tempRepo)
    if (-not $resolvedTempRepo.StartsWith($tempBase, [System.StringComparison]::OrdinalIgnoreCase) -or
        -not ([System.IO.Path]::GetFileName($resolvedTempRepo)).StartsWith("ebta-workflow-test-")) {
        throw "Refusing unsafe test cleanup path: $resolvedTempRepo"
    }
    if (Test-Path -LiteralPath $resolvedTempRepo) {
        Remove-Item -LiteralPath $resolvedTempRepo -Recurse -Force
    }
}

Write-Host "workflow_state_machine=PASS"
