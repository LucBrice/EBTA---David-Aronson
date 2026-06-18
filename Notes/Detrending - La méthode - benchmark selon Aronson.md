---
exported: 2026-06-12T08:57:54.365Z
source: NotebookLM
type: note
title: "Detrending - La méthode - benchmark selon Aronson"
---

# Detrending - La méthode - benchmark selon Aronson

导出时间: 12/06/2026 10:57:54

---

Voici la fiche méthode exhaustive et chronologique du **Detrending** (Dé-tendance), incluant précisément le timing, les entrées (_inputs_) et les sorties (_outputs_), conformément à la méthodologie de David Aronson.

### **Idées clés :**

**Neutralisation du biais :** Élimine le profit "gratuit" généré par un marché haussier ou baissier pour isoler le talent pur de la règle\[1\]\[2\].

**Stationnarité artificielle :** Transforme une série de prix en une série stationnaire dont la moyenne est strictement zéro\[3\]\[4\].

**Dualité des données :** Sépare les données servant à la décision (signaux) de celles servant à l'évaluation (profits)\[5\]\[6\].

**Benchmarking simplifié :** Évite de devoir calculer un étalon différent pour chaque règle testée\[6\]\[7\].

### **Référence :**

_A Simpler Solution to Benchmarking: Detrending the Market Data_ (Pages 27–30 ; Audiobook Transcriptions 136-146)\[5\]\[6\].

### **Citation Directe :**

« The easier method merely requires that the historical data for the market being traded (e.g., S&P 500 Index) be detrended prior to rule testing. It is important to point out that the detrended data is used only for the purpose of calculating daily rule returns. It is not used for signal generation. » (Page 27-28)\[5\]\[6\]._(Traduction : La méthode la plus simple exige seulement que les données historiques du marché... soient dé-tendancées avant le test de la règle. Il est important de souligner que les données dé-tendancées sont utilisées uniquement pour calculer les rendements quotidiens de la règle. Elles ne sont pas utilisées pour la génération de signaux.)_

\--------------------------------------------------------------------------------

### **Vision Macro**

L'enjeu est de créer un **étalon scientifique universel**. Aronson explique que l'analyse technique subjective échoue car elle ne sait pas si ses gains viennent d'une lecture géniale du prix ou simplement du fait que l'actif a monté pendant que le trader était à l'achat\[8\]\[9\]. Le detrending est le "tapis roulant arrêté" : il force la stratégie à prouver qu'elle peut générer un profit positif sur un marché qui, statistiquement, ne va nulle part (rendement attendu = 0)\[10\]\[11\].

\--------------------------------------------------------------------------------

### **Vision Micro : Le Processus Détaillé**

**1\. Phase de Pré-Traitement (Le "Quand" : Avant le backtest)**

**Input (Entrée) :** La série temporelle des prix réels (ex: clôtures quotidiennes du S&P 500)\[5\]\[12\].

**Processus :**

Calculer les rendements logarithmiques quotidiens pour chaque jour t : Rt​\=Log(Pt​/Pt−1​)\[13\]\[14\].

Calculer la moyenne arithmétique de tous les Rt​ sur l'ensemble de la période de test (Average Log Return - ALR)\[14\]\[15\].

Soustraire l'ALR de chaque rendement quotidien réel : Rdetrended,t​\=Rt​−ALR\[14\]\[15\].

**Output (Sortie) :** Une nouvelle série de rendements dont la somme et la moyenne sont exactement égales à zéro\[10\]\[11\].

**2\. Phase de Backtest (Le "Quand" : Pendant l'exécution)**

C'est ici que la méthode EBTA devient spécifique en utilisant deux flux de données parallèles :

**Flux A (Données Réelles) :** Sert d'**input** au moteur de calcul de la règle pour générer les signaux (ex: calculer une moyenne mobile sur les prix réels)\[5\]\[6\].

**Flux B (Données Detrendées) :** Sert d'**input** uniquement pour le calcul du profit\[5\]\[6\].

**Calcul de la performance :**

Si la règle dit "Long" (+1) à la clôture du jour 0, son profit pour le jour 1 sera : +1×Rdetrended,1​\[16\]\[17\].

Si elle dit "Short" (−1), son profit sera : −1×Rdetrended,1​\[16\]\[17\].

**3\. Phase de Résultat (Le "Quand" : Fin du test)**

**Output Final :** Le rendement moyen cumulé de la règle sur les données detrendées.

**Si** \>0 **:** La règle possède un pouvoir prédictif (elle a capturé des anomalies de prix au-delà de la tendance)\[13\]\[18\].

**Si** ≈0 **ou** ≤0 **:** La règle n'a aucune valeur ; ses profits en données réelles n'étaient qu'une illusion causée par la tendance du marché\[10\]\[11\].

\--------------------------------------------------------------------------------

### **Résumé Simplifié**

Imaginez un athlète qui court sur un train en marche. Le train (le marché) avance à 50 km/h. L'athlète (votre stratégie) court à 55 km/h dans la même direction. Le detrending consiste à arrêter le train par la pensée pour voir que l'athlète ne court réellement qu'à 5 km/h. Si l'athlète court à 50 km/h alors que le train va à 50 km/h, il ne bouge pas par rapport au train : son profit réel est de zéro.

\--------------------------------------------------------------------------------

### **Actions Concrètes pour le Trader**

**Séquence stricte :** Transformez votre base de données de prix en rendements logs, calculez la moyenne globale, et créez une colonne "rendements\_detrendés" avant de coder votre backtest\[13\].

**Honnêteté des signaux :** N'utilisez **jamais** les prix detrendés pour vos indicateurs (RSI, MACD, etc.). Utilisez les prix réels pour décider, mais les prix "aplatis" pour compter vos points\[5\]\[11\].

**Évaluation :** Toute règle qui finit négative sur des données detrendées doit être jetée, même si elle semble gagner de l'argent sur votre graphique habituel\[10\]\[11\].

\--------------------------------------------------------------------------------

### **À retenir absolument**

**Timing :** Le calcul de la moyenne de tendance se fait sur la **totalité** de l'échantillon historique avant de commencer\[5\]\[6\].

**Input du test :** Prix réels (pour le signal) + Rendements detrendés (pour le profit)\[5\].

**Output du detrending :** Une série de prix horizontale (moyenne = 0)\[10\]\[11\].

**Objectif :** Ne pas confondre la "marée montante" (marché) avec la "puissance du moteur" (votre règle)\[8\]\[9\].

**Rendement nul :** Une règle de hasard rapportera toujours **exactement 0** dans un monde detrendé\[11\].

J'ai terminé la fiche méthode détaillée sur le processus de detrending selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] undefined
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] undefined
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] undefined
[7] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[9] undefined
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] undefined
[12] undefined
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] undefined
[15] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[17] undefined
[18] undefined
