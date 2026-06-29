# Backlog / File d'attente IA

Ce dossier centralise tous les plans, brouillons de hooks et epics en attente de traitement pour l'ensemble du repository.

## Regle de structure obligatoire (Checklist)
**Tout plan depose dans ce dossier DOIT inclure une checklist sous forme de cases a cocher Markdown (`- [ ]`, `- [x]`).** C'est indispensable pour qu'une IA sache quelles portions du plan ont deja ete traitees.

## Flux de travail (Workflow)

1. **Depot :** L'humain ou l'IA depose ici les gros plans de travail (Epics). *Ils doivent contenir une checklist.*
2. **Decoupage (Chunking) :** Lorsqu'une IA prend le relais pour executer un plan, elle lit le document cible. Elle identifie la premiere tâche non cochee (`[ ]`).
3. **Activation (Micro) :** L'IA extrait cette tâche realisable et la place dans l'etabli local correspondant (ex: `Implementation/Active/HOOK.md`).
4. **Mise a jour :** Une fois la tâche locale terminee, l'IA coche la case (`[x]`) dans le document du backlog.
5. **Archivage (Nettoyage) :** Quand **toutes** les cases de l'Epic sont cochees, l'IA deplace physiquement le fichier de `backlog/` vers `.ai/archive/`.

**Responsabilite :** Ce dossier gere le *quoi* (gestion de projet). L'execution reelle (le *comment*) se passe toujours dans les dossiers `Active/` specifiques au composant.
