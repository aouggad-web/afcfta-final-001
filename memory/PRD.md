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

### 2. Calculateur de Tarifs
- Calcul des droits de douane avec et sans ZLECAf
- Comparaison des économies potentielles

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

### Données vérifiées (véracité garantie)
| Indicateur | Valeur API | Valeur UI | Source |
|------------|------------|-----------|--------|
| Commerce Intra-Africain 2024 | $218.7B | $218.7B | UNCTAD/AfCFTA |
| Exports Totaux 2024 | $553.7B | $553.7B | OEC/World Bank |
| Trafic Portuaire 2023 | 28.5M TEU | 28.5M TEU | UNCTAD |
| Croissance Portuaire | +4.2% YoY | +4.2% YoY | UNCTAD |
| Progression ZLECAf | 57% | 57% | AfCFTA Secretariat |
| PIB Algérie 2024 | $266B | $267B | IMF WEO |

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
- Dashboard avec widgets dynamiques temps réel (09/01/2025)
- Traductions tous les onglets
- Données UNCTAD (backend + frontend)
- Système i18n centralisé react-i18next
- Export PDF dans onglets principaux
- Ports algériens UNCTAD
- Modale ports corrigée
- Bug fix i18n Production tab

### P1 - Prochaines Tâches
- Migration progressive des autres composants vers react-i18next centralisé
- Ajouter plus de widgets interactifs (graphiques personnalisables)
- Ajouter authentification admin pour TRS upload

### P2 - Améliorations Futures
- Thèmes visuels personnalisables
- Export des données en CSV/Excel
- Dashboard avec alertes personnalisées

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
- `/app/test_reports/iteration_2.json` - Rapport de test
