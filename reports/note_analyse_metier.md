# Note d’analyse métier – NovaRetail

## 1) Contexte et objectifs

NovaRetail commercialise des solutions SaaS B2B et a activé plusieurs canaux d’acquisition en parallèle : **Emailing**, **Google Ads**, **LinkedIn Ads** et des actions **CRM**.
Le périmètre d’analyse est limité à **octobre 2025**.

Les objectifs de l’étude sont :
- mesurer la performance d’acquisition digitale (CTR, conversion, coût),
- relier ces résultats à la qualité commerciale des leads CRM,
- identifier des leviers d’optimisation par **canal**, **taille d’entreprise**, **secteur** et **région**.

## 2) Sélection des données et justification

### Données retenues
- `leads_novaretail` : `lead_id`, `date`, `channel`, `device`
- `campaign_novaretail` : `channel`, `cost`, `impressions`, `clicks`, `conversions`
- `crm_novaretail` : `lead_id`, `company_size`, `sector`, `region`, `status`

### Filtrage appliqué
- **Périmètre temporel** : `date` entre 2025-10-01 et 2025-10-31.

### Variables conservées
- **Performance marketing** : `cost`, `impressions`, `clicks`, `conversions` (nécessaires pour CTR, conversion, CPL).
- **Segmentation métier** : `company_size`, `sector`, `region`, `status` (nécessaires pour lecture business et activation commerciale).
- **Clés de jointure** : `lead_id` (CRM/leads), `channel` (campagnes/leads).

### Variables non prioritaires
- `campaign_id` non indispensable pour les KPI demandés (utile surtout pour audit de nomenclature).
- `device` non prioritaire dans le périmètre demandé, mais conservé en source pour analyses futures (mobile/desktop).

## 3) Résultats clés

### KPI par canal
- **Emailing** : CTR **3,00 %** ; taux de conversion **8,33 %** ; CPL **10,00 €**.
- **Google Ads** : CTR **2,67 %** ; taux de conversion **8,13 %** ; CPL **16,15 €**.
- **LinkedIn Ads** : CTR **2,20 %** ; taux de conversion **8,64 %** ; CPL **40,00 €**.

### Lecture des statuts CRM
- La distribution globale observée est équilibrée entre **MQL (4)**, **SQL (3)** et **Client (3)** sur l’échantillon.
- Les leads **Client** se concentrent davantage sur des segments à plus forte maturité (notamment Finance/SaaS dans les données disponibles).

### Segments entreprise / secteur / région
- **Tailles 50-100** : présence de plusieurs clients, suggérant une bonne adéquation produit-marché sur ce segment.
- **Île-de-France** : taux client élevé dans l’échantillon.
- Les secteurs **Finance** et **SaaS** montrent des signaux favorables de transformation.

## 4) Interprétation métier

1. **Arbitrage coût vs qualité**
   - Emailing est le plus efficient en coût.
   - LinkedIn Ads semble attirer des leads plus qualifiés (meilleur taux de conversion), mais à coût unitaire élevé.

2. **Canaux à rôle différencié**
   - Emailing : moteur de volume rentable.
   - LinkedIn Ads : canal de qualification premium.
   - Google Ads : canal hybride nécessitant optimisation fine.

3. **Segmentation commerciale utile**
   - Les entreprises 50-100 employés et certaines régions (IDF) offrent un potentiel de conversion plus élevé.

## 5) Recommandations opérationnelles

1. **Réallouer le budget par objectif**
   - Maintenir/incrémenter Emailing pour la génération de pipeline à coût maîtrisé.
   - Conserver LinkedIn Ads pour les cibles stratégiques à forte valeur (ABM, audiences lookalike B2B).

2. **Optimiser Google Ads**
   - Revoir mots-clés (intention forte), exclusions, et pages d’atterrissage.
   - Mettre en place des tests A/B sur annonces et formulaires.

3. **Activer la segmentation CRM**
   - Prioriser les séquences commerciales sur tailles 50-100 et secteurs performants.
   - Adapter les messages par région et maturité du lead (MQL vs SQL).

4. **Renforcer le pilotage**
   - Suivre chaque semaine : CTR, taux de conversion, CPL, coût/client, taux de passage MQL→SQL→Client.
   - Standardiser un tableau de bord unique Marketing + Sales Ops.
