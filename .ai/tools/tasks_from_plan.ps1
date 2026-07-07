<#
Backend mecanique de chunking : lit la section "Decoupage en phases" d'un
plan structure selon .ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md et genere
les steps/tasks correspondants dans Implementation/Active/tracking.json.

Convention de syntaxe attendue (non negociable, documentee dans le gabarit) :

  ### Phase <id> - <titre>

  Objectif : <une phrase>

  Classification : <GOVERNANCE|IMPLEMENTATION_DETAIL|...>   (optionnel)

  Actions :

  - <action 1>
  - <action 2>

  Livrables :

  - <livrable 1>

  Critere de sortie :

  - <critere 1>

Ce script ne remplace pas le jugement de l'IA sur le fond (objectifs,
livrables, criteres) : il remplace uniquement la traduction mecanique de ce
texte deja redige vers la structure JSON, pour que deux sessions qui lisent
le meme plan produisent le meme squelette de steps/tasks.

Usage :
  .\.ai\tools\tasks_from_plan.ps1 -PlanPath ".ai\backlog\mainline\MON_PLAN.md" -DryRun
  .\.ai\tools\tasks_from_plan.ps1 -PlanPath ".ai\backlog\mainline\MON_PLAN.md" -StepIdPrefix MON_PLAN
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$PlanPath,

    [string]$StepIdPrefix,

    [string]$TrackingPath = "Implementation/Active/tracking.json",

    [switch]$DryRun,

    [switch]$Force
)

$ErrorActionPreference = "Stop"
$ValidClassifications = @(
    "GOVERNANCE", "IMPLEMENTATION_DETAIL", "CONTRACT_ENCODING", "TEST_FIXTURE",
    "ADAPTER_MAPPING", "DOCUMENTATION_CLARIFICATION_NEEDED", "NORMATIVE_CHANGE_REQUIRED"
)

function Resolve-RepoRoot {
    $root = (git rev-parse --show-toplevel 2>$null)
    if (-not $root) {
        throw "Impossible de trouver la racine git. Lance la commande depuis le repo."
    }
    return (Resolve-Path $root).Path
}

function ConvertTo-Slug {
    param([string]$Value)
    $slug = $Value.Trim()
    $slug = $slug -replace "^-", "MINUS_"
    $slug = $slug -replace "[^A-Za-z0-9]+", "_"
    $slug = $slug.Trim("_").ToUpperInvariant()
    if (-not $slug) {
        throw "Impossible de deduire un identifiant de phase depuis '$Value'."
    }
    return $slug
}

function Get-PhaseBlocks {
    param([string]$Content)

    # Bornes de la section "Decoupage en phases" : du titre de section (## 6.
    # ... ou historiquement "## Phases d'implementation") jusqu'au prochain
    # titre de niveau 2 ("## ") ou fin de fichier. Regex en simple-quote pour
    # eviter toute expansion PowerShell de "$(" (subexpression) dans le motif.
    $sectionPattern = '(?ms)^##\s+(?:6\.\s*)?(?:Decoupage en phases|Phases d.implementation)[^\r\n]*\r?\n(?<body>.*?)(?=^##\s|\z)'
    $sectionMatch = [regex]::Match($Content, $sectionPattern)
    if (-not $sectionMatch.Success) {
        throw "Section 'Decoupage en phases' (ou 'Phases d'implementation') introuvable dans $PlanPath."
    }
    $sectionBody = $sectionMatch.Groups["body"].Value

    # Separateur id/titre exige au moins un espace de chaque cote du tiret,
    # pour ne pas couper un id du type "0-BIS" (tiret colle, sans espace) au
    # premier tiret rencontre.
    $phasePattern = '(?ms)^###\s+Phase\s+(?<pid>[^\r\n]+?)\s+-\s+(?<ptitle>[^\r\n]+?)\r?\n(?<body>.*?)(?=^###\s+Phase\s|\z)'
    $phaseMatches = [regex]::Matches($sectionBody, $phasePattern)
    if ($phaseMatches.Count -eq 0) {
        throw "Aucune phase au format '### Phase <id> - <titre>' trouvee dans la section Decoupage en phases."
    }
    return $phaseMatches
}

# Machine a etats ligne-par-ligne (plutot qu'un regex monolithique) : le texte
# source enveloppe naturellement les phrases et les puces sur plusieurs lignes
# physiques (retour a la ligne logiciel a ~80 colonnes). Un regex avec dotall
# capture trop (il avale les sections suivantes) ; un regex sans dotall
# tronque chaque champ a sa premiere ligne physique. Cette fonction recolle
# les lignes de continuation dans le champ ou la puce en cours.
function Get-PhaseFields {
    param([string]$Body)

    $labelKeys = @{
        "objectif"          = "objective"
        "classification"    = "classification"
        "actions"           = "actions"
        "livrables"         = "livrables"
        "critere de sortie" = "exit_criteria"
    }
    $listKeys = @("actions", "livrables", "exit_criteria")

    $result = [ordered]@{
        objective      = $null
        classification = $null
        actions        = New-Object System.Collections.Generic.List[string]
        livrables      = New-Object System.Collections.Generic.List[string]
        exit_criteria  = New-Object System.Collections.Generic.List[string]
    }

    $currentKey = $null
    $singleBuffer = $null

    foreach ($rawLine in ($Body -split "\r?\n")) {
        $labelMatch = [regex]::Match($rawLine, '^(?<label>Objectif|Classification|Actions|Livrables|Critere de sortie)\s*:\s*(?<inline>.*)$')
        if ($labelMatch.Success) {
            if ($currentKey -and ($listKeys -notcontains $currentKey) -and $singleBuffer) {
                $result[$currentKey] = $singleBuffer.Trim()
            }
            $currentKey = $labelKeys[$labelMatch.Groups["label"].Value.ToLowerInvariant()]
            $singleBuffer = $null
            $inline = $labelMatch.Groups["inline"].Value.Trim()
            if (($listKeys -notcontains $currentKey) -and $inline) {
                $singleBuffer = $inline
            }
            continue
        }

        if (-not $currentKey) { continue }

        if ($rawLine.Trim() -eq "") {
            if ($listKeys -contains $currentKey) {
                # Une ligne vide entre "Label :" et la premiere puce (ou entre
                # deux puces) ne termine pas une liste dans cette convention :
                # seule une nouvelle etiquette reconnue la termine.
                continue
            }
            if ($singleBuffer) {
                $result[$currentKey] = $singleBuffer.Trim()
            }
            $currentKey = $null
            $singleBuffer = $null
            continue
        }

        if ($listKeys -contains $currentKey) {
            $bulletMatch = [regex]::Match($rawLine, '^\s*-\s+(?<text>.+)$')
            if ($bulletMatch.Success) {
                $result[$currentKey].Add($bulletMatch.Groups["text"].Value.Trim())
            } elseif ($result[$currentKey].Count -gt 0) {
                $lastIndex = $result[$currentKey].Count - 1
                $result[$currentKey][$lastIndex] = ($result[$currentKey][$lastIndex] + " " + $rawLine.Trim()).Trim()
            }
        } else {
            if ($null -eq $singleBuffer) { $singleBuffer = "" }
            $singleBuffer = ($singleBuffer + " " + $rawLine.Trim()).Trim()
        }
    }
    if ($currentKey -and ($listKeys -notcontains $currentKey) -and $singleBuffer) {
        $result[$currentKey] = $singleBuffer.Trim()
    }

    return $result
}

$repoRoot = Resolve-RepoRoot
$planFullPath = Resolve-Path $PlanPath
$planContent = Get-Content -Raw $planFullPath

if (-not $StepIdPrefix) {
    $StepIdPrefix = ([System.IO.Path]::GetFileNameWithoutExtension($planFullPath) -replace "[^A-Za-z0-9]+", "_").Trim("_").ToUpperInvariant()
}

$phaseBlocks = Get-PhaseBlocks $planContent

$generatedSteps = @()
$previousStepId = $null
$previousLastTaskId = $null
$skippedPhases = @()

foreach ($phase in $phaseBlocks) {
    $pid_raw = $phase.Groups["pid"].Value.Trim()
    $ptitle = $phase.Groups["ptitle"].Value.Trim()
    $body = $phase.Groups["body"].Value
    $phaseErrors = @()

    $stepId = "${StepIdPrefix}_PHASE_" + (ConvertTo-Slug $pid_raw)

    $fields = Get-PhaseFields $body
    $objective = $fields.objective
    $classification = $fields.classification
    if (-not $classification) {
        $classification = "IMPLEMENTATION_DETAIL"
    } elseif ($ValidClassifications -notcontains $classification) {
        $phaseErrors += "Classification '$classification' invalide (attendu: $($ValidClassifications -join ', '))."
    }

    $actions = @($fields.actions)
    $livrables = @($fields.livrables)
    $exitCriteria = @($fields.exit_criteria)

    if (-not $objective) { $phaseErrors += "ligne 'Objectif :' manquante ou vide." }
    if ($actions.Count -eq 0) { $phaseErrors += "liste 'Actions :' manquante ou vide." }
    if ($exitCriteria.Count -eq 0) { $phaseErrors += "liste 'Critere de sortie :' manquante ou vide." }

    if ($phaseErrors.Count -gt 0) {
        $skippedPhases += [ordered]@{
            phase  = "Phase $pid_raw - $ptitle"
            errors = $phaseErrors
        }
        continue
    }

    $tasks = @()
    for ($i = 0; $i -lt $actions.Count; $i++) {
        $taskId = "${stepId}_T$($i + 1)"
        $blockedBy = if ($i -eq 0) { $previousLastTaskId } else { $tasks[$i - 1].id }
        $task = [ordered]@{
            id             = $taskId
            title          = $actions[$i]
            status         = "TODO"
            classification = $classification
            blocked_by     = $blockedBy
        }
        $tasks += $task
    }
    if ($livrables.Count -gt 0 -and $tasks.Count -gt 0) {
        $tasks[$tasks.Count - 1].deliverables = @($livrables)
    }

    $step = [ordered]@{
        id             = $stepId
        title          = $ptitle
        status         = "TODO"
        classification = $classification
        objective      = $objective
        tasks          = $tasks
        exit_criteria  = @($exitCriteria)
    }
    if ($previousStepId) {
        $step.entry_criteria = @("$previousStepId exit criteria completed")
        $step = [ordered]@{
            id = $step.id; title = $step.title; status = $step.status
            classification = $step.classification; objective = $step.objective
            entry_criteria = $step.entry_criteria; tasks = $step.tasks
            exit_criteria = $step.exit_criteria
        }
    }

    $generatedSteps += $step
    $previousStepId = $stepId
    if ($tasks.Count -gt 0) {
        $previousLastTaskId = $tasks[$tasks.Count - 1].id
    }
}

if ($skippedPhases.Count -gt 0) {
    Write-Warning "Phase(s) non chunkee(s) mecaniquement (non conformes a la convention de .ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md) :"
    foreach ($skipped in $skippedPhases) {
        Write-Warning "  - $($skipped.phase) : $($skipped.errors -join ' / ')"
    }
    Write-Warning "Ces phases restent hors de tracking.json tant qu'elles ne suivent pas la convention, ou doivent etre ajoutees manuellement si elles sont deliberement non actionnables (ex. phase differee sans Actions/Critere de sortie)."
}

if ($generatedSteps.Count -eq 0) {
    throw "Chunking refuse: aucune phase conforme n'a ete trouvee. Voir les avertissements ci-dessus pour corriger le plan."
}

if ($DryRun) {
    Write-Output ($generatedSteps | ConvertTo-Json -Depth 20)
    return
}

$trackingFullPath = Join-Path $repoRoot $TrackingPath
$tracking = Get-Content -Raw $trackingFullPath | ConvertFrom-Json

$existingIds = New-Object System.Collections.Generic.HashSet[string]
foreach ($s in $tracking.steps) {
    [void]$existingIds.Add($s.id)
    foreach ($t in $s.tasks) { [void]$existingIds.Add($t.id) }
}

$collisions = @()
foreach ($step in $generatedSteps) {
    if ($existingIds.Contains($step.id)) { $collisions += $step.id }
    foreach ($t in $step.tasks) { if ($existingIds.Contains($t.id)) { $collisions += $t.id } }
}
if ($collisions.Count -gt 0 -and -not $Force) {
    throw "Collision d'id avec tracking.json existant: $($collisions -join ', '). Utilise -Force pour ecraser volontairement, ou renomme les phases en conflit."
}

$tracking.steps = @($tracking.steps) + @($generatedSteps)

if ((-not $tracking.current_task_id) -and $generatedSteps.Count -gt 0) {
    $tracking.current_step = $generatedSteps[0].id
    $tracking.current_task_id = $generatedSteps[0].tasks[0].id
    if ($generatedSteps[0].tasks.Count -gt 1) {
        $tracking.next_task_id = $generatedSteps[0].tasks[1].id
    } elseif ($generatedSteps.Count -gt 1) {
        $tracking.next_task_id = $generatedSteps[1].tasks[0].id
    }
}

$tracking.updated_at = (Get-Date -Format "yyyy-MM-dd")
$tracking | ConvertTo-Json -Depth 20 | Set-Content -Encoding UTF8 $trackingFullPath

Write-Output "Chunking termine: $($generatedSteps.Count) phase(s) ajoutee(s) a $TrackingPath"
foreach ($step in $generatedSteps) {
    Write-Output "  - $($step.id) ($($step.tasks.Count) tache(s))"
}
Write-Output "Valider ensuite: python -m json.tool $TrackingPath"
