<#
Backend mecanique du cockpit IA.
Interface humaine attendue : /start, /continue, /close dans l'IA.
Ce script ne remplace pas l'audit semantique ; start exige -Audited apres
structuration du plan par l'IA.

Contrat "start" (deux fichiers distincts, jamais un seul deplace) :
  -Path          brouillon humain original dans "0 - HUMAN START HERE/".
                 Jamais reecrit. Archive tel quel sous
                 "0 - HUMAN START HERE/archive/" pour tracabilite.
  -RewrittenPath plan integralement reecrit par l'IA selon
                 .ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md, deja ecrit par
                 l'IA dans le dossier backlog cible (mainline/annexes/fixes)
                 AVANT d'appeler ce script. C'est ce fichier qui devient
                 source_path du chantier ; -Path original devient
                 original_draft_path (archive).
#>

param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet("start", "continue", "close")]
    [string]$Action,

    [string]$Path,
    [string]$RewrittenPath,
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

    # Structure enrichie exigee par .ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md.
    # Ce n'est pas une simple formalite : chaque phrase-cle ci-dessous doit
    # apparaitre reellement reecrite pour CE plan (pas copiee telle quelle du
    # gabarit) avant que start ne l'accepte.
    $templateSections = [ordered]@{
        "Bandeau de statut"                  = "Verifier si un chantier ou un verrou de gouvernance couvre deja ce perimetre."
        "Contexte obligatoire"                = "Lister les documents qu'une IA froide doit lire avant de coder."
        "Etat des lieux"                      = "Distinguer ce qui existe deja (a reutiliser) de ce qui manque reellement."
        "Decision d'architecture"             = "Expliquer pourquoi cette architecture, pas seulement ce qu'elle est."
        "Decoupage en phases"                 = "Separer phases de deblocage et phases d'implementation, chacune verifiable."
        "NO GO"                               = "Lister les actions explicitement interdites, verifiables en revue de diff."
        "Verification a chaque etape"         = "Donner la commande exacte de validation de chaque phase."
        "Journal des decisions humaines"      = "Tracer les autorisations humaines explicites, jamais deduites."
        "Definition of Done"                  = "Definir une sortie binaire et verifiable du chantier."
    }
    $missingSections = @()
    foreach ($key in $templateSections.Keys) {
        if ($content -notmatch [regex]::Escape($key)) {
            $missingSections += "$key ($($templateSections[$key]))"
        }
    }

    if ($missingSections.Count -gt 0) {
        throw ("Action start: plan non conforme au gabarit .ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md. " +
            "Sections manquantes ou non reecrites: `n- " + ($missingSections -join "`n- ") +
            "`nCeci n'est pas une simple erreur de formatage: l'IA doit relire le brouillon et " +
            "REDIGER chaque section manquante avec le contenu reel de ce chantier (pas coller le " +
            "gabarit vide), puis relancer start -Audited.")
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
        # -Path : brouillon humain original dans "0 - HUMAN START HERE/".
        #         N'est jamais reecrit ni deplace vers le backlog ; il est
        #         archive tel quel pour tracabilite.
        # -RewrittenPath : plan integralement reecrit par l'IA selon
        #         .ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md, deja ecrit par
        #         l'IA a l'emplacement cible avant d'appeler ce script.
        if (-not $Path) {
            throw "Action start: utilise -Path pour indiquer le brouillon original depose dans 0 - HUMAN START HERE/."
        }
        if (-not $RewrittenPath) {
            throw "Action start: utilise -RewrittenPath pour indiquer le plan deja reecrit selon le gabarit, deja present dans le dossier backlog cible."
        }
        if (-not $Audited) {
            throw "Action start: audit IA requis avant routage. Utilise /start via l'IA, ou relance avec -Audited apres audit explicite."
        }

        $draft = Resolve-Path $Path
        $draftPath = $draft.Path
        $draftRepoPath = ConvertTo-RepoPath $draftPath $repoRoot
        if (-not $draftRepoPath.StartsWith("0 - HUMAN START HERE/")) {
            throw "Action start: le brouillon original (-Path) doit se trouver dans 0 - HUMAN START HERE/."
        }
        if ($draftRepoPath.StartsWith("0 - HUMAN START HERE/archive/")) {
            throw "Action start: ce brouillon est deja archive."
        }

        $rewritten = Resolve-Path $RewrittenPath
        $rewrittenPathResolved = $rewritten.Path
        $rewrittenRepoPath = ConvertTo-RepoPath $rewrittenPathResolved $repoRoot
        $expectedFolder = (Get-BacklogFolder $Track) + "/"
        if (-not $rewrittenRepoPath.StartsWith($expectedFolder)) {
            throw "Action start: -RewrittenPath ('$rewrittenRepoPath') doit deja se trouver dans '$expectedFolder' (coherent avec -Track $Track). Ecris d'abord le plan reecrit a cet emplacement."
        }
        Assert-PlanAuditReady $rewrittenPathResolved

        if (-not $Id) {
            $Id = ConvertTo-PlanId $rewrittenPathResolved
        }
        if (-not $Title) {
            $Title = [System.IO.Path]::GetFileNameWithoutExtension($rewrittenPathResolved)
        }
        if (@(Find-Workstream $checkpoint $Id).Count -gt 0) {
            throw "Un chantier avec id '$Id' existe deja dans .ai/checkpoint.json."
        }

        $draftArchiveFolder = Join-Path $repoRoot "0 - HUMAN START HERE/archive"
        New-Item -ItemType Directory -Force $draftArchiveFolder | Out-Null
        $draftArchiveName = "{0}_{1}" -f (Get-Date -Format "yyyyMMdd"), ([System.IO.Path]::GetFileName($draftPath))
        $draftArchivePath = Join-Path $draftArchiveFolder $draftArchiveName
        if (Test-Path $draftArchivePath) {
            throw "Le brouillon archive existe deja: $draftArchivePath"
        }
        Move-Item -LiteralPath $draftPath -Destination $draftArchivePath
        $draftArchiveRepoPath = ConvertTo-RepoPath $draftArchivePath $repoRoot

        $workstream = [ordered]@{
            id = $Id
            title = $Title
            track = $Track
            status = "PENDING"
            lifecycle = "TRIAGED"
            classification = $Classification
            source_path = $rewrittenRepoPath
            original_draft_path = $draftArchiveRepoPath
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
        Write-Host "Plan demarre: $Id -> $rewrittenRepoPath (brouillon original archive: $draftArchiveRepoPath)"
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
