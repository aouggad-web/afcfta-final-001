# PRD - Application ZLECAf (Accord de la Zone de Libre-Échange Continentale Africaine)

## Description du Projet
Application web d'analyse des statistiques commerciales et économiques africaines dans le cadre de la ZLECAf.

## Fonctionnalités Principales

### 1. Calculateur de Tarifs
- Calcul des droits de douane avec et sans ZLECAf
- Comparaison des économies potentielles

### 2. Statistiques (Onglet)
- Vue d'ensemble du commerce africain 2024
- Top 10 Exportateurs/Importateurs
- Évolution du commerce intra-africain 2023-2030
- **Top 5 PIB Africains** avec comparaison commerce (corrigé 31/12/2024)
- **Top 20 Produits Commerciaux** (ajouté 31/12/2024):
  - Import du Monde
  - Export vers le Monde  
  - Import Intra-Africain
  - Export Intra-Africain

### 3. Production (Onglet)
- **Agriculture (FAOSTAT)**: Données 54 pays (2020-2023)
- **Manufacturing (UNIDO)**: Statistiques industrielles

### 4. Logistique (Onglet)
- Temps de dédouanement TRS
- Statistiques portuaires

### 5. Outils
- Règles d'origine
- Profils pays détaillés

### 6. Internationalisation (i18n)
- Support complet français/anglais ✅
- Tous les composants traduisibles
- Données API traduites selon la langue

## Corrections et Améliorations (31/12/2024 - 08/01/2025)

### Correction PIB - Classement Afrique
Mise à jour selon FMI World Economic Outlook (Oct 2024):
- **Algérie**: 260.1 → 266.5 Mds USD (Rang 3)
- **Nigéria**: 268.5 → 253.0 Mds USD (Rang 4)

Classement correct:
1. Afrique du Sud - 377.78 Mds USD
2. Égypte - 348.0 Mds USD
3. Algérie - 266.5 Mds USD
4. Nigéria - 253.0 Mds USD
5. Éthiopie - 156.1 Mds USD

### Internationalisation Complete (08/01/2025)
- Ajout des traductions pour tous les textes UI (français/anglais)
- Création du fichier `/app/backend/etl/translations.py` pour les traductions backend
- APIs avec paramètre `?lang=en` pour les données traduites
- Noms de produits et pays traduits dynamiquement

## Architecture Technique

### Backend (FastAPI)
- `/app/backend/server.py` - API principale
- `/app/backend/etl/` - Données ETL (FAOSTAT, UNIDO, Trade Products)
- `/app/backend/etl/translations.py` - Traductions produits/pays
- `/app/backend/data_loader.py` - Chargement données CSV

### Frontend (React)
- `/app/frontend/src/components/` - Composants UI
- Shadcn/UI pour les composants
- Système de traduction via props `language`

### Données Sources
- `/app/ZLECAf_ENRICHI_2024_COMMERCE.csv` - Données principales 54 pays

## Backlog (P1-P2)

### P1 - À faire
- Intégrer d'autres sources officielles (UNCTAD)
- Améliorer la visualisation des données

### P2 - Futur
- Mécanisme upload données TRS officielles
- Export PDF des rapports

## Sources de Données
- FMI World Economic Outlook 2024
- Banque Mondiale
- FAOSTAT
- UNIDO INDSTAT4
- UNCTAD COMTRADE
- AfCFTA Secretariat
