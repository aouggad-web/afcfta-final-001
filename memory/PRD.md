# PRD - Application ZLECAf (Accord de la Zone de Libre-Échange Continentale Africaine)

## Description du Projet
Application web d'analyse des statistiques commerciales et économiques africaines dans le cadre de la ZLECAf.

## Fonctionnalités Principales

### 1. Dashboard Dynamique (NEW - 09/01/2025)
- **Widgets en temps réel** récupérant les données depuis les APIs backend
- 9 types de widgets disponibles :
  - Commerce en Direct (Live Trade Stats)
  - Ports en Direct (Live Ports - UNCTAD)
  - Indice LSCI (Liner Shipping Connectivity Index)
  - Profil Pays (Country Profile)
  - Progression ZLECAf (AfCFTA Progress)
  - Balance Commerciale (Trade Balance)
  - Commerce Régional (Regional Trade)
  - Alertes & Actualités (Alerts)
  - Calculateur Rapide (Quick Calculator)
- **Drag & Drop** pour réorganiser les widgets
- **Personnalisation** : ajouter/supprimer des widgets
- **Sauvegarde** de la configuration dans localStorage
- **Actualisation automatique** des données (toutes les 60 secondes)

### 2. Calculateur de Tarifs (ENHANCED - 27/01/2025)
- Calcul des droits de douane avec et sans ZLECAf
- Comparaison des économies potentielles
- **COMPLETE: Base HS6 enrichie + Sous-positions nationales**
  - **825 codes HS6** dans la base principale avec métadonnées complètes (extension terminée)
  - **62 catégories** de produits (vehicles, coffee, ores, textiles, leather, steel, ships, etc.)
  - **747 codes avec sous-positions** détaillées
  - **54 pays africains** avec 768 sous-positions nationales
  - **Règles d'origine ZLECAf** intégrées par code HS6
- **Recherche intelligente** avec suggestions automatiques:
  - `/api/hs6/search` - Recherche par mot-clé
  - `/api/hs6/suggestions/{code}` - Suggestions sous-positions
  - `/api/hs6/smart-search` - Recherche combinée + règles d'origine
- **Indicateur de précision tarifaire**:
  - `sub_position` : Sous-position nationale (haute précision)
  - `hs6_country` : Tarif SH6 spécifique au pays
  - `chapter` : Tarif par chapitre (précision moyenne)

### 3. Statistiques (Onglet)
- Vue d'ensemble du commerce africain 2024
- Top 10 Exportateurs/Importateurs
- Évolution du commerce intra-africain 2023-2030
- Top 5 PIB Africains avec comparaison commerce
- Top 20 Produits Commerciaux

### 4. Production (Onglet)
- **Agriculture (FAOSTAT)**: Données 54 pays (2020-2023)
- **Manufacturing (UNIDO)**: Statistiques industrielles
- **Mining (USGS)**: Statistiques minières
- **Macro (World Bank/IMF)**: Valeur ajoutée

### 5. Logistique (Onglet)
- Maritime (Ports)
- Aérien (Fret)
- Terrestre (Corridors)
- Zones Franches
- **Sources UNCTAD** intégrées
- **Ports algériens** ajoutés

### 6. Outils
- Obstacles Non Tarifaires (NTB)
- Protocole Commerce Digital
- Guided Trade Initiative
- PAPSS - Système Panafricain de Paiements

### 7. Internationalisation (i18n) - Complète
- Support complet français/anglais
- Système centralisé react-i18next
- Tous les composants traduisibles

### 8. Sélecteur de Codes HS6 (NEW - 14/01/2025)
- **Composant HSCodeSearch** : Recherche inline de codes HS6
- **Composant HSCodeBrowser** : Navigateur complet avec 3 onglets
  - **Recherche** : Recherche par mot-clé (insensible aux accents)
  - **Navigation** : Liste des 97 chapitres avec codes
  - **Hiérarchie** : Vue par sections HS (21 sections, I-XXI)
- **Base de données** : 731 codes HS6 couvrant 97 chapitres
- **Intégration** :
  - Onglet Calculateur de Tarifs
  - Onglet Règles d'Origine ZLECAf
- **API Endpoints** :
  - `GET /api/hs-codes/statistics` - Statistiques (chapitres, codes)
  - `GET /api/hs-codes/search?q={query}` - Recherche par mot-clé
  - `GET /api/hs-codes/chapters` - Liste des chapitres
  - `GET /api/hs-codes/chapter/{chapter}` - Codes d'un chapitre
  - `GET /api/hs-codes/code/{code}` - Détails d'un code
- **Règles d'origine** : Affichage automatique du contenu régional requis par produit
- **Fichiers** :
  - `/app/frontend/src/components/HSCodeSelector.jsx`
  - `/app/backend/etl/hs_codes_data.py`
  - `/app/backend/server.py` (endpoints lignes 1851-1970)

### Corrections et Améliorations Récentes

### Bug Fix - Recherche par pays Production/Macro (09/01/2025)
- **Problème** : Le dropdown de sélection de pays était masqué par les éléments parents (overflow caché)
- **Solution** : Utilisation de `createPortal` React pour rendre le dropdown directement dans `document.body`
- **Fichier modifié** : `/app/frontend/src/components/production/EnhancedCountrySelector.jsx`
- **Test réussi** : Sélection "Algérie" → Données chargées (12 enregistrements, 3 secteurs)

### Bug Fix - Lien Port de Lobito (09/01/2025)
- **Problème** : Le lien du site web du port de Lobito (Angola) ne fonctionnait pas
- **Solution** : Correction de `www.portolobito.co.ao` vers `https://portodolobito.co.ao`
- **Fichier modifié** : `/app/ports_africains.json`

### Migration i18n - StatisticsTab & LogisticsTab (09/01/2025)
- **Migration** : Composants `StatisticsTab.jsx` et `LogisticsTab.jsx` vers `useTranslation()` de react-i18next
- **Synchronisation** : `App.js` maintenant synchronise le changement de langue avec `i18n.changeLanguage()`
- **Traductions ajoutées** : Sections `statistics` et `logistics` complètes en français et anglais
- **Fichiers modifiés** :
  - `/app/frontend/src/App.js`
  - `/app/frontend/src/components/statistics/StatisticsTab.jsx`
  - `/app/frontend/src/components/logistics/LogisticsTab.jsx`
  - `/app/frontend/src/i18n/locales/fr.json`
  - `/app/frontend/src/i18n/locales/en.json`

### Widgets Dynamiques Dashboard (09/01/2025)
- **Implémentation complète** des widgets dynamiques avec données temps réel
- **Fichiers créés/modifiés** :
  - `/app/frontend/src/components/dashboard/DynamicWidgets.jsx` - 8 widgets dynamiques
  - `/app/frontend/src/components/dashboard/DashboardTab.jsx` - Intégration widgets
  - `/app/frontend/src/i18n/locales/fr.json` - Traductions FR
  - `/app/frontend/src/i18n/locales/en.json` - Traductions EN
- **APIs utilisées** :
  - `GET /api/statistics` - Statistiques commerciales
  - `GET /api/statistics/unctad/ports` - Données portuaires
  - `GET /api/statistics/unctad/lsci` - Indice de connectivité
  - `GET /api/country-profile/{code}` - Profils pays
- **Tests réussis** : 24/24 tests backend, 100% frontend

### Nouveau Dashboard avec Fil d'Actualités (Décembre 2025)
- **Remplacement du dashboard statique** par un fil d'actualités économiques africaines dynamique
- **Sources** : Agence Ecofin, AllAfrica (mise à jour quotidienne)
- **Organisation** : Par région africaine et par catégorie économique
- **Widgets statistiques** compacts en en-tête (PIB, Commerce, Ports, ZLECAf)
- **Fichiers créés** :
  - `/app/backend/etl/news_aggregator.py` - Agrégateur RSS
  - `/app/frontend/src/components/dashboard/NewsDashboard.jsx` - Composant actualités
  - `/app/frontend/src/components/dashboard/DashboardTabNew.jsx` - Nouveau dashboard

### Mise à jour complète des données 2024-2025 - 54 PAYS (Décembre 2025)
- **TOUS les 54 pays africains** mis à jour avec données officielles FMI WEO Octobre 2025
- **Données incluses** : PIB nominal, PIB/habitant, croissance 2024, projection 2025, rang africain
- **Sources** : FMI WEO Oct 2025, Banque Mondiale, UNCTAD
- **Affichage dans Statistiques** : Tableau "Top 10 PIB Africains 2024" avec projections 2025
- **Affichage dans Profils Pays** : Bloc "Projection 2025" pour chaque pays
- **Fichiers modifiés** :
  - `/app/backend/country_data.py` - 54 pays avec `data_source: "FMI WEO Oct 2025"`
  - `/app/backend/etl/unctad_data.py` - Données portuaires et LSCI 2024
  - `/app/backend/server.py` - Endpoint top_10_gdp_2024
  - `/app/frontend/src/components/StatisticsZaubaStyle.jsx` - Tableau Top 10 PIB
  - `/app/frontend/src/components/profiles/CountryProfilesTab.jsx` - Bloc Projection 2025

### Données vérifiées (véracité garantie - Mise à jour Décembre 2025)
| Indicateur | Valeur API | Source |
|------------|------------|--------|
| **TOP 10 PIB Africains 2024** | | |
| 1. Nigeria | $334.34B | IMF WEO 2025 |
| 2. Afrique du Sud | $443.64B | IMF WEO 2025 |
| 3. Égypte | $349.30B | IMF WEO 2025 |
| 4. Algérie | $263.62B | IMF WEO 2025 |
| 5. Maroc | $154.43B | IMF WEO 2025 |
| 6. Kenya | $113.00B | World Bank 2025 |
| 7. Éthiopie | $149.74B | World Bank 2025 |
| 8. Ghana | $82.80B | IMF WEO 2025 |
| 9. Côte d'Ivoire | $86.54B | IMF WEO 2025 |
| 10. Tanzanie | $83.00B | World Bank 2025 |
| **Ports UNCTAD 2024** | | |
| Tanger Med (Maroc) | 10,241,392 TEU | Tanger Med Authority 2025 |
| Trafic Portuaire Africain 2024 | 35.5M TEU | UNCTAD 2025 |
| Croissance Portuaire 2024 | +8.1% YoY | Lloyd's List 2025 |
| **LSCI 2024** | | |
| Maroc (Rang #1 Afrique) | 82.5 | UNCTAD LSCI 2024 |
| Égypte (Rang #2 Afrique) | 70.8 | UNCTAD LSCI 2024 |
| **Commerce Intra-Africain** | $235.5B | UNCTAD 2024 |

## Architecture Technique

### Backend (FastAPI)
- `/app/backend/server.py` - API principale
- `/app/backend/etl/unctad_data.py` - Données UNCTAD

### Frontend (React)
- `/app/frontend/src/components/dashboard/` - Dashboard et widgets
- `/app/frontend/src/i18n/` - Traductions centralisées
- Shadcn/UI pour les composants
- Recharts pour les graphiques

### APIs Principales
- `GET /api/statistics` - Statistiques générales (trade_evolution, top_exporters, top_importers)
- `GET /api/statistics/unctad/ports` - Ports UNCTAD (throughput, growth_rate, top_ports)
- `GET /api/statistics/unctad/lsci` - LSCI (lsci_2023, rank_africa, rank_global)
- `GET /api/country-profile/{code}` - Profils économiques pays

## Backlog

### Complété ✅
- **Extension complète base HS6 (27/01/2025)** - COMPLETE
  - **825 codes HS6** (de 93 à 825, +732 codes)
  - **62 catégories** de produits (de 36 à 62)
  - **747 codes avec sous-positions** détaillées
  - Chapitres couverts : 01-89 du Système Harmonisé
  - Fichiers d'extension créés :
    - `/app/backend/etl/hs6_extended_ch01_06.py` - Animaux, viandes, poissons
    - `/app/backend/etl/hs6_extended_ch07_15.py` - Fruits, légumes, huiles
    - `/app/backend/etl/hs6_extended_ch16_24.py` - Préparations alimentaires
    - `/app/backend/etl/hs6_extended_ch25_40.py` - Minéraux, chimiques, plastiques
    - `/app/backend/etl/hs6_extended_ch41_63.py` - Cuir, textiles, vêtements
    - `/app/backend/etl/hs6_extended_ch72_89.py` - Métaux, machines, véhicules, navires
  - Tests : 40/40 passés (100% backend)
  - Rapport : `/app/test_reports/iteration_5.json`
- **Base HS6 enrichie + Recherche intelligente (24/01/2025)** - COMPLETE
  - **93 codes HS6** dans la base principale avec métadonnées complètes
  - **36 catégories** de produits (vehicles, coffee, ores, textiles, etc.)
  - **54 pays africains** avec **768 sous-positions nationales**
  - **Règles d'origine ZLECAf** intégrées par code HS6
  - **Recherche intelligente** avec suggestions automatiques
  - Nouveau fichier: `/app/backend/etl/hs6_database.py`
  - Nouveau composant: `/app/frontend/src/components/SmartHSSearch.jsx`
  - API endpoints:
    - `/api/hs6/search` - Recherche par mot-clé
    - `/api/hs6/info/{code}` - Info complète HS6
    - `/api/hs6/suggestions/{code}` - Suggestions sous-positions
    - `/api/hs6/rule-of-origin/{code}` - Règle d'origine
    - `/api/hs6/smart-search` - Recherche combinée
    - `/api/hs6/categories` - Liste catégories
    - `/api/hs6/statistics` - Statistiques base
- Mise à jour complète données 2024-2025 (20/01/2025)
  - 10 économies majeures: PIB, croissance, projections 2025
  - Données portuaires UNCTAD (Tanger Med: 10.24M TEU)
  - Indice LSCI 2024 actualisé
- Dashboard avec widgets dynamiques temps réel (09/01/2025)
- Sélecteur codes HS6 intégré (14/01/2025)
- Refonte tarifs/TVA pour 54 pays africains
- Traductions tous les onglets
- Données UNCTAD (backend + frontend)
- Système i18n centralisé react-i18next
- Export PDF dans onglets principaux
- Ports algériens UNCTAD
- Modale ports corrigée
- Bug fix i18n Production tab

### P1 - Prochaines Tâches
- **Indicateur de fraîcheur des données** : Afficher "Données vérifiées le : Jan 2025" sur les tarifs
- Migration progressive des autres composants vers react-i18next centralisé (ProductionTab)
- Ajouter plus de widgets interactifs (graphiques personnalisables)
- Ajouter authentification admin pour TRS upload

### P2 - Améliorations Futures
- Thèmes visuels personnalisables
- Export des données en CSV/Excel
- Dashboard avec alertes personnalisées
- Vérification automatique des liens externes
- Comparaison de pays côte à côte
- Sauvegarder les recherches HS fréquentes

## Sources de Données
- FMI World Economic Outlook 2024
- Banque Mondiale WDI
- FAOSTAT
- UNIDO INDSTAT4
- UNCTAD COMTRADE
- UNCTAD Maritime Transport Review
- AfCFTA Secretariat
- African Development Bank
- Observatory of Economic Complexity (OEC)

## Tests
- `/app/tests/test_dashboard_apis.py` - Tests API dashboard
- `/app/tests/test_2024_data_update.py` - Tests mise à jour données 2024-2025
- `/app/test_reports/iteration_4.json` - Rapport de test (36/36 tests passés)
- `/app/test_reports/iteration_5.json` - Tests extension HS6 (40/40 tests passés)
- `/app/backend/tests/test_hs6_extended_api.py` - Tests API HS6 étendues
