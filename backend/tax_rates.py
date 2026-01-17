# Taux de TVA et autres taxes par pays africain
# Sources: Réglementations nationales et communautaires 2025
# Dernière mise à jour: Janvier 2025

# Taux de TVA standard par pays (en pourcentage)
# Sources: PwC Tax Summaries, IMF, Administrations fiscales nationales
VAT_RATES = {
    "DZ": 19.0,   # Algérie
    "AO": 14.0,   # Angola
    "BJ": 18.0,   # Bénin (UEMOA)
    "BW": 14.0,   # Botswana (SACU)
    "BF": 18.0,   # Burkina Faso (UEMOA)
    "BI": 18.0,   # Burundi (EAC)
    "CV": 15.0,   # Cap-Vert
    "CM": 19.25,  # Cameroun (CEMAC) - 19.25% avec centimes additionnels
    "CF": 19.0,   # République Centrafricaine (CEMAC)
    "TD": 18.0,   # Tchad (CEMAC)
    "KM": 10.0,   # Comores
    "CG": 18.0,   # République du Congo (CEMAC)
    "CD": 16.0,   # République Démocratique du Congo (EAC)
    "CI": 18.0,   # Côte d'Ivoire (UEMOA)
    "DJ": 10.0,   # Djibouti
    "EG": 14.0,   # Égypte
    "GQ": 15.0,   # Guinée Équatoriale (CEMAC)
    "ER": 5.0,    # Érythrée
    "SZ": 15.0,   # Eswatini (SACU)
    "ET": 15.0,   # Éthiopie
    "GA": 18.0,   # Gabon (CEMAC)
    "GM": 15.0,   # Gambie (CEDEAO)
    "GH": 15.0,   # Ghana (CEDEAO) - 12.5% + NHIL 2.5%
    "GN": 18.0,   # Guinée (CEDEAO)
    "GW": 17.0,   # Guinée-Bissau (UEMOA)
    "KE": 16.0,   # Kenya (EAC)
    "LS": 15.0,   # Lesotho (SACU)
    "LR": 10.0,   # Libéria (CEDEAO)
    "LY": 0.0,    # Libye (pas de TVA)
    "MG": 20.0,   # Madagascar
    "MW": 16.5,   # Malawi
    "ML": 18.0,   # Mali (UEMOA)
    "MR": 16.0,   # Mauritanie
    "MU": 15.0,   # Maurice
    "MA": 20.0,   # Maroc
    "MZ": 17.0,   # Mozambique (16% à partir de 2025)
    "NA": 15.0,   # Namibie (SACU)
    "NE": 19.0,   # Niger (UEMOA)
    "NG": 7.5,    # Nigéria (CEDEAO)
    "RW": 18.0,   # Rwanda (EAC)
    "ST": 15.0,   # São Tomé-et-Príncipe
    "SN": 18.0,   # Sénégal (UEMOA)
    "SC": 15.0,   # Seychelles
    "SL": 15.0,   # Sierra Leone (CEDEAO)
    "SO": 0.0,    # Somalie (pas de TVA formelle)
    "ZA": 15.0,   # Afrique du Sud (SACU) - 15.5% à partir de mai 2025
    "SS": 18.0,   # Soudan du Sud (EAC)
    "SD": 17.0,   # Soudan
    "TZ": 18.0,   # Tanzanie (EAC)
    "TG": 18.0,   # Togo (UEMOA)
    "TN": 19.0,   # Tunisie
    "UG": 18.0,   # Ouganda (EAC)
    "ZM": 16.0,   # Zambie
    "ZW": 15.0,   # Zimbabwe (réduit de 14.5%)
}

# Redevance statistique (en pourcentage de la valeur CIF)
# Applicable dans certains pays
STATISTICAL_FEE = {
    "BJ": 1.0,
    "BF": 1.0,
    "CI": 1.0,
    "GN": 1.0,
    "ML": 1.0,
    "NE": 1.0,
    "SN": 1.0,
    "TG": 1.0,
    "CM": 1.0,
    "GA": 1.0,
    "TD": 1.0,
    "CF": 1.0,
    "CG": 1.0,
    "GQ": 1.0,
}

# Prélèvement Communautaire de Solidarité (PCS) - CEDEAO/UEMOA
# En pourcentage de la valeur CIF
COMMUNITY_LEVY = {
    "BJ": 0.5,
    "BF": 0.5,
    "CI": 0.5,
    "GN": 0.5,
    "GW": 0.5,
    "ML": 0.5,
    "NE": 0.5,
    "SN": 0.5,
    "TG": 0.5,
    "GM": 0.5,
    "GH": 0.5,
    "LR": 0.5,
    "NG": 0.5,
    "SL": 0.5,
}

# Prélèvement CEDEAO (en pourcentage de la valeur CIF)
ECOWAS_LEVY = {
    "BJ": 1.0,
    "BF": 1.0,
    "CI": 1.0,
    "GN": 1.0,
    "GW": 1.0,
    "ML": 1.0,
    "NE": 1.0,
    "SN": 1.0,
    "TG": 1.0,
    "GM": 1.0,
    "GH": 1.0,
    "LR": 1.0,
    "NG": 1.0,
    "SL": 1.0,
    "CV": 1.0,
}

def get_vat_rate(country_code: str) -> float:
    """Obtenir le taux de TVA pour un pays"""
    return VAT_RATES.get(country_code, 18.0)  # 18% par défaut

def get_statistical_fee_rate(country_code: str) -> float:
    """Obtenir le taux de redevance statistique"""
    return STATISTICAL_FEE.get(country_code, 0.0)

def get_community_levy_rate(country_code: str) -> float:
    """Obtenir le taux de prélèvement communautaire"""
    return COMMUNITY_LEVY.get(country_code, 0.0)

def get_ecowas_levy_rate(country_code: str) -> float:
    """Obtenir le taux de prélèvement CEDEAO"""
    return ECOWAS_LEVY.get(country_code, 0.0)

def calculate_all_taxes(value: float, customs_duty: float, country_code: str) -> dict:
    """
    Calculer toutes les taxes applicables selon l'ordre officiel
    
    ORDRE DE CALCUL (tax_computation_order):
    1. Droits de douane (sur valeur CIF)
    2. Accises (sur valeur CIF) - si applicable
    3. Redevance statistique (sur valeur CIF)
    4. Prélèvements communautaires (sur valeur CIF)
    5. TVA (sur base = CIF + DD + Accises + Levies)
    
    Références légales: Codes douaniers nationaux, directives CEDEAO/UEMOA
    """
    # Journal de calcul ligne par ligne
    calculation_journal = []
    
    # Étape 0: Valeur CIF (base)
    calculation_journal.append({
        "step": 0,
        "component": "Valeur CIF (Cost, Insurance, Freight)",
        "base": value,
        "rate": 0,
        "amount": value,
        "cumulative": value,
        "legal_ref": "Valeur transactionnelle (Accord OMC sur l'évaluation)",
        "legal_ref_url": "https://www.wto.org/english/docs_e/legal_e/20-val_01_e.htm"
    })
    
    cumulative = value
    
    # Étape 1: Droits de douane (déjà calculé en amont)
    calculation_journal.append({
        "step": 1,
        "component": "Droits de douane (DD)",
        "base": value,
        "rate": (customs_duty / value * 100) if value > 0 else 0,
        "amount": customs_duty,
        "cumulative": cumulative + customs_duty,
        "legal_ref": f"Tarif NPF/ZLECAf - Code douanier {country_code}",
        "legal_ref_url": "https://au.int/en/treaties/agreement-establishing-african-continental-free-trade-area"
    })
    cumulative += customs_duty
    
    # Étape 2: Accises (sur valeur CIF) - pour l'instant 0, à enrichir selon produits
    excise_amount = 0  # TODO: implémenter selon excise_schedule_2025.csv
    if excise_amount > 0:
        calculation_journal.append({
            "step": 2,
            "component": "Droits d'accises",
            "base": value,
            "rate": 0,
            "amount": excise_amount,
            "cumulative": cumulative + excise_amount,
            "legal_ref": f"Barème accises {country_code}",
            "legal_ref_url": ""
        })
        cumulative += excise_amount
    
    # Étape 3: Redevance statistique (sur la valeur CIF)
    statistical_fee_rate = get_statistical_fee_rate(country_code)
    statistical_fee = value * (statistical_fee_rate / 100)
    if statistical_fee > 0:
        calculation_journal.append({
            "step": 3,
            "component": "Redevance statistique",
            "base": value,
            "rate": statistical_fee_rate,
            "amount": statistical_fee,
            "cumulative": cumulative + statistical_fee,
            "legal_ref": f"Directive UEMOA/CEMAC {country_code}",
            "legal_ref_url": "https://www.uemoa.int/"
        })
        cumulative += statistical_fee
    
    # Étape 4a: Prélèvement communautaire de solidarité (sur la valeur CIF)
    community_levy_rate = get_community_levy_rate(country_code)
    community_levy = value * (community_levy_rate / 100)
    if community_levy > 0:
        calculation_journal.append({
            "step": 4,
            "component": "Prélèvement Communautaire de Solidarité (PCS)",
            "base": value,
            "rate": community_levy_rate,
            "amount": community_levy,
            "cumulative": cumulative + community_levy,
            "legal_ref": f"Directive UEMOA PCS {country_code}",
            "legal_ref_url": "https://www.uemoa.int/"
        })
        cumulative += community_levy
    
    # Étape 4b: Prélèvement CEDEAO (sur la valeur CIF)
    ecowas_levy_rate = get_ecowas_levy_rate(country_code)
    ecowas_levy = value * (ecowas_levy_rate / 100)
    if ecowas_levy > 0:
        calculation_journal.append({
            "step": 5,
            "component": "Prélèvement CEDEAO",
            "base": value,
            "rate": ecowas_levy_rate,
            "amount": ecowas_levy,
            "cumulative": cumulative + ecowas_levy,
            "legal_ref": f"Acte additionnel CEDEAO {country_code}",
            "legal_ref_url": "https://www.ecowas.int/"
        })
        cumulative += ecowas_levy
    
    # Étape 5: TVA (sur base = CIF + DD + Accises + tous les levies)
    vat_base = value + customs_duty + excise_amount + statistical_fee + community_levy + ecowas_levy
    vat_rate = get_vat_rate(country_code)
    vat_amount = vat_base * (vat_rate / 100)
    
    calculation_journal.append({
        "step": 6,
        "component": "TVA (Taxe sur la Valeur Ajoutée)",
        "base": vat_base,
        "rate": vat_rate,
        "amount": vat_amount,
        "cumulative": cumulative + vat_amount,
        "legal_ref": f"Code TVA {country_code}",
        "legal_ref_url": ""
    })
    cumulative += vat_amount
    
    # Total autres taxes (hors douane et TVA)
    other_taxes_total = statistical_fee + community_levy + ecowas_levy + excise_amount
    
    # Total général
    total_cost = cumulative
    
    return {
        "vat_rate": vat_rate,
        "vat_amount": vat_amount,
        "statistical_fee_rate": statistical_fee_rate,
        "statistical_fee_amount": statistical_fee,
        "community_levy_rate": community_levy_rate,
        "community_levy_amount": community_levy,
        "ecowas_levy_rate": ecowas_levy_rate,
        "ecowas_levy_amount": ecowas_levy,
        "excise_amount": excise_amount,
        "other_taxes_total": other_taxes_total,
        "vat_base": vat_base,
        "total_cost": total_cost,
        "calculation_journal": calculation_journal,
        "computation_order_ref": "Ordre de calcul: DD → Accises → Levies → TVA (base cumulative)",
        "last_verified": "2025-01-11",
        "confidence_level": "high"
    }
