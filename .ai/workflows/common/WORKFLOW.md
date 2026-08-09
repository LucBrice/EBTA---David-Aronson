# Workflow commun — cycle des plans et publication locale

Ce workflow porte les regles procedurales universelles du depot. Le lire pour
toute action substantielle apres le bootstrap `AGENTS.md`, puis lire le
workflow specialise selectionne dans `.ai/workflows/README.md`.

Il reste universel : son deplacement hors d'`AGENTS.md` reduit le bootstrap
sans restreindre la portee des regles.

## Forme obligatoire des commits

Tout commit touchant ce depot, par une IA ou un humain, suit la forme detaillee
deja presente dans l'historique (`94338b6` ou `184b013` comme exemples) :

1. titre `type(scope): summary`, avec scope/resume francais selon la
   convention du depot ;
2. corps expliquant le pourquoi — audit, plan ou finding ayant motive le
   changement, pas seulement ce qui a change ;
3. causes racines ou changements numerotes s'il y en a plusieurs ;
4. section `Fichiers modifies` listant chaque fichier et sa raison ;
5. section `Non touches` nommant les zones volontairement laissees intactes ;
6. section `Validation` avec les commandes reellement executees et leurs
   resultats reels ;
7. footer `Co-Authored-By` nommant l'IA auteure.

Un message d'une ligne est interdit pour les changements sous
`Implementation/`, `Protocole/` ou `.ai/`. S'il n'est pas encore pousse,
l'amender avant de poursuivre.

## Commandes conversationnelles

`/start`, `/continue` et `/close` sont les commandes humaines de gestion des
plans. `.ai/tools/plan.ps1` est leur backend mecanique : il peut refuser une
promotion dangereuse, mais ne remplace jamais l'audit, la structuration ou les
gates portes par l'IA.

### Autorisations de publication en deux temps

Quand un gate distant exige une publication avant `/close`, distinguer et
nommer explicitement les deux operations potentielles dans la demande
d'autorisation :

- **push A** : publier le ou les commits d'implementation nommes afin
  d'executer et de verifier le gate distant ;
- **push B** : publier conditionnellement le seul commit de fermeture cree
  apres les validations et la resolution complete de `/close`, retrospective
  automatique comprise.

L'autorisation du push A n'autorise jamais le push B. Une autorisation
anticipee peut couvrir A et B uniquement si elle les nomme separement. B reste
alors conditionne a la reussite des validations et du commit de fermeture ; si
l'un des deux echoue ou n'existe pas, B est interdit. Si seul A est autorise,
laisser le commit de fermeture local et signaler que B attend une autorisation
separee.

Avant chaque push, rafraichir la reference distante et enumerer la plage
distante -> `HEAD`. La plage de A doit contenir exactement les commits
d'implementation autorises ; apres la retrospective, la plage de B doit
contenir exactement le commit de fermeture autorise. Tout correctif
retrospectif, commit concurrent ou autre commit additionnel impose un arret et
une autorisation separee. Aucun push ne devient automatique par cette regle.

### `/learn-session` - retrospective sans transition d'etat

`/learn-session` invoque la procedure canonique
`.agents/skills/capture-coding-session-learnings/SKILL.md`. La commande ne
change aucun stage de workstream et ne passe jamais par `plan.ps1` :
`WORKFLOW.json` reste donc inchangé.

Cette meme procedure est invoquee automatiquement apres toute sortie terminale
de `/close`, au point exact defini dans la section `/close` ci-dessous. Le
declenchement automatique ne change ni la procedure ni son contrat
d'autorisation.

Contrat d'autorisation :

1. La commande seule autorise l'analyse des preuves bornees de la session et la
   proposition d'apprentissages classes.
2. Une ecriture n'est permise que si la demande humaine autorise explicitement
   la persistance et si chaque apprentissage passe le test de promotion du
   skill vers un proprietaire existant.
3. Une autorisation de persistance n'autorise pas un commit. Une autorisation de
   commit n'autorise pas un push ou une publication externe.
4. Les signaux insuffisants restent `NON_PROMU`; aucun ledger ou journal de
   sessions n'est cree par defaut.
5. Les verdicts `FAIL`, `DENIED`, `INCONCLUSIVE`, timeouts et absences de sortie
   restent inchanges dans la retrospective.

Le skill porte la procedure detaillee, les categories, les destinations et le
format de sortie. Ce workflow ne les duplique pas et ne devient pas une memoire
de sessions.

### `/start` — boucle d'intake

Avant d'auditer et restructurer un brouillon :

1. Invoquer `code-architecture-evaluator` (`/evaluate`) sur le brouillon
   **en place** sous `0 - HUMAN START HERE/`.
2. Corriger directement ce que l'audit signale, puis relancer `/evaluate`.
3. Executer au minimum deux passes et continuer jusqu'a convergence reelle
   (aucun nouvel angle mort majeur), avec un plafond de 5-6 passes.
4. Si des problemes majeurs apparaissent encore au plafond, arreter et
   escalader : le plan exige une decision humaine.

Cette boucle d'intake ne remplace pas la seconde boucle sur le plan normalise.

### `/start` — promotion

`/start` ne deplace ni ne reecrit le brouillon humain en place. Apres
convergence :

1. Ecrire un **nouveau fichier** dans `.ai/backlog/mainline/`,
   `.ai/backlog/annexes/` ou `.ai/backlog/fixes/`, completement restructure
   selon `.ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md`.
2. Appeler :

   ```powershell
   .\.ai\tools\plan.ps1 start `
     -Path "<brouillon original>" `
     -RewrittenPath "<nouveau plan backlog>" `
     -Track <mainline|annexe|fix> `
     -Id <ID> -Title "<titre>" `
     -Workflow <common|core-engine> `
     -Audited -IntakeAuditPasses <2..6> `
     -IntakeAuditEvidence "<reference du journal intake>"
   ```

3. Laisser `plan.ps1` archiver l'original intact sous
   `0 - HUMAN START HERE/archive/` et enregistrer le nouveau plan comme
   `source_path`, avec l'archive comme `original_draft_path`.

Ne pas demander a l'humain de prestructurer le brouillon sauf si son
intention est impossible a inferer.

Le backend refuse un plan sans sections requises ou dont `-RewrittenPath`
n'est pas deja dans le dossier du track. En cas de refus, corriger le contenu
reel du plan et reessayer ; ne jamais contourner le controle ni coller un
gabarit vide.

### Boucle post-`/start` et baseline

Avant toute implementation :

1. Invoquer `/evaluate` sur le plan normalise.
2. Corriger, relancer et executer au minimum deux passes jusqu'a convergence,
   avec le meme plafond de 5-6 passes.
3. Si la convergence echoue au plafond, arreter et demander la decision
   humaine manquante.
4. Une fois le plan converge, valider les fichiers machine touches puis
   committer une baseline pre-implementation selon la forme obligatoire
   ci-dessus.
5. Enregistrer la baseline dans l'etat machine, puis committer separement
   cette mutation du checkpoint :

   ```powershell
   .\.ai\tools\plan.ps1 baseline -Id <ID> `
     -PlanAuditPasses <2..6> `
     -PlanAuditEvidence "<reference du journal plan>" `
     -BaselineCommit <sha>
   ```

Le backend verifie que le SHA existe et contient le `source_path` du plan.
Il verifie la presence des references d'audit, pas leur veracite semantique.

L'implementation ne commence qu'apres cette baseline revue et reversible.

### Test universel multi-lot

Appliquer `.agents/skills/epic-orchestrator/SKILL.md` :

- pendant `/start`, avant de choisir entre plan simple et chantier mere ;
- pendant `/continue`, avant toute implementation.

Si au moins deux composantes satisfont le test multi-lot du skill, toute
implementation directe est interdite : structurer et executer les
sous-chantiers separement.

### `/continue`

1. Retrouver le workstream dans `.ai/checkpoint.json`.
2. S'il est `BASELINED`, appeler
   `.ai/tools/plan.ps1 continue -Id <ID>`. Toute autre etape est refusee.
3. Rejouer le test `epic-orchestrator` sur l'etat actuel du plan.
4. Reprendre la phase declaree par la Carte d'execution IA et respecter le
   workflow specialise applicable.

Ne pas rappeler `plan.ps1 continue` sur un workstream deja `ACTIVE` : les
transitions repetees sont refusees.

### `/close`

1. Lire le workflow specialise et appliquer tous ses gates de fermeture.
2. Ne pas appeler le backend tant qu'un gate procedural reste ouvert.
3. Enregistrer les preuves requises et franchir `READY_TO_CLOSE` :

   ```powershell
   .\.ai\tools\plan.ps1 ready -Id <ID> `
     -Evidence "plan_conformance=<reference>"
   ```

   Les workflows specialises peuvent exiger d'autres IDs. Une conclusion
   `DONE` est impossible avant cette transition.
4. Appeler ensuite
   `.ai/tools/plan.ps1 close -Id <ID> -Outcome <OUTCOME> -Reason "<raison>"`.
   Les outcomes `BLOCKED`, `REJECTED` et `SUPERSEDED` restent des sorties
   explicites depuis une etape non terminale et ne simulent pas `DONE`.
5. Valider tout fichier JSON d'etat touche :
   - `.ai/checkpoint.json` contre `.ai/checkpoint.schema.json` ;
   - `Implementation/Active/tracking.json` contre son schema s'il est touche.
6. Si et seulement si les validations passent, creer automatiquement un
   commit — jamais un push — limite exactement aux fichiers de fermeture.
7. Si une validation echoue, ne pas committer et rapporter l'echec.
8. Apres la resolution effective de l'etape 6 (commit de fermeture reussi) ou
   de l'etape 7 (validation echouee et echec rapporte), invoquer
   automatiquement `capture-coding-session-learnings` dans la meme
   conversation. Ne jamais l'invoquer entre les etapes 4 et 6. Cette
   invocation autorise uniquement l'analyse, la classification et le rapport :
   elle n'autorise par elle-meme aucune ecriture de fichier, aucun commit,
   aucun push ni aucune publication externe. Un echec, timeout ou absence de
   sortie de la retrospective est rapporte, mais n'annule ni ne transforme le
   statut terminal deja persiste.
9. Pour chaque signal `A_REUTILISER` ou `ERREUR_OU_FRICTION` portant
   `Portee: meta`, appliquer le correctif immediatement seulement si deux
   conditions sont reunies : tous les fichiers cibles appartiennent au
   perimetre d'ecriture deja autorise de la mission close, et le correctif
   reste directement rattache au sujet fonctionnel deja approuve. Cette
   application releve de l'autorisation preexistante de la mission, jamais du
   declenchement automatique de la retrospective. Si une autorisation de
   commit couvre deja ce meme perimetre et ce meme sujet, creer un second
   commit distinct du commit de fermeture, conforme a la forme obligatoire et
   referencant l'ID du workstream clos ainsi que le rapport de capitalisation.
   Si l'ecriture est autorisee mais pas le commit, laisser le correctif edite
   et signaler `correctif applique, commit en attente d'autorisation separee`.
   Sans autorisation d'ecriture, ou si le correctif est hors perimetre ou hors
   sujet, ne rien modifier et l'inscrire dans `Suites a prevoir`.

`Suites a prevoir` documente des travaux possibles sans declencher de cascade :
aucun `/start` automatique ou immediat n'en decoule. Les lignes s'accumulent
dans les plans clos et sont revues par lot, au rythme choisi par l'humain,
sans nouveau registre ni nouvel etat de workflow.

## Etat machine et migration

Le cycle nominal persiste :

```text
INTAKE_AUDITED -> TRIAGED -> BASELINED -> ACTIVE
               -> READY_TO_CLOSE -> DONE
```

Les transitions sont lues depuis `WORKFLOW.json`, non recodees dans cette
documentation. `migrate-workflows` est une commande administrative one-shot
pour les anciens checkpoints. Sa preuve `legacy_import` preserve l'etat
historique mais declare explicitement qu'aucune ancienne gate n'est
re-attestee.

## Clarification minimale

Si des parametres manquent, inspecter d'abord `0 - HUMAN START HERE/`,
`.ai/checkpoint.json` et le plan actif. Questionner l'humain uniquement si
plusieurs choix materiellement differents restent plausibles.

# Ce que ce workflow ne fait pas

- Ne pas porter de regle scientifique EBTA.
- Ne pas remplacer un workflow specialise ou un skill.
- Ne pas creer de source d'etat concurrente.
- Ne pas pousser automatiquement un commit.
