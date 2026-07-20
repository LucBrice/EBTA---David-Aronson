# Benchmark R4-long — lecture du rapport canonique

Le fichier `benchmark_report.json` est la preuve operationnelle generee le
2026-07-20 par `python -m ebta_engine.benchmarks.long_data`. Il mesure le chemin
Test pre-OOS reel sur `NASDAQ` et `XAUUSD`; il ne mesure aucune performance OOS
et ne constitue pas un verdict scientifique.

## Resultat

- statut canonique : `COMPLETED` ;
- duree totale : 316,074 s, sous le budget global de 1 080 s ;
- toutes les cellules : sous leurs timeouts et sous 8 Gio de peak RSS agrege ;
- cardinalite pipeline : 16 candidats, 2 folds, 32 segments Test par fenetre ;
- folds NASDAQ/XAUUSD : alignes ;
- decision pre-OOS observee : `DENIED`, exigence manquante `wrc_pass` ;
- exposition OOS : 0 segment, 0 barre, 0 evenement/journal d'acces ;
- validation du repertoire pre-OOS : `FAIL`, attendu car aucun package final
  ni artefact OOS n'est construit dans le scope ferme `PRE_OOS_BENCHMARK`.

## Mesures principales

| Fenetre | Barres chargees (2 actifs) | Barres Test uniques | Bar-evaluations | Couverture temporelle | Ordres | Duree pipeline | Peak RSS arbre |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 mois | 86 400 | 5 760 | 46 080 | 6,67 % | 28 | 87,33 s | 672 632 832 octets |
| 3 mois | 253 440 | 5 760 | 46 080 | 2,27 % | 28 | 91,27 s | 730 243 072 octets |
| 1 an | 1 019 520 | 5 760 | 46 080 | 0,56 % | 28 | 109,94 s | 995 188 736 octets |

`Bar-evaluations` compte les barres repassees dans chaque candidat/segment;
`Barres Test uniques` compte les timestamps distincts effectivement simules.
Le ratio de couverture utilise exclusivement le second compteur.

## Interpretation

La couche donnees passe l'echelle 1 an dans le budget : les deux actifs ont
chacun 509 760 barres, les comptes scan/chargement concordent et les controles
structurels n'ont trouve aucune anomalie. Les 11 gaps annuels sont publies a
titre descriptif, sans verdict de lacune puisqu'EBTA ne possede pas de calendrier
de venue normatif dans ce perimetre.

Le runner, lui, n'exploite pas davantage l'historique lorsque la fenetre grandit.
Le builder charge plus de donnees mais conserve le splitter fixe 2 jours Train /
1 jour Test / 1 jour OOS sur 2 folds. Les trois cellules executent donc le meme
volume Test et produisent le meme nombre d'ordres. Le benchmark prouve que le
chemin actuel tient son budget; il ne prouve pas une simulation exhaustive d'un
an. Une modification du calendrier Walk-Forward serait une decision scientifique
distincte et reste hors du Lot R4-long.

## Reproduction

Depuis `Implementation/`, avec le venv Nautilus du depot :

```powershell
adapters\nautilus_env\venv\Scripts\python.exe -m ebta_engine.benchmarks.long_data --output benchmarks\r4_long\benchmark_report.json
```

Le JSON enregistre versions Python/Nautilus, plateforme, CPU/RAM, budgets,
horodatages UTC, hashes de contenu des donnees et empreintes SHA-256 des modules
mesures. Une regeneration peut donc etre comparee sans assimiler le rapport a
son propre commit Git.
