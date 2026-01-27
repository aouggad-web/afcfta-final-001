import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Badge } from '../ui/badge';
import { Separator } from '../ui/separator';
import { Progress } from '../ui/progress';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../ui/table';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { toast } from '../../hooks/use-toast';
import { HSCodeSearch, HSCodeBrowser } from '../HSCodeSelector';
import SmartHSSearch from '../SmartHSSearch';
import { Package, ChevronDown, ChevronUp, Sparkles, AlertTriangle, Info } from 'lucide-react';
import './calculator.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Drapeaux par code ISO2
const countryFlagsISO2 = {
  'DZ': '🇩🇿', 'AO': '🇦🇴', 'BJ': '🇧🇯', 'BW': '🇧🇼', 'BF': '🇧🇫', 'BI': '🇧🇮', 'CM': '🇨🇲', 'CV': '🇨🇻',
  'CF': '🇨🇫', 'TD': '🇹🇩', 'KM': '🇰🇲', 'CG': '🇨🇬', 'CD': '🇨🇩', 'CI': '🇨🇮', 'DJ': '🇩🇯', 'EG': '🇪🇬',
  'GQ': '🇬🇶', 'ER': '🇪🇷', 'SZ': '🇸🇿', 'ET': '🇪🇹', 'GA': '🇬🇦', 'GM': '🇬🇲', 'GH': '🇬🇭', 'GN': '🇬🇳',
  'GW': '🇬🇼', 'KE': '🇰🇪', 'LS': '🇱🇸', 'LR': '🇱🇷', 'LY': '🇱🇾', 'MG': '🇲🇬', 'MW': '🇲🇼', 'ML': '🇲🇱',
  'MR': '🇲🇷', 'MU': '🇲🇺', 'MA': '🇲🇦', 'MZ': '🇲🇿', 'NA': '🇳🇦', 'NE': '🇳🇪', 'NG': '🇳🇬', 'RW': '🇷🇼',
  'ST': '🇸🇹', 'SN': '🇸🇳', 'SC': '🇸🇨', 'SL': '🇸🇱', 'SO': '🇸🇴', 'ZA': '🇿🇦', 'SS': '🇸🇸', 'SD': '🇸🇩',
  'TZ': '🇹🇿', 'TG': '🇹🇬', 'TN': '🇹🇳', 'UG': '🇺🇬', 'ZM': '🇿🇲', 'ZW': '🇿🇼'
};

// Fonction pour obtenir le drapeau (supporte ISO2 et ISO3)
const getFlag = (code) => {
  if (!code) return '🌍';
  // Si c'est ISO3, convertir en ISO2 pour le drapeau
  const ISO3_TO_ISO2 = {
    'DZA': 'DZ', 'AGO': 'AO', 'BEN': 'BJ', 'BWA': 'BW', 'BFA': 'BF', 'BDI': 'BI', 'CMR': 'CM', 'CPV': 'CV',
    'CAF': 'CF', 'TCD': 'TD', 'COM': 'KM', 'COG': 'CG', 'COD': 'CD', 'CIV': 'CI', 'DJI': 'DJ', 'EGY': 'EG',
    'GNQ': 'GQ', 'ERI': 'ER', 'SWZ': 'SZ', 'ETH': 'ET', 'GAB': 'GA', 'GMB': 'GM', 'GHA': 'GH', 'GIN': 'GN',
    'GNB': 'GW', 'KEN': 'KE', 'LSO': 'LS', 'LBR': 'LR', 'LBY': 'LY', 'MDG': 'MG', 'MWI': 'MW', 'MLI': 'ML',
    'MRT': 'MR', 'MUS': 'MU', 'MAR': 'MA', 'MOZ': 'MZ', 'NAM': 'NA', 'NER': 'NE', 'NGA': 'NG', 'RWA': 'RW',
    'STP': 'ST', 'SEN': 'SN', 'SYC': 'SC', 'SLE': 'SL', 'SOM': 'SO', 'ZAF': 'ZA', 'SSD': 'SS', 'SDN': 'SD',
    'TZA': 'TZ', 'TGO': 'TG', 'TUN': 'TN', 'UGA': 'UG', 'ZMB': 'ZM', 'ZWE': 'ZW'
  };
  const iso2 = code.length === 3 ? ISO3_TO_ISO2[code] : code;
  return countryFlagsISO2[iso2] || '🌍';
};

const countryFlags = countryFlagsISO2;

export default function CalculatorTab({ countries, language = 'fr' }) {
  const [originCountry, setOriginCountry] = useState('');
  const [destinationCountry, setDestinationCountry] = useState('');
  const [hsCode, setHsCode] = useState('');
  const [value, setValue] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showHSBrowser, setShowHSBrowser] = useState(false);
  const [hs6TariffInfo, setHs6TariffInfo] = useState(null);
  const [subPositions, setSubPositions] = useState(null);
  const [useSmartSearch, setUseSmartSearch] = useState(true);
  const [ruleOfOrigin, setRuleOfOrigin] = useState(null);
  const [selectedSubPositionDesc, setSelectedSubPositionDesc] = useState(null);

  const texts = {
    fr: {
      originCountry: "Pays d'origine",
      partnerCountry: "Pays partenaire",
      hsCodeLabel: "Code HS (6-12 chiffres)",
      hsCodeHint: "6 chiffres = HS international | 8-12 chiffres = sous-position nationale",
      valueLabel: "Valeur de la marchandise (USD)",
      calculateBtn: "Calculer avec Données Officielles",
      calculatorTitle: "Calculateur ZLECAf Complet",
      calculatorDesc: "Calculs basés sur les données officielles des organismes internationaux",
      rulesOrigin: "Règles d'Origine ZLECAf",
      missingFields: "Champs manquants",
      fillAllFields: "Veuillez remplir tous les champs",
      invalidHsCode: "Code HS invalide",
      hsCodeMust6to12: "Le code HS doit contenir entre 6 et 12 chiffres",
      calculationSuccess: "Calcul réussi",
      potentialSavings: "Économie potentielle",
      calculationError: "Erreur de calcul",
      calculating: "Calcul en cours...",
      detailedResults: "Résultats Détaillés",
      completeComparison: "Comparaison Complète: Valeur + DD + TVA + Autres Taxes",
      merchandiseValue: "Valeur marchandise",
      customsDuties: "Droits douane",
      vat: "TVA",
      otherTaxes: "Autres taxes",
      nfpTariff: "Tarif NPF",
      zlecafTariff: "Tarif ZLECAf",
      totalSavings: "ÉCONOMIE TOTALE (avec toutes les taxes)",
      totalSavingsPercent: "d'économie totale",
      totalCostComparison: "Sur un coût total de",
      vs: "vs",
      calculationJournal: "Journal de Calcul Détaillé (Ordre Officiel)",
      step: "Étape",
      component: "Composant",
      base: "Base",
      rate: "Taux",
      amount: "Montant",
      cumulative: "Cumulatif",
      legalRef: "Référence Légale",
      ruleType: "Type",
      requirement: "Exigence",
      minRegionalContent: "Contenu régional minimum",
      african: "africain",
      sectorPrefix: "Secteur",
      hsCodeSelectorTitle: "Sélecteur de Code SH6",
      hsCodeSelectorDesc: "Recherchez ou parcourez les codes du Système Harmonisé",
      browseHS: "Parcourir les codes HS",
      hideHSBrowser: "Masquer le navigateur",
      // Nouvelles traductions SH6
      hs6TariffInfo: "Tarif SH6 Précis",
      hs6TariffApplied: "Tarif spécifique SH6 appliqué",
      chapterTariffApplied: "Tarif par chapitre appliqué",
      tariffPrecision: "Précision tarifaire",
      productDescription: "Description produit",
      normalRate: "Taux NPF",
      zlecafRate: "Taux ZLECAf",
      savingsRate: "Économie",
      hs6DataSource: "Source: OMC ITC, CNUCED TRAINS, WITS",
      // Sous-positions nationales
      subPositionApplied: "Sous-position nationale appliquée",
      subPositionInfo: "Tarif Sous-Position Nationale",
      subPositionCode: "Code national",
      subPositionsAvailable: "sous-positions disponibles",
      varyingRates: "Taux variables selon la sous-position",
      viewAllSubPositions: "Voir toutes les sous-positions",
      precisionHigh: "Haute précision",
      precisionMedium: "Précision moyenne"
    },
    en: {
      originCountry: "Origin Country",
      partnerCountry: "Partner Country",
      hsCodeLabel: "HS Code (6-12 digits)",
      hsCodeHint: "6 digits = international HS | 8-12 digits = national sub-position",
      valueLabel: "Merchandise Value (USD)",
      calculateBtn: "Calculate with Official Data",
      calculatorTitle: "Complete AfCFTA Calculator",
      calculatorDesc: "Calculations based on official data from international organizations",
      rulesOrigin: "AfCFTA Rules of Origin",
      missingFields: "Missing Fields",
      fillAllFields: "Please fill in all fields",
      invalidHsCode: "Invalid HS Code",
      hsCodeMust6to12: "HS code must contain between 6 and 12 digits",
      calculationSuccess: "Calculation Successful",
      potentialSavings: "Potential Savings",
      calculationError: "Calculation Error",
      calculating: "Calculating...",
      detailedResults: "Detailed Results",
      completeComparison: "Complete Comparison: Value + Duties + VAT + Other Taxes",
      merchandiseValue: "Merchandise Value",
      customsDuties: "Customs Duties",
      vat: "VAT",
      otherTaxes: "Other Taxes",
      nfpTariff: "MFN Tariff",
      zlecafTariff: "AfCFTA Tariff",
      totalSavings: "TOTAL SAVINGS (including all taxes)",
      totalSavingsPercent: "total savings",
      totalCostComparison: "On a total cost of",
      vs: "vs",
      calculationJournal: "Detailed Calculation Journal (Official Order)",
      step: "Step",
      component: "Component",
      base: "Base",
      rate: "Rate",
      amount: "Amount",
      cumulative: "Cumulative",
      legalRef: "Legal Reference",
      ruleType: "Type",
      requirement: "Requirement",
      minRegionalContent: "Minimum regional content",
      african: "African",
      sectorPrefix: "Sector",
      hsCodeSelectorTitle: "HS6 Code Selector",
      hsCodeSelectorDesc: "Search or browse Harmonized System codes",
      browseHS: "Browse HS codes",
      hideHSBrowser: "Hide browser",
      // HS6 translations
      hs6TariffInfo: "Precise HS6 Tariff",
      hs6TariffApplied: "Specific HS6 tariff applied",
      chapterTariffApplied: "Chapter tariff applied",
      tariffPrecision: "Tariff precision",
      productDescription: "Product description",
      normalRate: "MFN Rate",
      zlecafRate: "AfCFTA Rate",
      savingsRate: "Savings",
      hs6DataSource: "Source: WTO ITC, UNCTAD TRAINS, WITS",
      // National sub-positions
      subPositionApplied: "National sub-position applied",
      subPositionInfo: "National Sub-Position Tariff",
      subPositionCode: "National code",
      subPositionsAvailable: "sub-positions available",
      varyingRates: "Rates vary by sub-position",
      viewAllSubPositions: "View all sub-positions",
      precisionHigh: "High precision",
      precisionMedium: "Medium precision"
    }
  };

  const t = texts[language];

  const getSectorName = (hsCode) => {
    const sector = hsCode.substring(0, 2);
    const sectorNames = {
      fr: {
        '01': 'Animaux vivants', '02': 'Viandes', '03': 'Poissons', '04': 'Lait & Œufs',
        '05': 'Autres produits animaux', '06': 'Plantes', '07': 'Légumes', '08': 'Fruits',
        '09': 'Café/Thé', '10': 'Céréales', '27': 'Combustibles minéraux', '84': 'Machines',
        '85': 'Électrique', '87': 'Véhicules'
      },
      en: {
        '01': 'Live Animals', '02': 'Meat', '03': 'Fish', '04': 'Dairy & Eggs',
        '05': 'Other Animal Products', '06': 'Plants', '07': 'Vegetables', '08': 'Fruits',
        '09': 'Coffee/Tea', '10': 'Cereals', '27': 'Mineral Fuels', '84': 'Machinery',
        '85': 'Electrical', '87': 'Vehicles'
      }
    };
    return sectorNames[language][sector] || `${t.sectorPrefix} ${sector}`;
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const getCountryName = (code) => {
    const country = countries.find(c => c.code === code);
    return country ? country.name : code;
  };

  const calculateTariff = async () => {
    if (!originCountry || !destinationCountry || !hsCode || !value) {
      toast({
        title: t.missingFields,
        description: t.fillAllFields,
        variant: "destructive"
      });
      return;
    }

    // Validation: code HS entre 6 et 12 chiffres
    const cleanHsCode = hsCode.replace(/[.\s]/g, '');
    if (cleanHsCode.length < 6 || cleanHsCode.length > 12) {
      toast({
        title: t.invalidHsCode,
        description: t.hsCodeMust6to12,
        variant: "destructive"
      });
      return;
    }

    setLoading(true);
    try {
      // Calcul des tarifs
      const response = await axios.post(`${API}/calculate-tariff`, {
        origin_country: originCountry,
        destination_country: destinationCountry,
        hs_code: cleanHsCode,
        value: parseFloat(value)
      });
      
      setResult(response.data);
      
      // Récupérer les sous-positions si disponibles pour le pays de destination
      const hs6 = cleanHsCode.substring(0, 6);
      try {
        const subPosResponse = await axios.get(`${API}/tariffs/sub-positions/${destinationCountry}/${hs6}?language=${language}`);
        setSubPositions(subPosResponse.data);
      } catch (subPosError) {
        setSubPositions(null);
      }
      
      // Récupérer les informations SH6 spécifiques si disponibles
      try {
        const hs6Response = await axios.get(`${API}/hs6-tariffs/code/${hs6}?language=${language}`);
        setHs6TariffInfo(hs6Response.data);
      } catch (hs6Error) {
        // Pas de tarif SH6 spécifique, ce n'est pas une erreur
        setHs6TariffInfo(null);
      }
      
      toast({
        title: t.calculationSuccess,
        description: `${t.potentialSavings}: ${formatCurrency(response.data.savings)}`,
      });
    } catch (error) {
      console.error('Calculation error:', error);
      toast({
        title: t.calculationError,
        description: error.response?.data?.detail || t.calculationError,
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6" style={{ minHeight: '600px' }}>
      {/* Formulaire de calcul */}
      <Card className="shadow-2xl border-t-4 border-t-green-600" style={{ minHeight: '400px' }}>
        <CardHeader className="bg-gradient-to-r from-green-50 to-yellow-50">
          <CardTitle className="flex items-center space-x-2 text-2xl text-green-700">
            <span>📊</span>
            <span>{t.calculatorTitle}</span>
          </CardTitle>
          <CardDescription className="text-gray-700 font-semibold">
            {t.calculatorDesc}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="origin">{t.originCountry}</Label>
              <Select value={originCountry} onValueChange={setOriginCountry}>
                <SelectTrigger>
                  <SelectValue placeholder={t.originCountry} />
                </SelectTrigger>
                <SelectContent>
                  {countries.map((country) => (
                    <SelectItem key={country.code} value={country.code}>
                      {getFlag(country.iso2 || country.code)} {country.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="destination">{t.partnerCountry}</Label>
              <Select value={destinationCountry} onValueChange={setDestinationCountry}>
                <SelectTrigger>
                  <SelectValue placeholder={t.partnerCountry} />
                </SelectTrigger>
                <SelectContent>
                  {countries.map((country) => (
                    <SelectItem key={country.code} value={country.code}>
                      {getFlag(country.iso2 || country.code)} {country.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="hs-code" className="flex items-center gap-2">
                <Package className="w-4 h-4" />
                {t.hsCodeLabel}
              </Label>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => setUseSmartSearch(!useSmartSearch)}
                className="text-xs text-purple-600 hover:text-purple-700"
              >
                <Sparkles className="w-3 h-3 mr-1" />
                {useSmartSearch ? 'Mode simple' : 'Recherche intelligente'}
              </Button>
            </div>
            
            {useSmartSearch ? (
              <SmartHSSearch
                value={hsCode}
                onChange={setHsCode}
                destinationCountry={destinationCountry}
                language={language}
                onSubPositionSelect={(code, desc) => {
                  setHsCode(code);
                  setSelectedSubPositionDesc(desc);
                }}
                onRuleOfOriginLoad={setRuleOfOrigin}
              />
            ) : (
              <>
                <HSCodeSearch
                  value={hsCode}
                  onChange={setHsCode}
                  language={language}
                  data-testid="hs-code-selector"
                />
                <p className="text-xs text-gray-500 italic">{t.hsCodeHint}</p>
              </>
            )}
            
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => setShowHSBrowser(!showHSBrowser)}
              className="w-full mt-2 text-blue-600 border-blue-300 hover:bg-blue-50"
              data-testid="toggle-hs-browser"
            >
              {showHSBrowser ? (
                <>
                  <ChevronUp className="w-4 h-4 mr-2" />
                  {t.hideHSBrowser}
                </>
              ) : (
                <>
                  <ChevronDown className="w-4 h-4 mr-2" />
                  {t.browseHS}
                </>
              )}
            </Button>
          </div>

          {/* HS Code Browser Panel */}
          {showHSBrowser && (
            <div className="border-2 border-blue-200 rounded-lg overflow-hidden">
              <HSCodeBrowser
                onSelect={(code) => {
                  setHsCode(code.code);
                  setShowHSBrowser(false);
                }}
                language={language}
                showRulesOfOrigin={true}
              />
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="value">{t.valueLabel}</Label>
            <Input
              id="value"
              type="number"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              placeholder="100000"
              min="0"
            />
          </div>

          <Button 
            onClick={calculateTariff}
            disabled={loading}
            className="w-full bg-gradient-to-r from-red-600 via-yellow-500 to-green-600 text-white font-bold text-lg py-6 shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all"
          >
            {loading ? `⏳ ${t.calculating}` : `🧮 ${t.calculateBtn}`}
          </Button>
        </CardContent>
      </Card>

      {/* Résultats complets avec visualisations */}
      {result && (
        <div className="space-y-4">
          <Card className="border-l-4 border-l-green-500 shadow-xl bg-gradient-to-br from-white to-green-50">
            <CardHeader className="bg-gradient-to-r from-green-600 to-yellow-500 text-white rounded-t-lg">
              <CardTitle className="flex items-center space-x-2 text-2xl">
                <span>💰</span>
                <span>{t.detailedResults}</span>
              </CardTitle>
              <CardDescription className="text-yellow-100 font-semibold">
                {countryFlags[result.origin_country]} {getCountryName(result.origin_country)} → {countryFlags[result.destination_country]} {getCountryName(result.destination_country)}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6 pt-6">
              {/* Information sur la sous-position nationale si utilisée */}
              {result.tariff_precision === 'sub_position' && (
                <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-lg border-2 border-purple-400 shadow-md">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-2xl">🎯</span>
                    <h4 className="font-bold text-lg text-purple-700">{t.subPositionInfo}</h4>
                    <Badge className="bg-purple-600 text-white ml-2">{t.subPositionApplied}</Badge>
                    <Badge className="bg-green-500 text-white ml-1">{t.precisionHigh}</Badge>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">{t.subPositionCode}</p>
                      <p className="font-bold text-purple-800 text-xl">{result.sub_position_used}</p>
                      {result.sub_position_description && (
                        <p className="font-semibold text-gray-700 mt-1">{result.sub_position_description}</p>
                      )}
                      <p className="text-xs text-purple-600 mt-1">HS6: {result.hs6_code}</p>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-center">
                      <div className="bg-red-100 p-3 rounded">
                        <p className="text-xs text-red-600">{t.normalRate}</p>
                        <p className="font-bold text-red-700 text-lg">{(result.normal_tariff_rate * 100).toFixed(1)}%</p>
                      </div>
                      <div className="bg-green-100 p-3 rounded">
                        <p className="text-xs text-green-600">{t.zlecafRate}</p>
                        <p className="font-bold text-green-700 text-lg">{(result.zlecaf_tariff_rate * 100).toFixed(1)}%</p>
                      </div>
                    </div>
                  </div>
                  {result.has_varying_sub_positions && (
                    <p className="text-xs text-orange-600 mt-2 font-semibold">
                      ⚠️ {t.varyingRates} ({result.available_sub_positions_count} {t.subPositionsAvailable})
                    </p>
                  )}
                </div>
              )}

              {/* Information sur le tarif SH6 précis */}
              {result.tariff_precision === 'hs6_country' && (
                <div className="bg-gradient-to-r from-blue-50 to-cyan-50 p-4 rounded-lg border-2 border-blue-300 shadow-md">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-2xl">🎯</span>
                    <h4 className="font-bold text-lg text-blue-700">{t.hs6TariffInfo}</h4>
                    <Badge className="bg-green-500 text-white ml-2">{t.hs6TariffApplied}</Badge>
                    <Badge className="bg-blue-500 text-white ml-1">{t.precisionHigh}</Badge>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">{t.productDescription}</p>
                      <p className="font-semibold text-gray-800">{hs6TariffInfo?.description || `Code ${result.hs6_code}`}</p>
                      <p className="text-xs text-blue-600 mt-1">Code: {result.hs6_code}</p>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-center">
                      <div className="bg-red-100 p-3 rounded">
                        <p className="text-xs text-red-600">{t.normalRate}</p>
                        <p className="font-bold text-red-700 text-lg">{(result.normal_tariff_rate * 100).toFixed(1)}%</p>
                      </div>
                      <div className="bg-green-100 p-3 rounded">
                        <p className="text-xs text-green-600">{t.zlecafRate}</p>
                        <p className="font-bold text-green-700 text-lg">{(result.zlecaf_tariff_rate * 100).toFixed(1)}%</p>
                      </div>
                    </div>
                  </div>
                  {result.available_sub_positions_count > 0 && (
                    <p className="text-xs text-orange-600 mt-2 font-semibold">
                      💡 {result.available_sub_positions_count} {t.subPositionsAvailable} - {t.varyingRates}
                    </p>
                  )}
                </div>
              )}

              {/* WARNING: Taux variables selon sous-positions nationales */}
              {result.rate_warning && result.rate_warning.has_variation && (
                <div 
                  className="rate-warning-box bg-gradient-to-r from-amber-50 via-orange-50 to-yellow-50 p-5 rounded-xl border-l-4 border-amber-500 shadow-lg" 
                  data-testid="rate-warning-box"
                >
                  <div className="flex items-start gap-4">
                    <div className="flex-shrink-0 w-12 h-12 bg-amber-100 rounded-full flex items-center justify-center">
                      <AlertTriangle className="w-6 h-6 text-amber-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="font-bold text-lg text-amber-800 mb-2">
                        {language === 'fr' ? 'Attention: Taux de droits variables' : 'Warning: Variable duty rates'}
                      </h4>
                      <p className="text-gray-700 text-sm leading-relaxed mb-4">
                        {language === 'fr' 
                          ? `Ce code SH6 (${result.hs6_code}) comporte plusieurs sous-positions nationales avec des taux différents.`
                          : `This HS6 code (${result.hs6_code}) has multiple national sub-headings with different rates.`}
                      </p>
                      
                      {/* Visualisation des taux min/max/utilisé */}
                      <div className="grid grid-cols-3 gap-3 mb-4">
                        <div className="rate-card bg-green-50 p-3 rounded-lg text-center border border-green-200 shadow-sm">
                          <p className="text-xs text-green-600 font-medium uppercase tracking-wide">{language === 'fr' ? 'Minimum' : 'Minimum'}</p>
                          <p className="text-2xl font-bold text-green-700 mt-1">{result.rate_warning.min_rate_pct}</p>
                        </div>
                        <div className="rate-card bg-blue-50 p-3 rounded-lg text-center border-2 border-blue-400 shadow-md relative">
                          <div className="absolute -top-2 left-1/2 transform -translate-x-1/2">
                            <Badge className="bg-blue-600 text-white text-xs px-2">
                              {language === 'fr' ? 'Utilisé' : 'Used'}
                            </Badge>
                          </div>
                          <p className="text-xs text-blue-600 font-medium uppercase tracking-wide mt-2">{language === 'fr' ? 'Actuel' : 'Current'}</p>
                          <p className="text-2xl font-bold text-blue-700 mt-1">{result.rate_warning.rate_used_pct}</p>
                        </div>
                        <div className="rate-card bg-red-50 p-3 rounded-lg text-center border border-red-200 shadow-sm">
                          <p className="text-xs text-red-600 font-medium uppercase tracking-wide">{language === 'fr' ? 'Maximum' : 'Maximum'}</p>
                          <p className="text-2xl font-bold text-red-700 mt-1">{result.rate_warning.max_rate_pct}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-start gap-2 bg-amber-100/50 p-3 rounded-lg">
                        <Info className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
                        <p className="text-sm text-amber-800">
                          {language === 'fr' 
                            ? 'Pour un calcul précis, sélectionnez la sous-position correspondant exactement à votre produit ci-dessous.'
                            : 'For an accurate calculation, select the sub-heading that exactly matches your product below.'}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Sous-positions détaillées - Affiché uniquement si taux variables */}
              {result.sub_positions_details && result.sub_positions_details.length > 0 && result.rate_warning?.has_variation && (
                <div className="result-section bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                  <div 
                    className="p-4 bg-gradient-to-r from-purple-50 to-indigo-50 border-b border-purple-100 cursor-pointer"
                    onClick={() => document.getElementById('sub-positions-details')?.toggleAttribute('open')}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                          <Package className="w-5 h-5 text-purple-600" />
                        </div>
                        <div>
                          <h4 className="font-bold text-purple-800">
                            {language === 'fr' ? 'Sous-positions disponibles' : 'Available sub-headings'}
                          </h4>
                          <p className="text-sm text-purple-600">
                            {language === 'fr' ? 'Cliquez pour sélectionner le taux exact' : 'Click to select exact rate'}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge className="bg-purple-600 text-white">{result.sub_positions_details.length}</Badge>
                        <Badge className="bg-gradient-to-r from-green-500 to-red-500 text-white text-xs">
                          {result.rate_warning.min_rate_pct} → {result.rate_warning.max_rate_pct}
                        </Badge>
                      </div>
                    </div>
                  </div>
                  
                  <details id="sub-positions-details" className="sub-positions-container" open>
                    <summary className="sr-only">Toggle sub-positions</summary>
                    <div className="p-4 space-y-2 max-h-80 overflow-y-auto">
                      {result.sub_positions_details.map((sp, idx) => {
                        const isMinRate = sp.dd_rate === result.rate_warning?.min_rate;
                        const isMaxRate = sp.dd_rate === result.rate_warning?.max_rate;
                        const isCurrentRate = sp.dd_rate === result.rate_warning?.rate_used;
                        
                        return (
                          <div 
                            key={idx} 
                            className={`sub-position-item p-3 rounded-lg cursor-pointer flex items-center justify-between border transition-all ${
                              isCurrentRate 
                                ? 'bg-blue-50 border-blue-300 shadow-sm' 
                                : 'bg-gray-50 border-gray-200 hover:border-purple-300 hover:bg-purple-50'
                            }`}
                            onClick={() => {
                              setHsCode(sp.code);
                              toast({
                                title: language === 'fr' ? 'Sous-position sélectionnée' : 'Sub-heading selected',
                                description: sp.code,
                              });
                            }}
                          >
                            <div className="flex items-center gap-3 min-w-0 flex-1">
                              <code className="font-mono font-bold text-purple-800 bg-purple-100 px-2 py-1 rounded text-sm">
                                {sp.code}
                              </code>
                              <span className="text-gray-700 text-sm truncate">
                                {language === 'fr' ? sp.description_fr : sp.description_en}
                              </span>
                            </div>
                            <div className="flex items-center gap-2 flex-shrink-0 ml-3">
                              {isCurrentRate && (
                                <Badge className="bg-blue-100 text-blue-700 text-xs">
                                  {language === 'fr' ? 'Actuel' : 'Current'}
                                </Badge>
                              )}
                              <Badge className={`text-white font-bold px-3 ${
                                isMinRate ? 'bg-green-500' :
                                isMaxRate ? 'bg-red-500' :
                                isCurrentRate ? 'bg-blue-500' : 'bg-gray-500'
                              }`}>
                                {sp.dd_rate_pct}
                              </Badge>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </details>
                </div>
              )}
              
              {/* Badge tarif par chapitre si pas de SH6 spécifique */}
              {result.tariff_precision === 'chapter' && (
                <div className="bg-gray-50 p-3 rounded-lg border border-gray-200">
                  <div className="flex items-center gap-2">
                    <span>📦</span>
                    <span className="text-sm text-gray-600">{t.chapterTariffApplied}</span>
                    <Badge variant="outline" className="text-gray-600">{t.sectorPrefix} {result.hs_code?.substring(0, 2)}</Badge>
                    <Badge variant="outline" className="text-yellow-600 ml-2">{t.precisionMedium}</Badge>
                  </div>
                </div>
              )}

              {/* Graphique comparaison complète avec TOUTES les taxes */}
              <div className="chart-container result-section bg-white p-5 rounded-xl shadow-md border border-gray-100">
                <h4 className="font-bold text-lg mb-4 text-gray-800 flex items-center gap-2">
                  <span className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">📊</span>
                  {t.completeComparison}
                </h4>
                <ResponsiveContainer width="100%" height={280} debounce={300}>
                  <BarChart data={[
                    { 
                      name: t.nfpTariff, 
                      [t.merchandiseValue]: result.value,
                      [t.customsDuties]: result.normal_tariff_amount,
                      [t.vat]: result.normal_vat_amount,
                      [t.otherTaxes]: result.normal_other_taxes_total
                    },
                    { 
                      name: t.zlecafTariff, 
                      [t.merchandiseValue]: result.value,
                      [t.customsDuties]: result.zlecaf_tariff_amount,
                      [t.vat]: result.zlecaf_vat_amount,
                      [t.otherTaxes]: result.zlecaf_other_taxes_total
                    }
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip formatter={(value) => formatCurrency(value)} />
                    <Legend />
                    <Bar dataKey={t.merchandiseValue} stackId="a" fill="#60a5fa" />
                    <Bar dataKey={t.customsDuties} stackId="a" fill="#ef4444" />
                    <Bar dataKey={t.vat} stackId="a" fill="#f59e0b" />
                    <Bar dataKey={t.otherTaxes} stackId="a" fill="#8b5cf6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Économies TOTALES */}
              <div className="savings-section result-section text-center bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 p-6 rounded-xl shadow-lg border border-green-200">
                <p className="text-base font-semibold text-gray-600 mb-3">{t.totalSavings}</p>
                <p className="text-4xl md:text-5xl font-extrabold text-green-600 mb-4">
                  {formatCurrency(result.total_savings_with_taxes)}
                </p>
                <div className="inline-flex items-center gap-2 bg-green-600 text-white px-5 py-2 rounded-full shadow-md">
                  <Sparkles className="w-5 h-5" />
                  <span className="text-xl font-bold">{result.total_savings_percentage.toFixed(1)}%</span>
                  <span className="text-sm opacity-90">{t.totalSavingsPercent}</span>
                </div>
                <Progress value={result.total_savings_percentage} className="w-full mt-5 h-2 bg-green-100" />
                <p className="text-sm text-gray-500 mt-4">
                  {t.totalCostComparison} <span className="font-semibold text-red-600">{formatCurrency(result.normal_total_cost)}</span> (NPF) 
                  {' '}{t.vs}{' '}
                  <span className="font-semibold text-green-600">{formatCurrency(result.zlecaf_total_cost)}</span> (ZLECAf)
                </p>
              </div>

              {/* Journal de calcul détaillé */}
              {result.normal_calculation_journal && (
                <Card className="journal-container result-section shadow-md border-0 overflow-hidden">
                  <CardHeader className="bg-gradient-to-r from-slate-50 to-gray-50 border-b border-gray-100 py-4">
                    <CardTitle className="text-lg font-bold text-gray-800 flex items-center gap-3">
                      <div className="w-9 h-9 bg-purple-100 rounded-lg flex items-center justify-center">
                        <Package className="w-5 h-5 text-purple-600" />
                      </div>
                      {t.calculationJournal}
                    </CardTitle>
                    <CardDescription className="text-gray-500 text-sm mt-1">
                      {result.computation_order_ref}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="p-0">
                    <div className="overflow-x-auto">
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>{t.step}</TableHead>
                            <TableHead>{t.component}</TableHead>
                            <TableHead>{t.base}</TableHead>
                            <TableHead>{t.rate}</TableHead>
                            <TableHead>{t.amount}</TableHead>
                            <TableHead>{t.cumulative}</TableHead>
                            <TableHead>{t.legalRef}</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {result.normal_calculation_journal.map((entry, index) => (
                            <TableRow key={index} className={index % 2 === 0 ? 'bg-gray-50' : ''}>
                              <TableCell className="font-bold">{entry.step}</TableCell>
                              <TableCell className="font-semibold">{entry.component}</TableCell>
                              <TableCell>{formatCurrency(entry.base)}</TableCell>
                              <TableCell className="font-semibold text-red-600">{entry.rate}</TableCell>
                              <TableCell className="font-bold text-blue-600">{formatCurrency(entry.amount)}</TableCell>
                              <TableCell className="font-bold">{formatCurrency(entry.cumulative)}</TableCell>
                              <TableCell className="text-xs">
                                {entry.legal_ref_url ? (
                                  <a href={entry.legal_ref_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                                    {entry.legal_ref}
                                  </a>
                                ) : (
                                  entry.legal_ref || '-'
                                )}
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Règles d'origine avec style africain */}
              <div className="bg-gradient-to-r from-amber-100 to-orange-100 p-6 rounded-xl border-l-4 border-orange-500 shadow-lg">
                <h4 className="font-bold text-xl text-orange-800 mb-3 flex items-center gap-2">
                  <span>📜</span> {t.rulesOrigin}
                </h4>
                <div className="bg-white p-4 rounded-lg space-y-2">
                  <p className="text-sm text-amber-800 font-semibold">
                    <strong className="text-orange-600">{t.ruleType}:</strong> {result.rules_of_origin.rule}
                  </p>
                  <p className="text-sm text-amber-800 font-semibold">
                    <strong className="text-orange-600">{t.requirement}:</strong> {result.rules_of_origin.requirement}
                  </p>
                  <div className="mt-3">
                    <Progress 
                      value={result.rules_of_origin.regional_content} 
                      className="w-full h-3"
                    />
                    <p className="text-sm text-amber-700 mt-2 font-bold text-center">
                      🌍 {t.minRegionalContent}: {result.rules_of_origin.regional_content}% {t.african}
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
