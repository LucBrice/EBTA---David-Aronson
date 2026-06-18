---
exported: 2026-06-12T08:56:54.301Z
source: NotebookLM
type: note
title: "115-L'Équilibre entre Biais de Minage et Taille d'Échantillon"
---

# 115-L'Équilibre entre Biais de Minage et Taille d'Échantillon

导出时间: 12/06/2026 10:56:54

---

### **CH 6 : DATA-MINING BIAS AS A FUNCTION OF UNIVERSE SIZE: IN A UNIVERSE OF VARIABLE MERIT**

Cette section explore comment l'ampleur du biais de minage de données évolue en fonction du nombre de règles testées dans un contexte réaliste où certaines règles possèdent un véritable pouvoir prédictif (mérite variable)\[1\]\[2\].

**Idées clés :**

**Impact massif de l'échantillon :** La taille de l'historique (nombre d'observations) est le facteur dominant qui détermine si le biais sera gérable ou catastrophique\[3\]\[4\].

**Biais extrême sur échantillon court :** Avec seulement deux mois de données, le biais de minage peut faire surévaluer le profit annuel de plus de 200 %\[3\].

**Stabilisation rapide :** Lorsque l'échantillon est suffisant (ex: 100 ou 1 000 mois), le biais cesse de croître de manière significative après que l'on a testé environ 30 règles\[5\].

**Le paradoxe du minage extensif :** Tester davantage de règles (passer de 30 à 250) augmente peu le biais si les données sont abondantes, mais augmente les chances de trouver une règle de haut mérite\[5\].

**Référence :**

_Data-Mining Bias as a Function of Universe Size: In a Universe of Variable Merit_ (Pages 311–314).

**Citation Directe :**

« For short performance histories, the data-mining bias is extreme. \[...\] After approximately 30 ATRs have been examined, increasing the number tested has a minimal effect on the size of the data-mining bias. » (Pages 312 et 314)\[3\]\[5\].

\--------------------------------------------------------------------------------

**Vision Macro :**

L'enjeu est de lever la peur du "nombre de tests" au profit de la "qualité des données". David Aronson démontre que, contrairement à une idée reçue, tester des milliers de règles n'est pas forcément suicidaire si l'on dispose d'un historique très long\[4\]\[5\]. Dans un univers où le talent existe (mérite variable), le minage de données intensif devient une stratégie gagnante car le coût statistique (l'augmentation du biais) plafonne rapidement, alors que le bénéfice potentiel (trouver une règle exceptionnelle) continue de croître\[5\]\[6\].

\--------------------------------------------------------------------------------

**Vision Micro :**

**L'Expérience avec 2 observations (Figure 6.44) :**

Sur un historique de seulement deux mois, le processus de sélection est "aveugle" au mérite réel\[6\].

Le biais explose : pour 256 règles testées, le profit affiché est gonflé de **200 %** par rapport à la réalité\[3\]. Ici, le minage ne produit que du « métal des fous »\[7\].

**L'Expérience avec 100 et 1 000 observations (Figures 6.45 & 6.46) :**

**À 100 mois :** Le biais pour 256 règles tombe à environ **18 %**\[3\].

**À 1,000 mois :** Le biais est réduit à moins de **3 %**\[3\].

**Convergence :** Les courbes montrent que le biais augmente fortement entre 1 et 30 règles, puis s'aplatit\[5\].

**Le seuil de 30 règles (Figure 6.48) :**

Aronson identifie un point d'inflexion : après 30 tentatives, la "cloche" du hasard a déjà produit ses effets les plus probables\[5\].

Au-delà de ce seuil, le "prix" à payer en termes de biais supplémentaire pour chaque nouvelle règle testée devient marginal\[5\].

\--------------------------------------------------------------------------------

**Résumé Simplifié :**

Imaginez que vous cherchiez un champion de tir. Si vous ne regardez qu'un seul tir (échantillon faible), tester 200 tireurs va forcément vous faire choisir un chanceux qui a touché le centre par accident (biais énorme)\[3\]. Mais si vous regardez 1 000 tirs par personne, tester 200 candidats au lieu de 30 ne vous trompera pas beaucoup plus, mais vous donnera beaucoup plus de chances de débusquer le véritable champion olympique caché dans la foule\[5\].

\--------------------------------------------------------------------------------

**Actions Concrètes :**

**Prioriser le "N" (Observations) sur le "N" (Règles) :** Ne vous limitez pas arbitrairement à tester 5 ou 10 règles si vous avez 20 ans de données ; vous pouvez en tester des centaines sans que le biais ne devienne incontrôlable\[5\].

**Seuil de méfiance automatique :** Si votre historique de backtest est court (moins de 2-3 ans de données mensuelles), considérez que n'importe quel profit affiché est une illusion totale\[3\].

**Exploiter le plafonnement du biais :** Une fois que vous avez optimisé une trentaine de variantes, sachez que continuer l'optimisation ne dégradera plus beaucoup la fiabilité de votre estimation, à condition d'utiliser un échantillon large\[5\].

\--------------------------------------------------------------------------------

**À retenir absolument :**

L'échantillon court rend le minage de données **dangereux et inutile**\[6\].

Le biais de minage **plafonne (se stabilise)** après environ 30 règles testées\[5\].

Sur un échantillon large, le biais est **étonnamment faible** (ex: < 3% sur 1000 mois)\[3\].

Tester plus de règles est une **bonne chose** si, et seulement si, l'échantillon est suffisant\[5\].

Le **nombre d'observations** est le véritable juge de paix de la validité EBTA\[8\].

J'ai terminé l'analyse de l'impact de la taille de l'univers de recherche sur le biais de minage selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[7] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
