/**
 * Trade Opportunities Summary Component
 * Displays aggregate view of intra-African trade opportunities
 * USING REAL DATA from OEC API
 */
import React, { useState, useEffect, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { 
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, 
  CartesianGrid, Tooltip, PieChart, Pie, Cell 
} from 'recharts';
import { 
  TrendingUp, DollarSign, Globe, Package, 
  ArrowUpRight, Loader2, AlertCircle, Database
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Color palette
const COLORS = ['#059669', '#0891b2', '#7c3aed', '#dc2626', '#ea580c', '#ca8a04', '#16a34a', '#2563eb'];

// Stat Card Component
const StatCard = ({ title, value, icon: Icon, trend, color = "emerald" }) => {
  const colorClasses = {
    emerald: "bg-emerald-100 text-emerald-600",
    blue: "bg-blue-100 text-blue-600",
    purple: "bg-purple-100 text-purple-600",
    orange: "bg-orange-100 text-orange-600"
  };

  return (
    <Card className="bg-white border-slate-200 shadow-lg hover:shadow-xl transition-shadow">
      <CardContent className="p-6">
        <div className="flex items-center gap-4">
          <div className={`flex-shrink-0 h-12 w-12 flex items-center justify-center rounded-full ${colorClasses[color]}`}>
            <Icon className="h-6 w-6" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-slate-500 truncate">{title}</p>
            <p className="text-2xl font-bold text-slate-900">{value}</p>
            {trend && (
              <div className="flex items-center gap-1 mt-1">
                <ArrowUpRight className="h-3 w-3 text-emerald-500" />
                <span className="text-xs text-emerald-600 font-medium">{trend}</span>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// Custom Tooltip for charts
const CustomTooltip = ({ active, payload, label, valueLabel }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white/95 backdrop-blur-sm p-3 border border-slate-200 rounded-lg shadow-lg text-sm">
        <p className="font-bold text-slate-800">{label}</p>
        <p className="text-emerald-600 font-semibold">
          {valueLabel}: {payload[0].value}
        </p>
      </div>
    );
  }
  return null;
};

// Format large numbers
const formatValue = (value) => {
  if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
  if (value >= 1e6) return `$${(value / 1e6).toFixed(1)}M`;
  if (value >= 1e3) return `$${(value / 1e3).toFixed(0)}K`;
  return `$${value?.toLocaleString() || 0}`;
};

export default function OpportunitySummary({ language = 'fr' }) {
  const { i18n } = useTranslation();
  const currentLang = i18n.language || language;
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  // Fetch real trade opportunities data
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // Fetch summary from new API endpoint
        const response = await axios.get(`${API}/substitution/summary?lang=${currentLang}`);
        const summaryData = response.data;
        
        // Format top import opportunities for chart
        const topImports = (summaryData.top_import_opportunities || []).slice(0, 8).map((opp, idx) => ({
          name: opp.imported_product?.name || `HS ${opp.imported_product?.hs_code}`,
          value: Math.round((opp.substitution_potential || 0) / 1000000),
          country: opp.country
        }));
        
        // Format sectors for pie chart
        const sectors = (summaryData.top_sectors || []).map((sector, idx) => ({
          name: sector.name,
          value: Math.round(sector.value / 1000000),
          count: sector.count
        }));

        setData({
          summary: summaryData.summary,
          topImports,
          topExports: (summaryData.top_export_opportunities || []).slice(0, 8).map(opp => ({
            name: opp.exportable_product?.name || `HS ${opp.exportable_product?.hs_code}`,
            value: Math.round((opp.estimated_capture || 0) / 1000000),
            country: opp.country
          })),
          sectors,
          source: summaryData.data_source || "OEC"
        });
        
      } catch (err) {
        console.error('Error fetching opportunities summary:', err);
        setError('Erreur lors du chargement des données');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [currentLang]);

  const texts = {
    fr: {
      title: "Résumé des Opportunités Commerciales",
      subtitle: "Vue agrégée du potentiel commercial intra-africain (Données Réelles OEC 2022)",
      importPotential: "Potentiel de Substitution",
      exportPotential: "Potentiel d'Export",
      totalPotential: "Potentiel Total",
      countriesAnalyzed: "Pays Analysés",
      topSubstitution: "Top Opportunités de Substitution",
      topSectors: "Secteurs Prioritaires",
      loading: "Chargement des données réelles...",
      noData: "Aucune donnée disponible",
      valueInMillions: "Valeur (M USD)",
      source: "Source",
      realData: "DONNÉES RÉELLES"
    },
    en: {
      title: "Trade Opportunities Summary",
      subtitle: "Aggregate view of intra-African trade potential (Real OEC Data 2022)",
      importPotential: "Substitution Potential",
      exportPotential: "Export Potential",
      totalPotential: "Total Potential",
      countriesAnalyzed: "Countries Analyzed",
      topSubstitution: "Top Substitution Opportunities",
      topSectors: "Priority Sectors",
      loading: "Loading real data...",
      noData: "No data available",
      valueInMillions: "Value (M USD)",
      source: "Source",
      realData: "REAL DATA"
    }
  };
  const txt = texts[currentLang] || texts.fr;

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-20 space-y-4">
        <Loader2 className="h-10 w-10 animate-spin text-emerald-600" />
        <p className="text-slate-500 font-medium">{txt.loading}</p>
        <p className="text-xs text-slate-400">Analyse des 5 principales économies africaines...</p>
      </div>
    );
  }

  if (error) {
    return (
      <Card className="bg-red-50 border-red-200">
        <CardContent className="py-10 text-center">
          <AlertCircle className="h-8 w-8 text-red-500 mx-auto mb-2" />
          <p className="text-red-700">{error}</p>
        </CardContent>
      </Card>
    );
  }

  if (!data) {
    return (
      <Card className="bg-slate-50 border-slate-200">
        <CardContent className="py-16 text-center">
          <p className="text-slate-500">{txt.noData}</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6" data-testid="opportunity-summary">
      {/* Header */}
      <div className="text-center">
        <div className="flex items-center justify-center gap-3 mb-2">
          <TrendingUp className="h-8 w-8 text-emerald-600" />
          <h2 className="text-3xl font-black text-slate-900 uppercase tracking-tight">
            {txt.title}
          </h2>
        </div>
        <p className="text-slate-500">{txt.subtitle}</p>
        <Badge className="mt-2 bg-emerald-100 text-emerald-700">
          <Database className="h-3 w-3 mr-1" />
          {txt.realData} - {data.source}
        </Badge>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title={txt.importPotential}
          value={formatValue(data.summary?.total_import_substitution_potential || 0)}
          icon={TrendingUp}
          color="emerald"
        />
        <StatCard
          title={txt.exportPotential}
          value={formatValue(data.summary?.total_export_potential || 0)}
          icon={Globe}
          color="blue"
        />
        <StatCard
          title={txt.totalPotential}
          value={formatValue(data.summary?.total_combined || 0)}
          icon={DollarSign}
          color="purple"
        />
        <StatCard
          title={txt.countriesAnalyzed}
          value={data.summary?.countries_analyzed || 5}
          icon={Package}
          color="orange"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Substitution Opportunities Bar Chart */}
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="text-lg font-bold">{txt.topSubstitution}</CardTitle>
          </CardHeader>
          <CardContent>
            {data.topImports?.length > 0 ? (
              <div className="h-[350px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={data.topImports}
                    layout="vertical"
                    margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" tick={{ fontSize: 11 }} />
                    <YAxis 
                      type="category" 
                      dataKey="name" 
                      tick={{ fontSize: 10 }} 
                      width={95}
                    />
                    <Tooltip 
                      content={<CustomTooltip valueLabel={txt.valueInMillions} />}
                    />
                    <Bar dataKey="value" fill="#059669" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <p className="text-center text-slate-400 py-10">Aucune donnée</p>
            )}
          </CardContent>
        </Card>

        {/* Top Sectors Pie Chart */}
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="text-lg font-bold">{txt.topSectors}</CardTitle>
          </CardHeader>
          <CardContent>
            {data.sectors?.length > 0 ? (
              <div className="h-[350px]">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={data.sectors}
                      cx="50%"
                      cy="50%"
                      outerRadius={120}
                      innerRadius={60}
                      paddingAngle={2}
                      dataKey="value"
                      label={({ name, value }) => `${name}: $${value}M`}
                      labelLine={{ stroke: '#64748b', strokeWidth: 1 }}
                    >
                      {data.sectors.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value) => [`$${value}M`, 'Valeur']}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <p className="text-center text-slate-400 py-10">Aucune donnée</p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Top Opportunities List */}
      {data.topImports?.length > 0 && (
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="text-lg font-bold">Détails des Opportunités</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {data.topImports.slice(0, 6).map((opp, idx) => (
                <div 
                  key={idx}
                  className="p-4 bg-gradient-to-br from-slate-50 to-white rounded-lg border border-slate-200 hover:border-emerald-400 transition-colors"
                >
                  <div className="flex items-center justify-between mb-2">
                    <Badge variant="outline" className="text-xs font-mono">#{idx + 1}</Badge>
                    <span className="text-xs text-slate-500">{opp.country}</span>
                  </div>
                  <h4 className="font-bold text-slate-800 text-sm mb-1 line-clamp-2">
                    {opp.name}
                  </h4>
                  <p className="text-lg font-black text-emerald-600">
                    ${opp.value}M
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Source footer */}
      <div className="text-center text-xs text-slate-400">
        {txt.source}: {data.source} | Données 2022
      </div>
    </div>
  );
}
