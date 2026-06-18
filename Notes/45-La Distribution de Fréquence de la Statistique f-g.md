---
exported: 2026-06-12T08:58:12.715Z
source: NotebookLM
type: note
title: "45-La Distribution de Fréquence de la Statistique f-g"
---

# 45-La Distribution de Fréquence de la Statistique f-g

导出时间: 12/06/2026 10:58:12

---

### **CH 4 - 8 : FREQUENCY DISTRIBUTION OF THE SAMPLE STATISTIC** f−g

Voici l'analyse de la distribution de fréquence de la statistique d'échantillon f−g, l'outil visuel qui permet de transformer des données brutes en une compréhension de la variabilité statistique.

### **Idées clés :**

**Visualisation de l'aléa :** La distribution de fréquence permet de voir d'un coup d'œil comment les résultats d'un échantillon s'éparpillent à cause du hasard\[1\]\[2\].

**La forme en "bosse" :** Les valeurs de f−g ont tendance à s'accumuler autour d'une valeur centrale, révélant la structure cachée derrière le chaos apparent\[3\]\[4\].

**L’équivalence fréquence-aire :** La surface occupée par les barres de l'histogramme correspond exactement au nombre d'observations, un principe fondamental pour calculer des probabilités\[5\]\[6\].

**Réduction de l'incertitude :** Une distribution étroite indique une connaissance plus fiable de la population qu'une distribution large\[7\]\[8\].

\--------------------------------------------------------------------------------

### **Référence :**

_Frequency Distribution of the Sample Statistic_ f−g (Pages 179–183 du PDF ; Transcriptions audio 138-143)\[2\]\[9\].

\--------------------------------------------------------------------------------

### **Citation Directe :**

« A plot called a frequency distribution or frequency histogram communicates this information more forcefully than words or a table. It displays how frequently each of f-g's possible values occurred over the 50 sampling experiments. » (Page 179)\[1\]\[2\].

\--------------------------------------------------------------------------------

### **Vision Macro :**

L'enjeu pour le trader est de cesser de regarder un résultat de backtest comme un chiffre unique et définitif. Aronson utilise l'expérience des billes pour démontrer que le rendement observé n'est qu'une des nombreuses possibilités qu'aurait pu produire le hasard\[10\]\[11\]. La distribution de fréquence est le "théâtre" où l'on observe la lutte entre la vérité de la stratégie (F−G) et le bruit de l'échantillonnage\[12\]\[13\]. Sans cette vision globale, le trader risque de sur-réagir à un échantillon chanceux ou de désespérer face à un échantillon malchanceux\[14\]\[15\].

\--------------------------------------------------------------------------------

### **Vision Micro :**

Le mécanisme de construction et d'interprétation de la distribution de f−g repose sur des étapes statistiques strictes :

**Définition de la variable :** Pour un échantillon de 20 billes, f−g peut prendre 21 valeurs possibles (de 0,00 à 1,00 par paliers de 0,05)\[16\]\[17\].

**Collecte et triage (Bins) :** Après 50 tirages, on compte combien de fois chaque valeur est apparue (ex: la valeur 0,60 est apparue 10 fois)\[2\]\[9\].

**Construction de l'histogramme :**

**Axe horizontal :** Les intervalles (bins) représentant les valeurs possibles de f−g\[1\]\[2\].

**Axe vertical :** La fréquence (le nombre de fois où cette valeur a été observée)\[1\]\[6\].

**Fréquence Relative :** On divise la fréquence absolue par le nombre total d'échantillons (50). Si une valeur apparaît 10 fois, sa fréquence relative est de 10/50\=0,20 (soit 20%)\[18\]\[19\].

**L’Aire comme Probabilité :** Puisque la somme de toutes les fréquences relatives est égale à 1,0 (100%), l'aire combinée de plusieurs barres permet de calculer la probabilité d'obtenir un résultat dans une certaine plage\[20\]\[21\].

_Exemple du livre :_ La fréquence relative d'obtenir un f−g≥0,65 est de 0,20. Cela signifie qu'il y a 20% de chances que le hasard produise un résultat aussi bon ou meilleur que celui-ci\[21\]\[22\].

\--------------------------------------------------------------------------------

### **Résumé Simplifié :**

Imagine que tu notes les scores de 50 parties de fléchettes. Au lieu de regarder chaque score un par un, tu fais un graphique qui montre combien de fois tu as fait 10, 20 ou 50 points. Ce graphique va former une "bosse" là où tu es le plus souvent\[3\]\[4\]. Cette bosse te dit quelle est ta force réelle, et les bords du graphique te montrent à quel point tu peux être chanceux ou malchanceux d'un coup à l'autre\[7\].

\--------------------------------------------------------------------------------

### **Actions Concrètes :**

**Ne vous contentez pas d'une moyenne :** Demandez toujours à voir la distribution des rendements quotidiens ou hebdomadaires de votre backtest.

**Vérifiez la "bosse" :** Si vos résultats sont totalement éparpillés sans centre clair, votre stratégie est probablement dominée par le bruit pur\[7\]\[8\].

**Calculez les probabilités de queue :** Utilisez la fréquence relative pour savoir si votre meilleur trade est un événement normal (au centre de la bosse) ou une anomalie chanceuse (dans la queue droite)\[22\]\[23\].

**Utilisez des barres de fréquence :** En programmation de backtest, générez des histogrammes de performance pour visualiser la "stabilité" de l'avantage statistique\[1\]\[2\].

\--------------------------------------------------------------------------------

### **À retenir absolument :**

L'histogramme est l'outil n°1 pour **voir le hasard** en action\[1\].

L'**Aire sous la courbe** est égale à la probabilité totale (1,0)\[20\].

La **Variabilité d'échantillonnage** est la raison pour laquelle f−g change à chaque tirage\[10\]\[11\].

Plus la distribution est **étroite**, plus votre estimation de la performance réelle est précise\[7\]\[8\].

Le hasard suit un **motif organisé** (la bosse) dès qu'on multiplie les tests\[3\]\[4\].

J'ai terminé l'analyse de la distribution de fréquence de la statistique f−g selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] undefined
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] undefined
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] undefined
[7] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[8] undefined
[9] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] undefined
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[13] undefined
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[15] undefined
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[17] undefined
[18] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[19] undefined
[20] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[21] undefined
[22] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[23] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
