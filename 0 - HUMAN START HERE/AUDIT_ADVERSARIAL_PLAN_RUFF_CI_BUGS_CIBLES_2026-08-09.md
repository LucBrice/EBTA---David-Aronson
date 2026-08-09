# Audit adversarial — PLAN_RUFF_CI_BUGS_CIBLES

Date : 2026-08-09

## Verdict

PASS — le gate est cible, exact et les contournements principaux sont
detectes.

## Contrastes

1. Etat initial vivant : 25 findings et exit non nul.
2. Etat final : 0 finding et exit nul.
3. Retrait/affaiblissement de la commande Ruff : ratchet CI en erreur.
4. Pin Ruff flottant ou installation additionnelle : ensemble exact en erreur.
5. Ruleset different, `--select ALL` ou `--fix` : test config/commande en erreur.
6. Longueurs divergentes sur les `zip(strict=True)` : erreur visible au lieu
   d'une troncature silencieuse.

## Faux positif activement chasse

La suppression initiale du re-export `DEFAULT_DATA_ROOT` a fait echouer le
test Nautilus reel. La suite a donc empeche un faux succes Ruff. L'alias public
explicite conserve l'API sans suppression de lint.

## Limite honnete

Le gate couvre seulement `Implementation/ebta_engine` et les familles
`F,E9,B,PLE,RUF`. Les 17 findings hors moteur observes dans tout
`Implementation` restent hors scope, conformement au plan.
