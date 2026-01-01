#!/usr/bin/env python3
"""
Tests spécifiques pour l'intégration des données ZLECAf 2024
Validation des nouveaux endpoints et données enrichies selon la demande de révision
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, List

# Configuration de l'API
BASE_URL = "https://african-trade-stats.preview.emergentagent.com/api"
TIMEOUT = 30

class ZLECAf2024DataTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'ZLECAf-2024-Data-Tester/1.0'
        })
        self.results = []
        
    def log_result(self, test_name: str, success: bool, message: str, details: Dict = None):
        """Enregistrer le résultat d'un test"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        self.results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}: {message}")
        if details and not success:
            print(f"   Détails: {details}")
    
    def test_trade_performance_2024(self):
        """Test GET /api/trade-performance - Données 2024 pour 54 pays"""
        try:
            response = self.session.get(f"{self.base_url}/trade-performance", timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                
                # Vérifier la structure de base
                if 'countries' not in data:
                    self.log_result(
                        "Trade Performance 2024", 
                        False, 
                        "Champ 'countries' manquant dans la réponse",
                        {'response_keys': list(data.keys())}
                    )
                    return
                
                countries = data['countries']
                
                # Vérifier le nombre de pays (au moins 45 pays avec données complètes)
                if len(countries) < 45:
                    self.log_result(
                        "Trade Performance 2024", 
                        False, 
                        f"Nombre de pays trop faible: {len(countries)} (minimum 45 attendu)",
                        {'count': len(countries)}
                    )
                    return
                
                # Vérifier la structure des données pour chaque pays
                required_fields = ['country', 'code', 'gdp_2024', 'exports_2024', 'imports_2024', 'trade_balance_2024', 'hdi_2024']
                sample_country = countries[0]
                missing_fields = [field for field in required_fields if field not in sample_country]
                
                if missing_fields:
                    self.log_result(
                        "Trade Performance 2024", 
                        False, 
                        f"Champs manquants dans les données pays: {missing_fields}",
                        {'sample_country': sample_country}
                    )
                    return
                
                # Vérifier des pays spécifiques avec leurs données 2024
                country_by_code = {country['code']: country for country in countries}
                
                # Vérifier l'Afrique du Sud (ZAF) - doit avoir 108.2B exports selon la demande
                if 'ZAF' in country_by_code:
                    zaf = country_by_code['ZAF']
                    if zaf['exports_2024'] < 100:  # Au moins 100B pour être proche de 108.2B
                        self.log_result(
                            "Trade Performance 2024", 
                            False, 
                            f"Exports Afrique du Sud trop faibles: {zaf['exports_2024']}B (attendu ~108.2B)",
                            {'zaf_exports': zaf['exports_2024']}
                        )
                        return
                
                # Vérifier le Nigeria (NGA) - doit avoir 68.5B exports selon la demande
                if 'NGA' in country_by_code:
                    nga = country_by_code['NGA']
                    if nga['exports_2024'] < 60:  # Au moins 60B pour être proche de 68.5B
                        self.log_result(
                            "Trade Performance 2024", 
                            False, 
                            f"Exports Nigeria trop faibles: {nga['exports_2024']}B (attendu ~68.5B)",
                            {'nga_exports': nga['exports_2024']}
                        )
                        return
                
                # Vérifier l'Angola (AGO) - doit avoir 42.8B exports selon la demande
                if 'AGO' in country_by_code:
                    ago = country_by_code['AGO']
                    if ago['exports_2024'] < 40:  # Au moins 40B pour être proche de 42.8B
                        self.log_result(
                            "Trade Performance 2024", 
                            False, 
                            f"Exports Angola trop faibles: {ago['exports_2024']}B (attendu ~42.8B)",
                            {'ago_exports': ago['exports_2024']}
                        )
                        return
                
                # Vérifier que tous les pays ont des données complètes (pas de 0)
                incomplete_countries = []
                for country in countries:
                    if (country['gdp_2024'] == 0 or 
                        country['exports_2024'] == 0 or 
                        country['imports_2024'] == 0):
                        incomplete_countries.append(country['code'])
                
                if incomplete_countries:
                    self.log_result(
                        "Trade Performance 2024", 
                        False, 
                        f"Pays avec données incomplètes: {incomplete_countries}",
                        {'incomplete_countries': incomplete_countries}
                    )
                    return
                
                self.log_result(
                    "Trade Performance 2024", 
                    True, 
                    f"Données 2024 complètes pour {len(countries)} pays avec exports validés",
                    {
                        'total_countries': len(countries),
                        'zaf_exports': country_by_code.get('ZAF', {}).get('exports_2024', 0),
                        'nga_exports': country_by_code.get('NGA', {}).get('exports_2024', 0),
                        'ago_exports': country_by_code.get('AGO', {}).get('exports_2024', 0),
                        'data_year': data.get('year', 2024)
                    }
                )
                
            else:
                self.log_result(
                    "Trade Performance 2024", 
                    False, 
                    f"Code de statut incorrect: {response.status_code}",
                    {'status_code': response.status_code}
                )
                
        except Exception as e:
            self.log_result(
                "Trade Performance 2024", 
                False, 
                f"Erreur lors de la récupération des données: {str(e)}",
                {'error': str(e)}
            )
    
    def test_enhanced_statistics_2024(self):
        """Test GET /api/statistics - Statistiques enrichies 2024"""
        try:
            response = self.session.get(f"{self.base_url}/statistics", timeout=TIMEOUT)
            
            if response.status_code == 200:
                stats = response.json()
                
                # Vérifier les nouvelles sections 2024
                required_2024_sections = [
                    'trade_evolution', 
                    'top_exporters_2024', 
                    'top_importers_2024', 
                    'product_analysis', 
                    'regional_integration', 
                    'sector_performance', 
                    'zlecaf_impact_metrics'
                ]
                
                missing_sections = [section for section in required_2024_sections if section not in stats]
                
                if missing_sections:
                    self.log_result(
                        "Enhanced Statistics 2024", 
                        False, 
                        f"Sections 2024 manquantes: {missing_sections}",
                        {'missing_sections': missing_sections}
                    )
                    return
                
                # Vérifier trade_evolution avec données 2023 et 2024
                trade_evolution = stats['trade_evolution']
                required_evolution_fields = ['intra_african_trade_2023', 'intra_african_trade_2024', 'growth_rate_2023_2024']
                missing_evolution_fields = [field for field in required_evolution_fields if field not in trade_evolution]
                
                if missing_evolution_fields:
                    self.log_result(
                        "Enhanced Statistics 2024", 
                        False, 
                        f"Champs manquants dans trade_evolution: {missing_evolution_fields}",
                        {'trade_evolution': trade_evolution}
                    )
                    return
                
                # Vérifier que les valeurs 2024 sont supérieures à 2023
                if trade_evolution['intra_african_trade_2024'] <= trade_evolution['intra_african_trade_2023']:
                    self.log_result(
                        "Enhanced Statistics 2024", 
                        False, 
                        "Commerce intra-africain 2024 doit être supérieur à 2023",
                        {
                            'trade_2023': trade_evolution['intra_african_trade_2023'],
                            'trade_2024': trade_evolution['intra_african_trade_2024']
                        }
                    )
                    return
                
                # Vérifier top_exporters_2024 avec Afrique du Sud, Nigeria, Angola
                top_exporters = stats['top_exporters_2024']
                if not isinstance(top_exporters, list) or len(top_exporters) < 3:
                    self.log_result(
                        "Enhanced Statistics 2024", 
                        False, 
                        "top_exporters_2024 doit contenir au moins 3 pays",
                        {'top_exporters': top_exporters}
                    )
                    return
                
                # Vérifier que l'Afrique du Sud est dans le top avec ~108.2B
                exporters_by_code = {exp.get('country', ''): exp for exp in top_exporters if isinstance(exp, dict)}
                
                expected_top_exporters = ['ZAF', 'NGA', 'AGO']  # Codes ISO3
                found_exporters = [code for code in expected_top_exporters if code in exporters_by_code]
                
                if len(found_exporters) < 2:  # Au moins 2 des 3 attendus
                    self.log_result(
                        "Enhanced Statistics 2024", 
                        False, 
                        f"Pas assez de top exporteurs attendus trouvés: {found_exporters}",
                        {'available_exporters': list(exporters_by_code.keys())}
                    )
                    return
                
                # Vérifier projections_updated
                if 'projections' not in stats:
                    self.log_result(
                        "Enhanced Statistics 2024", 
                        False, 
                        "Section projections manquante",
                        {'available_sections': list(stats.keys())}
                    )
                    return
                
                projections = stats['projections']
                if '2025' not in projections or '2030' not in projections:
                    self.log_result(
                        "Enhanced Statistics 2024", 
                        False, 
                        "Projections 2025 et 2030 manquantes",
                        {'projections_keys': list(projections.keys())}
                    )
                    return
                
                self.log_result(
                    "Enhanced Statistics 2024", 
                    True, 
                    f"Statistiques enrichies 2024 complètes avec évolution commerciale {trade_evolution['growth_rate_2023_2024']}%",
                    {
                        'trade_2023': trade_evolution['intra_african_trade_2023'],
                        'trade_2024': trade_evolution['intra_african_trade_2024'],
                        'growth_rate': trade_evolution['growth_rate_2023_2024'],
                        'top_exporters_count': len(top_exporters),
                        'projections_available': ['2025', '2030'] if '2025' in projections and '2030' in projections else []
                    }
                )
                
            else:
                self.log_result(
                    "Enhanced Statistics 2024", 
                    False, 
                    f"Code de statut incorrect: {response.status_code}",
                    {'status_code': response.status_code}
                )
                
        except Exception as e:
            self.log_result(
                "Enhanced Statistics 2024", 
                False, 
                f"Erreur lors de la récupération des statistiques: {str(e)}",
                {'error': str(e)}
            )
    
    def test_country_profile_enriched_zaf(self):
        """Test GET /api/country-profile/ZA - Profil enrichi Afrique du Sud"""
        try:
            response = self.session.get(f"{self.base_url}/country-profile/ZA", timeout=TIMEOUT)
            
            if response.status_code == 200:
                profile = response.json()
                
                # Vérifier les nouveaux champs enrichis 2024
                required_enriched_fields = ['projections']
                missing_fields = [field for field in required_enriched_fields if field not in profile]
                
                if missing_fields:
                    self.log_result(
                        "Country Profile ZAF Enriched", 
                        False, 
                        f"Champs enrichis manquants: {missing_fields}",
                        {'profile_keys': list(profile.keys())}
                    )
                    return
                
                projections = profile['projections']
                
                # Vérifier les nouveaux champs de commerce 2024
                required_commerce_fields = [
                    'main_exports', 'main_imports', 'export_partners', 'import_partners',
                    'exports_2024_billion_usd', 'imports_2024_billion_usd', 'trade_balance_2024_billion_usd'
                ]
                
                missing_commerce_fields = [field for field in required_commerce_fields if field not in projections]
                
                if missing_commerce_fields:
                    self.log_result(
                        "Country Profile ZAF Enriched", 
                        False, 
                        f"Champs commerce 2024 manquants: {missing_commerce_fields}",
                        {'projections_keys': list(projections.keys())}
                    )
                    return
                
                # Vérifier les données de notation (ratings)
                if 'risk_ratings' not in profile:
                    self.log_result(
                        "Country Profile ZAF Enriched", 
                        False, 
                        "Notations de risque manquantes",
                        {'profile_keys': list(profile.keys())}
                    )
                    return
                
                ratings = profile['risk_ratings']
                required_ratings = ['sp', 'moodys', 'fitch', 'scope']
                missing_ratings = [rating for rating in required_ratings if rating not in ratings]
                
                if missing_ratings:
                    self.log_result(
                        "Country Profile ZAF Enriched", 
                        False, 
                        f"Notations manquantes: {missing_ratings}",
                        {'available_ratings': list(ratings.keys())}
                    )
                    return
                
                # Vérifier que les exports 2024 sont cohérents (>100B pour ZAF)
                exports_2024 = projections.get('exports_2024_billion_usd', 0)
                if exports_2024 < 100:
                    self.log_result(
                        "Country Profile ZAF Enriched", 
                        False, 
                        f"Exports 2024 ZAF trop faibles: {exports_2024}B (attendu >100B)",
                        {'exports_2024': exports_2024}
                    )
                    return
                
                # Vérifier que les produits d'export/import sont des listes non vides
                main_exports = projections.get('main_exports', [])
                main_imports = projections.get('main_imports', [])
                
                if not isinstance(main_exports, list) or len(main_exports) == 0:
                    self.log_result(
                        "Country Profile ZAF Enriched", 
                        False, 
                        "Produits d'exportation manquants ou format incorrect",
                        {'main_exports': main_exports}
                    )
                    return
                
                if not isinstance(main_imports, list) or len(main_imports) == 0:
                    self.log_result(
                        "Country Profile ZAF Enriched", 
                        False, 
                        "Produits d'importation manquants ou format incorrect",
                        {'main_imports': main_imports}
                    )
                    return
                
                self.log_result(
                    "Country Profile ZAF Enriched", 
                    True, 
                    f"Profil ZAF enrichi validé - Exports: {exports_2024}B USD, {len(main_exports)} produits export, Notation S&P: {ratings.get('sp', 'NR')}",
                    {
                        'country': profile.get('country_name', 'ZAF'),
                        'exports_2024': exports_2024,
                        'imports_2024': projections.get('imports_2024_billion_usd', 0),
                        'trade_balance_2024': projections.get('trade_balance_2024_billion_usd', 0),
                        'main_exports_count': len(main_exports),
                        'main_imports_count': len(main_imports),
                        'sp_rating': ratings.get('sp', 'NR')
                    }
                )
                
            else:
                self.log_result(
                    "Country Profile ZAF Enriched", 
                    False, 
                    f"Code de statut incorrect: {response.status_code}",
                    {'status_code': response.status_code}
                )
                
        except Exception as e:
            self.log_result(
                "Country Profile ZAF Enriched", 
                False, 
                f"Erreur lors de la récupération du profil ZAF: {str(e)}",
                {'error': str(e)}
            )
    
    def test_country_profile_enriched_dza(self):
        """Test GET /api/country-profile/DZ - Profil enrichi Algérie"""
        try:
            response = self.session.get(f"{self.base_url}/country-profile/DZ", timeout=TIMEOUT)
            
            if response.status_code == 200:
                profile = response.json()
                
                # Vérifier la structure enrichie similaire à ZAF
                if 'projections' not in profile:
                    self.log_result(
                        "Country Profile DZA Enriched", 
                        False, 
                        "Section projections manquante",
                        {'profile_keys': list(profile.keys())}
                    )
                    return
                
                projections = profile['projections']
                
                # Vérifier les champs de commerce 2024
                required_commerce_fields = [
                    'main_exports', 'main_imports', 'export_partners', 'import_partners',
                    'exports_2024_billion_usd', 'imports_2024_billion_usd', 'trade_balance_2024_billion_usd'
                ]
                
                missing_commerce_fields = [field for field in required_commerce_fields if field not in projections]
                
                if missing_commerce_fields:
                    self.log_result(
                        "Country Profile DZA Enriched", 
                        False, 
                        f"Champs commerce 2024 manquants: {missing_commerce_fields}",
                        {'projections_keys': list(projections.keys())}
                    )
                    return
                
                # Vérifier les notations
                if 'risk_ratings' not in profile:
                    self.log_result(
                        "Country Profile DZA Enriched", 
                        False, 
                        "Notations de risque manquantes",
                        {'profile_keys': list(profile.keys())}
                    )
                    return
                
                # Vérifier que les données sont cohérentes pour l'Algérie
                exports_2024 = projections.get('exports_2024_billion_usd', 0)
                main_exports = projections.get('main_exports', [])
                main_imports = projections.get('main_imports', [])
                
                if exports_2024 < 30:  # L'Algérie devrait avoir des exports significatifs
                    self.log_result(
                        "Country Profile DZA Enriched", 
                        False, 
                        f"Exports 2024 DZA trop faibles: {exports_2024}B",
                        {'exports_2024': exports_2024}
                    )
                    return
                
                if not isinstance(main_exports, list) or len(main_exports) == 0:
                    self.log_result(
                        "Country Profile DZA Enriched", 
                        False, 
                        "Produits d'exportation DZA manquants",
                        {'main_exports': main_exports}
                    )
                    return
                
                self.log_result(
                    "Country Profile DZA Enriched", 
                    True, 
                    f"Profil DZA enrichi validé - Exports: {exports_2024}B USD, {len(main_exports)} produits export",
                    {
                        'country': profile.get('country_name', 'DZA'),
                        'exports_2024': exports_2024,
                        'imports_2024': projections.get('imports_2024_billion_usd', 0),
                        'main_exports_count': len(main_exports),
                        'main_imports_count': len(main_imports),
                        'sp_rating': profile.get('risk_ratings', {}).get('sp', 'NR')
                    }
                )
                
            else:
                self.log_result(
                    "Country Profile DZA Enriched", 
                    False, 
                    f"Code de statut incorrect: {response.status_code}",
                    {'status_code': response.status_code}
                )
                
        except Exception as e:
            self.log_result(
                "Country Profile DZA Enriched", 
                False, 
                f"Erreur lors de la récupération du profil DZA: {str(e)}",
                {'error': str(e)}
            )
    
    def test_updated_tariff_calculation_2024(self):
        """Test POST /api/calculate-tariff - Tarifs corrigés 2024"""
        # Test avec les paramètres spécifiques de la demande de révision
        test_payload = {
            "origin_country": "ZA",  # Afrique du Sud
            "destination_country": "NG",  # Nigeria
            "hs_code": "010121",
            "value": 100000
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/calculate-tariff", 
                json=test_payload, 
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                calculation = response.json()
                
                # Vérifier que les taux utilisent les corrections 2024
                normal_rate = calculation.get('normal_tariff_rate', 0)
                zlecaf_rate = calculation.get('zlecaf_tariff_rate', 0)
                
                # Le taux normal doit être > 0, ZLECAf peut être 0 (tarif préférentiel)
                if normal_rate == 0:
                    self.log_result(
                        "Updated Tariff Calculation 2024", 
                        False, 
                        f"Taux normal invalide: {normal_rate} (doit être > 0)",
                        {'normal_rate': normal_rate, 'zlecaf_rate': zlecaf_rate}
                    )
                    return
                
                # Le taux ZLECAf doit être inférieur ou égal au taux normal
                if zlecaf_rate > normal_rate:
                    self.log_result(
                        "Updated Tariff Calculation 2024", 
                        False, 
                        f"Taux ZLECAf doit être <= taux normal - Normal: {normal_rate}, ZLECAf: {zlecaf_rate}",
                        {'normal_rate': normal_rate, 'zlecaf_rate': zlecaf_rate}
                    )
                    return
                
                # Vérifier les économies
                savings = calculation.get('savings', 0)
                savings_percentage = calculation.get('savings_percentage', 0)
                
                if savings <= 0 or savings_percentage <= 0:
                    self.log_result(
                        "Updated Tariff Calculation 2024", 
                        False, 
                        f"Économies invalides - Montant: {savings}, Pourcentage: {savings_percentage}%",
                        {'savings': savings, 'savings_percentage': savings_percentage}
                    )
                    return
                
                # Vérifier que le calcul utilise les données 2024 (présence de champs enrichis)
                required_2024_fields = [
                    'normal_calculation_journal', 'zlecaf_calculation_journal',
                    'computation_order_ref', 'confidence_level'
                ]
                
                missing_2024_fields = [field for field in required_2024_fields if field not in calculation]
                
                if missing_2024_fields:
                    self.log_result(
                        "Updated Tariff Calculation 2024", 
                        False, 
                        f"Champs 2024 manquants: {missing_2024_fields}",
                        {'missing_fields': missing_2024_fields}
                    )
                    return
                
                # Vérifier la traçabilité
                if not calculation.get('computation_order_ref') or not calculation.get('confidence_level'):
                    self.log_result(
                        "Updated Tariff Calculation 2024", 
                        False, 
                        "Traçabilité 2024 manquante (computation_order_ref ou confidence_level)",
                        {
                            'computation_order_ref': calculation.get('computation_order_ref'),
                            'confidence_level': calculation.get('confidence_level')
                        }
                    )
                    return
                
                self.log_result(
                    "Updated Tariff Calculation 2024", 
                    True, 
                    f"Calcul tarifaire 2024 validé - ZA→NG: Normal {normal_rate*100:.1f}%, ZLECAf {zlecaf_rate*100:.1f}%, Économies {savings:.0f} USD ({savings_percentage:.1f}%)",
                    {
                        'origin': test_payload['origin_country'],
                        'destination': test_payload['destination_country'],
                        'hs_code': test_payload['hs_code'],
                        'normal_rate_pct': normal_rate * 100,
                        'zlecaf_rate_pct': zlecaf_rate * 100,
                        'savings_usd': savings,
                        'savings_pct': savings_percentage,
                        'confidence_level': calculation.get('confidence_level'),
                        'has_2024_traceability': bool(calculation.get('computation_order_ref'))
                    }
                )
                
            else:
                self.log_result(
                    "Updated Tariff Calculation 2024", 
                    False, 
                    f"Code de statut incorrect: {response.status_code}",
                    {'status_code': response.status_code, 'response': response.text}
                )
                
        except Exception as e:
            self.log_result(
                "Updated Tariff Calculation 2024", 
                False, 
                f"Erreur lors du calcul tarifaire 2024: {str(e)}",
                {'error': str(e), 'payload': test_payload}
            )
    
    def run_all_2024_tests(self):
        """Exécuter tous les tests spécifiques aux données 2024"""
        print(f"🚀 Tests d'intégration des données ZLECAf 2024")
        print(f"📍 Base URL: {self.base_url}")
        print(f"⏰ Timeout: {TIMEOUT}s")
        print("=" * 80)
        
        # Exécuter les tests spécifiques 2024
        self.test_trade_performance_2024()
        self.test_enhanced_statistics_2024()
        self.test_country_profile_enriched_zaf()
        self.test_country_profile_enriched_dza()
        self.test_updated_tariff_calculation_2024()
        
        # Résumé des résultats
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ DES TESTS 2024")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total des tests: {total_tests}")
        print(f"✅ Réussis: {passed_tests}")
        print(f"❌ Échoués: {failed_tests}")
        print(f"📈 Taux de réussite: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n🔍 TESTS ÉCHOUÉS:")
            for result in self.results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['message']}")
        
        print("\n" + "=" * 80)
        return passed_tests == total_tests

def main():
    """Fonction principale"""
    tester = ZLECAf2024DataTester()
    success = tester.run_all_2024_tests()
    
    # Sauvegarder les résultats détaillés
    with open('/app/test_results_2024_detailed.json', 'w', encoding='utf-8') as f:
        json.dump(tester.results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Résultats détaillés sauvegardés dans: /app/test_results_2024_detailed.json")
    
    if success:
        print("🎉 Tous les tests 2024 ont réussi!")
        sys.exit(0)
    else:
        print("⚠️  Certains tests 2024 ont échoué. Voir les détails ci-dessus.")
        sys.exit(1)

if __name__ == "__main__":
    main()