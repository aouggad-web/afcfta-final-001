"""
Product Name Translations for Trade Data
=========================================
French to English translations for product names and country names
"""

PRODUCT_TRANSLATIONS = {
    "Huiles de pétrole raffinées": "Refined petroleum oils",
    "Téléphones et équipements de télécommunication": "Telephones and telecommunication equipment",
    "Blé et méteil": "Wheat and meslin",
    "Véhicules automobiles": "Motor vehicles",
    "Machines automatiques de traitement de données (ordinateurs)": "Automatic data processing machines (computers)",
    "Médicaments": "Medicines",
    "Riz": "Rice",
    "Véhicules pour transport de marchandises": "Goods transport vehicles",
    "Sucre de canne ou de betterave": "Cane or beet sugar",
    "Huile de palme": "Palm oil",
    "Fer et acier": "Iron and steel",
    "Engrais": "Fertilizers",
    "Plastiques et ouvrages en plastiques": "Plastics and plastic articles",
    "Caoutchouc et articles en caoutchouc": "Rubber and rubber articles",
    "Papier et carton": "Paper and paperboard",
    "Articles d'habillement": "Clothing articles",
    "Équipements électriques": "Electrical equipment",
    "Meubles et mobilier": "Furniture",
    "Huiles de soja": "Soybean oils",
    "Produits laitiers": "Dairy products",
    "Huiles brutes de pétrole": "Crude petroleum oils",
    "Gaz naturel GNL": "Natural gas LNG",
    "Or": "Gold",
    "Diamants": "Diamonds",
    "Minerai de fer": "Iron ore",
    "Cuivre et concentrés de cuivre": "Copper and copper concentrates",
    "Phosphates": "Phosphates",
    "Cacao et préparations": "Cocoa and preparations",
    "Café": "Coffee",
    "Coton": "Cotton",
    "Fruits et noix": "Fruits and nuts",
    "Légumes": "Vegetables",
    "Poissons et crustacés": "Fish and crustaceans",
    "Charbon": "Coal",
    "Manganèse et minerais": "Manganese and ores",
    "Zinc et concentrés de zinc": "Zinc and zinc concentrates",
    "Aluminium": "Aluminum",
    "Tabac": "Tobacco",
    "Bois et articles en bois": "Wood and wood articles",
    "Véhicules automobiles usagés": "Used motor vehicles",
    "Énergie électrique": "Electrical energy",
    "Carburants et lubrifiants": "Fuels and lubricants",
    "Ciment": "Cement",
    "Produits chimiques organiques": "Organic chemicals",
    "Produits chimiques inorganiques": "Inorganic chemicals",
    "Textiles et tissus": "Textiles and fabrics",
    "Chaussures": "Footwear",
    "Machines et équipements mécaniques": "Machinery and mechanical equipment",
    "Appareils électroniques": "Electronic devices"
}

COUNTRY_TRANSLATIONS = {
    "Afrique du Sud": "South Africa",
    "Égypte": "Egypt",
    "Nigéria": "Nigeria",
    "Algérie": "Algeria",
    "Maroc": "Morocco",
    "Éthiopie": "Ethiopia",
    "Kenya": "Kenya",
    "Angola": "Angola",
    "Ghana": "Ghana",
    "Tanzanie": "Tanzania",
    "Côte d'Ivoire": "Côte d'Ivoire",
    "Tunisie": "Tunisia",
    "RD Congo": "DR Congo",
    "Cameroun": "Cameroon",
    "Ouganda": "Uganda",
    "Sénégal": "Senegal",
    "Mozambique": "Mozambique",
    "Zambie": "Zambia",
    "Zimbabwe": "Zimbabwe",
    "Botswana": "Botswana",
    "Namibie": "Namibia",
    "Maurice": "Mauritius",
    "Rwanda": "Rwanda",
    "Libye": "Libya",
    "Soudan": "Sudan",
    "Mali": "Mali",
    "Burkina Faso": "Burkina Faso",
    "Niger": "Niger",
    "Tchad": "Chad",
    "Bénin": "Benin",
    "Togo": "Togo",
    "Guinée": "Guinea",
    "Malawi": "Malawi",
    "Congo": "Congo",
    "Gabon": "Gabon",
    "Guinée Équatoriale": "Equatorial Guinea",
    "Mauritanie": "Mauritania",
    "Eswatini": "Eswatini",
    "Lesotho": "Lesotho",
    "Madagascar": "Madagascar",
    "Inde": "India",
    "Chine": "China",
    "États-Unis": "United States",
    "France": "France",
    "Allemagne": "Germany",
    "Japon": "Japan",
    "Arabie Saoudite": "Saudi Arabia",
    "Pays-Bas": "Netherlands",
    "Corée du Sud": "South Korea",
    "Vietnam": "Vietnam",
    "Russie": "Russia",
    "Ukraine": "Ukraine",
    "Canada": "Canada",
    "Thaïlande": "Thailand",
    "Pakistan": "Pakistan"
}

def translate_product(product_name: str, language: str = 'fr') -> str:
    """Translate product name to specified language"""
    if language == 'en' and product_name in PRODUCT_TRANSLATIONS:
        return PRODUCT_TRANSLATIONS[product_name]
    return product_name

def translate_country(country_name: str, language: str = 'fr') -> str:
    """Translate country name to specified language"""
    if language == 'en' and country_name in COUNTRY_TRANSLATIONS:
        return COUNTRY_TRANSLATIONS[country_name]
    return country_name

def translate_country_list(countries: list, language: str = 'fr') -> list:
    """Translate a list of country names"""
    return [translate_country(c, language) for c in countries]
