import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../ui/table';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, PieChart, Pie, Cell } from 'recharts';
import { ArrowUpRight, ArrowDownRight, Globe2, TrendingUp, Search, RefreshCw, BarChart3, Filter } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Palette de couleurs africaines moderne
const COLORS = ['#059669', '#0891b2', '#7c3aed', '#dc2626', '#ea580c', '#ca8a04', '#16a34a', '#2563eb', '#9333ea', '#e11d48'];

const formatValue = (value) => {
  if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
  if (value >= 1e6) return `$${(value / 1e6).toFixed(1)}M`;
  if (value >= 1e3) return `$${(value / 1e3).toFixed(0)}K`;
  return `$${value.toFixed(0)}`;
};

export default function OECTradeStats({ language = 'fr' }) {
  const [activeView, setActiveView] = useState('country');
  const [countries, setCountries] = useState([]);
  const [years] = useState([2023, 2022, 2021, 2020, 2019, 2018]); // Années disponibles pour HS Rev. 2017
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Filtres
  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedYear, setSelectedYear] = useState('2022');
  const [selectedFlow, setSelectedFlow] = useState('exports');
  const [hsCode, setHsCode] = useState('');
  const [secondCountry, setSecondCountry] = useState('');
  
  // Résultats
  const [tradeData, setTradeData] = useState(null);
  const [productData, setProductData] = useState(null);
  const [bilateralData, setBilateralData] = useState(null);

  const texts = {
    fr: {
      title: "Statistiques Commerciales OEC",
      subtitle: "Données en temps réel de l'Observatory of Economic Complexity",
      countryView: "Par Pays",
      productView: "Par Produit",
      bilateralView: "Commerce Bilatéral",
      selectCountry: "Sélectionner un pays",
      selectYear: "Année",
      tradeFlow: "Flux commercial",
      exports: "Exportations",
      imports: "Importations",
      hsCodeLabel: "Code HS (4-6 chiffres)",
      hsCodePlaceholder: "Ex: 0901 (Café)",
      search: "Rechercher",
      loading: "Chargement...",
      noData: "Aucune donnée disponible",
      totalValue: "Valeur totale",
      topPartners: "Principaux partenaires",
      topProducts: "Principaux produits",
      africanExporters: "Exportateurs africains",
      country: "Pays",
      value: "Valeur",
      share: "Part",
      sourceLabel: "Source: OEC / BACI Database",
      exporter: "Exportateur",
      importer: "Importateur",
      bilateralTitle: "Commerce bilatéral",
      product: "Produit",
      rank: "Rang",
      dataYear: "Données pour",
      refreshData: "Actualiser",
      popularProducts: "Produits populaires",
      coffee: "Café",
      cocoa: "Cacao", 
      cotton: "Coton",
      gold: "Or",
      oil: "Pétrole",
      diamonds: "Diamants"
    },
    en: {
      title: "OEC Trade Statistics",
      subtitle: "Real-time data from the Observatory of Economic Complexity",
      countryView: "By Country",
      productView: "By Product",
      bilateralView: "Bilateral Trade",
      selectCountry: "Select a country",
      selectYear: "Year",
      tradeFlow: "Trade flow",
      exports: "Exports",
      imports: "Imports",
      hsCodeLabel: "HS Code (4-6 digits)",
      hsCodePlaceholder: "Ex: 0901 (Coffee)",
      search: "Search",
      loading: "Loading...",
      noData: "No data available",
      totalValue: "Total value",
      topPartners: "Top partners",
      topProducts: "Top products",
      africanExporters: "African exporters",
      country: "Country",
      value: "Value",
      share: "Share",
      sourceLabel: "Source: OEC / BACI Database",
      exporter: "Exporter",
      importer: "Importer",
      bilateralTitle: "Bilateral trade",
      product: "Product",
      rank: "Rank",
      dataYear: "Data for",
      refreshData: "Refresh",
      popularProducts: "Popular products",
      coffee: "Coffee",
      cocoa: "Cocoa",
      cotton: "Cotton",
      gold: "Gold",
      oil: "Oil",
      diamonds: "Diamonds"
    }
  };

  const t = texts[language];

  // Popular HS codes for quick selection
  const popularHSCodes = [
    { code: '0901', label: t.coffee },
    { code: '1801', label: t.cocoa },
    { code: '5201', label: t.cotton },
    { code: '7108', label: t.gold },
    { code: '2709', label: t.oil },
    { code: '7102', label: t.diamonds }
  ];

  // Charger les pays africains
  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const response = await axios.get(`${API}/oec/countries?lang=${language}`);
        if (response.data.success) {
          setCountries(response.data.countries);
        }
      } catch (err) {
        console.error('Error loading countries:', err);
      }
    };
    fetchCountries();
  }, [language]);

  // Recherche par pays
  const searchByCountry = useCallback(async () => {
    if (!selectedCountry) return;
    setLoading(true);
    setError(null);
    
    try {
      const endpoint = selectedFlow === 'exports' 
        ? `${API}/oec/exports/${selectedCountry}`
        : `${API}/oec/imports/${selectedCountry}`;
      
      const response = await axios.get(endpoint, {
        params: { year: selectedYear, limit: 20 }
      });
      
      setTradeData(response.data);
    } catch (err) {
      setError(err.message);
      setTradeData(null);
    } finally {
      setLoading(false);
    }
  }, [selectedCountry, selectedYear, selectedFlow]);

  // Recherche par produit
  const searchByProduct = useCallback(async () => {
    if (!hsCode) return;
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get(`${API}/oec/product/${hsCode}`, {
        params: { year: selectedYear, trade_flow: selectedFlow, limit: 30 }
      });
      
      setProductData(response.data);
    } catch (err) {
      setError(err.message);
      setProductData(null);
    } finally {
      setLoading(false);
    }
  }, [hsCode, selectedYear, selectedFlow]);

  // Recherche commerce bilatéral
  const searchBilateral = useCallback(async () => {
    if (!selectedCountry || !secondCountry) return;
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get(
        `${API}/oec/bilateral/${selectedCountry}/${secondCountry}`,
        { params: { year: selectedYear, limit: 20 } }
      );
      
      setBilateralData(response.data);
    } catch (err) {
      setError(err.message);
      setBilateralData(null);
    } finally {
      setLoading(false);
    }
  }, [selectedCountry, secondCountry, selectedYear]);

  // Chart data preparation
  const prepareChartData = (data, limit = 10) => {
    if (!data || !data.data) return [];
    return data.data.slice(0, limit).map((item, index) => ({
      name: item['Exporter Country'] || item['Importer Country'] || `#${index + 1}`,
      value: item['Trade Value'] || 0,
      fill: COLORS[index % COLORS.length]
    }));
  };

  return (
    <div className="space-y-6" data-testid="oec-trade-stats">
      {/* Header moderne et épuré */}
      <Card className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white border-none shadow-2xl overflow-hidden relative">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wMyI+PHBhdGggZD0iTTM2IDM0djItSDI0di0yaDEyek0zNiAyNHYySDI0di0yaDEyeiIvPjwvZz48L2c+PC9zdmc+')] opacity-50"></div>
        <CardHeader className="relative z-10 pb-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-gradient-to-br from-emerald-400 to-cyan-500 rounded-2xl flex items-center justify-center shadow-lg">
                <Globe2 className="w-8 h-8 text-white" />
              </div>
              <div>
                <CardTitle className="text-2xl font-bold tracking-tight">{t.title}</CardTitle>
                <CardDescription className="text-slate-300 mt-1">{t.subtitle}</CardDescription>
              </div>
            </div>
            <Badge className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-3 py-1">
              <TrendingUp className="w-3 h-3 mr-1" />
              Live Data
            </Badge>
          </div>
        </CardHeader>
      </Card>

      {/* Navigation par onglets - Design moderne */}
      <Tabs value={activeView} onValueChange={setActiveView} className="space-y-6">
        <TabsList className="grid w-full grid-cols-3 bg-slate-100 p-1.5 rounded-xl h-auto">
          <TabsTrigger 
            value="country" 
            className="data-[state=active]:bg-white data-[state=active]:shadow-md data-[state=active]:text-slate-900 rounded-lg py-3 font-medium transition-all"
            data-testid="tab-country"
          >
            <Globe2 className="w-4 h-4 mr-2" />
            {t.countryView}
          </TabsTrigger>
          <TabsTrigger 
            value="product"
            className="data-[state=active]:bg-white data-[state=active]:shadow-md data-[state=active]:text-slate-900 rounded-lg py-3 font-medium transition-all"
            data-testid="tab-product"
          >
            <BarChart3 className="w-4 h-4 mr-2" />
            {t.productView}
          </TabsTrigger>
          <TabsTrigger 
            value="bilateral"
            className="data-[state=active]:bg-white data-[state=active]:shadow-md data-[state=active]:text-slate-900 rounded-lg py-3 font-medium transition-all"
            data-testid="tab-bilateral"
          >
            <ArrowUpRight className="w-4 h-4 mr-2" />
            {t.bilateralView}
          </TabsTrigger>
        </TabsList>

        {/* Vue par Pays */}
        <TabsContent value="country" className="space-y-6 mt-6">
          <Card className="shadow-lg border-slate-200">
            <CardContent className="pt-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="space-y-2">
                  <Label className="text-sm font-medium text-slate-700">{t.selectCountry}</Label>
                  <Select value={selectedCountry} onValueChange={setSelectedCountry}>
                    <SelectTrigger data-testid="country-select" className="bg-white">
                      <SelectValue placeholder={t.selectCountry} />
                    </SelectTrigger>
                    <SelectContent>
                      {countries.map((country) => (
                        <SelectItem key={country.iso3} value={country.iso3}>
                          {country.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label className="text-sm font-medium text-slate-700">{t.selectYear}</Label>
                  <Select value={selectedYear} onValueChange={setSelectedYear}>
                    <SelectTrigger className="bg-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {years.map((year) => (
                        <SelectItem key={year} value={year.toString()}>{year}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label className="text-sm font-medium text-slate-700">{t.tradeFlow}</Label>
                  <Select value={selectedFlow} onValueChange={setSelectedFlow}>
                    <SelectTrigger className="bg-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="exports">{t.exports}</SelectItem>
                      <SelectItem value="imports">{t.imports}</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex items-end">
                  <Button 
                    onClick={searchByCountry}
                    disabled={!selectedCountry || loading}
                    className="w-full bg-slate-900 hover:bg-slate-800 text-white font-medium"
                    data-testid="search-country-btn"
                  >
                    {loading ? (
                      <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    ) : (
                      <Search className="w-4 h-4 mr-2" />
                    )}
                    {loading ? t.loading : t.search}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Résultats par pays */}
          {tradeData && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Carte récapitulative */}
              <Card className="shadow-lg">
                <CardHeader className="bg-gradient-to-r from-emerald-50 to-cyan-50 border-b">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg font-semibold text-slate-800">
                      {selectedFlow === 'exports' ? t.exports : t.imports} - {tradeData.country?.name_fr || selectedCountry}
                    </CardTitle>
                    <Badge variant="outline" className="text-emerald-700 border-emerald-300">
                      {t.dataYear} {selectedYear}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="pt-6">
                  <div className="text-center mb-6">
                    <p className="text-sm text-slate-500 mb-1">{t.totalValue}</p>
                    <p className="text-4xl font-bold text-slate-900">{formatValue(tradeData.total_value || 0)}</p>
                    <p className="text-sm text-slate-500 mt-2">{tradeData.total_products} {t.topProducts}</p>
                  </div>
                  
                  {/* Chart */}
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={prepareChartData(tradeData)} layout="vertical">
                        <XAxis type="number" tickFormatter={(v) => formatValue(v)} />
                        <YAxis type="category" dataKey="name" width={100} tick={{ fontSize: 11 }} />
                        <Tooltip formatter={(v) => formatValue(v)} />
                        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                          {prepareChartData(tradeData).map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.fill} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>

              {/* Table des données */}
              <Card className="shadow-lg">
                <CardHeader className="border-b">
                  <CardTitle className="text-lg font-semibold">{t.topPartners}</CardTitle>
                </CardHeader>
                <CardContent className="p-0">
                  <div className="max-h-96 overflow-auto">
                    <Table>
                      <TableHeader className="sticky top-0 bg-slate-50">
                        <TableRow>
                          <TableHead className="w-12">{t.rank}</TableHead>
                          <TableHead>{t.product}</TableHead>
                          <TableHead className="text-right">{t.value}</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {tradeData.data?.slice(0, 15).map((item, idx) => (
                          <TableRow key={idx} className="hover:bg-slate-50">
                            <TableCell className="font-medium text-slate-500">{idx + 1}</TableCell>
                            <TableCell className="font-medium">{item['HS4'] || item['HS6'] || '-'}</TableCell>
                            <TableCell className="text-right font-semibold text-emerald-700">
                              {formatValue(item['Trade Value'] || 0)}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </TabsContent>

        {/* Vue par Produit */}
        <TabsContent value="product" className="space-y-6 mt-6">
          <Card className="shadow-lg border-slate-200">
            <CardContent className="pt-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="space-y-2 md:col-span-2">
                  <Label className="text-sm font-medium text-slate-700">{t.hsCodeLabel}</Label>
                  <Input
                    value={hsCode}
                    onChange={(e) => setHsCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                    placeholder={t.hsCodePlaceholder}
                    className="bg-white"
                    data-testid="hs-code-input"
                  />
                  {/* Quick select buttons */}
                  <div className="flex flex-wrap gap-2 mt-2">
                    <span className="text-xs text-slate-500">{t.popularProducts}:</span>
                    {popularHSCodes.map((item) => (
                      <button
                        key={item.code}
                        onClick={() => setHsCode(item.code)}
                        className={`text-xs px-2 py-1 rounded-full transition-all ${
                          hsCode === item.code 
                            ? 'bg-slate-900 text-white' 
                            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                        }`}
                      >
                        {item.label}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label className="text-sm font-medium text-slate-700">{t.selectYear}</Label>
                  <Select value={selectedYear} onValueChange={setSelectedYear}>
                    <SelectTrigger className="bg-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {years.map((year) => (
                        <SelectItem key={year} value={year.toString()}>{year}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex items-end">
                  <Button 
                    onClick={searchByProduct}
                    disabled={!hsCode || loading}
                    className="w-full bg-slate-900 hover:bg-slate-800 text-white font-medium"
                    data-testid="search-product-btn"
                  >
                    {loading ? (
                      <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    ) : (
                      <Search className="w-4 h-4 mr-2" />
                    )}
                    {loading ? t.loading : t.search}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Résultats par produit */}
          {productData && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Carte récapitulative */}
              <Card className="shadow-lg">
                <CardHeader className="bg-gradient-to-r from-violet-50 to-purple-50 border-b">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg font-semibold text-slate-800">
                      HS {productData.hs_code} - {selectedFlow === 'exports' ? t.exports : t.imports}
                    </CardTitle>
                    <Badge variant="outline" className="text-violet-700 border-violet-300">
                      {t.dataYear} {selectedYear}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="pt-6">
                  <div className="text-center mb-6">
                    <p className="text-sm text-slate-500 mb-1">{t.totalValue}</p>
                    <p className="text-4xl font-bold text-slate-900">{formatValue(productData.total_value || 0)}</p>
                    <p className="text-sm text-slate-500 mt-2">{productData.total_countries} {t.country}</p>
                  </div>
                  
                  {/* Pie Chart */}
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={prepareChartData(productData, 8)}
                          cx="50%"
                          cy="50%"
                          innerRadius={50}
                          outerRadius={80}
                          paddingAngle={2}
                          dataKey="value"
                          label={({ name }) => name}
                        >
                          {prepareChartData(productData, 8).map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.fill} />
                          ))}
                        </Pie>
                        <Tooltip formatter={(v) => formatValue(v)} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>

              {/* Table des pays */}
              <Card className="shadow-lg">
                <CardHeader className="border-b">
                  <CardTitle className="text-lg font-semibold">
                    {selectedFlow === 'exports' ? t.africanExporters : t.topPartners}
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-0">
                  <div className="max-h-96 overflow-auto">
                    <Table>
                      <TableHeader className="sticky top-0 bg-slate-50">
                        <TableRow>
                          <TableHead className="w-12">{t.rank}</TableHead>
                          <TableHead>{t.country}</TableHead>
                          <TableHead className="text-right">{t.value}</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {productData.data?.slice(0, 20).map((item, idx) => (
                          <TableRow key={idx} className="hover:bg-slate-50">
                            <TableCell className="font-medium text-slate-500">{idx + 1}</TableCell>
                            <TableCell className="font-medium">
                              {item['Exporter Country'] || item['Importer Country'] || '-'}
                            </TableCell>
                            <TableCell className="text-right font-semibold text-violet-700">
                              {formatValue(item['Trade Value'] || 0)}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </TabsContent>

        {/* Vue Bilatérale */}
        <TabsContent value="bilateral" className="space-y-6 mt-6">
          <Card className="shadow-lg border-slate-200">
            <CardContent className="pt-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="space-y-2">
                  <Label className="text-sm font-medium text-slate-700">{t.exporter}</Label>
                  <Select value={selectedCountry} onValueChange={setSelectedCountry}>
                    <SelectTrigger data-testid="exporter-select" className="bg-white">
                      <SelectValue placeholder={t.selectCountry} />
                    </SelectTrigger>
                    <SelectContent>
                      {countries.map((country) => (
                        <SelectItem key={country.iso3} value={country.iso3}>
                          {country.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label className="text-sm font-medium text-slate-700">{t.importer}</Label>
                  <Select value={secondCountry} onValueChange={setSecondCountry}>
                    <SelectTrigger data-testid="importer-select" className="bg-white">
                      <SelectValue placeholder={t.selectCountry} />
                    </SelectTrigger>
                    <SelectContent>
                      {countries.filter(c => c.iso3 !== selectedCountry).map((country) => (
                        <SelectItem key={country.iso3} value={country.iso3}>
                          {country.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label className="text-sm font-medium text-slate-700">{t.selectYear}</Label>
                  <Select value={selectedYear} onValueChange={setSelectedYear}>
                    <SelectTrigger className="bg-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {years.map((year) => (
                        <SelectItem key={year} value={year.toString()}>{year}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex items-end">
                  <Button 
                    onClick={searchBilateral}
                    disabled={!selectedCountry || !secondCountry || loading}
                    className="w-full bg-slate-900 hover:bg-slate-800 text-white font-medium"
                    data-testid="search-bilateral-btn"
                  >
                    {loading ? (
                      <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    ) : (
                      <Search className="w-4 h-4 mr-2" />
                    )}
                    {loading ? t.loading : t.search}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Résultats bilatéraux */}
          {bilateralData && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Carte récapitulative */}
              <Card className="shadow-lg">
                <CardHeader className="bg-gradient-to-r from-orange-50 to-amber-50 border-b">
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="text-lg font-semibold text-slate-800">
                        {t.bilateralTitle}
                      </CardTitle>
                      <CardDescription>
                        {bilateralData.exporter?.name_fr} → {bilateralData.importer?.name_fr}
                      </CardDescription>
                    </div>
                    <Badge variant="outline" className="text-orange-700 border-orange-300">
                      {t.dataYear} {selectedYear}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="pt-6">
                  <div className="text-center mb-6">
                    <p className="text-sm text-slate-500 mb-1">{t.totalValue}</p>
                    <p className="text-4xl font-bold text-slate-900">{formatValue(bilateralData.total_value || 0)}</p>
                    <div className="flex items-center justify-center gap-2 mt-3">
                      <span className="text-lg font-medium">{bilateralData.exporter?.name_fr}</span>
                      <ArrowUpRight className="w-5 h-5 text-orange-500" />
                      <span className="text-lg font-medium">{bilateralData.importer?.name_fr}</span>
                    </div>
                  </div>
                  
                  {/* Bar Chart */}
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={prepareChartData(bilateralData, 8)}>
                        <XAxis dataKey="name" tick={{ fontSize: 10 }} angle={-45} textAnchor="end" height={60} />
                        <YAxis tickFormatter={(v) => formatValue(v)} />
                        <Tooltip formatter={(v) => formatValue(v)} />
                        <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                          {prepareChartData(bilateralData, 8).map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.fill} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>

              {/* Table des produits échangés */}
              <Card className="shadow-lg">
                <CardHeader className="border-b">
                  <CardTitle className="text-lg font-semibold">{t.topProducts}</CardTitle>
                </CardHeader>
                <CardContent className="p-0">
                  <div className="max-h-96 overflow-auto">
                    <Table>
                      <TableHeader className="sticky top-0 bg-slate-50">
                        <TableRow>
                          <TableHead className="w-12">{t.rank}</TableHead>
                          <TableHead>{t.product}</TableHead>
                          <TableHead className="text-right">{t.value}</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {bilateralData.data?.slice(0, 15).map((item, idx) => (
                          <TableRow key={idx} className="hover:bg-slate-50">
                            <TableCell className="font-medium text-slate-500">{idx + 1}</TableCell>
                            <TableCell className="font-medium">{item['HS4'] || '-'}</TableCell>
                            <TableCell className="text-right font-semibold text-orange-700">
                              {formatValue(item['Trade Value'] || 0)}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </TabsContent>
      </Tabs>

      {/* Message d'erreur */}
      {error && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="py-4">
            <p className="text-red-700 text-center">{error}</p>
          </CardContent>
        </Card>
      )}

      {/* Footer source */}
      <Card className="bg-slate-50 border-slate-200">
        <CardContent className="py-3">
          <p className="text-xs text-slate-500 text-center">
            {t.sourceLabel}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
