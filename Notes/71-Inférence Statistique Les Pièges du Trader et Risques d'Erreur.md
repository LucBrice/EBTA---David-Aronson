---
exported: 2026-06-12T08:57:41.547Z
source: NotebookLM
type: note
title: "71-Inférence Statistique : Les Pièges du Trader et Risques d'Erreur"
---

# 71-Inférence Statistique : Les Pièges du Trader et Risques d'Erreur

导出时间: 12/06/2026 10:57:41

---

### **CH 5 - 5 : TEST CONCLUSIONS AND ERRORS**

Cette section traite des conclusions possibles d'un test d'hypothèse et des erreurs inhérentes à l'inférence statistique, soulignant les conséquences asymétriques pour le capital du trader\[1\]\[2\].

**Idées clés :**

**Quatre issues possibles :** Un test débouche sur deux types de décisions correctes ou deux types d'erreurs\[1\].

**Erreur de Type I (Faux Positif) :** Rejeter l'Hypothèse Nulle (H0​) alors qu'elle est vraie, ce qui revient à prendre de la chance pour du talent\[3\].

**Erreur de Type II (Faux Négatif) :** Retenir H0​ alors qu'elle est fausse, ce qui conduit à ignorer une règle réellement prédictive\[3\].

**Gravité asymétrique :** L'erreur de Type I est jugée plus sérieuse car elle expose le capital à un risque sans espoir de compensation\[2\].

**Référence :**

_Test Conclusions and Errors_ (Pages 233 à 234).

**Citation Directe :**

« A type I error, where H0​ is mistakenly rejected, leads to the use of a worthless rule. This exposes trading capital to risk without the prospect of compensation. » (Page 234)\[2\].

**Vision Macro :**

L'enjeu est la survie du trader dans un environnement incertain où la "Vérité" absolue n'est accessible qu'à une entité omnisciente\[1\]\[2\]. David Aronson explique que tout test statistique est un pari sur la réalité basé sur des preuves incomplètes\[1\]. Le trader doit naviguer entre deux écueils : la crédulité (Type I), qui détruit le capital, et l'excès de scepticisme (Type II), qui fait rater des opportunités\[2\]\[3\]. L'EBTA privilégie une posture conservatrice pour protéger les ressources financières\[2\].

**Vision Micro :**

Le mécanisme de décision se divise en fonction de l'état de la réalité et du résultat du test :

**Les Décisions Correctes :**

Rejeter H0​ quand la règle a du mérite (H0​ est fausse)\[4\].

Accepter H0​ quand la règle est inutile (H0​ est vraie)\[4\].

**L'Erreur de Type I (Le piège de la chance) :**

Elle se produit lorsqu'une p-value faible est obtenue par pur hasard\[3\].

Le trader conclut à tort que la règle a un pouvoir prédictif\[2\]\[3\].

**L'Erreur de Type II (Le talent ignoré) :**

Elle survient lorsqu'une p-value élevée est obtenue malgré la validité de la règle (souvent à cause d'un échantillon trop petit ou de "malchance" lors du backtest)\[3\].

La capacité d'un test à éviter cette erreur est appelée sa **puissance statistique** (Power)\[5\].

**Résumé Simplifié :**

Un test statistique est un tribunal pour tes stratégies\[1\]. Soit tu condamnes un innocent (Erreur Type I : tu trades une stratégie nulle en croyant qu'elle est bonne), soit tu libères un coupable (Erreur Type II : tu jettes une bonne stratégie en croyant qu'elle ne vaut rien)\[2\]\[3\]. Pour Aronson, il vaut mieux rater un gain que de subir une perte sur une illusion\[2\].

**Exemples du livre pour mieux comprendre :**

**La réalité "connue de Dieu seul" :** Aronson utilise cette expression pour rappeler qu'au moment du test, personne ne peut être certain qu'une erreur n'a pas été commise\[1\].

**Le capital vs l'opportunité :** Perdre son capital (Type I) signifie être "hors du jeu", alors que rater une opportunité (Type II) n'est pas fatal car il y aura toujours d'autres occasions sur le marché\[2\].

**Actions Concrètes :**

**Prioriser la défense :** Acceptez le risque de commettre une erreur de Type II (manquer un signal) pour minimiser radicalement le risque de Type I (perte de capital sur du bruit)\[2\].

**Rigidité du seuil :** Fixez un seuil de p-value strict (ex: 0,05) et ne le modifiez pas pour "sauver" une règle dont le résultat est ambigu\[6\].

**Augmenter la taille d'échantillon :** Pour réduire le risque de Type II (augmenter la puissance du test), utilisez le plus grand historique de données disponible\[7\].

**À retenir absolument :**

**Type I** = Croire à une illusion (rejet injustifié de H0​)\[3\].

**Type II** = Manquer une vérité (rétention injustifiée de H0​)\[3\].

Le Type I est l'erreur la plus **dangereuse** pour le trader\[2\].

Rétention de H0​ = Absence de preuve, pas preuve de nullité\[8\].

Un test n'est jamais une certitude, mais une **gestion des risques d'erreur**\[2\].

J'ai terminé l'analyse des conclusions et erreurs de test selon le protocole EBTA.
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
