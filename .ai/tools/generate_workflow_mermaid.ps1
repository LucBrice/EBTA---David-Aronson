param(
    [string]$RepoRoot
)

$ErrorActionPreference = "Stop"

if (-not $RepoRoot) {
    $RepoRoot = git rev-parse --show-toplevel 2>$null
}
if (-not $RepoRoot) {
    throw "Repository root not found."
}
$RepoRoot = (Resolve-Path $RepoRoot).Path
$workflowRoot = Join-Path $RepoRoot ".ai/workflows"

foreach ($contractFile in (Get-ChildItem $workflowRoot -Recurse -File -Filter "WORKFLOW.json" | Sort-Object FullName)) {
    $contract = Get-Content -Raw $contractFile.FullName | ConvertFrom-Json
    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add("%% GENERATED FROM WORKFLOW.json - DO NOT EDIT")
    $lines.Add("stateDiagram-v2")
    $lines.Add("    direction LR")

    foreach ($stage in $contract.stages) {
        $lines.Add("    state `"$($stage.id)`" as $($stage.id)")
    }
    foreach ($transition in $contract.transitions) {
        $label = [string]$transition.action
        $required = @($transition.required_evidence)
        if ($required.Count -gt 0) {
            $label += " [" + ($required -join ", ") + "]"
        }
        $lines.Add("    $($transition.from) --> $($transition.to): $label")
    }

    $outputPath = Join-Path $contractFile.Directory.FullName "WORKFLOW.mmd"
    $text = ($lines -join [Environment]::NewLine) + [Environment]::NewLine
    [System.IO.File]::WriteAllText($outputPath, $text, [System.Text.UTF8Encoding]::new($false))
    Write-Host "Generated: $outputPath"
}
