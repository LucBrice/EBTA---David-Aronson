# Manifeste de gel EBTA

Version gelée : `EBTA-DOC-1.0`

Date du gel documentaire : 2026-06-24

## Portée du gel

Ce manifeste fige le paquet documentaire EBTA après :

- revue individuelle des SOP 01 à 12 ;
- audit transversal de cohérence ;
- registre normatif ;
- template de configuration préenregistrée ;
- révision du protocole principal ;
- clôture de l’audit méthodologique ;
- création du paquet d’exécution documentaire.

Le gel est documentaire. Les schémas machine-readable, formulaires exécutables,
validateurs d’invariants et intégrations logicielles restent une phase
d’implémentation séparée.

## Verdict de gel

`EBTA-DOC-1.0` est gelé avec statut :

`DOCUMENTATION_FROZEN_WITH_DEFERRED_IMPLEMENTATION`

Toute évolution méthodologique future doit ouvrir une nouvelle version
documentaire identifiable.

## Hashes SHA-256

Le manifeste ne liste pas son propre hash afin d’éviter une dépendance circulaire.

| Document | SHA-256 |
| --- | --- |
| `0-README - Comprendre et maintenir le protocole EBTA.md` | `E2CF51003CE59A5FBFC2DC8A0440E26080E1FA6DEF5C16436CB4963A50E081E1` |
| `Archives\AUDIT METHODOLOGIQUE PROTOCOLE EBTA.md` | `73BD6BC302AF4ECC749E5F7CDE2BDB27914F78E272CD55DF0A548B4B1DFBDA07` |
| `HISTORIQUE DES VERSIONS EBTA.md` | `551865A3EE37D1AD8B4993DE7110BE8D473153C6DFEB4DCBB21495370CDEB9C3` |
| `Archives\HOOK - Finalisation du protocole EBTA après revue des SOP.md` | `2A06E3938BC33D711C1D74A763A931BBC0C143A02726C5C9C9A13C59BD51BCAC` |
| `MATRICE DE COHERENCE DES SOP EBTA.md` | `32327E8F1191EC40E950B3F19D5C0CC51879AC3C934C51F64C0705805A33AC40` |
| `PAQUET D'EXECUTION EBTA.md` | `A69EE6A225C62F2DD86369C215B34B9FC95265B986569377F86D31E20D67141E` |
| `PROTOCOLE EBTA.md` | `277D96E3BB47C86C292FECC7DC10484E5443A14D4DA785CE08575DEE651A7165` |
| `REGISTRE DES DECISIONS NORMATIVES EBTA.md` | `7C62ADA660D38C20D9C80869B63E0D9EE8D47DD7E4BEB9EC22BB18D0B47A911D` |
| `SOP 01 - Estimation et intervalle de confiance OOS.md` | `06BAE0A75BA9D3D58AA3314A917B84D93A7D76B662DCA13AD25D8112756599E1` |
| `SOP 02 - Inférence multiple WRC SPA Romano-Wolf MCP.md` | `D7088D110A620FAC724BBC7EEBB90B4A0043726803C4649F80253A7819F06715` |
| `SOP 03 - Registre des expériences et univers des règles candidates.md` | `3ADC69E89A3F91FA7FF1B1D40C4861B67909D8C6915E5116E83E885AEBFACD72` |
| `SOP 04 - Segmentation temporelle et Walk-Forward.md` | `04853767A33A34D0F4BEDA96583C8726AE5DB94ED903EC3AC53DBED53A0DF839` |
| `SOP 05 - Tests de robustesse et gouvernance du holdout.md` | `0A893E61DFA902BC7807EE6119552930B6C41623D92B996A085393778C3414E7` |
| `SOP 06 - Sélection des règles candidates et optimisation de la complexité.md` | `575F8BE0144C0270533DA0E1D7B1EF6238661D95CB648860B29447E214F89E5D` |
| `SOP 07 - Detrending benchmark et zero-centering.md` | `4707119ACDC052831FED6005F89C7118A78917DC65F2DB25E531541CBC2A4D77` |
| `SOP 08 - Mesures de performance et série de rendement de référence.md` | `C05EBE0564174CC273DF35A43A3263FF0458748F4A4551F81681F533B91710C9` |
| `SOP 09A - Données point-in-time et contrôles anti-leakage.md` | `DB9D0CC2624176617953CE375ABE80CD4A34BF9CE8897042A147A8741850F434` |
| `SOP 09B - Modèle d’exécution frictions capacité et sizing.md` | `10F182B9B2AEDFA9367CF6719C841F4F9ED024F5F12188CE89CD53AFE972D954` |
| `SOP 10 - Gouvernance OOS et gestion des échecs.md` | `816CF98712B791EAA4AF25CC6DDFA2968C5EAE6E3F149883B6A66BA91590E88E` |
| `SOP 11 - Incubation passage live et monitoring séquentiel.md` | `DCFD61BCC54A533B0AC70D4A8A6371C795CF3C8F686DBCED9F2BE30AE4F44919` |
| `SOP 12 - Reproductibilité et paquet de validation EBTA.md` | `09AC33465467916554B32D628857B6B0C4E31D1CC28CDCD2987382B3D4C63B7B` |
| `TEMPLATE - Configuration préenregistrée d'une recherche EBTA.md` | `0C396ACDAFFDD2E8FD8021EE7D8EF4732B82DD55433EB07A19CC4CEE8E7C9592` |

## Prochaine phase

Implémenter le paquet d’exécution en artefacts machine-readable :

- schéma JSON de configuration ;
- schéma JSONL du registre append-only ;
- schéma JSONL du journal d’accès OOS ;
- générateur de manifeste ;
- validateur d’invariants ;
- tests automatisés intégrés au pipeline EBTA.
