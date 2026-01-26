"""
RÈGLES D'ORIGINE ZLECAf (AfCFTA) - Annexe 2, Appendice IV
=========================================================
Basé sur:
- AfCFTA Rules of Origin Manual (AU, 2022)
- WCO Practical Guide for AfCFTA RoO Implementation
- AfCFTA Annex II Protocol on Trade in Goods

Sources officielles:
- https://au.int/sites/default/files/treaties/36437-ax-AfCFTA_RULES_OF_ORIGIN_MANUAL.pdf
- https://www.wcoomd.org/-/media/wco/public/global/pdf/topics/origin/instruments-and-tools/afcfta/

Méthodologies d'origine ZLECAf:
1. WHOLLY_OBTAINED - Entièrement obtenu dans la zone
2. CHANGE_TARIFF_HEADING (CTH) - Changement de position tarifaire
3. CHANGE_TARIFF_SUBHEADING (CTSH) - Changement de sous-position
4. VALUE_ADDED - Valeur ajoutée minimum (%)
5. SPECIFIC_PROCESS - Processus de fabrication spécifique

Statut des négociations (2024):
- 81% des règles d'origine convenues
- Secteurs en cours: textiles, vêtements, véhicules, certains produits agricoles
"""

# Types de règles d'origine
ORIGIN_TYPES = {
    "wholly_obtained": {
        "code": "WO",
        "name_fr": "Entièrement obtenu",
        "name_en": "Wholly Obtained",
        "description_fr": "Produit entièrement obtenu ou produit dans un État membre de la ZLECAf",
        "description_en": "Product wholly obtained or produced in an AfCFTA Member State"
    },
    "change_tariff_heading": {
        "code": "CTH",
        "name_fr": "Changement de position tarifaire",
        "name_en": "Change in Tariff Heading",
        "description_fr": "Transformation entraînant un changement de position tarifaire (4 chiffres)",
        "description_en": "Processing resulting in a change of tariff heading (4 digits)"
    },
    "change_tariff_subheading": {
        "code": "CTSH",
        "name_fr": "Changement de sous-position tarifaire",
        "name_en": "Change in Tariff Subheading",
        "description_fr": "Transformation entraînant un changement de sous-position (6 chiffres)",
        "description_en": "Processing resulting in a change of tariff subheading (6 digits)"
    },
    "value_added": {
        "code": "VA",
        "name_fr": "Valeur ajoutée",
        "name_en": "Value Added",
        "description_fr": "Pourcentage minimum de valeur ajoutée localement",
        "description_en": "Minimum percentage of locally added value"
    },
    "specific_process": {
        "code": "SP",
        "name_fr": "Processus spécifique",
        "name_en": "Specific Process",
        "description_fr": "Opérations de transformation spécifiques requises",
        "description_en": "Specific manufacturing operations required"
    }
}

# Règles d'origine par chapitre HS (basé sur AfCFTA Annex II Appendix IV)
# Statut: AGREED = convenu, PENDING = en négociation
CHAPTER_RULES = {
    # Section I - Animaux vivants et produits du règne animal
    "01": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Animaux vivants - doivent être nés et élevés dans la ZLECAf",
        "description_en": "Live animals - must be born and raised in AfCFTA"
    },
    "02": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Viandes - animaux nés et élevés, abattus dans la ZLECAf",
        "description_en": "Meat - animals born, raised and slaughtered in AfCFTA"
    },
    "03": {
        "status": "PENDING",
        "primary_rule": "wholly_obtained",
        "alternative_rule": "specific_process",
        "regional_content": 100,
        "description_fr": "Poissons - critères spécifiques pour navires/usines flottantes en négociation",
        "description_en": "Fish - specific criteria for vessels/factory ships under negotiation",
        "notes": "Vessel ownership and crew nationality criteria pending"
    },
    "04": {
        "status": "PENDING",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Produits laitiers - certains produits (babeurre, fromages) en négociation",
        "description_en": "Dairy products - some products (buttermilk, cheese) under negotiation"
    },
    "05": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Autres produits d'origine animale",
        "description_en": "Other products of animal origin"
    },
    
    # Section II - Produits du règne végétal
    "06": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Plantes vivantes - cultivées dans la ZLECAf",
        "description_en": "Live plants - grown in AfCFTA"
    },
    "07": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Légumes - récoltés dans la ZLECAf",
        "description_en": "Vegetables - harvested in AfCFTA"
    },
    "08": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Fruits - récoltés dans la ZLECAf",
        "description_en": "Fruits - harvested in AfCFTA"
    },
    "09": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Café, thé, épices - récoltés dans la ZLECAf",
        "description_en": "Coffee, tea, spices - harvested in AfCFTA"
    },
    "10": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Céréales - récoltées dans la ZLECAf",
        "description_en": "Cereals - harvested in AfCFTA"
    },
    "11": {
        "status": "PENDING",
        "primary_rule": "change_tariff_heading",
        "alternative_rule": "value_added",
        "regional_content": 40,
        "description_fr": "Produits de la minoterie - farine de blé en négociation",
        "description_en": "Milling products - wheat flour under negotiation"
    },
    "12": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Graines et fruits oléagineux",
        "description_en": "Oil seeds and oleaginous fruits"
    },
    "13": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Gommes, résines et autres sucs végétaux",
        "description_en": "Lac, gums, resins and other vegetable saps"
    },
    "14": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Matières à tresser et autres produits végétaux",
        "description_en": "Vegetable plaiting materials"
    },
    
    # Section III - Graisses et huiles
    "15": {
        "status": "PENDING",
        "primary_rule": "change_tariff_heading",
        "alternative_rule": "value_added",
        "regional_content": 40,
        "description_fr": "Graisses et huiles - huile de tournesol et autres en négociation",
        "description_en": "Fats and oils - sunflower oil and others under negotiation"
    },
    
    # Section IV - Produits alimentaires préparés
    "16": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Préparations de viandes et poissons",
        "description_en": "Preparations of meat or fish"
    },
    "17": {
        "status": "PENDING",
        "primary_rule": "change_tariff_heading",
        "alternative_rule": "value_added",
        "regional_content": 40,
        "description_fr": "Sucres - en négociation",
        "description_en": "Sugars - under negotiation"
    },
    "18": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Cacao et préparations",
        "description_en": "Cocoa and cocoa preparations"
    },
    "19": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Préparations à base de céréales",
        "description_en": "Preparations of cereals, flour, starch"
    },
    "20": {
        "status": "PENDING",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Préparations de légumes/fruits - certains jus en négociation",
        "description_en": "Preparations of vegetables/fruits - some juices under negotiation"
    },
    "21": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Préparations alimentaires diverses",
        "description_en": "Miscellaneous edible preparations"
    },
    "22": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Boissons, liquides alcooliques",
        "description_en": "Beverages, spirits and vinegar"
    },
    "23": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Résidus des industries alimentaires",
        "description_en": "Residues from food industries"
    },
    "24": {
        "status": "PENDING",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Tabac - certains produits en négociation",
        "description_en": "Tobacco - some products under negotiation"
    },
    
    # Section V - Produits minéraux
    "25": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Sel, soufre, terres et pierres",
        "description_en": "Salt, sulphur, earths and stone"
    },
    "26": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Minerais, scories et cendres",
        "description_en": "Ores, slag and ash"
    },
    "27": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "alternative_rule": "change_tariff_heading",
        "regional_content": 50,
        "description_fr": "Combustibles minéraux, huiles",
        "description_en": "Mineral fuels, oils"
    },
    
    # Section VI - Produits chimiques
    "28": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Produits chimiques inorganiques",
        "description_en": "Inorganic chemicals"
    },
    "29": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Produits chimiques organiques",
        "description_en": "Organic chemicals"
    },
    "30": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Produits pharmaceutiques",
        "description_en": "Pharmaceutical products"
    },
    "31": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Engrais",
        "description_en": "Fertilisers"
    },
    "32": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Extraits tannants, colorants, peintures",
        "description_en": "Tanning extracts, dyes, paints"
    },
    "33": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Huiles essentielles, parfumerie, cosmétiques",
        "description_en": "Essential oils, perfumery, cosmetics"
    },
    "34": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Savons, cires, bougies",
        "description_en": "Soap, waxes, candles"
    },
    "35": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Matières albuminoïdes, colles",
        "description_en": "Albuminoidal substances, glues"
    },
    "36": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Explosifs, allumettes",
        "description_en": "Explosives, matches"
    },
    "37": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Produits photographiques",
        "description_en": "Photographic goods"
    },
    "38": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Produits chimiques divers",
        "description_en": "Miscellaneous chemical products"
    },
    
    # Section VII - Plastiques et caoutchouc
    "39": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Matières plastiques et ouvrages",
        "description_en": "Plastics and articles thereof"
    },
    "40": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Caoutchouc et ouvrages",
        "description_en": "Rubber and articles thereof"
    },
    
    # Section VIII - Cuirs et peaux
    "41": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Peaux et cuirs",
        "description_en": "Raw hides and skins, leather"
    },
    "42": {
        "status": "PENDING",
        "primary_rule": "change_tariff_heading",
        "alternative_rule": "value_added",
        "regional_content": 45,
        "description_fr": "Ouvrages en cuir - articles de voyage en négociation",
        "description_en": "Articles of leather - travel goods under negotiation"
    },
    "43": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Pelleteries et fourrures",
        "description_en": "Furskins and artificial fur"
    },
    
    # Section IX - Bois et ouvrages
    "44": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Bois et ouvrages en bois",
        "description_en": "Wood and articles of wood"
    },
    "45": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Liège et ouvrages",
        "description_en": "Cork and articles of cork"
    },
    "46": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Ouvrages de sparterie ou vannerie",
        "description_en": "Manufactures of straw, basketware"
    },
    
    # Section X - Pâtes de bois, papier
    "47": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Pâtes de bois ou autres matières",
        "description_en": "Pulp of wood or other cellulosic"
    },
    "48": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Papiers et cartons",
        "description_en": "Paper and paperboard"
    },
    "49": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Produits de l'édition, presse",
        "description_en": "Printed books, newspapers"
    },
    
    # Section XI - Textiles et vêtements (secteur sensible - majorité en négociation)
    "50": {
        "status": "PENDING",
        "primary_rule": "specific_process",
        "alternative_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Soie - règles spécifiques en négociation",
        "description_en": "Silk - specific rules under negotiation"
    },
    "51": {
        "status": "PENDING",
        "primary_rule": "specific_process",
        "regional_content": 40,
        "description_fr": "Laine et poils fins",
        "description_en": "Wool, fine or coarse animal hair"
    },
    "52": {
        "status": "PENDING",
        "primary_rule": "specific_process",
        "regional_content": 40,
        "description_fr": "Coton - filage, tissage requis dans ZLECAf",
        "description_en": "Cotton - spinning, weaving required in AfCFTA"
    },
    "53": {
        "status": "PENDING",
        "primary_rule": "specific_process",
        "regional_content": 40,
        "description_fr": "Autres fibres textiles végétales",
        "description_en": "Other vegetable textile fibres"
    },
    "54": {
        "status": "PENDING",
        "primary_rule": "specific_process",
        "regional_content": 40,
        "description_fr": "Filaments synthétiques ou artificiels",
        "description_en": "Man-made filaments"
    },
    "55": {
        "status": "PENDING",
        "primary_rule": "specific_process",
        "regional_content": 40,
        "description_fr": "Fibres synthétiques discontinues",
        "description_en": "Man-made staple fibres"
    },
    "56": {
        "status": "PENDING",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Ouates, feutres, cordages",
        "description_en": "Wadding, felt and nonwovens"
    },
    "57": {
        "status": "PENDING",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Tapis et autres revêtements de sol",
        "description_en": "Carpets and other floor coverings"
    },
    "58": {
        "status": "PENDING",
        "primary_rule": "specific_process",
        "regional_content": 40,
        "description_fr": "Tissus spéciaux - en négociation",
        "description_en": "Special woven fabrics - under negotiation"
    },
    "59": {
        "status": "PENDING",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Tissus imprégnés, enduits",
        "description_en": "Impregnated, coated or laminated textile"
    },
    "60": {
        "status": "PENDING",
        "primary_rule": "specific_process",
        "regional_content": 40,
        "description_fr": "Étoffes de bonneterie",
        "description_en": "Knitted or crocheted fabrics"
    },
    "61": {
        "status": "PENDING",
        "primary_rule": "specific_process",
        "alternative_rule": "value_added",
        "regional_content": 45,
        "description_fr": "Vêtements en bonneterie - règles spécifiques en négociation",
        "description_en": "Articles of apparel, knitted - specific rules under negotiation",
        "notes": "Single transformation vs double transformation debate"
    },
    "62": {
        "status": "PENDING",
        "primary_rule": "specific_process",
        "alternative_rule": "value_added",
        "regional_content": 45,
        "description_fr": "Vêtements tissés - règles spécifiques en négociation",
        "description_en": "Articles of apparel, woven - specific rules under negotiation",
        "notes": "Single transformation vs double transformation debate"
    },
    "63": {
        "status": "PENDING",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Autres articles textiles confectionnés - textiles ménagers en négociation",
        "description_en": "Other made up textile articles - household textiles under negotiation"
    },
    
    # Section XII - Chaussures, coiffures
    "64": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Chaussures, guêtres",
        "description_en": "Footwear, gaiters"
    },
    "65": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Coiffures et parties",
        "description_en": "Headgear and parts"
    },
    "66": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Parapluies, cannes",
        "description_en": "Umbrellas, walking-sticks"
    },
    "67": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Plumes et duvets apprêtés",
        "description_en": "Prepared feathers and down"
    },
    
    # Section XIII - Ouvrages en pierre, céramique, verre
    "68": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Ouvrages en pierres, plâtre, ciment",
        "description_en": "Articles of stone, plaster, cement"
    },
    "69": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Produits céramiques",
        "description_en": "Ceramic products"
    },
    "70": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Verre et ouvrages en verre",
        "description_en": "Glass and glassware"
    },
    
    # Section XIV - Perles, pierres précieuses, métaux précieux
    "71": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "alternative_rule": "change_tariff_heading",
        "regional_content": 50,
        "description_fr": "Perles, pierres précieuses, métaux précieux",
        "description_en": "Pearls, precious stones, precious metals"
    },
    
    # Section XV - Métaux communs
    "72": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Fonte, fer et acier",
        "description_en": "Iron and steel"
    },
    "73": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Ouvrages en fonte, fer ou acier",
        "description_en": "Articles of iron or steel"
    },
    "74": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Cuivre et ouvrages",
        "description_en": "Copper and articles thereof"
    },
    "75": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Nickel et ouvrages",
        "description_en": "Nickel and articles thereof"
    },
    "76": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Aluminium et ouvrages",
        "description_en": "Aluminium and articles thereof"
    },
    "78": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Plomb et ouvrages",
        "description_en": "Lead and articles thereof"
    },
    "79": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Zinc et ouvrages",
        "description_en": "Zinc and articles thereof"
    },
    "80": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Étain et ouvrages",
        "description_en": "Tin and articles thereof"
    },
    "81": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Autres métaux communs",
        "description_en": "Other base metals"
    },
    "82": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Outils et articles de coutellerie",
        "description_en": "Tools, cutlery of base metal"
    },
    "83": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Ouvrages divers en métaux communs",
        "description_en": "Miscellaneous articles of base metal"
    },
    
    # Section XVI - Machines et appareils
    "84": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "alternative_rule": "value_added",
        "regional_content": 40,
        "description_fr": "Machines, appareils mécaniques",
        "description_en": "Nuclear reactors, boilers, machinery"
    },
    "85": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "alternative_rule": "value_added",
        "regional_content": 40,
        "description_fr": "Machines et appareils électriques",
        "description_en": "Electrical machinery and equipment"
    },
    
    # Section XVII - Matériel de transport
    "86": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Véhicules et matériel ferroviaires",
        "description_en": "Railway or tramway locomotives"
    },
    "87": {
        "status": "PENDING",
        "primary_rule": "value_added",
        "alternative_rule": "specific_process",
        "regional_content": 45,
        "description_fr": "Véhicules automobiles et pièces - en négociation",
        "description_en": "Motor vehicles and parts - under negotiation",
        "notes": "Automotive sector rules highly contentious, value-added threshold debated"
    },
    "88": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Navigation aérienne ou spatiale",
        "description_en": "Aircraft, spacecraft"
    },
    "89": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Navigation maritime ou fluviale",
        "description_en": "Ships, boats"
    },
    
    # Section XVIII - Instruments et appareils
    "90": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Instruments optiques, médicaux",
        "description_en": "Optical, medical instruments"
    },
    "91": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Horlogerie",
        "description_en": "Clocks and watches"
    },
    "92": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Instruments de musique",
        "description_en": "Musical instruments"
    },
    
    # Section XIX - Armes et munitions
    "93": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Armes et munitions",
        "description_en": "Arms and ammunition"
    },
    
    # Section XX - Marchandises et produits divers
    "94": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Meubles, literie, éclairage",
        "description_en": "Furniture, bedding, lighting"
    },
    "95": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Jouets, jeux, articles de sport",
        "description_en": "Toys, games, sports equipment"
    },
    "96": {
        "status": "AGREED",
        "primary_rule": "change_tariff_heading",
        "regional_content": 40,
        "description_fr": "Ouvrages divers",
        "description_en": "Miscellaneous manufactured articles"
    },
    
    # Section XXI - Objets d'art
    "97": {
        "status": "AGREED",
        "primary_rule": "wholly_obtained",
        "regional_content": 100,
        "description_fr": "Objets d'art, de collection, antiquités",
        "description_en": "Works of art, collectors' pieces, antiques"
    },
}


def get_rule_of_origin(hs6_code: str, language: str = "fr") -> dict:
    """
    Retourne la règle d'origine pour un code HS6 donné.
    
    Args:
        hs6_code: Code HS6 (6 chiffres)
        language: 'fr' ou 'en'
    
    Returns:
        Dictionnaire avec les détails de la règle d'origine
    """
    chapter = hs6_code[:2]
    rule = CHAPTER_RULES.get(chapter, {})
    
    if not rule:
        return {
            "hs6_code": hs6_code,
            "chapter": chapter,
            "status": "UNKNOWN",
            "message_fr": "Règle non définie pour ce chapitre",
            "message_en": "Rule not defined for this chapter"
        }
    
    primary_type = ORIGIN_TYPES.get(rule.get("primary_rule", ""), {})
    alt_type = ORIGIN_TYPES.get(rule.get("alternative_rule", ""), {})
    
    desc_key = f"description_{language}"
    name_key = f"name_{language}"
    
    result = {
        "hs6_code": hs6_code,
        "chapter": chapter,
        "status": rule.get("status", "UNKNOWN"),
        "primary_rule": {
            "type": rule.get("primary_rule", ""),
            "code": primary_type.get("code", ""),
            "name": primary_type.get(name_key, ""),
            "description": primary_type.get(desc_key, "")
        },
        "regional_content": rule.get("regional_content", 0),
        "chapter_description": rule.get(desc_key, ""),
        "notes": rule.get("notes", "")
    }
    
    if alt_type:
        result["alternative_rule"] = {
            "type": rule.get("alternative_rule", ""),
            "code": alt_type.get("code", ""),
            "name": alt_type.get(name_key, ""),
            "description": alt_type.get(desc_key, "")
        }
    
    return result


def get_chapter_status_summary() -> dict:
    """Retourne un résumé du statut des négociations par chapitre."""
    agreed = sum(1 for r in CHAPTER_RULES.values() if r.get("status") == "AGREED")
    pending = sum(1 for r in CHAPTER_RULES.values() if r.get("status") == "PENDING")
    total = len(CHAPTER_RULES)
    
    return {
        "total_chapters": total,
        "agreed": agreed,
        "pending": pending,
        "agreed_percentage": round(agreed / total * 100, 1) if total > 0 else 0,
        "pending_chapters": [ch for ch, r in CHAPTER_RULES.items() if r.get("status") == "PENDING"]
    }
