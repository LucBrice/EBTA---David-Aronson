<# 
Backend mecanique du cockpit IA.
Interface humaine attendue : /start, /continue, /close dans l'IA.
Ce script ne remplace pas l'audit semantique ; start exige -Audited apres
structuration du plan par l'IA.
#>

param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet("start", "continue", "close")]
    [string]$Action,

    [string]$Path,
    [string]$Id,
    [string]$Title,

    [ValidateSet("mainline", "annexe", "fix")]
    [string]$Track = "annexe",

    [ValidateSet(
        "GOVERNANCE",
        "IMPLEMENTATION_DETAIL",
        "CONTRACT_ENCODING",
        "TEST_FIXTURE",
        "ADAPTER_MAPPING",
        "DOCUMENTATION_CLARIFICATION_NEEDED",
        "NORMATIVE_CHANGE_REQUIRED"
    )]
    [string]$Classification = "GOVERNANCE",

    [ValidateSet("DONE", "REJECTED", "SUPERSEDED", "BLOCKED")]
    [string]$Outcome = "DONE",

    [switch]$Audited,

    [string]$Reason = "Updated via .ai/tools/plan.ps1"
)

$ErrorActionPreference = "Stop"

function Resolve-RepoRoot {
    $root = (git rev-parse --show-toplevel 2>$null)
    if (-not $root) {
        throw "Impossible de trouver la racine git. Lance la commande depuis le repo."
    }
    return (Resolve-Path $root).Path
}

function ConvertTo-RepoPath {
    param([string]$AbsolutePath, [string]$RepoRoot)
    # PS 5.1 compat
    $relative = $AbsolutePath.Replace($RepoRoot, "").TrimStart("\").TrimStart("/")
    return ($relative -replace "\\", "/")
}

function ConvertTo-PlanId {
    param([string]$Value)
    $idValue = [System.IO.Path]::GetFileNameWithoutExtension($Value)
    $idValue = ($idValue -replace "[^A-Za-z0-9]+", "_").Trim("_").ToUpperInvariant()
    if (-not $idValue) {
        throw "Impossible de deduire un id depuis '$Value'. Utilise -Id."
    }
    return $idValue
}

function Get-BacklogFolder {
    param([string]$Track)
    switch ($Track) {
        "mainline" { return ".ai/backlog/mainline" }
        "annexe" { return ".ai/backlog/annexes" }
        "fix" { return ".ai/backlog/fixes" }
    }
}

function Read-Checkpoint {
    param([string]$CheckpointPath)
    return Get-Content -Raw $CheckpointPath | ConvertFrom-Json
}

function Write-Checkpoint {
    param([object]$Checkpoint, [string]$CheckpointPath)
    $Checkpoint.updated_at = (Get-Date -Format "yyyy-MM-dd")
    $Checkpoint | ConvertTo-Json -Depth 20 | Set-Content -Encoding UTF8 $CheckpointPath
}

function Find-Workstream {
    param([object]$Checkpoint, [string]$WorkstreamId)
    return @($Checkpoint.workstreams | Where-Object { $_.id -eq $WorkstreamId })
}


function Assert-PlanAuditReady {
    param([string]$PlanPath)
    $content = Get-Content -Raw $PlanPath
    $missing = @()

    if ($content -notmatch "(?m)^-\s+\[[ xX]\]") {
        $missing += "checklist Markdown"
    }
    foreach ($label in @("Track", "Lifecycle", "Scope", "Non-goals", "Source", "Exit criteria")) {
        if ($content -notmatch "(?im)(^|\|)\s*$([regex]::Escape($label))\s*(\||:|$)") {
            $missing += $label
        }
    }

    if ($missing.Count -gt 0) {
        throw "Action start: plan non pret pour routage. Sections manquantes: $($missing -join ', '). Auditer et structurer le plan avant start."
    }
}

function Set-ActiveWorkstream {
    param([object]$Checkpoint, [object]$Workstream)
    # Point active_workstream_id at the new active workstream.
    # Clear is_active on all others first, then set on the target.
    foreach ($ws in $Checkpoint.workstreams) {
        $ws | Add-Member -NotePropertyName "is_active" -NotePropertyValue $false -Force
    }
    $Workstream | Add-Member -NotePropertyName "is_active" -NotePropertyValue $true -Force
    $Checkpoint.active_workstream_id = $Workstream.id
}

$repoRoot = Resolve-RepoRoot
$checkpointPath = Join-Path $repoRoot ".ai/checkpoint.json"
$checkpoint = Read-Checkpoint $checkpointPath

switch ($Action) {
    "start" {
        if (-not $Path) {
            throw "Action start: utilise -Path pour indiquer le plan depose dans 0 - HUMAN START HERE/."
        }
        if (-not $Audited) {
            throw "Action start: audit IA requis avant routage. Utilise /start via l'IA, ou relance avec -Audited apres audit explicite."
        }

        $source = Resolve-Path $Path
        $sourcePath = $source.Path
        $sourceRepoPath = ConvertTo-RepoPath $sourcePath $repoRoot
        if (-not $sourceRepoPath.StartsWith("0 - HUMAN START HERE/")) {
            throw "Action start: le plan doit partir de 0 - HUMAN START HERE/."
        }
        Assert-PlanAuditReady $sourcePath

        if (-not $Id) {
            $Id = ConvertTo-PlanId $sourcePath
        }
        if (-not $Title) {
            $Title = [System.IO.Path]::GetFileNameWithoutExtension($sourcePath)
        }
        if (@(Find-Workstream $checkpoint $Id).Count -gt 0) {
            throw "Un chantier avec id '$Id' existe deja dans .ai/checkpoint.json."
        }

        $targetFolder = Join-Path $repoRoot (Get-BacklogFolder $Track)
        New-Item -ItemType Directory -Force $targetFolder | Out-Null
        $targetPath = Join-Path $targetFolder ([System.IO.Path]::GetFileName($sourcePath))
        if (Test-Path $targetPath) {
            throw "Le fichier cible existe deja: $targetPath"
        }
        Move-Item -LiteralPath $sourcePath -Destination $targetPath
        $targetRepoPath = ConvertTo-RepoPath $targetPath $repoRoot

        $workstream = [ordered]@{
            id = $Id
            title = $Title
            track = $Track
            status = "PENDING"
            lifecycle = "TRIAGED"
            classification = $Classification
            source_path = $targetRepoPath
            active_runtime_path = $null
            opened_at = (Get-Date -Format "yyyy-MM-dd")
            last_moved_at = (Get-Date -Format "yyyy-MM-dd")
            routing_decision = $Track
            routing_reason = $Reason
            moved_by = "ai"
            blocks_mainline = ($Track -eq "mainline")
            advances_mainline = ($Track -eq "mainline")
            closure_reason = $null
            non_goals = @()
        }

        $checkpoint.workstreams = @($checkpoint.workstreams) + @($workstream)
        Write-Checkpoint $checkpoint $checkpointPath
        Write-Host "Plan demarre: $Id -> $targetRepoPath"
    }

    "continue" {
        if (-not $Id) {
            throw "Action continue: utilise -Id pour choisir le chantier."
        }
        $foundWorkstreams = @(Find-Workstream $checkpoint $Id)
        if ($foundWorkstreams.Count -ne 1) {
            throw "Chantier introuvable ou ambigu: $Id"
        }
        $workstream = $foundWorkstreams[0]
        $workstream.status = "ACTIVE"
        $workstream.lifecycle = "ACTIVE"
        $workstream.last_moved_at = (Get-Date -Format "yyyy-MM-dd")
        if ($Reason) {
            $workstream.routing_reason = $Reason
        }
        Set-ActiveWorkstream $checkpoint $workstream
        Write-Checkpoint $checkpoint $checkpointPath
        Write-Host "Plan actif: $Id"
    }

    "close" {
        if (-not $Id) {
            throw "Action close: utilise -Id pour choisir le chantier."
        }
        $foundWorkstreams = @(Find-Workstream $checkpoint $Id)
        if ($foundWorkstreams.Count -ne 1) {
            throw "Chantier introuvable ou ambigu: $Id"
        }
        $workstream = $foundWorkstreams[0]

        $sourcePath = Join-Path $repoRoot ($workstream.source_path -replace "/", "\")
        if (Test-Path $sourcePath) {
            $archiveFolder = Join-Path $repoRoot ".ai/archive"
            New-Item -ItemType Directory -Force $archiveFolder | Out-Null
            $archiveName = "{0}_{1}" -f (Get-Date -Format "yyyyMMdd"), ([System.IO.Path]::GetFileName($sourcePath))
            $archivePath = Join-Path $archiveFolder $archiveName
            if (Test-Path $archivePath) {
                throw "Le fichier archive existe deja: $archivePath"
            }
            Move-Item -LiteralPath $sourcePath -Destination $archivePath
            $workstream.source_path = ConvertTo-RepoPath $archivePath $repoRoot
        }

        if ($Outcome -eq "BLOCKED") {
            $workstream.status = "BLOCKED"
            $workstream.lifecycle = "BLOCKED"
        } else {
            $workstream.status = "DONE"
            $workstream.lifecycle = $Outcome
        }
        $workstream.last_moved_at = (Get-Date -Format "yyyy-MM-dd")
        $workstream.closure_reason = $Reason

        if ($checkpoint.active_workstream_id -eq $Id) {
            # Closed workstream was the active one — clear the pointer.
            $checkpoint.active_workstream_id = $null
            $workstream | Add-Member -NotePropertyName "is_active" -NotePropertyValue $false -Force
        }

        Write-Checkpoint $checkpoint $checkpointPath
        Write-Host "Plan cloture: $Id -> $($workstream.lifecycle)"
    }
}
