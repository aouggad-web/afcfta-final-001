import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import EnhancedCountrySelector from './EnhancedCountrySelector';
import { Wheat, Beef, Fish, TrendingUp, Award, AlertTriangle, Loader2, Info } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CHART_COLORS = ['#10b981', '#059669', '#047857', '#065f46', '#064e3b', '#22c55e', '#16a34a', '#15803d'];

function ProductionAgriculture({ language = 'fr' }) {
  const [selectedCountry, setSelectedCountry] = useState('CIV');
  const [faostatData, setFaostatData] = useState(null);
  const [faostatStats, setFaostatStats] = useState(null);
  const [topProducers, setTopProducers] = useState({});
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('crops');

  // Translations
  const texts = {
    fr: {
      title: "Production Agricole FAOSTAT",
      subtitle: "Données officielles FAO - Production agricole, élevage et pêche (2020-2023)",
      countries: "pays",
      products: "produits",
      loading: "Chargement des données FAOSTAT...",
      noData: "Données non disponibles",
      noDataDesc: "Aucune donnée FAOSTAT disponible pour ce pays.",
      data: "Données",
      agriGdp: "Agriculture / PIB",
      agriEmployment: "Emploi agricole",
      arableLand: "Terres arables",
      foodImports: "Import. alimentaires",
      cropsTab: "Productions Végétales",
      livestockTab: "Élevage",
      fisheriesTab: "Pêche",
      mainCrops: "Principales Cultures",
      productionDist: "Répartition de la Production 2023",
      productionDetails: "Détails de Production 2023",
      tonnes: "tonnes",
      africa: "Afrique",
      evolution: "Évolution de la Production (2020-2023)",
      rankings: "Classements Africains",
      livestock2023: "Cheptel 2023",
      noLivestockData: "Données d'élevage non disponibles pour ce pays",
      fisheries2023: "Pêche et Aquaculture 2023",
      capture: "Pêche de capture",
      inAfrica: "en Afrique",
      aquaculture: "Aquaculture",
      noFisheriesData: "Données de pêche non disponibles pour ce pays",
      source: "Source:",
      sourceNote: "Les données sont issues de FAOSTAT (FAO) et des instituts statistiques nationaux. Les chiffres 2024 sont des estimations préliminaires."
    },
    en: {
      title: "FAOSTAT Agricultural Production",
      subtitle: "Official FAO data - Agricultural production, livestock and fisheries (2020-2023)",
      countries: "countries",
      products: "products",
      loading: "Loading FAOSTAT data...",
      noData: "Data not available",
      noDataDesc: "No FAOSTAT data available for this country.",
      data: "Data",
      agriGdp: "Agriculture / GDP",
      agriEmployment: "Agricultural employment",
      arableLand: "Arable land",
      foodImports: "Food imports",
      cropsTab: "Crop Production",
      livestockTab: "Livestock",
      fisheriesTab: "Fisheries",
      mainCrops: "Main Crops",
      productionDist: "Production Distribution 2023",
      productionDetails: "Production Details 2023",
      tonnes: "tonnes",
      africa: "Africa",
      evolution: "Production Evolution (2020-2023)",
      rankings: "African Rankings",
      livestock2023: "Livestock 2023",
      noLivestockData: "Livestock data not available for this country",
      fisheries2023: "Fisheries and Aquaculture 2023",
      capture: "Capture fisheries",
      inAfrica: "in Africa",
      aquaculture: "Aquaculture",
      noFisheriesData: "Fisheries data not available for this country",
      source: "Source:",
      sourceNote: "Data is from FAOSTAT (FAO) and national statistical institutes. 2024 figures are preliminary estimates."
    }
  };
  const t = texts[language] || texts.fr;

  useEffect(() => {
    fetchFaostatStats();
  }, []);

  useEffect(() => {
    if (selectedCountry) {
      fetchFaostatData(selectedCountry);
    }
  }, [selectedCountry]);

  const fetchFaostatStats = async () => {
    try {
      const response = await axios.get(`${API}/production/faostat/statistics`);
      setFaostatStats(response.data);
    } catch (error) {
      console.error('Error fetching FAOSTAT statistics:', error);
    }
  };

  const fetchFaostatData = async (countryIso3) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/production/faostat/${countryIso3}`);
      setFaostatData(response.data);
      
      // Fetch top producers for main crops
      if (response.data.main_crops) {
        const producersData = {};
        for (const crop of response.data.main_crops.slice(0, 3)) {
          try {
            const prodResponse = await axios.get(`${API}/production/faostat/top-producers/${crop}`);
            if (prodResponse.data.producers && prodResponse.data.producers.length > 0) {
              producersData[crop] = prodResponse.data.producers;
            }
          } catch (err) {
            // Silent fail for individual crop rankings
          }
        }
        setTopProducers(producersData);
      }
    } catch (error) {
      console.error('Error fetching FAOSTAT data:', error);
      setFaostatData(null);
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(0)}K`;
    return num?.toLocaleString() || '0';
  };

  const prepareEvolutionData = () => {
    if (!faostatData?.evolution) return [];
    
    const years = [2020, 2021, 2022, 2023];
    return years.map(year => {
      const dataPoint = { year };
      Object.entries(faostatData.evolution).forEach(([crop, records]) => {
        const yearRecord = records.find(r => r.year === year);
        if (yearRecord) {
          dataPoint[crop] = yearRecord.value;
        }
      });
      return dataPoint;
    });
  };

  const prepareCropsPieData = () => {
    if (!faostatData?.production_2023) return [];
    
    return Object.entries(faostatData.production_2023)
      .slice(0, 6)
      .map(([name, data], index) => ({
        name,
        value: data.value,
        fill: CHART_COLORS[index % CHART_COLORS.length]
      }));
  };

  const prepareLivestockData = () => {
    if (!faostatData?.livestock_2023) return [];
    
    return Object.entries(faostatData.livestock_2023).map(([name, data]) => ({
      name,
      value: data.value,
      unit: data.unit,
      rank: data.rank_africa
    }));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="bg-gradient-to-r from-green-600 via-emerald-600 to-teal-600 text-white shadow-xl overflow-hidden">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <CardTitle className="text-3xl font-bold flex items-center gap-3">
                <Wheat className="w-8 h-8" />
                {t.title}
              </CardTitle>
              <CardDescription className="text-green-100 text-lg mt-2">
                {t.subtitle}
              </CardDescription>
            </div>
            {faostatStats && (
              <div className="text-right">
                <Badge className="bg-white/20 text-white hover:bg-white/30">
                  {faostatStats.total_countries} {t.countries}
                </Badge>
                <p className="text-xs text-green-200 mt-1">{faostatStats.total_commodities} {t.products}</p>
              </div>
            )}
          </div>
        </CardHeader>
      </Card>

      {/* Enhanced Country Selector */}
      <div style={{ position: 'relative', zIndex: 100 }}>
        <Card className="border-2 border-green-200 shadow-lg" style={{ overflow: 'visible' }}>
          <CardContent className="pt-6" style={{ overflow: 'visible' }}>
            <EnhancedCountrySelector
              value={selectedCountry}
              onChange={setSelectedCountry}
              label={language === 'en' ? "Select an African country" : "Sélectionner un pays africain"}
              variant="prominent"
              language={language}
            />
          </CardContent>
        </Card>
      </div>

      {/* Loading State */}
      {loading && (
        <Card className="animate-pulse">
          <CardContent className="flex items-center justify-center h-48">
            <div className="text-center">
              <Loader2 className="w-12 h-12 animate-spin text-green-600 mx-auto" />
              <p className="mt-4 text-gray-600">{t.loading}</p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* No Data State */}
      {!loading && (!faostatData || faostatData.message) && (
        <Card className="border-l-4 border-l-amber-500">
          <CardContent className="flex items-center gap-4 py-8">
            <AlertTriangle className="w-12 h-12 text-amber-500" />
            <div>
              <h3 className="font-bold text-lg text-gray-800">{t.noData}</h3>
              <p className="text-gray-600">{t.noDataDesc}</p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Main Content */}
      {!loading && faostatData && !faostatData.message && (
        <>
          {/* Country Overview */}
          <Card className="bg-gradient-to-r from-green-50 to-emerald-50 border-green-200">
            <CardHeader className="pb-2">
              <CardTitle className="text-2xl text-green-800 flex items-center gap-3">
                <span className="text-4xl">{faostatData.region === 'Afrique du Nord' ? '🌍' : faostatData.region === 'Afrique de l\'Ouest' ? '🌴' : '🌿'}</span>
                {faostatData.country_name}
              </CardTitle>
              <CardDescription className="text-green-700 flex items-center gap-2">
                <Badge variant="outline" className="border-green-500 text-green-700">{faostatData.region}</Badge>
                <Badge variant="outline" className="border-green-500 text-green-700">{t.data} {faostatData.data_year}</Badge>
              </CardDescription>
            </CardHeader>
            <CardContent>
              {/* Key Indicators */}
              {faostatData.key_indicators && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                  {faostatData.key_indicators.agri_gdp_percent && (
                    <div className="bg-white p-4 rounded-xl shadow-sm border border-green-100">
                      <p className="text-xs text-gray-500 uppercase tracking-wide">{t.agriGdp}</p>
                      <p className="text-2xl font-bold text-green-700">{faostatData.key_indicators.agri_gdp_percent}%</p>
                    </div>
                  )}
                  {faostatData.key_indicators.agri_employment_percent && (
                    <div className="bg-white p-4 rounded-xl shadow-sm border border-green-100">
                      <p className="text-xs text-gray-500 uppercase tracking-wide">{t.agriEmployment}</p>
                      <p className="text-2xl font-bold text-green-700">{faostatData.key_indicators.agri_employment_percent}%</p>
                    </div>
                  )}
                  {faostatData.key_indicators.arable_land_ha && (
                    <div className="bg-white p-4 rounded-xl shadow-sm border border-green-100">
                      <p className="text-xs text-gray-500 uppercase tracking-wide">{t.arableLand}</p>
                      <p className="text-2xl font-bold text-green-700">{formatNumber(faostatData.key_indicators.arable_land_ha)} ha</p>
                    </div>
                  )}
                  {faostatData.key_indicators.food_import_value_mln_usd && (
                    <div className="bg-white p-4 rounded-xl shadow-sm border border-green-100">
                      <p className="text-xs text-gray-500 uppercase tracking-wide">{t.foodImports}</p>
                      <p className="text-2xl font-bold text-amber-600">${formatNumber(faostatData.key_indicators.food_import_value_mln_usd * 1000000)}</p>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Tabs for different sections */}
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-3 bg-green-100 p-1 h-auto">
              <TabsTrigger value="crops" className="data-[state=active]:bg-green-600 data-[state=active]:text-white py-3">
                <Wheat className="w-4 h-4 mr-2" /> {t.cropsTab}
              </TabsTrigger>
              <TabsTrigger value="livestock" className="data-[state=active]:bg-green-600 data-[state=active]:text-white py-3">
                <Beef className="w-4 h-4 mr-2" /> {t.livestockTab}
              </TabsTrigger>
              <TabsTrigger value="fisheries" className="data-[state=active]:bg-green-600 data-[state=active]:text-white py-3">
                <Fish className="w-4 h-4 mr-2" /> {t.fisheriesTab}
              </TabsTrigger>
            </TabsList>

            {/* Crops Tab */}
            <TabsContent value="crops" className="space-y-6">
              {/* Main Crops */}
              {faostatData.main_crops && (
                <Card>
                  <CardHeader className="bg-gradient-to-r from-green-50 to-emerald-50">
                    <CardTitle className="text-xl text-green-700 flex items-center gap-2">
                      <Wheat className="w-5 h-5" /> {t.mainCrops}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-4">
                    <div className="flex flex-wrap gap-2">
                      {faostatData.main_crops.map((crop, index) => (
                        <Badge 
                          key={crop} 
                          className="text-sm py-1 px-3"
                          style={{ backgroundColor: CHART_COLORS[index % CHART_COLORS.length], color: 'white' }}
                        >
                          {crop}
                        </Badge>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Production Details */}
              {faostatData.production_2023 && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Pie Chart */}
                  <Card className="shadow-lg">
                    <CardHeader>
                      <CardTitle className="text-lg text-gray-700">{t.productionDist}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                          <Pie
                            data={prepareCropsPieData()}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                            outerRadius={100}
                            fill="#8884d8"
                            dataKey="value"
                          >
                            {prepareCropsPieData().map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={entry.fill} />
                            ))}
                          </Pie>
                          <Tooltip formatter={(value) => formatNumber(value) + ' ' + t.tonnes} />
                        </PieChart>
                      </ResponsiveContainer>
                    </CardContent>
                  </Card>

                  {/* Production Table */}
                  <Card className="shadow-lg">
                    <CardHeader>
                      <CardTitle className="text-lg text-gray-700">{t.productionDetails}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3 max-h-80 overflow-y-auto">
                        {Object.entries(faostatData.production_2023).map(([crop, data], index) => (
                          <div key={crop} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                            <div className="flex items-center gap-3">
                              <div 
                                className="w-3 h-3 rounded-full" 
                                style={{ backgroundColor: CHART_COLORS[index % CHART_COLORS.length] }}
                              />
                              <div>
                                <p className="font-medium text-gray-800">{crop}</p>
                                <p className="text-xs text-gray-500">{formatNumber(data.area_ha)} ha</p>
                              </div>
                            </div>
                            <div className="text-right">
                              <p className="font-bold text-green-700">{formatNumber(data.value)} t</p>
                              {data.rank_africa && (
                                <Badge variant="outline" className="text-xs">
                                  <Award className="w-3 h-3 mr-1" /> #{data.rank_africa} {t.africa}
                                </Badge>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}

              {/* Evolution Chart */}
              {faostatData.evolution && Object.keys(faostatData.evolution).length > 0 && (
                <Card className="shadow-lg">
                  <CardHeader className="bg-gradient-to-r from-green-50 to-teal-50">
                    <CardTitle className="text-xl text-green-700 flex items-center gap-2">
                      <TrendingUp className="w-5 h-5" /> {t.evolution}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <ResponsiveContainer width="100%" height={350}>
                      <LineChart data={prepareEvolutionData()}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="year" />
                        <YAxis tickFormatter={formatNumber} />
                        <Tooltip formatter={(value) => formatNumber(value) + ' ' + t.tonnes} />
                        <Legend />
                        {Object.keys(faostatData.evolution).map((crop, index) => (
                          <Line 
                            key={crop}
                            type="monotone" 
                            dataKey={crop} 
                            stroke={CHART_COLORS[index % CHART_COLORS.length]}
                            strokeWidth={3}
                            dot={{ r: 5 }}
                            activeDot={{ r: 8 }}
                          />
                        ))}
                      </LineChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              )}

              {/* Top Producers Rankings */}
              {Object.keys(topProducers).length > 0 && (
                <Card className="shadow-lg">
                  <CardHeader>
                    <CardTitle className="text-xl text-gray-700 flex items-center gap-2">
                      <Award className="w-5 h-5 text-amber-500" /> {t.rankings}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      {Object.entries(topProducers).map(([crop, producers]) => (
                        <div key={crop} className="bg-amber-50 p-4 rounded-xl">
                          <h4 className="font-bold text-amber-800 mb-3">{crop}</h4>
                          <div className="space-y-2">
                            {producers.slice(0, 4).map((producer, idx) => (
                              <div 
                                key={producer.country} 
                                className={`flex items-center justify-between p-2 rounded ${producer.country === selectedCountry ? 'bg-green-100 font-bold' : 'bg-white'}`}
                              >
                                <div className="flex items-center gap-2">
                                  <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${idx === 0 ? 'bg-amber-400 text-white' : idx === 1 ? 'bg-gray-300' : idx === 2 ? 'bg-amber-600 text-white' : 'bg-gray-100'}`}>
                                    {producer.rank}
                                  </span>
                                  <span className="text-sm">{producer.name}</span>
                                </div>
                                <span className="text-xs text-gray-500">{producer.share_africa}%</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </TabsContent>

            {/* Livestock Tab */}
            <TabsContent value="livestock" className="space-y-6">
              {faostatData.livestock_2023 ? (
                <Card className="shadow-lg">
                  <CardHeader className="bg-gradient-to-r from-amber-50 to-orange-50">
                    <CardTitle className="text-xl text-amber-700 flex items-center gap-2">
                      <Beef className="w-5 h-5" /> {t.livestock2023}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {Object.entries(faostatData.livestock_2023).map(([animal, data]) => (
                        <div key={animal} className="bg-gradient-to-br from-amber-50 to-orange-50 p-4 rounded-xl border border-amber-200">
                          <div className="flex items-center justify-between mb-2">
                            <h4 className="font-bold text-amber-800">{animal}</h4>
                            {data.rank_africa && (
                              <Badge className="bg-amber-500 text-white">
                                #{data.rank_africa} {t.africa}
                              </Badge>
                            )}
                          </div>
                          <p className="text-3xl font-bold text-amber-700">{formatNumber(data.value)}</p>
                          <p className="text-sm text-amber-600">{data.unit}</p>
                        </div>
                      ))}
                    </div>
                    
                    {/* Bar Chart */}
                    <div className="mt-8">
                      <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={prepareLivestockData()}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="name" />
                          <YAxis tickFormatter={formatNumber} />
                          <Tooltip formatter={(value) => formatNumber(value)} />
                          <Bar dataKey="value" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </CardContent>
                </Card>
              ) : (
                <Card className="border-l-4 border-l-gray-300">
                  <CardContent className="py-8 text-center text-gray-500">
                    <Beef className="w-12 h-12 mx-auto mb-4 opacity-30" />
                    {t.noLivestockData}
                  </CardContent>
                </Card>
              )}
            </TabsContent>

            {/* Fisheries Tab */}
            <TabsContent value="fisheries" className="space-y-6">
              {faostatData.fisheries_2023 ? (
                <Card className="shadow-lg">
                  <CardHeader className="bg-gradient-to-r from-blue-50 to-cyan-50">
                    <CardTitle className="text-xl text-blue-700 flex items-center gap-2">
                      <Fish className="w-5 h-5" /> {t.fisheries2023}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {faostatData.fisheries_2023.capture && (
                        <div className="bg-gradient-to-br from-blue-50 to-cyan-50 p-6 rounded-xl border border-blue-200">
                          <div className="flex items-center gap-3 mb-4">
                            <div className="p-3 bg-blue-500 rounded-full">
                              <Fish className="w-6 h-6 text-white" />
                            </div>
                            <div>
                              <h4 className="font-bold text-blue-800">{t.capture}</h4>
                              {faostatData.fisheries_2023.capture.rank_africa && (
                                <Badge className="bg-blue-500 text-white text-xs">
                                  #{faostatData.fisheries_2023.capture.rank_africa} {t.inAfrica}
                                </Badge>
                              )}
                            </div>
                          </div>
                          <p className="text-4xl font-bold text-blue-700">
                            {formatNumber(faostatData.fisheries_2023.capture.value)}
                          </p>
                          <p className="text-blue-600">{faostatData.fisheries_2023.capture.unit}</p>
                        </div>
                      )}
                      
                      {faostatData.fisheries_2023.aquaculture && (
                        <div className="bg-gradient-to-br from-teal-50 to-emerald-50 p-6 rounded-xl border border-teal-200">
                          <div className="flex items-center gap-3 mb-4">
                            <div className="p-3 bg-teal-500 rounded-full">
                              <Fish className="w-6 h-6 text-white" />
                            </div>
                            <div>
                              <h4 className="font-bold text-teal-800">{t.aquaculture}</h4>
                              {faostatData.fisheries_2023.aquaculture.rank_africa && (
                                <Badge className="bg-teal-500 text-white text-xs">
                                  #{faostatData.fisheries_2023.aquaculture.rank_africa} {t.inAfrica}
                                </Badge>
                              )}
                            </div>
                          </div>
                          <p className="text-4xl font-bold text-teal-700">
                            {formatNumber(faostatData.fisheries_2023.aquaculture.value)}
                          </p>
                          <p className="text-teal-600">{faostatData.fisheries_2023.aquaculture.unit}</p>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ) : (
                <Card className="border-l-4 border-l-gray-300">
                  <CardContent className="py-8 text-center text-gray-500">
                    <Fish className="w-12 h-12 mx-auto mb-4 opacity-30" />
                    {t.noFisheriesData}
                  </CardContent>
                </Card>
              )}
            </TabsContent>
          </Tabs>

          {/* Source Information */}
          <Card className="bg-gray-50 border-gray-200">
            <CardContent className="py-4">
              <div className="flex items-start gap-3">
                <Info className="w-5 h-5 text-gray-400 mt-0.5" />
                <div className="text-sm text-gray-600">
                  <p><strong>{t.source}</strong> {faostatData.source}</p>
                  <p className="mt-1">{t.sourceNote}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}

export default ProductionAgriculture;
