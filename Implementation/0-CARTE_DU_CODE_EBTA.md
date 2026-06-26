# 🗺️ Carte du Dossier : Pour ne plus être perdu

*Si vous êtes perdu dans tous ces fichiers, vous êtes au bon endroit.* 

Ce dossier `Implementation` contient beaucoup de choses, mais tout s'organise logiquement. Voici l'explication "terre-à-terre" de ce que contient chaque dossier et fichier.

---

## 1. Les Documents de Cadrage (Les Plans de l'Architecte)
Ce sont les fichiers `.md` (Markdown) à la racine. Ce n'est pas du code, ce sont les plans, les to-do lists et les historiques.

*   **`GUIDE - Construire un pipeline de recherche EBTA.md`** : 🏆 **Le plus important pour vous**. C'est le mode d'emploi pratique. Il explique comment brancher votre backtester sur ce moteur.
*   **`HISTORIQUE DES VERSIONS EBTA ENGINE.md`** : Le journal intime des développeurs. Tout ce qui a été codé, jour après jour, y est justifié.
*   **`HOOK - Plan actif stabilisation archive et pipeline pilote.md`** : Le point de reprise courant. Il indique la prochaine étape de travail.
*   **`Archives/completed_2026-06-26/HOOK - Reprise EBTA Engine Core autonome.md`** : L'ancien point de départ, conservé pour comprendre pourquoi le moteur a été construit ainsi.
*   **`Archives/completed_2026-06-26/PLAN - Procedures de calcul EBTA et optimisation ML.md`** : L'ancienne To-Do list des calculs mathématiques, terminée et conservée en archive.
*   **`PROCEDURE_CALCULATION_MAP.md`** : La carte mentale qui relie nos fichiers de calcul Python aux chapitres du livre de David Aronson.
*   **`TRACEABILITY_MATRIX.md`** : Le tableau qui prouve à un auditeur que chaque ligne de code respecte scrupuleusement la théorie du protocole.
*   **`EXTERNAL_ENGINE_PROCEDURE_MAPPING.md`** : Le plan de traduction ("comment les données de Backtrader devront se transformer pour entrer dans notre moteur").

---

## 2. Le Code Source du Moteur : Dossier `ebta_engine/`
C'est le "Laboratoire". C'est ici que se trouve le vrai code Python fonctionnel.

*   **`procedures/`** : 🧮 **La salle des mathématiques**. Contient les fichiers vitaux comme `wrc.py` (White's Reality Check), `detrending.py` (dé-tendance), `bootstrap.py`. C'est là que le moteur calcule si votre stratégie a triché ou non.
*   **`validators/` et `schemas/`** : 👮 **La douane**. Ce code vérifie que les fichiers générés par votre backtester ont la bonne forme (les *schemas*) et qu'ils respectent les règles de validation, les fameuses "Gates" (les *validators*).
*   **`manifests/`** : ⚖️ **Le notaire**. Ce code rassemble tous les résultats et crée le Manifeste Cryptographique final (le fichier infalsifiable qui prouve le succès).
*   **`adapters/`** : 🔌 **La prise électrique**. Ce sont les bouts de code qui servent d'interface pour brancher un outil externe (comme le backtester Backtrader) à notre moteur.
*   **`tests/` et `fixtures/`** : 🛠️ **La maintenance**. Ce code sert uniquement aux développeurs. Il injecte de "fausses" données (les *fixtures*) dans le moteur pour s'assurer que notre code tourne sans bug (les *tests*).
*   **`persistence.py`** : 💾 Code qui gère l'écriture et la sauvegarde sécurisée des résultats sur le disque dur.

---

## 3. La Démonstration : Dossier `examples/`
*   **`examples/minimal_pilot_pipeline/`** : 🚀 **Le simulateur de vol**. Pour prouver que le moteur fonctionne, nous y avons mis un "faux" backtester. Il fait semblant de générer des trades et appelle le moteur EBTA pour montrer par l'exemple comment tout ce code s'agence du début à la fin. 

---

## 4. La Mémoire de l'IA
*   **`task_tracking.json`** : 🤖 C'est le suivi actif que l'intelligence artificielle utilise pour ne pas perdre le fil.
*   **`Archives/completed_2026-06-26/implementation_context.json`** : Ancien contexte IA du lot procédures terminé.

---

### 💡 Par où commencer ?
Si vous cherchez à **comprendre comment l'utiliser**, lisez le `GUIDE`.
Si vous cherchez à **comprendre les mathématiques**, regardez le dossier `ebta_engine/procedures/`.
