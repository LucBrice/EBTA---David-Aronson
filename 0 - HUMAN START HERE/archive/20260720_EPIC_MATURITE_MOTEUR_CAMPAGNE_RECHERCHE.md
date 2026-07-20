# Chantier mere - Maturite du moteur EBTA pour une vraie campagne de recherche

> Note d'intake, pas encore un plan route. Deposee dans `0 - HUMAN START HERE/`
> pour boucle `/evaluate` en place puis `/start`. Redigee selon
> `.agents/skills/epic-orchestrator/SKILL.md` (chantier mere de suivi qui ne
> code rien lui-meme et coordonne des sous-chantiers independants).
> Etat machine a la redaction : branche `main`, HEAD `9f461b2`,
> `.ai/checkpoint.json::active_workstream_id = null`, tous les workstreams
> `DONE`.

---

## 0. Sujet principal a cloturer (le "rappel")

La question ouverte depuis l'audit du 2026-07-13, toujours ouverte au 2026-07-20,
est :

```text
Le moteur EBTA est-il pret pour une vraie campagne de recherche
quantitative ?
```

Aujourd'hui la reponse honnete (audit
`0 - HUMAN START HERE/AUDIT_MATURITE_MOTEUR_RECHERCHE_2026-07-13.md`,
section 2) est :

```text
Pipeline EBTA/Nautilus coherent, capable de produire un FAIL honnete,
mais pas encore un moteur de campagne robuste, calibre et reproductible.
```

**Cloturer ce sujet = amener le moteur au niveau "campagne de RECHERCHE
robuste, calibree et reproductible" en levant les risques `OUVERT` / `PARTIEL`
de la matrice de l'audit qui relevent de la recherche : R5 (couts calibres),
R6 (stress reel), R7 (reproductibilite), R8 (scalabilite du runner, absorbe
par le benchmark), horodatage transversal / attestations, et R4-long
(benchmark donnees longues).** Ce chantier mere existe pour porter ce sujet de
bout en bout, pour que la question "quelle est la suite ?" ne se repose plus
a chaque session : la suite est ce document, jusqu'a sa propre cloture.

**Frontiere explicite recherche vs live (decision d'architecture).** "Pret
pour une campagne de RECHERCHE" n'est PAS "pret pour un deploiement LIVE".
Le risque **R10** de l'audit (cycle reel incubation -> paper trading ->
deploiement -> live -> kill switch -> monitoring) releve du deploiement
operationnel, pas de la validation de recherche. **R10 est explicitement HORS
du perimetre de ce sujet** (deja exclu par la decision R3 du 2026-07-17,
reconduite ici) : aucun lot ne le couvre, et sa presence residuelle en
`OUVERT` dans la matrice de l'audit ne bloque PAS la cloture de ce chantier.
Si un jour une strategie survit reellement a l'OOS, R10 fera l'objet d'un
sujet distinct.

Ce qui est deja fait et ne doit PAS etre rouvert (audit section 2, matrice) :
R1 (moteur de signaux reel), R2 (extraction Nautilus reelle), R4 (M1 reel
branche), le WRC masque, le statut global de package, G5, et l'ensemble des
attestations residuelles de `gates.json` + `invariant_evidence.json` (EPIC
C/A2/B et EPIC R3, tous `DONE`).

---

## 1. Verdict du test de detection multi-lot

Test de detection (`.agents/skills/epic-orchestrator/SKILL.md`, section "Test
de detection") applique explicitement. **Verdict : MULTI_LOT, ce skill
s'applique.** Les composantes ci-dessous satisfont les trois conditions
simultanement :

1. **Exit criteria independants** : chaque lot a un critere de sortie
   verifiable sur lui-meme, sans dependre de l'etat des autres. R7 (data root
   parametrable + hash reel) se prouve seul ; R5/R6 (couts calibres + stress
   echouable) se prouve seul ; l'horodatage se prouve seul ; R4-long
   (benchmark documente) se prouve seul.
2. **Ordre non contraint par le SENS de chaque lot** : reordonner ne change
   le sens ni la cloture d'aucun lot pris isolement. L'ordre retenu (section
   2.2) est une optimisation de *qualite de preuve*, avec UNE dependance reelle
   assumee et documentee : R4-long adosse sa valeur (reproductibilite,
   portabilite) a R7 ; le faire avant R7 produirait un benchmark non portable,
   donc une preuve degradee - pas un lot au sens change. Toutes les autres
   paires sont librement permutables. Le test reste satisfait : au moins deux
   lots (R7, horodatage) sont pleinement independants de tous les autres.
3. **Blocage non contaminant** : une pause sur une composante (ex. decision
   humaine de seuil sur R6) n'empeche pas les autres d'avancer.

Consequence mecanique : chaque lot devient son propre workstream distinct,
route par son propre `plan.ps1 start`, avec `-Reason` commencant par
`"Sous-chantier <n>/<total> de EPIC_MATURITE_MOTEUR_CAMPAGNE_RECHERCHE"`.
Aucun `parent_workstream_id` dans `.ai/checkpoint.schema.json` (le lien reste
narratif). Ce chantier mere ne modifie AUCUN fichier de `Implementation/`.

---

## 2. Reponses aux trois arbitrages delegues (bonne pratique)

L'humain a delegue explicitement trois decisions "selon la bonne pratique".
Voici les choix retenus, avec justification traçable.

### 2.1 Track du chantier mere = `mainline`

Les EPIC precedents (C/A2/B, R3) etaient `fix` parce qu'ils **corrigeaient
des facades** (attestations codees en dur a `True`). Ce chantier-ci est de
nature differente : il **construit la capacite scientifique manquante**
(realisme des couts, stress de robustesse reel, reproductibilite, validation
a l'echelle campagne). C'est la continuation directe de la lignee mainline
R1/R2/R4 (toutes `advances_mainline: true`), pas une correction de bug
masque. La question qui le definit ("le moteur est-il pret pour une vraie
campagne ?") est une question d'avancement de la mainline. Donc `mainline`
pour la mere. Le track de CHAQUE lot est decide a son propre `/start` (R7 et
l'horodatage peuvent legitimement etre `fix` ; R5/R6 et R4-long sont
`mainline`).

### 2.2 Ordre des lots = R7 -> R5/R6 -> Horodatage/attestations -> R4-long

Principe directeur : **enabler -> coeur scientifique -> gouvernance ->
validation**. Cet ordre devie volontairement du numerotage de la section 3 de
l'audit (qui liste R5/R6 en priorite 1), et voici pourquoi c'est la bonne
pratique ici :

- **R7 d'abord** : l'audit lui-meme le qualifie de "Independant, rapide, gros
  gain" (H5). C'est un enabler bon marche ET un prerequis dur du benchmark
  donnees longues (on ne peut pas benchmarker proprement sur un `DEFAULT_DATA_ROOT`
  = chemin Windows absolu en dur, ni sceller des artefacts avec un
  `document_hash = "NAUTILUS_MVP_CONFIG_HASH_PLACEHOLDER"` litteral). Le faire
  en premier ameliore l'integrite des preuves de TOUS les lots suivants.
- **R5/R6 ensuite** : c'est le plus gros trou scientifique restant (le gate de
  robustesse ne peut structurellement pas echouer, voir section 4), donc le
  coeur du chantier, mais aussi le plus lourd - fait sur une base reproductible.
- **Horodatage/attestations** : gouvernance transversale independante, deja
  identifiee par la cloture de l'EPIC R3 comme "chantier transversal distinct".
- **R4-long en dernier** : c'est la validation a l'echelle campagne qui
  consomme R5 (perf/couts calibres) et R7 (data root portable).

### 2.3 Idees "annexe" de l'audit (section 3, backlog) = pas de lots orphelins

Ne pas creer de micro-lots disperses (l'anti-pattern que ce skill existe
justement pour empecher). Chaque idee recoit un lot "d'accueil naturel", et la
promotion en sous-chantier propre est decidee A L'OUVERTURE du lot d'accueil,
via le test de detection reapplique a ce moment-la (voir section 5) :

| Idee backlog (audit section 3) | Lot d'accueil | Promotion possible ? |
| --- | --- | --- |
| Validateur qualite CSV M1 (timestamps monotones, trous, OHLC, volumes) | R4-long | Oui, si substantiel : prerequis du benchmark |
| Warm-up inter-fold / lookback | R5/R6 | Sous-composante du realisme d'execution |
| Edge cases Nautilus (position ouverte, fill partiel, ordre rejete, precision) | R5/R6 | Oui, en groupe "durcissement adapter" avec l'idee suivante |
| Invariant `PASS` non inerte (exposition non nulle, couts presents si modele l'exige) | R5/R6 | Face validation du realisme des couts |
| Frontiere bug-hunter vs validation scientifique | Horodatage/attestations (gouvernance) | Non - principe documente, pas un lot de code |

---

## 3. Les quatre lots

| # | ID prevu | Objet (risque audit) | Track pressenti |
| --- | --- | --- | --- |
| 1 | `PLAN_REPRODUCTIBILITE_OPERATIONNELLE_R7` | R7 : data root parametrable, hash de config reel, doc environnement Nautilus (venv hors git) | fix ou mainline |
| 2 | `PLAN_REALISME_ECONOMIQUE_R5_R6` | R5 (couts/slippage/latence calibres) + R6 (stress de robustesse reel). **Candidat sous-chantier mere** - voir section 5. | mainline |
| 3 | `PLAN_HORODATAGE_TRANSVERSAL_ET_ATTESTATIONS` | Generaliser l'horodatage UTC automatique aux autres jalons (patron pose par Lot F de R3) + expliciter les attestations humaines/post-OOS legitimes | fix |
| 4 | `PLAN_BENCHMARK_DONNEES_LONGUES_R4_LONG` | R4-long / R8 : benchmark 1 mois / 3 mois / 1 an, budget temps/memoire/ordres/exposition OOS, scalabilite du runner | mainline |

Ordre d'execution par defaut : 1 -> 2 -> 3 -> 4 (justification section 2.2).

**Regle anti-stagnation** (sert directement l'objectif "ne plus revenir
demander la suite") : si un lot se met en pause sur une decision humaine non
encore tranchee (section 7), l'ordre par defaut cede le pas - le prochain lot
INDEPENDANT dont la qualite de preuve ne se degrade pas d'etre avance peut
etre execute pendant la pause. Exemple : si le Lot 2 (R5/R6) attend une
decision de seuil, le Lot 3 (horodatage, pleinement independant) peut avancer.
La seule paire a ne PAS reordonner est R7 -> R4-long (degrade la preuve, cf.
section 1 condition 2). On ne stoppe jamais tout l'EPIC sur une seule decision
en attente tant qu'un lot independant reste realisable.

---

## 4. Etat des lieux verifie dans le code courant (2026-07-20)

Constats de l'audit reverifies directement dans le code (pas herites d'un
audit potentiellement perime) :

| Constat | Preuve code | Lot |
| --- | --- | --- |
| Data root = chemin Windows absolu en dur | `Implementation/ebta_engine/data/local_ohlcv.py:17` (`DEFAULT_DATA_ROOT = Path(r"D:\TRADING\...\Data")`) | R7 |
| Hash de config = placeholder litteral | `Implementation/ebta_engine/package_builder/nautilus_research_package.py:80` (`"document_hash": "NAUTILUS_MVP_CONFIG_HASH_PLACEHOLDER"`) | R7 |
| Trois scenarios de robustesse identiques, seuil `-1.0` (jamais echouable) | `nautilus_research_package.py:569-594` : CENTRAL/PLAUSIBLE/EXTREME, tous `minimum_mean_return: -1.0`, seul le label et `blocking` different, aucun choc de cout/slippage/latence applique | R6 |
| Frais indicatifs, slippage/latence quasi nuls | `nautilus_research_package.py:355` (`prob_slippage=0.0`), `:371-372`/`:389-390` (`maker_fee="0.0002"`, `taker_fee="0.0005"` indicatifs) | R5 |
| venv Nautilus local, non suivi par git, a documenter/recreer | `Implementation/adapters/nautilus_env/` (audit section H2, "Dette structurelle") | R7 |

Ces constats sont la matiere premiere de l'etat des lieux (section 4 du
gabarit) de chaque lot ; ils seront revalides une derniere fois a l'ouverture
de chaque lot (la nature peut avoir change entre-temps).

---

## 5. Recursion : un lot peut lui-meme etre multi-lot

Point souleve explicitement par l'humain, et deja rencontre (l'EPIC R3 est
devenu chantier mere de Lots D/E/F). Le mecanisme se **generalise par
recursion du meme skill**, sans structure de nesting dediee :

- Le test de detection se rejoue **a chaque niveau**, a l'ouverture d'un lot,
  pas seulement a la racine.
- Si en creusant un lot (etape 1 de la boucle epic-orchestrator : "revalider
  dans le code reel avant de rediger") je decouvre qu'il contient lui-meme
  plusieurs composantes independantes, ce lot devient a son tour un chantier
  mere (document coordinateur qui ne code rien), route normalement, et ses
  enfants sont routes avec `-Reason` = `"Sous-chantier X/Y de <ID_DU_LOT>"`.
- Vu du chantier mere du dessus, ce lot-devenu-mere compte comme **un seul
  lot** qui avance quand sa propre "Cloture generale" (bug-hunter +
  conformance sur l'union de ses enfants) est atteinte. Le parent n'a jamais
  besoin de connaitre le detail des petits-enfants.
- `.ai/checkpoint.json` reste **plat** : tous les workstreams, a tous les
  niveaux, sont des entrees au meme niveau du tableau `workstreams[]`. La
  hierarchie n'existe que dans le texte (chaque document liste ses enfants,
  chaque enfant nomme son parent dans `routing_reason`).

**Garde-fou : pas de nesting preventif.** On ne pre-decoupe pas "au cas ou".
Le split ne se fait que si le test de detection se declenche reellement a
l'ouverture du lot.

Application concrete a ce chantier :

- **Lot 2 (R5/R6)** est le candidat sous-chantier mere le plus probable : R5
  (calibrer les couts/slippage/latence) et R6 (stresser reellement la
  robustesse) ont des Exit criteria plausiblement independants (R5 = des
  parametres calibres et sources ; R6 = des scenarios qui appliquent de vrais
  chocs et peuvent echouer). Le split R5 / R6 (+ eventuel "durcissement
  adapter" absorbant les edge cases Nautilus) sera tranche a l'ouverture du
  Lot 2, pas maintenant.
- **Lot 4 (R4-long)** pourrait aussi se scinder (validateur qualite CSV M1 /
  benchmark / scalabilite runner) - meme regle : decide a l'ouverture.

---

## 6. Triage (pour le `/start`)

| Champ | Valeur |
| --- | --- |
| Track | `mainline` (justification section 2.1) |
| Lifecycle | `INTAKE` (deviendra `TRIAGED` au `/start`) |
| Type de chantier | `MULTI_LOT` (verdict section 1) |
| Scope | Chantier mere de suivi (aucune modification directe de `Implementation/`) coordonnant quatre sous-chantiers independants (R7, R5/R6, horodatage/attestations, R4-long) jusqu'a ce que le moteur EBTA soit reproductible, calibre, stresse et valide a l'echelle campagne, cloturant le sujet "pret pour une vraie campagne de recherche". |
| Non-goals | Ne pas rouvrir R1/R2/R4, le WRC masque, le statut global package, G5, ni les attestations C/A2/B/R3 deja `DONE`. Ne pas exiger un package global `PASS` comme condition de succes (un `FAIL`/`INCONCLUSIVE` reel reste un verdict EBTA legitime). Ne pas modifier `Protocole/`. Ne pas fusionner deux lots dans un commit/boucle `/evaluate`/cloture. Ne pas etendre `.ai/checkpoint.schema.json` (pas de `parent_workstream_id`). Ne pas construire un vrai cycle live/kill-switch/monitoring (R10, hors perimetre "recherche", deja exclu par R3 - voir section 0). Ce document ne code rien lui-meme. |
| Source | Demande humaine du 2026-07-20 : mettre en place un chantier multi-lot couvrant tous les travaux restants de l'audit de maturite, pour cloturer le sujet principal sans re-demander la suite a chaque session. Priorite d'origine : audit section 3. |
| Exit criteria | (1) Lot 1 R7 `DONE`. (2) Lot 2 R5/R6 `DONE` (ou clos via ses propres sous-chantiers s'il devient mere). (3) Lot 3 horodatage/attestations `DONE` ou explicitement differe par decision humaine documentee. (4) Lot 4 R4-long `DONE`. (5) **Preuve globale concrete** : un package de recherche (le `nautilus_mvp` regenere et/ou un package benchmark sur donnee longue) est produit par `nautilus_research_package.py::main()` puis passe `validate_package_dir()`, avec preuve documentee que, sur le chemin de production reel : (a) le data root est parametrable et le `document_hash` n'est plus le placeholder litteral (R7) ; (b) les couts/slippage/latence sont calibres et non nuls et les scenarios de robustesse different reellement et PEUVENT echouer - un test de contraste le prouve (R5/R6) ; (c) l'horodatage des jalons vises est capture automatiquement (Lot 3) ; (d) un rapport de budget benchmark (temps, memoire, ordres, exposition OOS) existe pour au moins la fenetre longue ciblee (R4-long) ; et CHAQUE gate affiche un verdict reel derive (`PASS` ou `FAIL`/`INCONCLUSIVE` honnete), aucune facade `True` codee en dur ne subsistant dans le perimetre des quatre lots. Le statut global du package peut rester `FAIL` : c'est la CAPACITE demontree, pas un `PASS` obtenu, qui clot le sujet. (6) Ce chantier mere lui-meme clos (`plan.ps1 close`) seulement quand (1)-(5) sont satisfaits. |

---

## 7. Journal des decisions humaines (deja actees)

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-20 | Mettre en place un chantier mere multi-lot couvrant tous les travaux restants de l'audit de maturite. | Autorise la redaction de cette note d'intake et sa boucle `/evaluate`. |
| 2026-07-20 | Les trois arbitrages (ordre, absorption des annexes, track) sont delegues a l'IA "selon la bonne pratique". | Autorise les choix de la section 2 (ordre R7->R5/R6->horodatage->R4-long ; annexes rattachees a un lot d'accueil ; track mainline) sans validation prealable supplementaire. |
| 2026-07-20 | Un sous-chantier peut lui-meme devenir un chantier mere (recursion). | Autorise le split d'un lot a son ouverture si le test de detection se declenche (section 5), sans nesting preventif. |

Decisions restant a trancher (au `/start` du lot concerne, pas ici) :
- Seuils de calibration R5 (couts/slippage/latence : quelles sources, quelles
  valeurs) - decision de methode humaine probable au Lot 2.
- Magnitude des chocs de stress R6 et seuil `minimum_mean_return` reel -
  decision de seuil humaine probable au Lot 2.
- Perimetre exact des attestations humaines/post-OOS a expliciter vs deriver
  (Lot 3).

Prerequis factuels a verifier (a l'ouverture du lot concerne, pas ici) :
- **Disponibilite des donnees longues (Lot 4)** : l'audit (H1) affirme
  l'existence de "8 actifs en 1-minute sur toute l'annee 2020" au data root.
  Cette presence, ce volume et cette qualite (timestamps, trous, format)
  doivent etre verifies concretement a l'ouverture du Lot 4 : un benchmark
  1 mois / 3 mois / 1 an est bloque si la donnee est absente ou insuffisante.
  C'est un prerequis factuel (au sens du gabarit section "Prerequis
  factuels"), a statuer `disponible` / `manquant` / `bloquant` a ce moment-la.
- **Plateforme/venv Nautilus (Lot 1)** : le venv `nautilus_env` est local et
  non suivi par git ; sa recreabilite documentee est justement l'objet de R7,
  a verifier au Lot 1.

---

## 8. Ce que ce document ne fait pas

- Il ne code rien et ne modifie aucun fichier de `Implementation/`.
- Il ne recopie pas le contenu technique des plans de lots (chaque lot porte
  le sien).
- Il ne tranche pas les decisions de seuil/methode a la place de l'humain -
  il les identifie et s'arrete pour les demander au bon moment.
- Il ne cree pas de hierarchie structurelle dans `.ai/checkpoint.json` - le
  lien parent/enfant reste narratif.
