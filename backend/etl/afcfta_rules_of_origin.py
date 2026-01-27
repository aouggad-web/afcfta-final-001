"""
AfCFTA Rules of Origin Database
Based on Annex II, Appendix IV of the AfCFTA Agreement
Product-Specific Rules (PSRs) linked to HS6 codes

Sources:
- AfCFTA Rules of Origin Manual
- AfCFTA Protocol on Trade in Goods
- AU Secretariat Guidelines
"""

# Rule Types
ORIGIN_TYPES = {
    "WO": {"en": "Wholly Obtained", "fr": "Entièrement Obtenu"},
    "CC": {"en": "Change of Chapter", "fr": "Changement de Chapitre"},
    "CTH": {"en": "Change of Tariff Heading", "fr": "Changement de Position Tarifaire"},
    "CTSH": {"en": "Change of Tariff Subheading", "fr": "Changement de Sous-Position"},
    "VA": {"en": "Value Added", "fr": "Valeur Ajoutée"},
    "SP": {"en": "Specific Process", "fr": "Processus Spécifique"},
    "RVC": {"en": "Regional Value Content", "fr": "Contenu de Valeur Régionale"},
}

# Chapter-level rules (for products not yet in PSR list)
CHAPTER_RULES = {
    "01": {"primary": "WO", "alt": None, "rvc": 0, "description_fr": "Animaux vivants - entièrement obtenus", "description_en": "Live animals - wholly obtained"},
    "02": {"primary": "WO", "alt": "CC", "rvc": 0, "description_fr": "Viandes - entièrement obtenues ou CC", "description_en": "Meat - wholly obtained or CC"},
    "03": {"primary": "WO", "alt": None, "rvc": 0, "description_fr": "Poissons - entièrement obtenus", "description_en": "Fish - wholly obtained"},
    "04": {"primary": "WO", "alt": "CC", "rvc": 0, "description_fr": "Produits laitiers - entièrement obtenus ou CC", "description_en": "Dairy - wholly obtained or CC"},
    "05": {"primary": "WO", "alt": None, "rvc": 0, "description_fr": "Produits animaux - entièrement obtenus", "description_en": "Animal products - wholly obtained"},
    "06": {"primary": "WO", "alt": None, "rvc": 0, "description_fr": "Plantes vivantes - entièrement obtenues", "description_en": "Live plants - wholly obtained"},
    "07": {"primary": "WO", "alt": None, "rvc": 0, "description_fr": "Légumes - entièrement obtenus", "description_en": "Vegetables - wholly obtained"},
    "08": {"primary": "WO", "alt": None, "rvc": 0, "description_fr": "Fruits - entièrement obtenus", "description_en": "Fruits - wholly obtained"},
    "09": {"primary": "WO", "alt": "CTH", "rvc": 0, "description_fr": "Café, thé, épices - entièrement obtenus ou CTH", "description_en": "Coffee, tea, spices - wholly obtained or CTH"},
    "10": {"primary": "WO", "alt": None, "rvc": 0, "description_fr": "Céréales - entièrement obtenues", "description_en": "Cereals - wholly obtained"},
    "11": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Produits de minoterie - CTH ou 40% VA", "description_en": "Milling products - CTH or 40% VA"},
    "12": {"primary": "WO", "alt": None, "rvc": 0, "description_fr": "Graines oléagineuses - entièrement obtenues", "description_en": "Oil seeds - wholly obtained"},
    "15": {"primary": "CC", "alt": "VA40", "rvc": 40, "description_fr": "Graisses animales/végétales - CC ou 40% VA", "description_en": "Animal/vegetable fats - CC or 40% VA"},
    "16": {"primary": "CC", "alt": "VA40", "rvc": 40, "description_fr": "Préparations de viandes - CC ou 40% VA", "description_en": "Meat preparations - CC or 40% VA"},
    "17": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Sucres - CTH ou 40% VA", "description_en": "Sugars - CTH or 40% VA"},
    "18": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Cacao et préparations - CTH ou 40% VA", "description_en": "Cocoa preparations - CTH or 40% VA"},
    "19": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Préparations à base de céréales - CTH ou 40% VA", "description_en": "Cereal preparations - CTH or 40% VA"},
    "20": {"primary": "CC", "alt": "VA40", "rvc": 40, "description_fr": "Préparations de légumes/fruits - CC ou 40% VA", "description_en": "Vegetable/fruit preparations - CC or 40% VA"},
    "21": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Préparations alimentaires diverses - CTH ou 40% VA", "description_en": "Misc food preparations - CTH or 40% VA"},
    "22": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Boissons - CTH ou 40% VA", "description_en": "Beverages - CTH or 40% VA"},
    "24": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Tabacs - CTH ou 40% VA", "description_en": "Tobacco - CTH or 40% VA"},
    "25": {"primary": "WO", "alt": "CTH", "rvc": 0, "description_fr": "Sel, soufre, terres - entièrement obtenus ou CTH", "description_en": "Salt, sulphur, earths - WO or CTH"},
    "26": {"primary": "WO", "alt": "CTH", "rvc": 0, "description_fr": "Minerais - entièrement obtenus ou CTH", "description_en": "Ores - WO or CTH"},
    "27": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Combustibles minéraux - CTH ou 40% VA", "description_en": "Mineral fuels - CTH or 40% VA"},
    "28": {"primary": "CTH", "alt": "CTSH", "rvc": 0, "description_fr": "Produits chimiques inorganiques - CTH ou CTSH", "description_en": "Inorganic chemicals - CTH or CTSH"},
    "29": {"primary": "CTH", "alt": "CTSH", "rvc": 0, "description_fr": "Produits chimiques organiques - CTH ou CTSH", "description_en": "Organic chemicals - CTH or CTSH"},
    "30": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Produits pharmaceutiques - CTH ou 40% VA", "description_en": "Pharmaceuticals - CTH or 40% VA"},
    "31": {"primary": "CTH", "alt": None, "rvc": 0, "description_fr": "Engrais - CTH", "description_en": "Fertilizers - CTH"},
    "32": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Tannage, teintures - CTH ou 40% VA", "description_en": "Tanning, dyeing - CTH or 40% VA"},
    "33": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Parfums, cosmétiques - CTH ou 40% VA", "description_en": "Perfumes, cosmetics - CTH or 40% VA"},
    "34": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Savons, cires - CTH ou 40% VA", "description_en": "Soaps, waxes - CTH or 40% VA"},
    "38": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Produits chimiques divers - CTH ou 40% VA", "description_en": "Misc chemicals - CTH or 40% VA"},
    "39": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Plastiques - CTH ou 40% VA", "description_en": "Plastics - CTH or 40% VA"},
    "40": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Caoutchouc - CTH ou 40% VA", "description_en": "Rubber - CTH or 40% VA"},
    "41": {"primary": "CC", "alt": "VA40", "rvc": 40, "description_fr": "Cuirs et peaux - CC ou 40% VA", "description_en": "Hides, leather - CC or 40% VA"},
    "42": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Ouvrages en cuir - CTH ou 40% VA", "description_en": "Leather articles - CTH or 40% VA"},
    "44": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Bois - CTH ou 40% VA", "description_en": "Wood - CTH or 40% VA"},
    "48": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Papiers et cartons - CTH ou 40% VA", "description_en": "Paper and paperboard - CTH or 40% VA"},
    "50": {"primary": "CC", "alt": "SP", "rvc": 0, "description_fr": "Soie - CC ou processus spécifique", "description_en": "Silk - CC or specific process"},
    "51": {"primary": "CC", "alt": "SP", "rvc": 0, "description_fr": "Laine - CC ou processus spécifique", "description_en": "Wool - CC or specific process"},
    "52": {"primary": "CC", "alt": "SP", "rvc": 0, "description_fr": "Coton - CC ou processus spécifique", "description_en": "Cotton - CC or specific process"},
    "53": {"primary": "CC", "alt": "SP", "rvc": 0, "description_fr": "Autres fibres textiles végétales - CC", "description_en": "Other vegetable textile fibers - CC"},
    "54": {"primary": "CC", "alt": "SP", "rvc": 0, "description_fr": "Filaments synthétiques - CC ou processus spécifique", "description_en": "Man-made filaments - CC or SP"},
    "55": {"primary": "CC", "alt": "SP", "rvc": 0, "description_fr": "Fibres synthétiques discontinues - CC ou SP", "description_en": "Man-made staple fibers - CC or SP"},
    "61": {"primary": "CC", "alt": "VA40", "rvc": 40, "description_fr": "Vêtements tricotés - CC ou 40% VA", "description_en": "Knitted apparel - CC or 40% VA"},
    "62": {"primary": "CC", "alt": "VA40", "rvc": 40, "description_fr": "Vêtements non tricotés - CC ou 40% VA", "description_en": "Woven apparel - CC or 40% VA"},
    "63": {"primary": "CC", "alt": "VA40", "rvc": 40, "description_fr": "Autres textiles confectionnés - CC ou 40% VA", "description_en": "Other textile articles - CC or 40% VA"},
    "64": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Chaussures - CTH ou 40% VA", "description_en": "Footwear - CTH or 40% VA"},
    "68": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Ouvrages en pierres - CTH ou 40% VA", "description_en": "Articles of stone - CTH or 40% VA"},
    "69": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Produits céramiques - CTH ou 40% VA", "description_en": "Ceramic products - CTH or 40% VA"},
    "70": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Verre - CTH ou 40% VA", "description_en": "Glass - CTH or 40% VA"},
    "71": {"primary": "CTH", "alt": "VA30", "rvc": 30, "description_fr": "Pierres précieuses, métaux précieux - CTH ou 30% VA", "description_en": "Precious stones/metals - CTH or 30% VA"},
    "72": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Fonte, fer et acier - CTH ou 40% VA", "description_en": "Iron and steel - CTH or 40% VA"},
    "73": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Ouvrages en fer/acier - CTH ou 40% VA", "description_en": "Articles of iron/steel - CTH or 40% VA"},
    "74": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Cuivre - CTH ou 40% VA", "description_en": "Copper - CTH or 40% VA"},
    "76": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Aluminium - CTH ou 40% VA", "description_en": "Aluminium - CTH or 40% VA"},
    "84": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Machines et appareils mécaniques - CTH ou 40% VA", "description_en": "Machinery - CTH or 40% VA"},
    "85": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Machines et appareils électriques - CTH ou 40% VA", "description_en": "Electrical equipment - CTH or 40% VA"},
    "87": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Véhicules automobiles - CTH ou 40% VA", "description_en": "Vehicles - CTH or 40% VA"},
    "88": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Aéronautique - CTH ou 40% VA", "description_en": "Aircraft - CTH or 40% VA"},
    "89": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Navigation maritime - CTH ou 40% VA", "description_en": "Ships, boats - CTH or 40% VA"},
    "90": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Instruments optiques/médicaux - CTH ou 40% VA", "description_en": "Optical/medical instruments - CTH or 40% VA"},
    "94": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Meubles - CTH ou 40% VA", "description_en": "Furniture - CTH or 40% VA"},
    "95": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Jouets, jeux - CTH ou 40% VA", "description_en": "Toys, games - CTH or 40% VA"},
    "96": {"primary": "CTH", "alt": "VA40", "rvc": 40, "description_fr": "Ouvrages divers - CTH ou 40% VA", "description_en": "Misc manufactured articles - CTH or 40% VA"},
}

# Product-Specific Rules (PSR) - Selected HS6 codes
# Source: AfCFTA Annex II Appendix IV
HS6_RULES_OF_ORIGIN = {
    # Chapter 09 - Coffee, Tea
    "090111": {"primary": "WO", "alt": None, "rvc": 0, "status": "AGREED", "notes_fr": "Café non torréfié - cultivé et récolté en Afrique", "notes_en": "Coffee not roasted - grown and harvested in Africa"},
    "090121": {"primary": "CTH", "alt": "VA40", "rvc": 40, "status": "AGREED", "notes_fr": "Café torréfié - torréfaction en Afrique", "notes_en": "Roasted coffee - roasted in Africa"},
    
    # Chapter 10 - Cereals
    "100110": {"primary": "WO", "alt": None, "rvc": 0, "status": "AGREED", "notes_fr": "Blé dur - cultivé et récolté en Afrique", "notes_en": "Durum wheat - grown and harvested in Africa"},
    "100190": {"primary": "WO", "alt": None, "rvc": 0, "status": "AGREED", "notes_fr": "Autres blés - cultivés et récoltés en Afrique", "notes_en": "Other wheat - grown and harvested in Africa"},
    "100510": {"primary": "WO", "alt": None, "rvc": 0, "status": "AGREED", "notes_fr": "Maïs de semence - cultivé en Afrique", "notes_en": "Maize seed - grown in Africa"},
    "100590": {"primary": "WO", "alt": None, "rvc": 0, "status": "AGREED", "notes_fr": "Autres maïs - cultivés en Afrique", "notes_en": "Other maize - grown in Africa"},
    "100630": {"primary": "CTH", "alt": "VA40", "rvc": 40, "status": "AGREED", "notes_fr": "Riz blanchi - transformation en Afrique", "notes_en": "Milled rice - processed in Africa"},
    
    # Chapter 11 - Milling products  
    "110100": {"primary": "CTH", "alt": "VA40", "rvc": 40, "status": "AGREED", "notes_fr": "Farines de blé - moulues en Afrique", "notes_en": "Wheat flour - milled in Africa"},
    
    # Chapter 18 - Cocoa
    "180100": {"primary": "WO", "alt": None, "rvc": 0, "status": "AGREED", "notes_fr": "Fèves de cacao - cultivées en Afrique", "notes_en": "Cocoa beans - grown in Africa"},
    "180310": {"primary": "CTH", "alt": "VA40", "rvc": 40, "status": "AGREED", "notes_fr": "Pâte de cacao - transformation en Afrique", "notes_en": "Cocoa paste - processed in Africa"},
    
    # Chapter 27 - Mineral fuels
    "270900": {"primary": "WO", "alt": "CTH", "rvc": 0, "status": "AGREED", "notes_fr": "Pétrole brut - extrait en Afrique", "notes_en": "Crude petroleum - extracted in Africa"},
    
    # Chapter 71 - Precious metals
    "710812": {"primary": "WO", "alt": "CTH", "rvc": 0, "status": "AGREED", "notes_fr": "Or brut - extrait en Afrique", "notes_en": "Gold unwrought - extracted in Africa"},
    
    # Chapter 87 - Vehicles
    "870323": {"primary": "CTH", "alt": "VA40", "rvc": 40, "status": "AGREED", "notes_fr": "Voitures 1500-3000cc - assemblage ou 40% VA", "notes_en": "Cars 1500-3000cc - assembly or 40% VA"},
}


def get_chapter_rule(chapter: str, lang: str = "fr") -> dict:
    """Get default rule for a chapter"""
    chapter = chapter.zfill(2)
    if chapter in CHAPTER_RULES:
        rule = CHAPTER_RULES[chapter]
        desc_key = f"description_{lang}"
        return {
            "primary_code": rule["primary"],
            "primary_name": ORIGIN_TYPES.get(rule["primary"], {}).get(lang, rule["primary"]),
            "alt_code": rule.get("alt"),
            "alt_name": ORIGIN_TYPES.get(rule.get("alt"), {}).get(lang, "") if rule.get("alt") else None,
            "rvc": rule.get("rvc", 40),
            "description": rule.get(desc_key, "")
        }
    return None


def get_rule_of_origin(hs_code: str, lang: str = "fr") -> dict:
    """
    Get rules of origin for an HS code
    First checks PSR at HS6 level, falls back to chapter rules
    """
    hs6 = hs_code[:6] if len(hs_code) >= 6 else hs_code.ljust(6, '0')
    chapter = hs_code[:2].zfill(2)
    
    # Check PSR first
    if hs6 in HS6_RULES_OF_ORIGIN:
        psr = HS6_RULES_OF_ORIGIN[hs6]
        primary_type = psr["primary"]
        alt_type = psr.get("alt")
        notes_key = f"notes_{lang}"
        
        return {
            "hs6_code": hs6,
            "chapter": chapter,
            "chapter_description": CHAPTER_RULES.get(chapter, {}).get(f"description_{lang}", ""),
            "status": psr.get("status", "AGREED"),
            "primary_rule": {
                "code": primary_type,
                "type": primary_type,
                "name": ORIGIN_TYPES.get(primary_type, {}).get(lang, primary_type),
                "description": ORIGIN_TYPES.get(primary_type, {}).get(lang, "")
            },
            "alternative_rule": {
                "code": alt_type,
                "type": alt_type,
                "name": ORIGIN_TYPES.get(alt_type, {}).get(lang, alt_type) if alt_type else None,
                "description": ORIGIN_TYPES.get(alt_type, {}).get(lang, "") if alt_type else None
            } if alt_type else None,
            "regional_content": psr.get("rvc", 40) if psr.get("rvc", 0) > 0 else 40,
            "notes": psr.get(notes_key, ""),
            "source": "PSR",
            "source_detail": "AfCFTA Annex II Appendix IV - Product Specific Rules"
        }
    
    # Fall back to chapter rules
    chapter_rule = get_chapter_rule(chapter, lang)
    if chapter_rule:
        return {
            "hs6_code": hs6,
            "chapter": chapter,
            "chapter_description": chapter_rule.get("description", ""),
            "status": "AGREED",
            "primary_rule": {
                "code": chapter_rule["primary_code"],
                "type": chapter_rule["primary_code"],
                "name": chapter_rule["primary_name"],
                "description": chapter_rule["primary_name"]
            },
            "alternative_rule": {
                "code": chapter_rule["alt_code"],
                "type": chapter_rule["alt_code"],
                "name": chapter_rule["alt_name"],
                "description": chapter_rule["alt_name"]
            } if chapter_rule.get("alt_code") else None,
            "regional_content": chapter_rule.get("rvc", 40),
            "notes": "",
            "source": "CHAPTER",
            "source_detail": "AfCFTA Annex II - Chapter-level default rules"
        }
    
    return {
        "hs6_code": hs6,
        "chapter": chapter,
        "status": "UNKNOWN",
        "notes": "Règles d'origine non définies" if lang == "fr" else "Rules of origin not defined"
    }
