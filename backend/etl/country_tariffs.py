"""
Tarifs douaniers par pays - Données officielles
Source: Tarifs douaniers nationaux officiels
"""

from typing import Dict, Optional

# =============================================================================
# ALGÉRIE - 4 taux officiels: 30%, 15%, 5%, 0%
# Source: Direction Générale des Douanes Algériennes
# =============================================================================
ALGERIA_TARIFFS = {
    # Taux 30% - Produits de consommation finale, produits de luxe
    "30": [
        "04",  # Produits laitiers, oeufs, miel
        "16",  # Préparations de viandes, poissons
        "17",  # Sucres et sucreries
        "19",  # Préparations à base de céréales
        "20",  # Préparations de légumes, fruits
        "21",  # Préparations alimentaires diverses
        "22",  # Boissons, liquides alcooliques
        "24",  # Tabacs
        "33",  # Huiles essentielles, parfumerie, cosmétiques
        "34",  # Savons, détergents
        "42",  # Ouvrages en cuir
        "61",  # Vêtements tricotés
        "62",  # Vêtements non tricotés
        "63",  # Autres articles textiles confectionnés
        "64",  # Chaussures
        "65",  # Coiffures
        "69",  # Produits céramiques
        "70",  # Verre et ouvrages en verre
        "71",  # Perles, pierres précieuses, bijouterie
        "91",  # Horlogerie
        "92",  # Instruments de musique
        "94",  # Meubles, literie
        "95",  # Jouets, jeux
        "96",  # Ouvrages divers
    ],
    # Taux 15% - Produits semi-finis, intrants industriels
    "15": [
        "01",  # Animaux vivants
        "02",  # Viandes
        "03",  # Poissons, crustacés
        "05",  # Autres produits d'origine animale
        "06",  # Plantes vivantes
        "07",  # Légumes
        "08",  # Fruits
        "09",  # Café, thé, épices
        "10",  # Céréales
        "11",  # Produits de la minoterie
        "12",  # Graines oléagineuses
        "13",  # Gommes, résines
        "14",  # Matières à tresser
        "15",  # Graisses et huiles
        "23",  # Résidus industries alimentaires
        "32",  # Extraits tannants, colorants
        "35",  # Matières albuminoïdes, colles
        "36",  # Poudres, explosifs
        "37",  # Produits photographiques
        "38",  # Produits chimiques divers
        "39",  # Matières plastiques
        "40",  # Caoutchouc
        "41",  # Peaux et cuirs
        "43",  # Pelleteries
        "44",  # Bois et ouvrages en bois
        "45",  # Liège
        "46",  # Ouvrages de sparterie
        "47",  # Pâtes de bois
        "48",  # Papiers et cartons
        "49",  # Produits de l'édition
        "50",  # Soie
        "51",  # Laine
        "52",  # Coton
        "53",  # Autres fibres textiles végétales
        "54",  # Filaments synthétiques
        "55",  # Fibres synthétiques discontinues
        "56",  # Ouates, feutres
        "57",  # Tapis
        "58",  # Tissus spéciaux
        "59",  # Tissus imprégnés
        "60",  # Étoffes de bonneterie
        "66",  # Parapluies
        "67",  # Plumes apprêtées
        "68",  # Ouvrages en pierres
        "72",  # Fonte, fer et acier
        "73",  # Ouvrages en fonte, fer, acier
        "74",  # Cuivre
        "75",  # Nickel
        "76",  # Aluminium
        "78",  # Plomb
        "79",  # Zinc
        "80",  # Étain
        "81",  # Autres métaux communs
        "82",  # Outils, coutellerie
        "83",  # Ouvrages divers en métaux
    ],
    # Taux 5% - Équipements, matières premières, biens d'investissement
    "05": [
        "25",  # Sel, soufre, terres, pierres
        "26",  # Minerais, scories
        "27",  # Combustibles minéraux (hors carburants finis)
        "28",  # Produits chimiques inorganiques
        "29",  # Produits chimiques organiques
        "30",  # Produits pharmaceutiques
        "31",  # Engrais
        "84",  # Machines, appareils mécaniques
        "85",  # Machines, appareils électriques
        "86",  # Véhicules ferroviaires
        "87",  # Voitures automobiles, tracteurs (certains)
        "88",  # Navigation aérienne
        "89",  # Navigation maritime
        "90",  # Instruments optiques, médicaux
        "93",  # Armes et munitions
    ],
    # Taux 0% - Exemptions, accords spécifiques
    "00": [
        # Produits exonérés par accords ou régimes spéciaux
        # À compléter selon les conventions
    ]
}

# =============================================================================
# MAROC - Taux officiels: 40%, 25%, 17.5%, 10%, 2.5%, 0%
# Source: Administration des Douanes et Impôts Indirects (ADII)
# =============================================================================
MOROCCO_TARIFFS = {
    "40": ["22", "24"],  # Boissons alcoolisées, tabacs
    "25": ["04", "16", "17", "19", "20", "21", "33", "61", "62", "63", "64", "94", "95"],
    "17.5": ["01", "02", "03", "07", "08", "09", "15", "39", "40", "42", "44", "48", "69", "70", "72", "73", "76", "82", "83"],
    "10": ["06", "10", "11", "12", "23", "28", "29", "32", "35", "38", "47", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "68", "74", "75"],
    "2.5": ["25", "26", "27", "30", "31", "84", "85", "86", "87", "88", "89", "90"],
    "00": []
}

# =============================================================================
# ÉGYPTE - Taux officiels: 60%, 40%, 30%, 20%, 10%, 5%, 2%, 0%
# Source: Egyptian Customs Authority
# =============================================================================
EGYPT_TARIFFS = {
    "60": ["22", "24"],  # Alcool, tabac
    "40": ["33", "61", "62", "64", "71", "91", "95"],
    "30": ["04", "16", "17", "19", "20", "21", "42", "63", "65", "69", "70", "94"],
    "20": ["01", "02", "03", "07", "08", "09", "15", "39", "40", "44", "48", "57", "72", "73", "76", "82", "83"],
    "10": ["06", "10", "11", "12", "23", "32", "35", "38", "47", "50", "51", "52", "53", "54", "55", "56", "58", "59", "60", "68", "74", "75"],
    "05": ["25", "26", "27", "28", "29", "31", "84", "85", "86", "88", "89", "90"],
    "02": ["30", "87"],  # Médicaments, véhicules (certains)
    "00": []
}

# =============================================================================
# TUNISIE - Taux officiels: 36%, 27%, 20%, 15%, 10%, 0%
# Source: Douane Tunisienne
# =============================================================================
TUNISIA_TARIFFS = {
    "36": ["22", "24", "33", "61", "62", "64", "71", "91", "95"],
    "27": ["04", "16", "17", "19", "20", "21", "42", "63", "65", "69", "70", "94"],
    "20": ["01", "02", "03", "07", "08", "09", "15", "39", "40", "44", "48", "57", "72", "73", "76", "82", "83"],
    "15": ["06", "10", "11", "12", "23", "32", "35", "38", "47", "50", "51", "52", "53", "54", "55", "56", "58", "59", "60", "68", "74", "75"],
    "10": ["25", "26", "27", "28", "29", "31", "84", "85", "86", "87", "88", "89", "90"],
    "00": ["30"]  # Médicaments exemptés
}

# =============================================================================
# AFRIQUE DU SUD - Taux officiels: 45%, 30%, 25%, 20%, 15%, 10%, 5%, 0%
# Source: South African Revenue Service (SARS)
# =============================================================================
SOUTH_AFRICA_TARIFFS = {
    "45": ["22", "24"],
    "30": ["61", "62", "64"],
    "25": ["04", "16", "17", "19", "20", "21", "33", "42", "63", "65", "69", "70", "71", "91", "94", "95"],
    "20": ["01", "02", "03", "07", "08", "09", "15", "39", "40", "44", "48", "57", "72", "73", "76", "82", "83", "87"],
    "15": ["06", "10", "11", "12", "23", "32", "35", "38", "47", "50", "51", "52", "53", "54", "55", "56", "58", "59", "60", "68", "74", "75"],
    "10": ["25", "26", "27", "28", "29", "31"],
    "05": ["84", "85", "86", "88", "89", "90"],
    "00": ["30"]
}

# =============================================================================
# NIGÉRIA - Taux officiels: 35%, 20%, 10%, 5%, 0%
# Source: Nigeria Customs Service
# =============================================================================
NIGERIA_TARIFFS = {
    "35": ["22", "24", "33", "61", "62", "64", "71", "91", "94", "95"],
    "20": ["01", "02", "03", "04", "07", "08", "09", "15", "16", "17", "19", "20", "21", "39", "40", "42", "44", "48", "57", "63", "65", "69", "70", "72", "73", "76", "82", "83", "87"],
    "10": ["06", "10", "11", "12", "23", "25", "26", "27", "28", "29", "31", "32", "35", "38", "47", "50", "51", "52", "53", "54", "55", "56", "58", "59", "60", "68", "74", "75"],
    "05": ["84", "85", "86", "88", "89", "90"],
    "00": ["30"]
}

# Mapping code pays -> tarifs
COUNTRY_TARIFFS = {
    "DZ": ALGERIA_TARIFFS,
    "MA": MOROCCO_TARIFFS,
    "EG": EGYPT_TARIFFS,
    "TN": TUNISIA_TARIFFS,
    "ZA": SOUTH_AFRICA_TARIFFS,
    "NG": NIGERIA_TARIFFS,
}


def get_country_tariff_rate(country_code: str, hs_chapter: str) -> float:
    """
    Obtenir le taux de douane pour un pays et un chapitre HS donné
    
    Args:
        country_code: Code ISO 2 du pays (ex: 'DZ' pour Algérie)
        hs_chapter: Chapitre HS à 2 chiffres (ex: '01', '87')
    
    Returns:
        Taux de douane en pourcentage (ex: 0.15 pour 15%)
    """
    # Si pas de données spécifiques pour le pays, retourner None
    if country_code not in COUNTRY_TARIFFS:
        return None
    
    country_tariffs = COUNTRY_TARIFFS[country_code]
    
    # Chercher dans quel taux se trouve le chapitre
    for rate_str, chapters in country_tariffs.items():
        if hs_chapter in chapters:
            # Convertir le taux en décimal (ex: "30" -> 0.30)
            return float(rate_str) / 100
    
    # Taux par défaut si chapitre non trouvé (15% pour Algérie)
    default_rates = {
        "DZ": 0.15,  # Algérie: 15% par défaut
        "MA": 0.175,  # Maroc: 17.5% par défaut
        "EG": 0.20,  # Égypte: 20% par défaut
        "TN": 0.20,  # Tunisie: 20% par défaut
        "ZA": 0.20,  # Afrique du Sud: 20% par défaut
        "NG": 0.20,  # Nigéria: 20% par défaut
    }
    
    return default_rates.get(country_code, 0.15)


def get_available_rates(country_code: str) -> list:
    """
    Obtenir la liste des taux disponibles pour un pays
    
    Args:
        country_code: Code ISO 2 du pays
    
    Returns:
        Liste des taux en pourcentage
    """
    if country_code not in COUNTRY_TARIFFS:
        return []
    
    rates = [float(r) for r in COUNTRY_TARIFFS[country_code].keys()]
    return sorted(rates, reverse=True)


def get_country_tariff_info(country_code: str) -> Optional[Dict]:
    """
    Obtenir les informations sur les tarifs d'un pays
    
    Args:
        country_code: Code ISO 2 du pays
    
    Returns:
        Dictionnaire avec les taux et les chapitres associés
    """
    if country_code not in COUNTRY_TARIFFS:
        return None
    
    country_tariffs = COUNTRY_TARIFFS[country_code]
    
    info = {
        "country_code": country_code,
        "available_rates": get_available_rates(country_code),
        "rate_details": {}
    }
    
    for rate_str, chapters in country_tariffs.items():
        rate_pct = float(rate_str)
        info["rate_details"][f"{rate_pct}%"] = {
            "rate_decimal": rate_pct / 100,
            "chapters": chapters,
            "chapter_count": len(chapters)
        }
    
    return info
