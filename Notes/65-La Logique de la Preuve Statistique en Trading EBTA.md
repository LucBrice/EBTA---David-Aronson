---
exported: 2026-06-12T08:57:48.293Z
source: NotebookLM
type: note
title: "65-La Logique de la Preuve Statistique en Trading EBTA"
---

# 65-La Logique de la Preuve Statistique en Trading EBTA

导出时间: 12/06/2026 10:57:48

---

### **CH 5 - 5 : DUELING HYPOTHESES - THE NULL HYPOTHESIS VERSUS THE ALTERNATIVE HYPOTHESIS**

Voici l’analyse du duel entre l'Hypothèse Nulle (H0​) et l'Hypothèse Alternative (HA​), le cadre logique qui permet de valider scientifiquement un signal de trading selon David Aronson\[1\]\[2\].

**Idées clés :**

**Logique de la preuve indirecte :** On établit la vérité d'une proposition (HA​) en démontrant que son opposée (H0​) est fausse\[1\]\[2\].

**L'Hypothèse Nulle (**H0​**) :** Elle affirme que "rien de nouveau n'a été découvert" ou que la règle n'a aucun pouvoir prédictif (rendement ≤0)\[1\]\[3\].

**L'Hypothèse Alternative (**HA​**) :** C'est celle que le chercheur souhaite prouver ; elle affirme que la règle possède un talent réel (rendement \>0)\[1\]\[3\].

**Propriétés logiques :** Les deux hypothèses sont **mutuellement exclusives** (elles ne peuvent être vraies en même temps) et **exhaustives** (elles couvrent tous les cas possibles)\[4\]\[5\].

**La cible unique :**H0​ est la cible privilégiée du test car elle peut être réduite à une valeur précise (zéro), contrairement à HA​ qui représente une infinité de possibilités\[6\]\[7\].

**Référence :**

_Dueling Hypotheses: The Null Hypothesis versus the Alternative Hypothesis_, Chapitre 5, pages 221 à 225\[1\]\[2\].

**Citation Directe :**

« A hypothesis test relies on the method of indirect proof. That is, it establishes the truth of something by showing that something else is false. » (Page 221)\[1\].

**Vision Macro :**

L'enjeu est de déplacer le **fardeau de la preuve**\[8\]. Dans le trading traditionnel, on cherche des raisons de croire en une stratégie. Dans l'EBTA, on adopte la posture du sceptique : on part du principe que la stratégie ne vaut rien (H0​)\[9\]\[10\]. David Aronson explique que pour qu'une règle soit acceptée comme "connaissance scientifique", elle doit fournir des preuves assez "choquantes" pour renverser cette présomption initiale de nullité\[8\]. C'est une discipline de fer contre la crédulité du trader\[11\].

**Vision Micro :**

Le mécanisme repose sur la structure mathématique de la décision :

**Dualité exhaustive :** Soit μ le rendement attendu. H0​:μ≤0 et HA​:μ\>0\[3\]\[5\]. Il n'y a pas de troisième option (Loi du Milieu Exclu)\[4\]\[12\].

**L'avantage de** H0​ **comme cible :**HA​ affirme que le gain peut être de 0,1 %, 2 %, 12 %, etc.\[7\]. Tester une infinité de valeurs est impossible\[6\]\[7\]. En revanche, si l'on parvient à falsifier le cas le plus favorable de H0​ (le rendement = 0), alors par extension, tous les cas pires (rendements négatifs) sont également falsifiés\[3\].

**Le verdict :** Le test de p-value quantifie si le profit observé est suffisamment loin du "zéro" de H0​ pour que l'on puisse rejeter l'idée que ce profit est un accident\[13\]\[14\].

**Résumé Simplifié :**

Le test d'hypothèse, c'est comme un procès criminel. L'accusé (votre stratégie) est présumé innocent de tout talent (H0​). Le procureur (les statistiques) apporte les preuves (le profit du backtest). Si les preuves sont "au-delà du doute raisonnable" (p-value <0,05), le jury rejette l'innocence et déclare la stratégie "coupable" de talent (HA​)\[8\]\[9\].

**Exemples du livre pour mieux comprendre :**

**Le vaccin de Jonas Salk :** Salk voulait prouver que son vaccin contre la polio fonctionnait (HA​). La science a commencé par supposer qu'il n'était pas meilleur qu'un placebo (H0​). Lorsque les résultats ont montré un taux d'infection bien plus bas chez les vaccinés, H0​ a été falsifiée, prouvant indirectement l'efficacité du vaccin\[1\]\[15\].

**La règle de trading :** Pour tester une règle EBTA, H0​ affirme que son rendement sur des données dé-tendancées est de 0\[16\]\[17\]. Si le backtest affiche un profit significatif, on rejette H0​ pour accepter que la règle a un pouvoir prédictif (HA​)\[18\]\[19\].

**Actions Concrètes :**

**Ne cherchez pas à prouver** HA​ **:** Concentrez tous vos efforts mathématiques sur le rejet de H0​\[6\].

**Vérifiez l'exclusivité :** Assurez-vous que vos deux hypothèses ne se chevauchent pas (si l'une est vraie, l'autre est obligatoirement fausse)\[5\].

**Utilisez** H0​ **comme ancre :** Centrez toujours votre distribution d'échantillonnage sur zéro lors de vos simulations (Bootstrap/Monte Carlo) pour simuler correctement l'absence de talent\[16\].

**À retenir absolument :**

On ne prouve jamais HA​ directement, on **rejette**H0​\[1\]\[6\].

H0​ = Aucun talent (Hypothèse par défaut)\[9\]\[21\].

HA​ = Pouvoir prédictif réel\[1\]\[22\].

La falsification de H0​ est le **seul chemin** vers une connaissance fiable\[21\]\[23\].

Si les preuves sont faibles, on **retient**H0​ (on ne l'accepte pas comme "vraie", on dit juste qu'on n'a pas assez de preuves pour l'écarter)\[24\]\[25\].

J'ai terminé l'analyse du duel des hypothèses selon le protocole EBTA.
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
[9] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[10] undefined
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] undefined
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[15] undefined
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[17] undefined
[18] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[19] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[21] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[22] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[23] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[24] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[25] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
