#!/usr/bin/env python3
"""
Test spécifique pour les endpoints FAOSTAT et UNIDO
"""

import requests
import json
import sys
from datetime import datetime

# Configuration de l'API
BASE_URL = "https://tariff-analyzer.preview.emergentagent.com/api"
TIMEOUT = 30

def test_faostat_unido_endpoints():
    """Test des endpoints FAOSTAT et UNIDO"""
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'User-Agent': 'ZLECAf-API-Tester/1.0'
    })
    
    results = []
    
    def log_result(test_name, success, message, details=None):
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}: {message}")
        if details and not success:
            print(f"   Détails: {details}")
    
    print("🌾 Tests FAOSTAT Production Agricole")
    print("-" * 50)
    
    # Test FAOSTAT Statistics
    try:
        response = session.get(f"{BASE_URL}/production/faostat/statistics", timeout=TIMEOUT)
        if response.status_code == 200:
            stats = response.json()
            if stats.get('total_countries') == 54 and stats.get('total_commodities') == 47 and stats.get('data_year') == 2023:
                log_result("FAOSTAT Statistics", True, f"Statistiques validées - {stats['total_countries']} pays, {stats['total_commodities']} commodités, année {stats['data_year']}")
            else:
                log_result("FAOSTAT Statistics", False, f"Valeurs incorrectes", stats)
        else:
            log_result("FAOSTAT Statistics", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_result("FAOSTAT Statistics", False, f"Erreur: {str(e)}")
    
    # Test FAOSTAT CIV
    try:
        response = session.get(f"{BASE_URL}/production/faostat/CIV", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if data.get('country_name') == "Côte d'Ivoire" and data.get('region') == "Afrique de l'Ouest" and 'Cacao' in str(data.get('main_crops', '')):
                log_result("FAOSTAT CIV", True, f"Données CIV validées - {data['country_name']}, Cacao présent")
            else:
                log_result("FAOSTAT CIV", False, f"Données incorrectes", data)
        else:
            log_result("FAOSTAT CIV", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_result("FAOSTAT CIV", False, f"Erreur: {str(e)}")
    
    # Test FAOSTAT EGY
    try:
        response = session.get(f"{BASE_URL}/production/faostat/EGY", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            production_str = str(data.get('production_2023', ''))
            if data.get('country_name') == "Égypte" and 'Blé' in production_str and 'Riz' in production_str:
                log_result("FAOSTAT EGY", True, f"Données EGY validées - {data['country_name']}, Blé et Riz présents")
            else:
                log_result("FAOSTAT EGY", False, f"Données incorrectes", data)
        else:
            log_result("FAOSTAT EGY", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_result("FAOSTAT EGY", False, f"Erreur: {str(e)}")
    
    # Test FAOSTAT Top Producers Cacao
    try:
        response = session.get(f"{BASE_URL}/production/faostat/top-producers/Cacao", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            producers = data.get('producers', [])
            if len(producers) >= 2 and producers[0].get('country') == 'CIV' and producers[1].get('country') == 'GHA':
                log_result("FAOSTAT Top Producers Cacao", True, f"Classement validé - {len(producers)} producteurs, CIV #1, GHA #2")
            else:
                log_result("FAOSTAT Top Producers Cacao", False, f"Classement incorrect", {'producers': producers[:2]})
        else:
            log_result("FAOSTAT Top Producers Cacao", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_result("FAOSTAT Top Producers Cacao", False, f"Erreur: {str(e)}")
    
    # Test FAOSTAT Commodities
    try:
        response = session.get(f"{BASE_URL}/production/faostat/commodities", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            commodities = data.get('commodities', [])
            if len(commodities) > 0:
                log_result("FAOSTAT Commodities", True, f"Liste validée - {len(commodities)} commodités")
            else:
                log_result("FAOSTAT Commodities", False, f"Aucune commodité", data)
        else:
            log_result("FAOSTAT Commodities", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_result("FAOSTAT Commodities", False, f"Erreur: {str(e)}")
    
    # Test FAOSTAT Fisheries
    try:
        response = session.get(f"{BASE_URL}/production/faostat/fisheries", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if data:
                log_result("FAOSTAT Fisheries", True, "Données de pêche validées")
            else:
                log_result("FAOSTAT Fisheries", False, "Aucune donnée de pêche")
        else:
            log_result("FAOSTAT Fisheries", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_result("FAOSTAT Fisheries", False, f"Erreur: {str(e)}")
    
    print("\n🏭 Tests UNIDO Production Industrielle")
    print("-" * 50)
    
    # Test UNIDO Statistics
    try:
        response = session.get(f"{BASE_URL}/production/unido/statistics", timeout=TIMEOUT)
        if response.status_code == 200:
            stats = response.json()
            mva = stats.get('total_mva_bln_usd', 0)
            if stats.get('total_countries') == 54 and abs(mva - 289.9) <= 10:
                log_result("UNIDO Statistics", True, f"Statistiques validées - {stats['total_countries']} pays, MVA ${mva}B")
            else:
                log_result("UNIDO Statistics", False, f"Valeurs incorrectes", stats)
        else:
            log_result("UNIDO Statistics", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_result("UNIDO Statistics", False, f"Erreur: {str(e)}")
    
    # Test UNIDO MAR
    try:
        response = session.get(f"{BASE_URL}/production/unido/MAR", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            mva = data.get('mva_2023_mln_usd', 0)
            gdp_pct = data.get('mva_gdp_percent', 0)
            if data.get('country_name') == "Maroc" and abs(mva - 32500) <= 1000 and abs(gdp_pct - 24.8) <= 2:
                log_result("UNIDO MAR", True, f"Données MAR validées - MVA ${mva}M, MVA/PIB {gdp_pct}%")
            else:
                log_result("UNIDO MAR", False, f"Données incorrectes", data)
        else:
            log_result("UNIDO MAR", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_result("UNIDO MAR", False, f"Erreur: {str(e)}")
    
    # Test UNIDO ZAF
    try:
        response = session.get(f"{BASE_URL}/production/unido/ZAF", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            top_sectors_str = str(data.get('top_sectors', ''))
            if data.get('country_name') == "Afrique du Sud" and 'automobile' in top_sectors_str.lower():
                log_result("UNIDO ZAF", True, f"Données ZAF validées - automobile présent")
            else:
                log_result("UNIDO ZAF", False, f"Données incorrectes", data)
        else:
            log_result("UNIDO ZAF", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_result("UNIDO ZAF", False, f"Erreur: {str(e)}")
    
    # Test UNIDO Ranking
    try:
        response = session.get(f"{BASE_URL}/production/unido/ranking", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            ranking = data.get('ranking', [])
            top_countries = [item.get('country_iso3', '') for item in ranking[:5]]
            expected_top = ['ZAF', 'EGY', 'NGA']
            if all(country in top_countries for country in expected_top):
                log_result("UNIDO Ranking", True, f"Classement validé - {len(ranking)} pays, ZAF/EGY/NGA dans le top")
            else:
                log_result("UNIDO Ranking", False, f"Classement incorrect", {'top_5': top_countries})
        else:
            log_result("UNIDO Ranking", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_result("UNIDO Ranking", False, f"Erreur: {str(e)}")
    
    # Test UNIDO Sector Analysis
    try:
        response = session.get(f"{BASE_URL}/production/unido/sector-analysis/10", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if data:
                log_result("UNIDO Sector Analysis 10", True, "Analyse secteur alimentaire validée")
            else:
                log_result("UNIDO Sector Analysis 10", False, "Aucune analyse")
        else:
            log_result("UNIDO Sector Analysis 10", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_result("UNIDO Sector Analysis 10", False, f"Erreur: {str(e)}")
    
    # Test UNIDO ISIC Sectors
    try:
        response = session.get(f"{BASE_URL}/production/unido/isic-sectors", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            sectors = data.get('sectors', {})
            isic_codes = list(sectors.keys())
            expected_range = [str(i) for i in range(10, 34)]
            missing_codes = [code for code in expected_range if code not in isic_codes]
            if not missing_codes:
                log_result("UNIDO ISIC Sectors", True, f"Classification ISIC validée - {len(sectors)} secteurs, codes 10-33 présents")
            else:
                log_result("UNIDO ISIC Sectors", False, f"Codes manquants: {missing_codes}")
        else:
            log_result("UNIDO ISIC Sectors", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_result("UNIDO ISIC Sectors", False, f"Erreur: {str(e)}")
    
    # Résumé
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['success'])
    failed_tests = total_tests - passed_tests
    
    print(f"\n📊 RÉSUMÉ DES TESTS FAOSTAT/UNIDO")
    print("=" * 50)
    print(f"Total des tests: {total_tests}")
    print(f"✅ Réussis: {passed_tests}")
    print(f"❌ Échoués: {failed_tests}")
    print(f"📈 Taux de réussite: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests > 0:
        print(f"\n🔍 TESTS ÉCHOUÉS:")
        for result in results:
            if not result['success']:
                print(f"   • {result['test']}: {result['message']}")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = test_faostat_unido_endpoints()
    sys.exit(0 if success else 1)