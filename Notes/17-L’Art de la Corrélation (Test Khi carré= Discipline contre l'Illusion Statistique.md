---
exported: 2026-06-12T08:58:45.216Z
source: NotebookLM
type: note
title: "17 - L’Art de la Corrélation (Test Khi carré= : Discipline contre l'Illusion Statistique"
---

# 17 - L’Art de la Corrélation (Test Khi carré= : Discipline contre l'Illusion Statistique

导出时间: 12/06/2026 10:58:45

---

**Idées clés :**

**Insuffisance de la confirmation :** Les instances confirmatoires (Cellule A) sont nécessaires pour établir une corrélation, mais elles ne sont jamais suffisantes à elles seules\[1\]\[2\].

**La Table de Contingence 2x2 :** Pour évaluer un signal, il faut impérativement comptabiliser les quatre issues possibles : succès confirmatoires, faux signaux, opportunités manquées et non-événements corrects\[3\]\[4\].

**Analyse de proportion :** Une corrélation n'est réelle que si la proportion de succès en présence du signal est significativement différente de la proportion de succès en l'absence du signal\[5\]\[6\].

**Le test du Chi-carré (**χ2**) :** C'est l'outil statistique rigoureux pour déterminer si la répartition des données dans les quatre cellules s'écarte du hasard\[5\]\[7\].

**Référence :**_GIVING ALL CELLS THEIR DUE_ (Pages 77–78) ; _Necessary versus Sufficient Evidence_ (Page 75).

**Citation Directe :**« In reality, the number of instances falling into all four cells of the contingency table must be taken into account to determine if valid correlation exists. » (Page 75).

**Vision Macro :**L'enjeu est de combattre la **corrélation illusoire**, un biais cognitif où l'on perçoit une relation entre un signal et un mouvement de prix alors qu'elle n'existe pas. Aronson explique que le cerveau humain est naturellement attiré par la « saillance » des succès (la cellule supérieure gauche), car ils sont gratifiants et confirment nos hypothèses. « Donner à toutes les cellules leur dû » est un acte de discipline scientifique qui force le trader à regarder l'ensemble du tableau statistique, incluant les échecs et les cas où le marché a bougé sans signal, pour transformer une intuition en connaissance justifiée.

**Vision Micro :**Le mécanisme de vérification repose sur la comparaison de deux ratios issus de la table de contingence (où le signal est le prédicteur binaire et le mouvement de prix est l'issue binaire) :

**Ratio avec signal (**P1​**) :** On divise le nombre de succès (Cellule A) par le total des signaux émis (Cellule A + Cellule B).

**Ratio sans signal (**P2​**) :** On divise le nombre de fois où le résultat espéré s'est produit sans signal (Cellule C) par le total des périodes sans signal (Cellule C + Cellule D).

**Comparaison :** Si P1​ est approximativement égal à P2​, le signal n'a aucun pouvoir prédictif. Il n'est qu'un témoin passif d'un événement qui se serait produit de toute façon\[5\]\[6\].

**Validation :** Le test du Chi-carré est ensuite appliqué pour mesurer si l'écart entre ces proportions est assez grand pour ne pas être attribué à un simple « saupoudrage aléatoire » des instances entre les quatre cellules\[5\]\[7\].

**Exemple du livre (L'étude de Smedslund, 1963) :**Aronson cite une expérience où des infirmières devaient juger si un symptôme était lié à une maladie sur 100 cas.

**Résultats :** 37 cas avec symptôme + maladie (Cellule A) ; 17 cas avec symptôme mais sans maladie (Cellule B) ; 33 cas sans symptôme mais avec maladie (Cellule C).

**Erreur :** 85 % des infirmières ont conclu que le symptôme était un bon prédicteur à cause des 37 succès « saillants »\[8\]\[9\].

**Réalité EBTA :** Le ratio de maladie avec symptôme était de 0,685 (37/54), tandis que le ratio sans symptôme était quasiment identique à 0,717 (33/46). La probabilité d'avoir la maladie était la même avec ou sans le symptôme. Le symptôme était donc inutile, malgré les nombreux cas de confirmation\[5\]\[6\].

**Résumé Simplifié :**Pour savoir si ton indicateur est bon, ne regarde pas seulement combien de fois il a "gagné". Regarde si tu aurais gagné autant d'argent en ne l'utilisant pas. Si le marché monte 70 % du temps quand ton indicateur dit "Achat", mais qu'il monte aussi 70 % du temps quand l'indicateur ne dit rien, alors ton indicateur est une illusion.

**Actions Concrètes :**

**Ne pas se fier aux graphiques choisis :** Ignorer toute présentation de stratégie qui ne montre que des exemples gagnants ("cherry picking")\[10\].

**Exiger les statistiques des 4 cellules :** Lors d'un backtest, vérifiez toujours le nombre de faux signaux (Cellule B) et la performance "naturelle" du marché (Base Rate).

**Calculer les deux proportions :** Calculez systématiquement le taux de réussite quand le signal est présent vs quand il est absent.

**Utiliser des règles objectives :** L'AT subjective ne permet pas de faire ce calcul car elle ne peut pas définir précisément quand un signal est "absent" ou quand il y a un "échec" sans changer les critères après coup\[11\]\[12\].

**À retenir absolument :**

La cellule "Haut-Gauche" (Succès) est un piège pour l'intuition si elle est isolée\[4\]\[13\].

Un signal valide doit **changer** la probabilité de l'issue\[5\]\[6\].

La saillance des preuves confirmatoires crée une illusion de validité\[3\]\[14\].

Sans les données sur les échecs et les non-événements, l'analyse est mythologique, pas scientifique\[11\].

Le test du Chi-carré est le juge de paix de la corrélation binaire\[5\]\[7\].
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] undefined
[7] undefined
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[9] undefined
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] undefined
[13] undefined
[14] undefined
