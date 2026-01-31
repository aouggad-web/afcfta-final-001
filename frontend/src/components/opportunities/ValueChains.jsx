/**
 * Value Chains Component
 * Analyzes African value chains and industrial transformation opportunities
 * USING REAL DATA from Gemini AI (Industrial Mode)
 */
import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { 
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, 
  CartesianGrid, Tooltip, Cell
} from 'recharts';
import { 
  Factory, ArrowRight, Globe, TrendingUp, Package, 
  Loader2, Layers, Sparkles, AlertTriangle, Database
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const COLORS = ['#059669', '#0891b2', '#7c3aed', '#dc2626', '#ea580c', '#ca8a04'];

// Format value
const formatValue = (value) => {
  if (value >= 1000) return `$${(value / 1000).toFixed(1)}B`;
  if (value >= 1) return `$${value.toFixed(0)}M`;
  return `$${(value * 1000).toFixed(0)}K`;
};

// Value Chain Card Component
const ValueChainCard = ({ opportunity, index, language }) => {
  const isEstimation = opportunity.is_estimation;
  
  const product = opportunity.product || {};
  const input = opportunity.industrial_input || {};
  const targets = opportunity.target_markets || [];
  
  return (
    <Card className={`bg-white border-slate-200 shadow-lg hover:shadow-xl transition-all ${
      isEstimation ? 'border-l-4 border-l-amber-400' : 'border-l-4 border-l-emerald-500'
    }`}>
      <CardContent className="p-5">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <Badge variant="outline" className="font-mono">
            HS {product.hs_code || '----'}
          </Badge>
          {isEstimation && (
            <Badge className="bg-amber-100 text-amber-700 text-[10px]">
              <AlertTriangle className="h-3 w-3 mr-1" />
              ESTIMATION
            </Badge>
          )}
        </div>

        {/* Transformation Flow */}
        <div className="bg-gradient-to-r from-blue-50 to-emerald-50 rounded-lg p-4 mb-4">
          <p className="text-xs font-bold text-blue-600 uppercase mb-2">
            Chaîne de Transformation
          </p>
          <div className="flex items-center gap-2 flex-wrap">
            <div className="flex-1 min-w-[100px]">
              <p className="text-xs text-slate-500">Intrant importé</p>
              <p className="font-bold text-slate-800 text-sm">{input.name || 'N/A'}</p>
              {input.import_volume && (
                <p className="text-xs text-slate-500 mt-1">{input.import_volume}</p>
              )}
            </div>
            <ArrowRight className="h-6 w-6 text-emerald-500 flex-shrink-0" />
            <div className="flex-1 min-w-[100px]">
              <p className="text-xs text-slate-500">Produit fini</p>
              <p className="font-bold text-emerald-700 text-sm">{product.name || 'N/A'}</p>
              {opportunity.estimated_production && (
                <p className="text-xs text-emerald-600 mt-1">{opportunity.estimated_production}</p>
              )}
            </div>
          </div>
        </div>

        {/* Value & Markets */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <p className="text-xs text-slate-500">Potentiel</p>
            <p className="text-xl font-black text-emerald-600">
              {formatValue(opportunity.potential_value_musd || 0)}
            </p>
          </div>
          <div>
            <p className="text-xs text-slate-500">Réduction tarifaire</p>
            <p className="text-lg font-bold text-blue-600">
              {opportunity.tariff_reduction ? `-${opportunity.tariff_reduction}%` : 'N/A'}
            </p>
          </div>
        </div>

        {/* Target Markets */}
        {targets.length > 0 && (
          <div className="border-t border-slate-200 pt-3">
            <p className="text-xs font-bold text-slate-500 uppercase mb-2 flex items-center gap-1">
              <Globe className="h-3 w-3" />
              Marchés cibles
            </p>
            <div className="flex flex-wrap gap-1">
              {targets.slice(0, 4).map((market, idx) => (
                <Badge key={idx} variant="secondary" className="text-xs">
                  {market}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Transformation Logic */}
        {opportunity.transformation_logic && (
          <div className="mt-3 p-3 bg-slate-50 rounded text-xs text-slate-600">
            <p className="font-bold text-slate-700 mb-1">Logique de transformation:</p>
            {opportunity.transformation_logic}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

// Main Component
export default function ValueChains({ language = 'fr' }) {
  const { i18n } = useTranslation();
  const currentLang = i18n.language || language;

  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [chainData, setChainData] = useState(null);

  const texts = {
    fr: {
      title: "Chaînes de Valeur Industrielles",
      subtitle: "Opportunités de transformation: Intrants importés → Produits finis exportables",
      selectCountry: "Sélectionnez un pays",
      analyze: "Analyser avec IA",
      loading: "Analyse des chaînes de valeur...",
      loadingMessages: [
        "Analyse des imports d'intrants UNCTAD...",
        "Cartographie des capacités industrielles...",
        "Identification des opportunités de transformation...",
        "Calcul des potentiels d'export..."
      ],
      opportunities: "Opportunités identifiées",
      totalPotential: "Potentiel total",
      noData: "Sélectionnez un pays pour analyser ses chaînes de valeur industrielles",
      poweredBy: "Analyse par Gemini AI",
      realData: "DONNÉES RÉELLES"
    },
    en: {
      title: "Industrial Value Chains",
      subtitle: "Transformation opportunities: Imported inputs → Exportable finished products",
      selectCountry: "Select a country",
      analyze: "Analyze with AI",
      loading: "Analyzing value chains...",
      loadingMessages: [
        "Analyzing UNCTAD input imports...",
        "Mapping industrial capacities...",
        "Identifying transformation opportunities...",
        "Computing export potentials..."
      ],
      opportunities: "Opportunities identified",
      totalPotential: "Total potential",
      noData: "Select a country to analyze its industrial value chains",
      poweredBy: "Analysis by Gemini AI",
      realData: "REAL DATA"
    }
  };
  const txt = texts[currentLang] || texts.fr;

  // Loading message animation
  const [loadingMessage, setLoadingMessage] = useState(0);
  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(() => {
        setLoadingMessage(prev => (prev + 1) % txt.loadingMessages.length);
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [loading, txt.loadingMessages.length]);

  // Fetch countries
  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const res = await axios.get(`${API}/substitution/countries?lang=${currentLang}`);
        setCountries(res.data.countries || []);
      } catch (err) {
        console.error('Error fetching countries:', err);
      }
    };
    fetchCountries();
  }, [currentLang]);

  // Analyze value chains using Gemini AI (Industrial mode)
  const analyzeChains = useCallback(async () => {
    if (!selectedCountry) return;

    setLoading(true);
    setError(null);
    setChainData(null);

    const countryObj = countries.find(c => c.iso3 === selectedCountry);
    const countryName = countryObj?.name || selectedCountry;

    try {
      const res = await axios.get(
        `${API}/ai/opportunities/${encodeURIComponent(countryName)}`,
        { params: { mode: 'industrial', lang: currentLang } }
      );
      
      setChainData({
        country: countryName,
        opportunities: res.data.opportunities || [],
        sources: res.data.sources || [],
        generatedBy: res.data.generated_by
      });
      
    } catch (err) {
      console.error('Value chain analysis error:', err);
      setError(err.response?.data?.detail || 'Erreur lors de l\'analyse');
    } finally {
      setLoading(false);
    }
  }, [selectedCountry, currentLang, countries]);

  // Calculate summary stats
  const summaryStats = React.useMemo(() => {
    if (!chainData?.opportunities) return null;

    const opps = chainData.opportunities;
    const totalValue = opps.reduce((sum, opp) => sum + (opp.potential_value_musd || 0), 0);
    const hasEstimations = opps.some(opp => opp.is_estimation);

    return {
      count: opps.length,
      totalValue,
      hasEstimations
    };
  }, [chainData]);

  // Chart data
  const chartData = React.useMemo(() => {
    if (!chainData?.opportunities) return [];
    return chainData.opportunities.slice(0, 10).map(opp => ({
      name: opp.product?.name?.substring(0, 20) || 'N/A',
      value: opp.potential_value_musd || 0
    }));
  }, [chainData]);

  return (
    <div className="space-y-6" data-testid="value-chains">
      {/* Header */}
      <div className="text-center">
        <div className="flex items-center justify-center gap-3 mb-2">
          <Factory className="h-8 w-8 text-indigo-600" />
          <h2 className="text-3xl font-black text-slate-900 uppercase tracking-tight">
            {txt.title}
          </h2>
        </div>
        <p className="text-slate-500">{txt.subtitle}</p>
      </div>

      {/* Controls */}
      <Card className="shadow-lg">
        <CardContent className="p-6">
          <div className="flex flex-col sm:flex-row gap-4 items-end">
            {/* Country selection */}
            <div className="flex-1 space-y-2">
              <label className="text-sm font-medium text-slate-700">{txt.selectCountry}</label>
              <Select value={selectedCountry} onValueChange={setSelectedCountry}>
                <SelectTrigger className="w-full" data-testid="valuechains-country-select">
                  <SelectValue placeholder={txt.selectCountry} />
                </SelectTrigger>
                <SelectContent>
                  {countries.map(country => (
                    <SelectItem key={country.iso3} value={country.iso3}>
                      {country.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Analyze button */}
            <Button
              onClick={analyzeChains}
              disabled={!selectedCountry || loading}
              className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700"
              data-testid="valuechains-analyze-btn"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Sparkles className="h-4 w-4 mr-2" />
              )}
              {txt.analyze}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Loading state */}
      {loading && (
        <Card className="bg-gradient-to-r from-indigo-50 to-purple-50 border-indigo-200">
          <CardContent className="py-16 text-center">
            <div className="relative w-20 h-20 mx-auto mb-6">
              <div className="absolute inset-0 border-4 border-indigo-200 rounded-full"></div>
              <div className="absolute inset-0 border-4 border-t-indigo-500 rounded-full animate-spin"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <Factory className="h-8 w-8 text-indigo-500" />
              </div>
            </div>
            <p className="text-xl font-bold text-slate-800 mb-2">{txt.loading}</p>
            <p className="text-indigo-600 font-medium text-sm animate-pulse">
              {txt.loadingMessages[loadingMessage]}
            </p>
          </CardContent>
        </Card>
      )}

      {/* Error state */}
      {error && (
        <Card className="bg-red-50 border-red-200">
          <CardContent className="py-8 text-center">
            <AlertTriangle className="h-8 w-8 text-red-500 mx-auto mb-2" />
            <p className="text-red-700">{error}</p>
          </CardContent>
        </Card>
      )}

      {/* Results */}
      {!loading && !error && chainData && (
        <>
          {/* Summary Stats */}
          {summaryStats && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card className="bg-white shadow-lg">
                <CardContent className="p-5">
                  <div className="flex items-center gap-4">
                    <div className="h-12 w-12 flex items-center justify-center rounded-full bg-indigo-100 text-indigo-600">
                      <Layers className="h-6 w-6" />
                    </div>
                    <div>
                      <p className="text-sm text-slate-500">{txt.opportunities}</p>
                      <p className="text-2xl font-bold text-slate-900">{summaryStats.count}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white shadow-lg">
                <CardContent className="p-5">
                  <div className="flex items-center gap-4">
                    <div className="h-12 w-12 flex items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
                      <TrendingUp className="h-6 w-6" />
                    </div>
                    <div>
                      <p className="text-sm text-slate-500">{txt.totalPotential}</p>
                      <p className="text-2xl font-bold text-emerald-600">
                        {formatValue(summaryStats.totalValue)}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white shadow-lg">
                <CardContent className="p-5">
                  <div className="flex items-center gap-4">
                    <div className="h-12 w-12 flex items-center justify-center rounded-full bg-purple-100 text-purple-600">
                      <Database className="h-6 w-6" />
                    </div>
                    <div>
                      <p className="text-sm text-slate-500">Source</p>
                      <p className="text-lg font-bold text-purple-600">
                        {chainData.generatedBy || 'Gemini AI'}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Chart */}
          {chartData.length > 0 && (
            <Card className="shadow-lg">
              <CardHeader>
                <CardTitle className="text-lg font-bold">Potentiel par Produit Fini</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={chartData}
                      layout="vertical"
                      margin={{ top: 5, right: 30, left: 120, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" tickFormatter={(v) => `$${v}M`} />
                      <YAxis type="category" dataKey="name" width={115} tick={{ fontSize: 10 }} />
                      <Tooltip formatter={(value) => [`$${value}M`, 'Potentiel']} />
                      <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                        {chartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Opportunities Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {chainData.opportunities.slice(0, 12).map((opp, idx) => (
              <ValueChainCard
                key={idx}
                opportunity={opp}
                index={idx}
                language={currentLang}
              />
            ))}
          </div>

          {/* Sources footer */}
          {chainData.sources?.length > 0 && (
            <Card className="bg-slate-50 border-slate-200">
              <CardContent className="py-4 px-6">
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <Sparkles className="h-4 w-4 text-purple-500" />
                  <span className="font-medium">{txt.poweredBy}</span>
                  <span className="text-slate-400">|</span>
                  <span>Sources: {chainData.sources.join(', ')}</span>
                </div>
              </CardContent>
            </Card>
          )}
        </>
      )}

      {/* Empty state */}
      {!loading && !error && !chainData && (
        <Card className="bg-slate-50 border-slate-200">
          <CardContent className="py-16 text-center">
            <Factory className="h-16 w-16 text-slate-300 mx-auto mb-4" />
            <p className="text-slate-500">{txt.noData}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
