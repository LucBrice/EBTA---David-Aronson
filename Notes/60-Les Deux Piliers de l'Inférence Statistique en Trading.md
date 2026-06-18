---
exported: 2026-06-12T08:57:53.334Z
source: NotebookLM
type: note
title: "60-Les Deux Piliers de l'Inférence Statistique en Trading"
---

# 60-Les Deux Piliers de l'Inférence Statistique en Trading

导出时间: 12/06/2026 10:57:53

---

### **CH 5 - 1 : TWO TYPES OF STATISTICAL INFERENCE**

Voici l’analyse des deux piliers de l'inférence statistique, les outils que David Aronson utilise pour transformer les données de backtesting en connaissances scientifiques exploitables\[1\]\[2\].

**Idées clés :**

L'inférence statistique se subdivise en deux procédures distinctes : le **test d'hypothèse** et l'**estimation de paramètre**\[1\].

Ces deux méthodes s'intéressent à la valeur inconnue d'un **paramètre de population** (la performance future réelle de la stratégie) à partir d'un échantillon limité (le backtest)\[1\]\[3\].

Le test d'hypothèse est une procédure de décision binaire : il détermine si un effet est présent ou non\[1\]\[3\].

L'estimation est une procédure quantitative : elle cherche à déterminer la taille ou l'ampleur de cet effet\[1\].

**Référence :**

_TWO TYPES OF STATISTICAL INFERENCE_ (Pages 217–218 ; Audiobook Transcriptions 135-136, 168).

**Citation Directe :**

« Statistical inference encompasses two procedures: hypothesis testing and parameter estimation. Both are concerned with the unknown value of a population parameter. \[...\] A hypothesis test tells us if an effect is present or not, whereas an estimate tells us about the size of an effect. » (Page 217)\[1\].

**Vision Macro :**

L'enjeu pour le trader est de naviguer dans l'incertitude sans se fier à des "comptes de fées"\[4\]. Comme on ne peut pas observer l'intégralité du futur, on doit faire un "saut inductif"\[3\]\[5\]. Le test d'hypothèse agit comme un garde-fou contre l'illusion (la chance), tandis que l'estimation permet de planifier rationnellement l'avenir financier en quantifiant ce que la stratégie peut réellement rapporter\[6\]\[7\].

**Vision Micro :**

**Le Test d'Hypothèse (Hypothesis Testing) :**

**Mécanisme :** On commence par une conjecture (souvent l'Hypothèse Nulle H0​ : "la règle n'a aucun talent")\[8\]\[9\].

**Logic :** On utilise la falsification. Si le résultat observé est trop improbable sous l'hypothèse H0​, on rejette cette dernière au profit de l'hypothèse alternative HA​\[10\]\[11\].

**Résultat :** Une conclusion du type "Rejeter" ou "Ne pas rejeter" H0​\[12\].

**L'Estimation de Paramètre (Parameter Estimation) :**

**Point Estimate (Estimation ponctuelle) :** C'est une valeur unique, comme la moyenne des rendements du backtest, utilisée pour deviner le rendement futur\[13\]\[14\].

**Interval Estimate (Estimation par intervalle) :** On définit une plage de valeurs (ex: entre 5 % et 15 %) assortie d'un niveau de probabilité (ex: 95 %)\[13\]\[15\].

**Avantage :** L'intervalle de confiance est plus informatif car il combine l'estimation du profit avec la mesure de l'incertitude (variabilité)\[16\].

**Résumé Simplifié :**

Imagine que tu testes un nouveau moteur. Le **test d'hypothèse** répond à la question : "Est-ce que le moteur démarre vraiment grâce à sa technologie ou est-ce un hasard ?" (C'est le filtre de sécurité). L'**estimation** répond à : "À quelle vitesse va-t-il me propulser et avec quelle marge d'erreur ?" (C'est l'outil de mesure de performance)\[1\]\[2\].

**Actions Concrètes :**

**Ne jamais estimer avant de tester :** Ne perdez pas de temps à calculer vos gains futurs potentiels si votre stratégie n'a pas d'abord prouvé sa signification statistique (p-value < 0,05)\[17\]\[18\].

**Utiliser l'estimation comme appoint :** Dans les études EBTA, l'estimation est utilisée comme un complément aux tests d'hypothèse pour affiner la compréhension de la règle\[15\].

**Privilégier les intervalles :** Ne dites jamais "ma stratégie rapporte 10 %", dites "il y a 95 % de chances que ma stratégie rapporte entre 5 % et 15 %" pour rester ancré dans la réalité statistique\[13\]\[15\].

**À retenir absolument :**

**Test d'hypothèse** = Existe-t-il un avantage réel ?\[1\].

**Estimation** = Quelle est l'importance de cet avantage ?\[1\].

Toute inférence est un **saut inductif** et comporte donc un risque d'erreur\[3\].

L'**intervalle de confiance** est la forme la plus riche d'estimation car il quantifie le doute\[16\].

Sans ces outils, le trader est victime de ses propres **biais cognitifs** (ex: biais de confirmation)\[6\]\[10\].

J'ai terminé l'analyse des deux types d'inférence statistique selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] undefined
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] undefined
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[7] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[9] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[15] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[17] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[18] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
