/**
 * Product Analysis View Component
 * Detailed market intelligence by HS code
 * USING REAL DATA from OEC API
 */
import React, { useState, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { 
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, 
  CartesianGrid, Tooltip, Cell
} from 'recharts';
import { 
  Search, Package, TrendingUp, TrendingDown, ArrowRight,
  Loader2, AlertCircle, Database, Globe
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Format large numbers
const formatValue = (value) => {
  if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
  if (value >= 1e6) return `$${(value / 1e6).toFixed(1)}M`;
  if (value >= 1e3) return `$${(value / 1e3).toFixed(0)}K`;
  return `$${value?.toLocaleString() || 0}`;
};

// Data Bar Chart Component
const DataBarChart = ({ data, barColor, title, valueKey = 'value' }) => {
  if (!data || data.length === 0) {
    return (
      <div className="h-[300px] flex items-center justify-center text-slate-400 italic">
        Aucune donnée disponible
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart 
        data={data} 
        layout="vertical" 
        margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
        barCategoryGap="20%"
      >
        <CartesianGrid strokeDasharray="3 3" horizontal={false} strokeOpacity={0.3} />
        <XAxis 
          type="number" 
          tickFormatter={(v) => formatValue(v)} 
          tick={{ fontSize: 10, fill: '#64748b' }} 
        />
        <YAxis 
          dataKey="country" 
          type="category" 
          width={95} 
          tick={{ fontSize: 10, fontWeight: 'bold', fill: '#334155' }} 
          interval={0} 
        />
        <Tooltip 
          formatter={(value) => [formatValue(value), 'Valeur']}
          contentStyle={{ 
            borderRadius: '12px', 
            border: 'none', 
            boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
            background: 'rgba(255,255,255,0.95)'
          }}
        />
        <Bar dataKey={valueKey} fill={barColor} radius={[0, 4, 4, 0]} barSize={18}>
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fillOpacity={1 - (index * 0.07)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

// Substitution Opportunity Card
const SubstitutionCard = ({ opp, index }) => (
  <div className="p-4 bg-gradient-to-br from-emerald-50 to-white rounded-lg border border-emerald-200 hover:border-emerald-400 transition-colors">
    <div className="flex items-center gap-2 mb-2">
      <Badge variant="outline" className="text-xs">#{index + 1}</Badge>
    </div>
    <div className="flex items-center gap-2 text-sm">
      <span className="font-medium text-slate-600">{opp.exporter}</span>
      <ArrowRight className="h-4 w-4 text-emerald-500" />
      <span className="font-medium text-slate-600">{opp.importer}</span>
    </div>
    <p className="text-lg font-black text-emerald-600 mt-2">
      {formatValue(opp.potential_value)}
    </p>
  </div>
);

// Main Component
export default function ProductAnalysisView({ language = 'fr' }) {
  const { i18n } = useTranslation();
  const currentLang = i18n.language || language;
  
  const [hsCode, setHsCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [productData, setProductData] = useState(null);

  // Popular products for quick selection
  const popularProducts = [
    { code: '0901', name: 'Café' },
    { code: '1801', name: 'Cacao' },
    { code: '2709', name: 'Pétrole brut' },
    { code: '7108', name: 'Or' },
    { code: '5201', name: 'Coton' },
    { code: '2711', name: 'Gaz naturel' },
    { code: '1001', name: 'Blé' },
    { code: '8703', name: 'Véhicules' }
  ];

  const texts = {
    fr: {
      title: "Analyse par Produit",
      subtitle: "Intelligence de marché détaillée par code HS (Données Réelles OEC)",
      searchLabel: "Code HS (2-6 chiffres)",
      searchPlaceholder: "Ex: 0901 (Café), 27 (Combustibles)",
      searchBtn: "Analyser",
      popularProducts: "Produits populaires",
      topExporters: "Exportateurs Africains",
      topImporters: "Importateurs Africains",
      substitutionOpps: "Opportunités de Substitution",
      africaTrade: "Commerce Africain",
      totalExports: "Exports Africains",
      totalImports: "Imports Africains",
      potential: "Potentiel Intra-Africain",
      noData: "Entrez un code HS pour voir l'analyse",
      loading: "Analyse en cours...",
      realData: "DONNÉES RÉELLES"
    },
    en: {
      title: "Product Analysis",
      subtitle: "Detailed market intelligence by HS code (Real OEC Data)",
      searchLabel: "HS Code (2-6 digits)",
      searchPlaceholder: "Ex: 0901 (Coffee), 27 (Fuels)",
      searchBtn: "Analyze",
      popularProducts: "Popular products",
      topExporters: "African Exporters",
      topImporters: "African Importers",
      substitutionOpps: "Substitution Opportunities",
      africaTrade: "African Trade",
      totalExports: "African Exports",
      totalImports: "African Imports",
      potential: "Intra-African Potential",
      noData: "Enter an HS code to see the analysis",
      loading: "Analyzing...",
      realData: "REAL DATA"
    }
  };
  const txt = texts[currentLang] || texts.fr;

  // Search product data
  const searchProduct = useCallback(async (code) => {
    const searchCode = code || hsCode;
    if (!searchCode || searchCode.length < 2) return;
    
    setLoading(true);
    setError(null);
    
    try {
      // Use real API
      const response = await axios.get(
        `${API}/substitution/product/${searchCode}?year=2022&lang=${currentLang}`
      );
      
      const data = response.data;
      
      // Format for charts
      const exporters = (data.top_exporters || []).map(exp => ({
        country: exp.country,
        iso3: exp.iso3,
        value: exp.value
      }));
      
      const importers = (data.top_importers || []).map(imp => ({
        country: imp.country,
        iso3: imp.iso3,
        value: imp.value
      }));
      
      setProductData({
        product: data.product,
        africanTrade: data.african_trade,
        exporters,
        importers,
        substitutionOpps: data.substitution_opportunities || [],
        year: data.year,
        source: data.data_source
      });
      
    } catch (err) {
      console.error('Error fetching product data:', err);
      setError('Erreur lors de l\'analyse du produit');
    } finally {
      setLoading(false);
    }
  }, [hsCode, currentLang]);

  // Handle quick product selection
  const handleQuickSelect = (code) => {
    setHsCode(code);
    searchProduct(code);
  };

  return (
    <div className="space-y-6" data-testid="product-analysis">
      {/* Header */}
      <div className="text-center">
        <div className="flex items-center justify-center gap-3 mb-2">
          <Package className="h-8 w-8 text-blue-600" />
          <h2 className="text-3xl font-black text-slate-900 uppercase tracking-tight">
            {txt.title}
          </h2>
        </div>
        <p className="text-slate-500">{txt.subtitle}</p>
      </div>

      {/* Search Bar */}
      <Card className="shadow-lg">
        <CardContent className="p-6">
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1">
              <label className="text-sm font-medium text-slate-700 mb-2 block">
                {txt.searchLabel}
              </label>
              <div className="flex gap-2">
                <Input
                  type="text"
                  placeholder={txt.searchPlaceholder}
                  value={hsCode}
                  onChange={(e) => setHsCode(e.target.value.replace(/\D/g, ''))}
                  maxLength={6}
                  className="font-mono text-lg"
                  data-testid="hs-code-input"
                />
                <Button
                  onClick={() => searchProduct()}
                  disabled={loading || hsCode.length < 2}
                  className="bg-blue-600 hover:bg-blue-700"
                  data-testid="analyze-product-btn"
                >
                  {loading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Search className="h-4 w-4" />
                  )}
                  <span className="ml-2">{txt.searchBtn}</span>
                </Button>
              </div>
            </div>
          </div>

          {/* Popular Products */}
          <div className="mt-4">
            <p className="text-xs font-medium text-slate-500 mb-2">{txt.popularProducts}:</p>
            <div className="flex flex-wrap gap-2">
              {popularProducts.map(product => (
                <Button
                  key={product.code}
                  variant="outline"
                  size="sm"
                  onClick={() => handleQuickSelect(product.code)}
                  className="text-xs hover:bg-blue-50 hover:border-blue-400"
                >
                  <span className="font-mono mr-1">{product.code}</span>
                  {product.name}
                </Button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Loading State */}
      {loading && (
        <Card className="bg-blue-50 border-blue-200">
          <CardContent className="py-16 text-center">
            <Loader2 className="h-10 w-10 animate-spin text-blue-500 mx-auto mb-3" />
            <p className="text-blue-700 font-medium">{txt.loading}</p>
            <p className="text-xs text-blue-500 mt-1">Interrogation de l'API OEC...</p>
          </CardContent>
        </Card>
      )}

      {/* Error State */}
      {error && (
        <Card className="bg-red-50 border-red-200">
          <CardContent className="py-8 text-center">
            <AlertCircle className="h-8 w-8 text-red-500 mx-auto mb-2" />
            <p className="text-red-700">{error}</p>
          </CardContent>
        </Card>
      )}

      {/* Results */}
      {!loading && !error && productData && (
        <>
          {/* Product Header */}
          <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between flex-wrap gap-4">
                <div>
                  <Badge className="bg-blue-600 text-white font-mono text-lg px-3 py-1">
                    HS {productData.product?.hs_code}
                  </Badge>
                  <h3 className="text-2xl font-black text-slate-900 mt-2">
                    {productData.product?.name}
                  </h3>
                  {productData.product?.chapter && (
                    <p className="text-sm text-slate-500 mt-1">
                      Chapitre {productData.product.chapter}
                    </p>
                  )}
                </div>
                <Badge className="bg-emerald-100 text-emerald-700">
                  <Database className="h-3 w-3 mr-1" />
                  {txt.realData} - {productData.source}
                </Badge>
              </div>
            </CardContent>
          </Card>

          {/* Trade Summary Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="bg-emerald-50 border-emerald-200 shadow">
              <CardContent className="p-5 text-center">
                <TrendingUp className="h-6 w-6 text-emerald-600 mx-auto mb-2" />
                <p className="text-sm text-emerald-600 font-medium">{txt.totalExports}</p>
                <p className="text-2xl font-black text-emerald-700">
                  {formatValue(productData.africanTrade?.total_exports || 0)}
                </p>
              </CardContent>
            </Card>
            <Card className="bg-orange-50 border-orange-200 shadow">
              <CardContent className="p-5 text-center">
                <TrendingDown className="h-6 w-6 text-orange-600 mx-auto mb-2" />
                <p className="text-sm text-orange-600 font-medium">{txt.totalImports}</p>
                <p className="text-2xl font-black text-orange-700">
                  {formatValue(productData.africanTrade?.total_imports || 0)}
                </p>
              </CardContent>
            </Card>
            <Card className="bg-purple-50 border-purple-200 shadow">
              <CardContent className="p-5 text-center">
                <Globe className="h-6 w-6 text-purple-600 mx-auto mb-2" />
                <p className="text-sm text-purple-600 font-medium">{txt.potential}</p>
                <p className="text-2xl font-black text-purple-700">
                  {formatValue(productData.africanTrade?.intra_african_potential || 0)}
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Exporters Chart */}
            <Card className="shadow-lg">
              <CardHeader>
                <CardTitle className="text-lg font-bold flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-emerald-500" />
                  {txt.topExporters}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <DataBarChart 
                  data={productData.exporters} 
                  barColor="#059669"
                />
              </CardContent>
            </Card>

            {/* Importers Chart */}
            <Card className="shadow-lg">
              <CardHeader>
                <CardTitle className="text-lg font-bold flex items-center gap-2">
                  <TrendingDown className="h-5 w-5 text-orange-500" />
                  {txt.topImporters}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <DataBarChart 
                  data={productData.importers} 
                  barColor="#ea580c"
                />
              </CardContent>
            </Card>
          </div>

          {/* Substitution Opportunities */}
          {productData.substitutionOpps?.length > 0 && (
            <Card className="shadow-lg">
              <CardHeader>
                <CardTitle className="text-lg font-bold">{txt.substitutionOpps}</CardTitle>
                <CardDescription>
                  Potentiel de commerce intra-africain pour ce produit
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {productData.substitutionOpps.slice(0, 9).map((opp, idx) => (
                    <SubstitutionCard key={idx} opp={opp} index={idx} />
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Data Year */}
          <div className="text-center text-xs text-slate-400">
            Données {productData.year} | Source: {productData.source}
          </div>
        </>
      )}

      {/* Empty State */}
      {!loading && !error && !productData && (
        <Card className="bg-slate-50 border-slate-200">
          <CardContent className="py-16 text-center">
            <Package className="h-16 w-16 text-slate-300 mx-auto mb-4" />
            <p className="text-slate-500">{txt.noData}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
