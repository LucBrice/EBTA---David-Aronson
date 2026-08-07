param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

# Vérifier si le fichier existe
if (-Not (Test-Path $FilePath)) {
    Write-Host "Erreur : Le fichier spécifié n'existe pas : $FilePath" -ForegroundColor Red
    exit
}

# Lire le contenu du fichier .mmd et l'encoder en Base64 pour éviter tout problème d'échappement HTML/JS
$ContentBytes = [System.Text.Encoding]::UTF8.GetBytes((Get-Content -Path $FilePath -Raw))
$Base64Content = [Convert]::ToBase64String($ContentBytes)

# Créer un chemin pour le fichier HTML temporaire
$TempFile = [System.IO.Path]::GetTempFileName()
$HtmlPath = $TempFile -replace '\.tmp$', '.html'
Remove-Item $TempFile

# Extraire le nom du fichier pour le titre
$FileName = Split-Path $FilePath -Leaf

# Template HTML dynamique avec les boutons Horizontal / Vertical
$HtmlTemplate = @"
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Visualisation - $FileName</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 20px;
        }
        h2 { text-align: center; color: #333; margin-bottom: 5px; }
        .file-path { text-align: center; color: #666; font-size: 0.9em; margin-bottom: 20px; }
        .controls { text-align: center; margin-bottom: 25px; }
        button {
            background-color: #0f172a;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 0 10px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 15px;
            font-weight: 500;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.1s, background 0.3s;
        }
        button:hover { background-color: #334155; transform: translateY(-1px); }
        button:active { transform: translateY(1px); }
        .mermaid-container { 
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            padding: 20px;
            overflow: auto;
            text-align: center;
        }
        /* Garantir que le diagramme reste lisible sans être écrasé */
        .mermaid-container svg {
            min-width: 800px;
            height: auto;
            max-width: 100% !important;
        }
    </style>
</head>
<body>
    <h2>$FileName</h2>
    <div class="file-path">$FilePath</div>
    
    <div class="controls">
        <button onclick="updateDirection('LR')">➡️ Mode Horizontal</button>
        <button onclick="updateDirection('TB')">⬇️ Mode Vertical</button>
    </div>

    <div class="mermaid-container" id="mermaid-container">
        <!-- Le graphe sera rendu ici dynamiquement -->
    </div>

    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        
        mermaid.initialize({ 
            startOnLoad: false, 
            theme: 'default' 
        });

        // Récupérer le contenu sans aucun problème d'échappement grâce à l'encodage Base64
        const b64 = "$Base64Content";
        const binString = atob(b64);
        const bytes = new Uint8Array(binString.length);
        for (let i = 0; i < binString.length; i++) {
            bytes[i] = binString.charCodeAt(i);
        }
        const originalContent = new TextDecoder('utf-8').decode(bytes);

        window.updateDirection = async function(direction) {
            const container = document.getElementById('mermaid-container');
            let newContent = originalContent;

            // Remplacer intelligemment la direction dans le texte mermaid
            if (newContent.match(/direction\s+(LR|TB|RL|BT)/)) {
                newContent = newContent.replace(/direction\s+(LR|TB|RL|BT)/g, 'direction ' + direction);
            } else {
                // Si aucune direction n'existe, on l'ajoute juste après la déclaration du type de graphe
                newContent = newContent.replace(/(stateDiagram-v2|graph|flowchart)(\s+(TD|TB|LR|RL|BT))?/g, "$$1 " + direction);
            }

            try {
                const { svg } = await mermaid.render('mermaidGraph', newContent);
                container.innerHTML = svg;
            } catch (e) {
                container.innerHTML = "<p style='color:red;'>Erreur lors du rendu Mermaid : " + e.message + "</p>";
            }
        };

        // Rendu initial (On cherche la direction d'origine, sinon LR par défaut)
        let defaultDir = 'LR';
        const match = originalContent.match(/direction\s+(LR|TB|RL|BT)/);
        if (match) {
            defaultDir = match[1];
        }
        // Lancer le premier affichage
        window.updateDirection(defaultDir);
    </script>
</body>
</html>
"@

# Sauvegarder le fichier HTML
Set-Content -Path $HtmlPath -Value $HtmlTemplate -Encoding UTF8

Write-Host "✓ Ouverture de $FileName dans votre navigateur web..." -ForegroundColor Green

# Ouvrir le fichier HTML dans le navigateur
Start-Process $HtmlPath
