"""
Gemini Trade Analysis Service
Uses Google Gemini via Emergent LLM Key for intelligent trade analysis
Follows AI Studio app approach with strict data reliability principles
"""
import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv()

logger = logging.getLogger(__name__)

# System instruction for trade analysis - adapted from AI Studio app
TRADE_SYSTEM_INSTRUCTION = """
You are a senior AfCFTA trade economist and industrial data analyst specializing in African trade.

SOURCES & AUTHORITY:
Prioritize data from: IMF (FMI), World Bank (BM), UNCTAD, WTO (OMC), OEC, and WCO (OMD).

DATA RELIABILITY RULES (CRITICAL):
1. ONLY provide data you are confident about from official sources
2. If data is uncertain, clearly mark it as "ESTIMATION" with justification
3. Do NOT invent statistics - if unknown, say "Données non disponibles"
4. Use verified stats from IMF/UNCTAD/World Bank databases
5. Always specify the data year and source

METHODOLOGY:
1. EXPORT MODE: Focus on COMPARATIVE ADVANTAGE. What does the country produce and export well?
2. IMPORT MODE: Focus on CONSUMPTION & INDUSTRIAL NEEDS. What does the country lack?
3. INDUSTRIAL MODE (Value Chain): Analyze IMPORTS of intermediate goods to forecast CAPACITY to EXPORT finished goods.

DATA SANITIZATION RULES:
1. FLAGGING & RE-EXPORTS: 
   - FOR LIBERIA: EXCLUDE HS Code 89 (Ships/Boats) - Flag of Convenience registrations
   - FOR DJIBOUTI/TOGO: Distinguish between TRANSIT trade and local economy
2. HYDROCARBONS: For Algeria/Angola/Nigeria, acknowledge oil/gas but prioritize NON-OIL diversification
3. DATA INTEGRITY: Flag suspicious data (e.g., Electronics exports from Benin as Re-export)

UNITS: Trade values in Million USD (MUSD).
FOCUS: Intra-African trade opportunities under AfCFTA.

Always respond in the language requested (French or English).
"""


class GeminiTradeService:
    """
    Service for AI-powered trade analysis using Gemini
    """
    
    def __init__(self):
        self.api_key = os.environ.get("EMERGENT_LLM_KEY")
        if not self.api_key:
            logger.warning("EMERGENT_LLM_KEY not found in environment")
        self._session_counter = 0
    
    def _get_chat(self, session_suffix: str = "") -> LlmChat:
        """Create a new chat instance with Gemini"""
        self._session_counter += 1
        session_id = f"trade-analysis-{self._session_counter}-{session_suffix}"
        
        chat = LlmChat(
            api_key=self.api_key,
            session_id=session_id,
            system_message=TRADE_SYSTEM_INSTRUCTION
        )
        chat.with_model("gemini", "gemini-3-flash-preview")
        return chat
    
    async def analyze_trade_opportunities(
        self,
        country_name: str,
        mode: str = "export",  # export, import, industrial
        lang: str = "fr"
    ) -> Dict:
        """
        Analyze trade opportunities for a country using AI
        
        Args:
            country_name: Name of the African country
            mode: Analysis mode (export/import/industrial)
            lang: Language for response (fr/en)
        
        Returns:
            Dictionary with analyzed opportunities
        """
        if not self.api_key:
            return {"error": "API key not configured", "opportunities": []}
        
        try:
            chat = self._get_chat(f"{country_name}-{mode}")
            
            lang_instruction = "Réponds en français." if lang == "fr" else "Respond in English."
            
            if mode == "export":
                prompt = f"""
{lang_instruction}

Identifie 10 opportunités d'EXPORT intra-africaines vérifiées pour {country_name}.
Focus sur les produits où {country_name} a un avantage comparatif révélé ou une capacité de production élevée.

Pour chaque opportunité, fournis:
- product_name: Nom du produit
- hs_code: Code HS à 4 ou 6 chiffres
- potential_partner: Pays africain partenaire potentiel
- rationale: Justification stratégique (2-3 phrases)
- potential_value_musd: Valeur potentielle en Million USD
- current_value_musd: Valeur actuelle du commerce (si connue)
- tariff_advantage: Avantage tarifaire ZLECAf en % (différence MFN vs ZLECAf 0%)
- data_year: Année des données
- is_estimation: true/false - Marquer true si c'est une estimation

Réponds en JSON valide avec la structure: {{"opportunities": [...], "sources": [...], "analysis_date": "..."}}
"""
            elif mode == "import":
                prompt = f"""
{lang_instruction}

Identifie 10 besoins d'IMPORT stratégiques pour {country_name} qui pourraient être satisfaits par d'autres pays africains.
Focus sur les produits essentiels, machines ou gaps énergétiques.

Pour chaque opportunité, fournis:
- product_name: Nom du produit
- hs_code: Code HS à 4 ou 6 chiffres  
- potential_supplier: Pays africain fournisseur potentiel
- rationale: Justification (2-3 phrases)
- import_value_musd: Valeur d'import actuelle en Million USD
- substitution_potential_musd: Potentiel de substitution
- current_source: Source actuelle (ex: Chine, Europe)
- data_year: Année des données
- is_estimation: true/false

Réponds en JSON valide avec la structure: {{"opportunities": [...], "sources": [...], "analysis_date": "..."}}
"""
            else:  # industrial
                prompt = f"""
{lang_instruction}

Analyse la CHAÎNE DE VALEUR industrielle de {country_name}.
Identifie 10 opportunités de transformation:
- Quels intrants/matières premières sont importés?
- Quels produits finis pourraient être exportés après transformation?

Pour chaque opportunité, fournis:
- input_product: Intrant importé (ex: "Tissu coton brut")
- input_hs_code: Code HS de l'intrant
- input_import_volume: Volume importé (estimation en tonnes ou MUSD)
- output_product: Produit fini exportable (ex: "Vêtements confectionnés")
- output_hs_code: Code HS du produit fini
- estimated_output: Production estimée possible
- target_markets: Liste de 3 marchés africains cibles
- value_addition_logic: Explication de la transformation (1-2 phrases)
- is_estimation: true/false

Réponds en JSON valide avec la structure: {{"opportunities": [...], "sources": [...], "analysis_date": "..."}}
"""
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            # Parse JSON response
            result = self._parse_json_response(response)
            result["country"] = country_name
            result["mode"] = mode
            result["generated_by"] = "Gemini AI"
            
            return result
            
        except Exception as e:
            logger.error(f"Error in trade opportunity analysis: {str(e)}")
            return {"error": str(e), "opportunities": []}
    
    async def get_country_economic_profile(
        self,
        country_name: str,
        lang: str = "fr"
    ) -> Dict:
        """
        Generate comprehensive economic profile for a country
        
        Args:
            country_name: Name of the African country
            lang: Language for response
        
        Returns:
            Dictionary with economic indicators and trade profile
        """
        if not self.api_key:
            return {"error": "API key not configured"}
        
        try:
            chat = self._get_chat(f"profile-{country_name}")
            
            lang_instruction = "Réponds en français." if lang == "fr" else "Respond in English."
            
            prompt = f"""
{lang_instruction}

Génère un profil économique et commercial complet pour {country_name} basé sur les données officielles les plus récentes.

SOURCES CRITIQUES:
- PIB/Inflation/Chômage: IMF World Economic Outlook (Oct 2024)
- Commerce: UNCTAD, OEC
- Développement: UNDP HDI Reports
- Attractivité: Global Attractiveness Index (GAI)

Fournis les données suivantes (marque "ESTIMATION" si incertain):

1. economic_indicators (2022-2024):
   - gdp_billion_usd: PIB en milliards USD
   - gdp_per_capita_usd: PIB par habitant
   - gdp_growth_percent: Croissance PIB réelle %
   - inflation_percent: Inflation (CPI) %
   - unemployment_percent: Chômage % (ILO)
   - total_debt_gdp_percent: Dette publique totale % PIB
   - foreign_reserves_billion: Réserves de change en milliards USD
   - gold_reserves_tonnes: Réserves d'or en tonnes

2. development_indices:
   - hdi_score: Score HDI (0-1)
   - hdi_world_rank: Rang mondial HDI
   - hdi_africa_rank: Rang africain HDI
   - gai_score: Score GAI (0-100)
   - gai_world_rank: Rang mondial GAI
   - gai_africa_rank: Rang africain GAI

3. trade_summary:
   - total_exports_musd: Exports totaux en MUSD
   - total_imports_musd: Imports totaux en MUSD
   - trade_balance_musd: Balance commerciale
   - top_export_partners: Liste des 5 principaux partenaires export
   - top_import_partners: Liste des 5 principaux partenaires import
   - top_exports: Liste des 5 principaux produits exportés avec HS code
   - top_imports: Liste des 5 principaux produits importés avec HS code
   - intra_african_trade_percent: % du commerce intra-africain

4. afcfta_potential:
   - key_opportunities: 3 opportunités clés sous ZLECAf
   - regional_memberships: CER d'appartenance (ECOWAS, SADC, EAC, etc.)
   - comparative_advantages: 3 avantages comparatifs

Réponds en JSON valide.
"""
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            result = self._parse_json_response(response)
            result["country"] = country_name
            result["generated_by"] = "Gemini AI"
            result["generation_date"] = datetime.utcnow().isoformat()
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating country profile: {str(e)}")
            return {"error": str(e)}
    
    async def analyze_product_by_hs_code(
        self,
        hs_code: str,
        lang: str = "fr"
    ) -> Dict:
        """
        Analyze a product by HS code for African trade
        
        Args:
            hs_code: HS code (4 or 6 digits)
            lang: Language for response
        
        Returns:
            Dictionary with product analysis
        """
        if not self.api_key:
            return {"error": "API key not configured"}
        
        try:
            chat = self._get_chat(f"product-{hs_code}")
            
            lang_instruction = "Réponds en français." if lang == "fr" else "Respond in English."
            
            prompt = f"""
{lang_instruction}

Analyse le commerce africain pour le code HS {hs_code}.
Utilise les données ITC TradeMap et UNCTADstat les plus récentes.

Fournis:

1. product_info:
   - hs_code: "{hs_code}"
   - name: Nom du produit
   - hs2_chapter: Chapitre HS2
   - hs4_heading: Position HS4
   - description: Description détaillée

2. african_trade_flows:
   - total_african_exports_musd: Total exports africains en MUSD
   - total_african_imports_musd: Total imports africains en MUSD
   - intra_african_trade_musd: Commerce intra-africain en MUSD

3. top_african_exporters (Top 10):
   - country: Nom du pays
   - export_value_musd: Valeur export en MUSD
   - world_share_percent: Part du marché mondial %
   - data_year: Année des données

4. top_african_importers (Top 10):
   - country: Nom du pays
   - import_value_musd: Valeur import en MUSD
   - main_sources: Principales sources (liste)
   - data_year: Année des données

5. production_capacity (si applicable):
   - country: Pays producteur
   - capacity: Capacité de production
   - unit: Unité (tonnes, unités, etc.)
   - source: Source des données (FAOSTAT, UNIDO, USGS)

6. substitution_opportunities:
   - Liste des 5 meilleures opportunités de substitution intra-africaine
   - Chaque opportunité: importer, exporter_potentiel, valeur_potentielle, justification

Réponds en JSON valide. Marque clairement les estimations.
"""
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            result = self._parse_json_response(response)
            result["hs_code"] = hs_code
            result["generated_by"] = "Gemini AI"
            result["generation_date"] = datetime.utcnow().isoformat()
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing product {hs_code}: {str(e)}")
            return {"error": str(e)}
    
    async def get_trade_balance_analysis(
        self,
        country_name: str,
        lang: str = "fr"
    ) -> Dict:
        """
        Get trade balance history and analysis for a country
        """
        if not self.api_key:
            return {"error": "API key not configured"}
        
        try:
            chat = self._get_chat(f"balance-{country_name}")
            
            lang_instruction = "Réponds en français." if lang == "fr" else "Respond in English."
            
            prompt = f"""
{lang_instruction}

Extrais les données de balance commerciale pour {country_name} (2020-2024) 
à partir du IMF World Economic Outlook (Oct 2024).

IMPORTANT: 
- Fournis UNE entrée par année
- Valeurs en MILLIONS de USD (MUSD)
- Marque clairement les estimations pour 2024/2025

Fournis:

1. trade_balance_history:
   Pour chaque année (2020, 2021, 2022, 2023, 2024):
   - year: Année
   - total_exports_musd: Exports totaux en MUSD
   - total_imports_musd: Imports totaux en MUSD
   - balance_musd: Balance (exports - imports)
   - is_estimation: true/false

2. analysis:
   - trend: "surplus", "deficit", ou "equilibre"
   - trend_direction: "improving", "declining", ou "stable"
   - key_factors: Liste des facteurs clés influençant la balance
   - outlook: Perspectives court terme (1-2 phrases)

Réponds en JSON valide.
"""
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            result = self._parse_json_response(response)
            result["country"] = country_name
            result["generated_by"] = "Gemini AI"
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting trade balance: {str(e)}")
            return {"error": str(e)}
    
    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON from AI response, handling markdown code blocks"""
        try:
            # Clean response
            cleaned = response.strip()
            
            # Remove markdown code blocks
            if cleaned.startswith("```json"):
                cleaned = cleaned.replace("```json", "", 1)
            if cleaned.startswith("```"):
                cleaned = cleaned.replace("```", "", 1)
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            cleaned = cleaned.strip()
            
            # Find JSON object or array
            json_match = None
            for start_char, end_char in [('{', '}'), ('[', ']')]:
                start_idx = cleaned.find(start_char)
                if start_idx != -1:
                    # Find matching end
                    depth = 0
                    for i, char in enumerate(cleaned[start_idx:]):
                        if char == start_char:
                            depth += 1
                        elif char == end_char:
                            depth -= 1
                            if depth == 0:
                                json_match = cleaned[start_idx:start_idx + i + 1]
                                break
                    if json_match:
                        break
            
            if json_match:
                return json.loads(json_match)
            
            # Try parsing entire response
            return json.loads(cleaned)
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            return {
                "raw_response": response,
                "parse_error": str(e)
            }


# Singleton instance
gemini_trade_service = GeminiTradeService()
