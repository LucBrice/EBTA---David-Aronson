# Brouillon — Lot 5 : isolation des tests dépendants de Nautilus (clôture REJECTED)

Track : fix
Lifecycle : INTAKE
Scope : Acter mécaniquement le refus humain du 2026-08-07 de la recommandation
5 de l'audit source (isoler les tests dépendants de l'environnement Nautilus
dans un groupe distinct de la suite stdlib-only), sans implémenter cette
segmentation.
Non-goals : Ne modifie ni `CLAUDE.md`, ni la commande canonique
`python -m unittest discover -s Implementation/ebta_engine/tests -t
Implementation`, ni `.ai/checkpoint.json::validation.commands`, ni aucun
fichier de test. Ne rouvre pas la décision humaine déjà actée.
Source : Sous-chantier 5/6 de `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE`
(`.ai/backlog/fixes/EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE.md`, section
"Sous-chantiers" et section 10 "Journal des décisions humaines"). Recommandation
5 de l'audit source
`0 - HUMAN START HERE/archive/20260807_AUDIT_ROBUSTESSE_ARCHITECTURE_FACE_ERREURS_IA_2026-08-07.md`.
Exit criteria : Ce workstream existe dans `.ai/checkpoint.json` avec
`status: DONE` / `lifecycle: REJECTED`, et aucun fichier hors de ce plan et du
chantier mère n'a été modifié.

## Constat factuel (déjà vérifié par le chantier mère, non refait ici)

Vérification directe du 2026-08-07 (rapportée par le chantier mère, section
10) : aucun des sept fichiers de test `nautilus` du dépôt n'utilise
`skipUnless`, `skipIf` ni `import nautilus_trader` — ils s'exécutent
intégralement hors venv avec des simulateurs factices. Le seul test
réellement dépendant de l'environnement Nautilus installé est
`test_long_data_benchmark.py`, traité par le lot 3
(`PLAN_GARDE_ENVIRONNEMENT_BENCHMARK_NAUTILUS`), pas par ce lot.

La prémisse de la recommandation 5 (« un échec d'environnement se noie dans
le run ») tombe donc dès que le lot 3 est livré : le seul point de rupture
d'environnement réel est isolé à la source (une garde locale dans
`long_data.py`), pas par une segmentation de la suite. Le coût de la
segmentation (mise à jour cohérente de `CLAUDE.md` et de
`.ai/checkpoint.json::validation.commands`) resterait réel pour un bénéfice
devenu nul.

## Décision humaine déjà actée (2026-08-07, journalisée dans le chantier mère)

> **Lot 5 refusé tel que cadré.** L'isolation des tests dépendants de
> Nautilus n'est pas retenue. Motif : la prémisse tombe après le lot 3. La
> question résiduelle (« ces tests passent-ils pour de bonnes raisons ? »)
> revient au lot 4. Lot 5 à clôturer `status: DONE` / `lifecycle: REJECTED`.

Ce brouillon ne redemande pas cette décision : il la formalise pour
permettre le routage mécanique (`plan.ps1 start` puis `plan.ps1 close
-Outcome REJECTED`), conformément à `.agents/skills/epic-orchestrator/SKILL.md`
étape 10 et au précédent `EPIC_ARCHITECTURE_IA_RAG` (chantier routé puis
clôturé `REJECTED` sans implémentation).

## Boucle `/evaluate` d'intake (2 passes, convergée)

Cette section documente l'audit d'intake exigé par
`.ai/workflows/common/WORKFLOW.md` avant `/start`, appliqué à CE brouillon en
tant que brouillon routable (pas une nouvelle passe d'audit de robustesse du
dépôt — celle-ci est déjà faite et citée ci-dessus).

**Passe 1** — Vérification que ce brouillon ne recrée pas de contenu déjà
tranché : le fait factuel (sept fichiers de test, aucun `skipUnless`) est
repris tel quel du chantier mère, sans le rouvrir. La décision humaine est
citée verbatim, pas reformulée de façon à en changer le sens. Le plan ne
propose aucune implémentation, conformément à la section 5 "Phase 5" du
chantier mère. Un point à corriger : le brouillon initial ne citait pas
explicitement le précédent `EPIC_ARCHITECTURE_IA_RAG` comme modèle de
clôture `REJECTED` sans implémentation — corrigé ci-dessus.

**Passe 2** — Confirmation qu'aucun fichier hors de ce plan n'est requis pour
le clôturer : `plan.ps1 start` (TRIAGED) puis `plan.ps1 close -Outcome
REJECTED` (transition `close_rejected` depuis `TRIAGED`, aucune preuve
requise selon `.ai/workflows/common/WORKFLOW.json` et
`.ai/workflows/core-engine/WORKFLOW.json`, transitions identiques sur ce
point). Aucun angle mort nouveau trouvé. Convergence à 2 passes sur 6
autorisées.

## Définition de fin

- [ ] Routé via `plan.ps1 start -Audited` avec ce brouillon.
- [ ] Clôturé via `plan.ps1 close -Outcome REJECTED -Reason` citant la
      décision de section 10 du chantier mère.
- [ ] `.ai/checkpoint.json` valide contre son schéma après chaque étape.
- [ ] Aucun fichier de test, `CLAUDE.md`, ou `validation.commands` modifié.
