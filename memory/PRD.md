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
- **Indicateur de source** en bas de page

### 3. Production (Onglet)
- **Agriculture (FAOSTAT)**: Données 54 pays (2020-2023)
- **Manufacturing (UNIDO)**: Statistiques industrielles
- **Mining (USGS)**: Statistiques minières
- **Macro (World Bank/IMF)**: Valeur ajoutée

### 4. Logistique (Onglet)
- Maritime (Ports)
- Aérien (Fret)
- Terrestre (Corridors)
- Zones Franches
- **Interface upload TRS** pour données officielles
- **Sources UNCTAD** intégrées

### 5. Outils
- Obstacles Non Tarifaires (NTB)
- Protocole Commerce Digital
- Guided Trade Initiative
- PAPSS - Système Panafricain de Paiements
- Ressources additionnelles

### 6. Internationalisation (i18n) - Complète
- Support complet français/anglais ✅
- Tous les composants traduisibles ✅
- Données API traduites selon la langue ✅
- **Indicateurs de source** en petit caractère ✅
- **Ports et Aéroports** détails traduits ✅

## Corrections et Améliorations (31/12/2024 - 08/01/2025)

### Correction PIB - Classement Afrique
Mise à jour selon FMI World Economic Outlook (Oct 2024):
- **Algérie**: 260.1 → 266.5 Mds USD (Rang 3)
- **Nigéria**: 268.5 → 253.0 Mds USD (Rang 4)

### Internationalisation Complete (08/01/2025)
- Tous les onglets traduits : Statistics, Production, Logistics, Tools
- Fichier traductions backend : `/app/backend/etl/translations.py`
- APIs avec paramètre `?lang=en`
- Interface upload TRS dans Logistics

### Données UNCTAD (08/01/2025)
- Nouveau fichier : `/app/backend/etl/unctad_data.py`
- APIs UNCTAD : `/api/statistics/unctad/ports`, `/api/statistics/unctad/trade-flows`, `/api/statistics/unctad/lsci`
- Statistiques portuaires africaines
- Flux commerciaux
- Indice de connectivité maritime (LSCI)

## Architecture Technique

### Backend (FastAPI)
- `/app/backend/server.py` - API principale
- `/app/backend/etl/` - Données ETL
  - `faostat_data.py` - Agriculture
  - `unido_data.py` - Manufacturing
  - `trade_products_data.py` - Produits commerciaux
  - `translations.py` - Traductions
  - `unctad_data.py` - Données UNCTAD (NEW)
- `/app/backend/data_loader.py` - Chargement données CSV

### Frontend (React)
- `/app/frontend/src/components/` - Composants UI
- Shadcn/UI pour les composants
- Système de traduction via props `language`

### Données Sources
- `/app/ZLECAf_ENRICHI_2024_COMMERCE.csv` - Données principales 54 pays

## APIs Principales
- `GET /api/statistics` - Statistiques générales
- `GET /api/statistics/trade-products/imports-world?lang=en` - Import monde (traduit)
- `GET /api/statistics/unctad` - Données UNCTAD
- `GET /api/production/faostat/all` - Données agriculture
- `GET /api/production/unido/all` - Données industrie

## Backlog

### Complété ✅
- Traductions tous les onglets
- Données UNCTAD
- Interface upload TRS
- Indicateurs de source

### P2 - Futur
- Export PDF des rapports
- Graphiques interactifs améliorés
- Dashboard personnalisable

## Sources de Données
- FMI World Economic Outlook 2024
- Banque Mondiale WDI
- FAOSTAT
- UNIDO INDSTAT4
- **UNCTAD COMTRADE** (NEW)
- **UNCTAD Maritime Transport Review** (NEW)
- AfCFTA Secretariat
- African Development Bank
