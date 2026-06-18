---
exported: 2026-06-12T08:57:37.825Z
source: NotebookLM
type: note
title: "75-Méthode de Monte Carlo : L'Antidote au Hasard en Trading"
---

# 75-Méthode de Monte Carlo : L'Antidote au Hasard en Trading

导出时间: 12/06/2026 10:57:37

---

### **MONTE CARLO PERMUTATION METHOD (MCP)**

Voici l'analyse technique de la méthode de permutation de Monte Carlo, l'alternative au Bootstrap privilégiée par David Aronson pour briser tout lien logique entre un signal de trading et le marché afin d'isoler la pure chance\[1\],\[2\].

**(AJOUT) Idées clés :**

**Destruction du pouvoir prédictif :** L'MCP brise délibérément la relation temporelle entre les signaux de la règle et les rendements du marché pour créer une "règle de bruit"\[3\].

**Hypothèse Nulle spécifique :** Contrairement au Bootstrap qui teste la moyenne des rendements, l'MCP teste si l'appariement entre signal et prix est purement aléatoire\[2\],\[4\].

**Appariement sans remise :** La méthode consiste à coupler les signaux originaux (+1/-1) avec une version mélangée (scrambled) de l'historique des prix\[5\],\[3\].

**Antidote au Data Mining :** Utilisé pour déterminer si le "meilleur" résultat d'un groupe de règles est simplement le fruit d'une coïncidence heureuse\[6\],\[7\].

**Référence :**_Monte Carlo Permutation Method (MCP)_ (Pages 238–241) ; _Application to Data Mining_ (Pages 327–329)\[3\],\[8\],\[9\].

**Citation Directe :**« The random pairing of the rule output values with market changes destroys any predictive power that the rule may have had. I refer to this random pairing as a noise rule. » (Page 239)\[3\].

**Vision Macro :**L'enjeu est de prouver que vos signaux d'achat et de vente ne sont pas juste du "bruit" qui a eu de la chance. David Aronson explique que sur un historique donné, il est possible qu'une suite de signaux aléatoires corresponde parfaitement aux mouvements du marché par pur accident\[3\],\[10\]. L'MCP agit comme un "mélangeur de cartes" : il garde vos décisions mais les applique à des jours de marché choisis au hasard. Si votre performance réelle n'est pas bien meilleure que ces milliers de tests "mélangés", alors votre stratégie n'a aucune valeur intellectuelle ; elle est statistiquement indiscernable d'un singe lançant des fléchettes\[11\],\[3\].

**Vision Micro : Le Processus pas à pas**

**Données d'entrée :** On utilise la séquence chronologique des signaux de la règle (+1, -1) et la série des rendements quotidiens **detrendés** du marché\[2\],\[12\].

**Permutation (Le mélange) :** On prend tous les rendements quotidiens du marché, on les met dans une "urne" virtuelle, et on les tire un par un **sans remise** pour les associer aux signaux de la règle dans leur ordre original\[5\],\[12\],\[13\].

**Calcul du profit "Bruit" :** Pour chaque jour, on multiplie le signal (+1/-1) par le rendement permuté. On calcule ensuite la moyenne de ces résultats pour obtenir le rendement d'une "règle de bruit"\[3\],\[13\].

**Simulation massive :** On répète ce mélange et ce calcul 5 000 fois pour construire la distribution d'échantillonnage de la chance\[8\],\[14\].

**Verdict (p-value) :** On regarde combien de fois (sur 5 000) le hasard a fait mieux que votre règle réelle. Si c'est moins de 5% du temps (p < 0,05), l'appariement entre vos signaux et le prix est jugé intentionnel et prédictif\[14\],\[15\].

**(AJOUT) Résumé Simplifié :**Imagine que tu prétendes connaître le résultat de 10 matchs de foot. Pour vérifier, on prend tes 10 pronostics et on les compare à 10 matchs tirés au hasard dans l'histoire. Si tu as toujours raison même sur des matchs aléatoires, c'est que tu as de la chance. Si tu n'as raison **que** sur les vrais matchs et que le hasard échoue lamentablement, alors tu as un vrai don de voyance\[11\],\[3\].

**Actions Concrètes :**

**Utilisez l'MCP pour valider la logique :** Si votre règle est complexe, l'MCP est le meilleur test pour vérifier que la complexité n'est pas juste un "ajustement au bruit"\[16\].

**Conservez les signaux :** Pour appliquer l'MCP, vous devez enregistrer la suite de vos positions (+1, 0, -1) et non pas seulement le résultat final\[12\],\[17\].

**Priorité au domaine public :** David Aronson note que l'MCP est dans le domaine public (développé par Dr. Timothy Masters), contrairement à certaines versions brevetées du Bootstrap\[1\],\[18\].

**(AJOUT) À retenir absolument :**

**MCP** = Test de la validité de la relation **Signal/Prix**\[3\].

Utilise le rééchantillonnage **sans remise**\[5\],\[13\].

Crée une **"Noise Rule"** (Règle de bruit) comme étalon\[3\].

Nécessite impérativement des données **detrendées** pour être juste\[19\],\[12\].

Fournit une **p-value** presque identique au Bootstrap si les données sont bien centrées\[20\].

J'ai terminé l'analyse de la méthode de permutation de Monte Carlo selon le protocole EBTA.
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
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[15] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[17] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[18] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[19] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[20] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
