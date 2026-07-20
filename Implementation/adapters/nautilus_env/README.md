# Environnement NautilusTrader reproductible

Ce dossier contient la procedure executable pour recreer l'environnement
NautilusTrader subordonne au runtime EBTA. La version est epinglee dans
`requirements.txt` (`nautilus_trader==1.230.0`). Le venv est local et ne doit
jamais etre committe.

## Creation canonique depuis la racine du repository

```powershell
.\Implementation\adapters\nautilus_env\setup_env.ps1
```

Le script mappe temporairement la racine du repository sur `N:` puis cree le
venv sous `N:\Implementation\.venv-nautilus`. Ce chemin court est le defaut
canonique retenu pour eviter les limites de longueur de chemins Windows. Le
mapping `subst` peut etre recree a chaque invocation ; le venv physique reste
dans `Implementation\.venv-nautilus`.

Pour verifier un environnement canonique deja installe sans reinstaller les
dependances :

```powershell
.\Implementation\adapters\nautilus_env\setup_env.ps1 -SkipInstall
```

Le smoke final doit afficher `nautilus_trader 1.230.0`, le chemin de l'executable
Python et `Cache`.

## Venv historique de compatibilite

Cette machine possede aussi le venv historique
`Implementation\adapters\nautilus_env\venv`. Il peut etre reutilise sans creer
une seconde installation lourde :

```powershell
.\Implementation\adapters\nautilus_env\setup_env.ps1 `
  -VenvRelativePath "Implementation\adapters\nautilus_env\venv" `
  -SkipInstall
```

Cet override est une compatibilite locale, pas un second defaut officiel.

## Selection du data root

Le build resout la racine OHLCV une seule fois avec la precedence suivante :

1. argument Python `data_root` explicite ;
2. variable d'environnement `EBTA_DATA_ROOT` ;
3. fallback Windows historique du repo.

Exemple pour une autre machine :

```powershell
$env:EBTA_DATA_ROOT = "D:\donnees\EBTA"
```

Le dossier doit contenir les sous-dossiers d'actifs attendus par
`ebta_engine.data.local_ohlcv`.

## Build du package Nautilus

Avec le venv canonique, depuis la racine :

```powershell
Push-Location .\Implementation
try {
  .\.venv-nautilus\Scripts\python.exe -m ebta_engine.package_builder.nautilus_research_package
} finally {
  Pop-Location
}
```

Avec le venv historique, remplacer l'executable par
`.\adapters\nautilus_env\venv\Scripts\python.exe`.

Un statut global `FAIL` ou `INCONCLUSIVE` peut etre un verdict EBTA reel ; il ne
doit pas etre masque. La reproductibilite de l'environnement n'implique pas un
resultat scientifique `PASS`.
