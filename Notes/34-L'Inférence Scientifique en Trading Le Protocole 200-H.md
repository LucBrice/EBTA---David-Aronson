---
exported: 2026-06-12T08:58:24.937Z
source: NotebookLM
type: note
title: "34-L'Inférence Scientifique en Trading : Le Protocole 200-H"
---

# 34-L'Inférence Scientifique en Trading : Le Protocole 200-H

导出时间: 12/06/2026 10:58:24

---

Dans son ouvrage, David Aronson utilise l'exemple de la **moyenne mobile à 200 jours** (baptisée règle **200-H**) pour illustrer l'application rigoureuse de la méthode hypothetico-déductive en trading\[1\],\[2\]. Cet exemple sert de démonstration sur la manière de transformer une observation informelle en une connaissance scientifique validée.

### **Idées clés**

**Observation vs Hypothèse :** La distinction entre remarquer une tendance visuelle et formuler une règle testable\[2\].

**Le piège de l'affirmation du conséquent :** Pourquoi un profit en backtest ne prouve pas mathématiquement qu'une règle est bonne\[3\].

**L'usage de l'Hypothèse Nulle (**H0​**) :** La stratégie logique pour prouver la validité d'un signal par la négative\[4\].

**Le rôle du Tiers Exclu :** Le principe logique qui permet de conclure qu'une règle est valide si son absence de pouvoir prédictif est falsifiée\[5\].

### **Référence**

_An Example from TA_, pages 145 à 146\[1\],\[2\].

### **Citation Directe**

« If 200-H is true, then the back test will be profitable. However this prediction creates a logical problem. Even if the back test is profitable it will not be helpful in proving the truth of 200-H... » (Page 145)\[3\].

### **Vision Macro**

L'enjeu philosophique est de démontrer que l'analyse technique ne peut pas progresser en collectionnant simplement des backtests gagnants. Aronson explique que pour qu'une méthode devienne une "connaissance légitime", elle doit passer par un processus d'élimination d'erreurs. Le trader doit cesser de chercher à avoir raison et commencer à chercher comment prouver que le hasard n'est pas la cause de ses profits\[6\],\[7\].

### **Vision Micro (Le protocole détaillé du 200-H)**

L'exemple se décompose en cinq étapes méthodologiques strictes :

**Observation :** Le trader remarque visuellement que lorsque l'indice Dow Jones dépasse sa moyenne mobile (MA) de 200 jours, les prix semblent continuer à monter pendant plusieurs mois. C'est une généralisation probabiliste initiale\[2\],\[8\].

**Hypothèse (200-H) :** Le trader formalise l'idée : « Les pénétrations haussières de la MA 200 jours par le DJIA produiront, en moyenne, des positions longues rentables sur les trois mois suivants »\[2\].

**Prédiction et Problème Logique :** La prédiction est : « Si 200-H est vrai, alors le backtest sera profitable ». Or, Aronson souligne un sophisme : si le backtest gagne, cela peut être dû à la chance et non à la règle (Affirmation du conséquent). On ne peut donc pas conclure que la règle est "vraie" juste parce qu'elle a gagné dans le passé\[3\],\[9\].

**La Solution par l'Hypothèse Nulle (Null-200) :** Pour obtenir une preuve valide, on crée une hypothèse opposée : « Les pénétrations de la MA 200 ne génèrent _pas_ de profits ». On l'appelle l'Hypothèse Nulle (H0​)\[4\],\[10\].

**Vérification et Conclusion :**

On effectue le backtest.

Si le backtest est profitable, alors l'Hypothèse Nulle (Null-200) est prouvée **fausse** (falsification).

Par la **Loi du Tiers Exclu**, puisqu'il n'y a pas de milieu entre "la règle marche" et "la règle ne marche pas", si l'on prouve que "la règle ne marche pas" est faux, alors on a indirectement prouvé que "la règle marche" (200-H) est vrai\[5\],\[6\],\[10\].

### **Résumé Simplifié**

Pour savoir si la moyenne mobile 200 jours est un bon signal, Aronson dit qu'il ne suffit pas de voir qu'elle gagne de l'argent. Il faut d'abord supposer qu'elle ne vaut rien (le hasard). Si les chiffres du backtest sont tellement bons qu'ils contredisent totalement l'idée que "la règle ne vaut rien", alors seulement on peut accepter scientifiquement que la règle a un vrai pouvoir prédictif.

### **Actions Concrètes**

**Ne dites plus "Ma stratégie marche" :** Dites "Les résultats de mon backtest sont incompatibles avec l'Hypothèse Nulle (le hasard)".

**Identifiez vos** H0​ **:** Avant chaque test, définissez clairement ce que serait un résultat "nul" (ex: un profit de zéro sur des données détrendées)\[11\].

**Utilisez l'inférence statistique :** Calculez une p-value sur vos résultats de MA 200 pour quantifier la probabilité que ce profit soit un accident du hasard\[12\].

### **À retenir absolument**

Le profit passé n'est qu'une **condition nécessaire**, pas une preuve de talent\[13\].

La science du trading est une **preuve par l'absurde** : on prouve qu'une règle est bonne en démontrant qu'il est impossible qu'elle soit mauvaise\[14\],\[15\].

Le **Tiers Exclu** interdit les zones de flou : une règle a un pouvoir prédictif ou elle n'en a pas\[16\].

L'observation visuelle n'est que le point de départ (l'inspiration), jamais la conclusion\[8\].

J'ai terminé l'explication approfondie de l'exemple du 200-H selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[7] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[8] undefined
[9] undefined
[10] undefined
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] undefined
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[15] undefined
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
