# Carnet technique – NovaRetail (Exercice 1)

## 1) Problème : formats hétérogènes de données
- **Description** : les ressources proviennent de plusieurs formats (`.csv`, `.json`, `.xlsx` annoncé dans l’énoncé).
- **Solution apportée** : normalisation des sources en fichiers plats (`csv/json`) et traitement automatisé dans un script Python unique.
- **Justification technique** : les modules standards (`csv`, `json`) évitent toute dépendance externe et garantissent l’exécution dans un environnement restreint.

## 2) Problème : alignement du périmètre temporel
- **Description** : l’analyse doit porter uniquement sur octobre 2025.
- **Solution apportée** : conversion de la date et filtre borné `2025-10-01` à `2025-10-31`.
- **Justification technique** : sécurise la conformité méthodologique vis-à-vis des consignes d’examen.

## 3) Problème : jointure marketing / CRM
- **Description** : nécessité de relier la performance campagne aux caractéristiques business des leads.
- **Solution apportée** : jointure `lead_id` entre leads et CRM, puis rattachement des métriques campagne via `channel`.
- **Justification technique** : garantit la cohérence métier entre acquisition (canal) et qualité commerciale (statut).

## 4) Problème : calcul et homogénéité des KPI
- **Description** : risque d’incohérence sur les définitions de CTR, conversion, CPL et coûts dérivés.
- **Solution apportée** : implémentation centralisée dans le script `analysis/analyse_novaretail.py`.
- **Justification technique** : limite les écarts de version de calcul et facilite la vérification.

## 5) Problème : visualisations orientées décision
- **Description** : éviter les graphiques décoratifs et redondants.
- **Solution apportée** : sélection de 5 visualisations métier intégrées en syntaxe Mermaid dans le dashboard.
- **Justification technique** : format léger, lisible et exploitable sans installation graphique spécifique.

## 6) Problème : traçabilité des livrables
- **Description** : besoin de réutiliser facilement les résultats dans différents supports.
- **Solution apportée** : export automatique des tables d’analyse en CSV dans `outputs/` + dashboard/documentation en Markdown dans `reports/`.
- **Justification technique** : formats interopérables avec Excel/Power BI/Tableau et compatibles avec Git.
