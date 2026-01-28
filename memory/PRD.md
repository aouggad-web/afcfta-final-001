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
  - **5831 codes HS6** dans la base complète (hs6_database.py) avec métadonnées complètes
  - **62 catégories** de produits (vehicles, coffee, ores, textiles, leather, steel, ships, etc.)
  - **5429 codes avec sous-positions** détaillées
  - **54 pays africains** avec sous-positions nationales
- **BUG FIX P0 - Règles d'Origine (27/01/2025)** ✅ 
  - **CORRIGÉ**: Les règles d'origine étaient génériques ("35% valeur ajoutée africaine") pour tous les produits
  - **SOLUTION**: Base de données complète des Règles d'Origine officielles de la ZLECAf
    - Source: **AfCFTA Annex II, Appendix IV (COM-12, December 2023)**
    - **96 chapitres** couverts avec règles spécifiques
    - **87 chapitres convenus** (AGREED)
    - **65 règles par position tarifaire** (heading-specific)
    - **48 positions en négociation** (YTB)
  - **Types de règles implémentées**:
    - WO (Wholly Obtained) - Entièrement Obtenu
    - CTH (Change of Tariff Heading) - Changement de Position Tarifaire
    - CTSH (Change of Tariff Subheading) - Changement de Sous-Position
    - VA40/VA50/VA60 (Value Added) - Max X% valeur non-originaire
    - YARN (Manufacture from yarn) - Fabrication à partir de fils
    - YTB (Yet to be agreed) - En cours de négociation
  - **Nouveau fichier**: `/app/backend/etl/afcfta_rules_of_origin.py` (750+ lignes)
  - **Tests passés**: 34/34 (100% backend)
  - **API endpoints**:
    - `GET /api/rules-of-origin/stats` - Statistiques de couverture
    - `GET /api/rules-of-origin/{hs_code}` - Règle spécifique par produit
- **FEATURE: Warning Taux Variables par Sous-Position (27/01/2025)** ✅ 
  - **IMPLÉMENTÉ**: Détection et affichage des taux de DD variables selon les sous-positions nationales
  - **Méthodologie**: 
    - Analyse des sous-positions (8-12 chiffres) pour chaque code SH6
    - Si toutes les sous-positions ont le même taux → pas de warning
    - Si des taux différents existent → affichage d'un warning avec min/max
  - **Exemples testés**:
    - Riz (100630) vers Nigeria: 50% → 70% (5 sous-positions)
    - Voitures (870323) vers Nigeria: 35% → 70% (6 sous-positions selon âge)
    - Médicaments (300490): Pas de warning (0% uniforme)
  - **Réponse API enrichie**:
    - `rate_warning`: Message d'avertissement bilingue + taux min/max/utilisé
    - `sub_positions_details`: Liste complète des sous-positions avec leurs taux
    - `has_varying_sub_positions`: Booléen indiquant si variation
  - **Tests passés**: 15/15 (100% backend)
  - **Fichiers modifiés**: `/app/backend/models.py`, `/app/backend/server.py`
  - **Frontend**: Nouveau composant de warning avec visualisation min/max/utilisé
- **BUG FIX (27/01/2025)** : Navigateur HS affiche maintenant 5831 codes (corrigé depuis 731)

### Code Architecture - REFACTORING COMPLET (27/01/2025)
**Backend refactorisé** - server.py réduit de 3473 à 2435 lignes (**-30%**)

Structure modulaire créée dans `/app/backend/routes/` (1718 lignes totales):
| Module | Description | Lignes |
|--------|-------------|--------|
| `health.py` | Health check endpoints | 46 |
| `news.py` | African economic news | 94 |
| `oec.py` | OEC Trade Statistics | 96 |
| `hs_codes.py` | HS Code browser - 5831 codes | 184 |
| `production.py` | FAOSTAT, UNIDO, USGS, World Bank | 133 |
| `logistics.py` | Ports, airports, land corridors | 347 |
| `countries.py` | **NEW** Country profiles (54 pays) | 204 |
| `tariffs.py` | **NEW** Tariff calculations, RoO | 431 |
| `statistics.py` | **NEW** Trade statistics, UNCTAD | 143 |

Modules partagés créés (378 lignes):
- `constants.py` - AFRICAN_COUNTRIES, ZLECAF_RULES_OF_ORIGIN
- `models.py` - Pydantic models (CountryInfo, TariffCalculationResponse, etc.)
- `translations.py` - Country/region/rules translations FR/EN
- `gold_reserves_data.py` - Gold reserves and GAI 2025 data

**Frontend i18n migration (27/01/2025)**:
- `ProductionTab.jsx` migré vers `react-i18next`
- Traductions enrichies dans `/app/frontend/src/i18n/locales/fr.json` et `en.json`

**Frontend sous-composants** créés dans `/app/frontend/src/components/stats/oec/`:
- `utils.js` - Constants, formatters, translations
- `OECResultsDisplay.jsx` - Chart and table display components
- `index.js` - Module exports
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
- **NEW - Statistiques Commerciales OEC (27/01/2025)** ✅
  - **Intégration API OEC** (Observatory of Economic Complexity)
  - **3 modes de recherche** :
    - Par Pays : Exportations/Importations d'un pays africain
    - Par Produit : Statistiques par code SH6 (Café, Cacao, Pétrole, Or, Coton, Diamants)
    - Commerce Bilatéral : Flux entre deux pays africains
  - **Format SH2022** : Utilisation du cube HS Rev. 2017 (compatible SH2022)
  - **Codes HS6** exclusivement pour cohérence avec la base de données
  - **Données 2018-2023** disponibles
  - **Graphiques interactifs** (Pie chart, Bar chart via Recharts)
  - **Tableau classé** des exportateurs/importateurs
  - **API Endpoints** :
    - `GET /api/oec/countries` - Liste 54 pays africains
    - `GET /api/oec/years` - Années disponibles (2018-2023)
    - `GET /api/oec/exports/{country_iso3}` - Exportations par pays
    - `GET /api/oec/imports/{country_iso3}` - Importations par pays
    - `GET /api/oec/product/{hs_code}` - Statistiques par produit HS6
    - `GET /api/oec/bilateral/{exporter}/{importer}` - Commerce bilatéral
  - **Fichiers** :
    - `/app/backend/services/oec_trade_service.py` - Service OEC
    - `/app/frontend/src/components/stats/OECTradeStats.jsx` - Composant UI

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

### NEW - Intégration OEC Trade Statistics (27/01/2025) ✅
- **Bug corrigé** : Format d'identifiant HS pour l'API OEC
  - Implémentation de `_format_oec_hs6_id()` avec mapping des préfixes par section HS
  - L'API OEC utilise des préfixes 1-21 selon la section du Système Harmonisé
- **Migration vers SH2022** :
  - Utilisation du cube `trade_i_baci_a_17` (HS Rev. 2017, compatible SH2022)
  - Tous les codes en format HS6 exclusivement
  - Années disponibles : 2018-2023
- **Volumes ajoutés** : Affichage valeur + volume (tonnes) pour tous les résultats
- **Tri par valeur** : Résultats triés par valeur décroissante
- **Dénomination SH6** : Affichage automatique de la description du code HS

### NEW - Uniformisation Codes ISO3 (27/01/2025) ✅
- **Standard adopté** : ISO 3166-1 alpha-3 (codes à 3 lettres)
- **Fichiers centralisés créés** :
  - `/app/backend/country_codes.py` - Mapping complet 54 pays africains
  - `/app/frontend/src/utils/countryCodes.js` - Utilitaires frontend
- **Fonctionnalités** :
  - Conversion automatique ISO2 ↔ ISO3
  - Mapping par nom (FR/EN)
  - Drapeaux emoji par pays
  - Régions économiques (UEMOA, CEMAC, CEDEAO, EAC, SACU, SADC)
- **Fichiers mis à jour** :
  - `tax_rates.py` : Tous les taux en ISO3 (DZA, AGO, BEN...)
  - Compatibilité ISO2 maintenue via `_normalize_country_code()`
- **Composant Frontend** : `OECTradeStats.jsx`
  - Design moderne avec 3 onglets (Par Pays, Par Produit, Commerce Bilatéral)
  - Graphiques interactifs (Recharts)
  - Produits populaires : Café, Cacao, Coton, Or, Pétrole, Diamants
- **Tests validés** :
  - Cacao (180100) : $6.16B - Côte d'Ivoire leader
  - Pétrole (270900) : $179.93B - Angola leader
  - Tous les produits fonctionnels
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
- **Bug P0 - Règles d'Origine Spécifiques (27/01/2025)** - COMPLETE ✅
  - **Problème**: Règle générique "35% valeur ajoutée africaine" affichée pour tous les produits
  - **Solution**: Implémentation complète des PSR (Product-Specific Rules) de la ZLECAf
  - **Base de données**: 96 chapitres, 65 règles par position, source Annexe II Appendice IV
  - **Tests validés** (exemples):
    - Blé (100110) → WO (Entièrement Obtenu) ✅
    - Café (090111) → WO (Entièrement Obtenu) ✅
    - Machines (850440) → CTH/VA60 ✅
    - Vêtements (620311) → YARN (Fabrication à partir de fils) ✅
    - Véhicules (870310) → YTB (En cours de négociation) ✅
  - **Fichiers créés/modifiés**:
    - `/app/backend/etl/afcfta_rules_of_origin.py` - Base complète des règles
    - `/app/backend/server.py` - Endpoint /api/rules-of-origin/stats ajouté
    - `/app/backend/tests/test_rules_of_origin.py` - Tests automatisés
  - **Rapport de tests**: `/app/test_reports/iteration_7.json`

- **Feature - Warning Taux Variables par Sous-Position (27/01/2025)** - COMPLETE ✅
  - **Besoin**: Vérifier les taux DD, TVA, taxes réels par pays selon sous-positions nationales
  - **Méthodologie implémentée**:
    1. Analyse des sous-positions (8-12 chiffres) de chaque code SH6
    2. Si taux identiques → utilise le taux commun
    3. Si taux différents → affiche warning avec min/max et liste des possibilités
  - **Exemples validés**:
    - Riz (100630) → Nigeria: Warning ⚠️ 50%-70% (5 sous-positions)
    - Voitures (870323) → Nigeria: Warning ⚠️ 35%-70% (6 sous-positions: neuf vs occasion)
    - Médicaments (300490): Pas de warning (0% uniforme)
  - **Réponse API enrichie**: `rate_warning`, `sub_positions_details`
  - **Tests passés**: 15/15 (100%)
  - **Rapport de tests**: `/app/test_reports/iteration_8.json`
  - **UI/UX amélioré (27/01/2025)**:
    - Nouveau fichier CSS: `/app/frontend/src/components/calculator/calculator.css`
    - Animations fluides (fade-in, transitions CSS)
    - Warning box avec design moderne (icône AlertTriangle, cartes min/max/utilisé)
    - Liste des sous-positions cliquables avec code couleur
    - Suppression des duplications dans l'affichage
    - Espacement cohérent pour éviter les superpositions

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

### En Cours 🔄
- **Refactoring Backend `server.py` (27/01/2025)** - IN PROGRESS (~60%)
  - **Objectif**: Décomposer le fichier monolithique en modules de routes
  - **Progrès**:
    - AVANT: 2561 lignes dans `server.py`
    - APRÈS: 2136 lignes (-425 lignes, -17%)
  - **Routes migrées vers `/app/backend/routes/`**:
    - `health.py` - Health checks ✅
    - `news.py` - Economic news ✅
    - `oec.py` - OEC Trade Statistics ✅
    - `hs_codes.py` - HS Code browser ✅
    - `production.py` - Production data (FAOSTAT, UNIDO) ✅
    - `logistics.py` - Logistics (ports, corridors, airports) ✅
    - `countries.py` - Country profiles ✅
    - `tariffs.py` - Tariff lookups ✅
    - `statistics.py` - Basic trade statistics ✅
    - `etl.py` - ETL administration (NOUVEAU) ✅
  - **Routes restantes dans `server.py`** (53 endpoints):
    - `/statistics` (11) - Routes MongoDB complexes
    - `/calculate-tariff` (1) - Calculateur principal avec DB
    - `/hs6-tariffs/*` (5) - Tarifs SH6 détaillés
    - `/hs6/*` (8) - Sous-positions nationales
    - `/trade-performance/*` (2)
    - `/country-tariffs/*` (2)
    - `/production/*` (12) - Certaines routes spécifiques FAOSTAT
  - **Prochaines étapes**:
    - Migrer les routes `/production/*` FAOSTAT restantes
    - Extraire les routes `/statistics` MongoDB dans un module dédié
    - Objectif final: `server.py` < 500 lignes (config + init seulement)
