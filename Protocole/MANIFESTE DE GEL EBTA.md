# Manifeste de gel EBTA

Version gelée : `EBTA-DOC-1.1`

Date du gel documentaire : 2026-07-01

## Portée du gel

Ce manifeste fige le paquet documentaire EBTA après :

- revue individuelle des SOP 01 à 12 ;
- audit transversal de cohérence ;
- registre normatif ;
- template de configuration préenregistrée ;
- révision du protocole principal ;
- clôture de l’audit méthodologique ;
- création du paquet d’exécution documentaire ;
- ajout de la gouvernance des biais humains, organisationnels et assistés par IA
  par SOP 13, `BIAS_RISK_REGISTER.md`, templates d'incident/dérogation et gate
  transversal `G-BIAS`.

Le gel est documentaire. Les schémas machine-readable, formulaires exécutables,
validateurs d’invariants et intégrations logicielles restent une phase
d’implémentation séparée.

## Verdict de gel

`EBTA-DOC-1.1` est gelé avec statut :

`DOCUMENTATION_FROZEN_WITH_DEFERRED_IMPLEMENTATION`

Toute évolution méthodologique future doit ouvrir une nouvelle version
documentaire identifiable.

## Hashes SHA-256

Le manifeste ne liste pas son propre hash afin d’éviter une dépendance circulaire.

| Document | SHA-256 |
| --- | --- |
| `0-README - Comprendre et maintenir le protocole EBTA.md` | `F2C2E1A72F0DC52D3B84E8B9F352C42FE0F8CD46979A278B9B192D25ACC599BF` |
| `Archives\AUDIT METHODOLOGIQUE PROTOCOLE EBTA.md` | `73BD6BC302AF4ECC749E5F7CDE2BDB27914F78E272CD55DF0A548B4B1DFBDA07` |
| `Archives\HOOK - Finalisation du protocole EBTA après revue des SOP.md` | `2A06E3938BC33D711C1D74A763A931BBC0C143A02726C5C9C9A13C59BD51BCAC` |
| `BIAS_RISK_REGISTER.md` | `BA1F99A5686FAA22874E725D23F4582849A41554B07A57DA22E0CC009D9AEBCB` |
| `HISTORIQUE DES VERSIONS EBTA.md` | `95C58780C6C1953C0A3AFE07BB4A8119B99DC68EC4281282909B08CA665C544F` |
| `MATRICE DE COHERENCE DES SOP EBTA.md` | `46AFFA4E2D8BA9F2ECBDCFB65D2ABAD4BBBD22450E956A7503C04190EFCB7419` |
| `PAQUET D'EXECUTION EBTA.md` | `CC94BD64F2056DD3789E2CAE1EB0F1D620D5A5E83C2F56D48589448BCD2E0C92` |
| `PROTOCOLE EBTA.md` | `602C7150E7C754A4BFF95A70EB52038C54ACE3210767FE4F95FF41DD4F68460D` |
| `REGISTRE DES DECISIONS NORMATIVES EBTA.md` | `5EB2A3000461E6681CF6B9797C572311CEF9A01E5EB940DC6773022C533A6362` |
| `SOP 01 - Estimation et intervalle de confiance OOS.md` | `06BAE0A75BA9D3D58AA3314A917B84D93A7D76B662DCA13AD25D8112756599E1` |
| `SOP 02 - Inférence multiple WRC SPA Romano-Wolf MCP.md` | `D7088D110A620FAC724BBC7EEBB90B4A0043726803C4649F80253A7819F06715` |
| `SOP 03 - Registre des expériences et univers des règles candidates.md` | `B1B398111C011207D370B966A6D32CFABE170964518F010985593FABAEA9CB2F` |
| `SOP 04 - Segmentation temporelle et Walk-Forward.md` | `04853767A33A34D0F4BEDA96583C8726AE5DB94ED903EC3AC53DBED53A0DF839` |
| `SOP 05 - Tests de robustesse et gouvernance du holdout.md` | `E328B23AC3664384F5154475109296EEC8B98BF78151C355A18B526B864483E6` |
| `SOP 06 - Sélection des règles candidates et optimisation de la complexité.md` | `575F8BE0144C0270533DA0E1D7B1EF6238661D95CB648860B29447E214F89E5D` |
| `SOP 07 - Detrending benchmark et zero-centering.md` | `4707119ACDC052831FED6005F89C7118A78917DC65F2DB25E531541CBC2A4D77` |
| `SOP 08 - Mesures de performance et série de rendement de référence.md` | `7E43D032501E4E125215FC581CA0CAB6113A92E486A9699FB8E0BCE8216253A0` |
| `SOP 09A - Données point-in-time et contrôles anti-leakage.md` | `47D5F7A1DA29AD6F129CD5A6C43FF9A756B9C1FBF46976A96544854BB6AA80EE` |
| `SOP 09B - Modèle d’exécution frictions capacité et sizing.md` | `10F182B9B2AEDFA9367CF6719C841F4F9ED024F5F12188CE89CD53AFE972D954` |
| `SOP 10 - Gouvernance OOS et gestion des échecs.md` | `904397731BDC3347EBCEFEC6B5A58E60ADD1A379DAF14C57B637941A9FFC6E72` |
| `SOP 11 - Incubation passage live et monitoring séquentiel.md` | `DCFD61BCC54A533B0AC70D4A8A6371C795CF3C8F686DBCED9F2BE30AE4F44919` |
| `SOP 12 - Reproductibilité et paquet de validation EBTA.md` | `55E23288CB2491219AF35ADF99F3B652AC5E74DF93855DF9A840A8051117109E` |
| `SOP 13 - Gouvernance des biais humains et incidents méthodologiques.md` | `B52DF1B9D70A295A3E58D2A507F68BBE26E7F94268ADDC2CF028145F24466E65` |
| `TEMPLATE - Configuration préenregistrée d'une recherche EBTA.md` | `0C396ACDAFFDD2E8FD8021EE7D8EF4732B82DD55433EB07A19CC4CEE8E7C9592` |
| `TEMPLATE - Dérogation méthodologique EBTA.md` | `B4384476A502E26AC97863932419DDFD5ED2009EA4A3366D1A6E82064CDEEBA9` |
| `TEMPLATE - Incident de biais EBTA.md` | `91C7004296A9668358D64FE51F5720BE60D48EE5885478634E2D6EDF977857D0` |

## Prochaine phase

Implémenter le paquet d’exécution en artefacts machine-readable :

- schéma JSON de configuration ;
- schéma JSONL du registre append-only ;
- schéma JSONL du journal d’accès OOS ;
- générateur de manifeste ;
- validateur d’invariants ;
- tests automatisés intégrés au pipeline EBTA.
