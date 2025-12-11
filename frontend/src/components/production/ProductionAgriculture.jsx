import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Badge } from '../ui/badge';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const COUNTRIES_PILOT = [
  { code: 'ZAF', name: 'Afrique du Sud' },
  { code: 'NGA', name: 'Nigéria' },
  { code: 'EGY', name: 'Égypte' },
  { code: 'KEN', name: 'Kenya' },
  { code: 'GHA', name: 'Ghana' },
  { code: 'ETH', name: 'Éthiopie' },
  { code: 'CIV', name: 'Côte d\'Ivoire' },
  { code: 'TZA', name: 'Tanzanie' },
  { code: 'MAR', name: 'Maroc' },
  { code: 'SEN', name: 'Sénégal' }
];

function ProductionAgriculture() {
  const [selectedCountry, setSelectedCountry] = useState('ZAF');
  const [agriData, setAgriData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedCountry) {
      fetchAgriData(selectedCountry);
    }
  }, [selectedCountry]);

  const fetchAgriData = async (countryIso3) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/production/agriculture/${countryIso3}`);
      setAgriData(response.data);
    } catch (error) {
      console.error('Error fetching agriculture data:', error);
    } finally {
      setLoading(false);
    }
  };

  const prepareChartData = () => {
    if (!agriData || !agriData.data_by_commodity) return [];

    const years = [2021, 2022, 2023, 2024];
    return years.map(year => {
      const dataPoint = { year };
      
      Object.entries(agriData.data_by_commodity).forEach(([commodity, records]) => {
        const yearRecord = records.find(r => r.year === year);
        if (yearRecord) {
          dataPoint[commodity] = yearRecord.value;
        }
      });
      
      return dataPoint;
    });
  };

  const formatNumber = (num) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(0)}K`;
    return num.toString();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="bg-gradient-to-r from-green-600 to-emerald-600 text-white shadow-xl">
        <CardHeader>
          <CardTitle className="text-3xl font-bold flex items-center gap-3">
            <span>🌾</span>
            <span>Production Agricole (FAOSTAT)</span>
          </CardTitle>
          <CardDescription className="text-green-100 text-lg">
            Données de production physique des principales cultures africaines (2021-2024)
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Country Selector */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center gap-4">
            <label className="text-sm font-semibold text-gray-700">Sélectionner un pays:</label>
            <Select value={selectedCountry} onValueChange={setSelectedCountry}>
              <SelectTrigger className="w-64">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {COUNTRIES_PILOT.map(country => (
                  <SelectItem key={country.code} value={country.code}>
                    {country.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {agriData && (
              <Badge variant="outline" className="text-sm">
                {agriData.total_records} enregistrements
              </Badge>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Charts */}
      {loading ? (
        <Card>
          <CardContent className="flex items-center justify-center h-96">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Chargement des données agricoles...</p>
            </div>
          </CardContent>
        </Card>
      ) : agriData && agriData.data_by_commodity ? (
        <>
          {/* Line Chart: Evolution Production */}
          <Card className="shadow-lg">
            <CardHeader className="bg-gradient-to-r from-green-50 to-emerald-50">
              <CardTitle className="text-xl text-green-700">
                📈 Évolution de la Production Agricole (tonnes)
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={prepareChartData()}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis 
                    label={{ value: 'Production (tonnes)', angle: -90, position: 'insideLeft' }}
                    tickFormatter={formatNumber}
                  />
                  <Tooltip 
                    formatter={(value) => value.toLocaleString() + ' tonnes'}
                  />
                  <Legend />
                  {Object.keys(agriData.data_by_commodity).map((commodity, index) => (
                    <Line 
                      key={commodity}
                      type="monotone" 
                      dataKey={commodity} 
                      stroke={['#10b981', '#059669', '#047857'][index % 3]}
                      strokeWidth={2}
                      dot={{ r: 5 }}
                    />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Bar Chart: Comparison */}
          <Card className="shadow-lg">
            <CardHeader className="bg-gradient-to-r from-emerald-50 to-teal-50">
              <CardTitle className="text-xl text-emerald-700">
                📊 Production par Culture et Année
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={prepareChartData()}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis 
                    label={{ value: 'Production (tonnes)', angle: -90, position: 'insideLeft' }}
                    tickFormatter={formatNumber}
                  />
                  <Tooltip 
                    formatter={(value) => value.toLocaleString() + ' tonnes'}
                  />
                  <Legend />
                  {Object.keys(agriData.data_by_commodity).map((commodity, index) => (
                    <Bar 
                      key={commodity}
                      dataKey={commodity} 
                      fill={['#10b981', '#059669', '#047857'][index % 3]}
                    />
                  ))}
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Details Cards */}
          <Card className="shadow-lg">
            <CardHeader className="bg-gradient-to-r from-gray-50 to-slate-50">
              <CardTitle className="text-xl text-gray-700">
                🌾 Données Détaillées par Culture
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(agriData.data_by_commodity).map(([commodity, records]) => (
                  <div key={commodity} className="border-l-4 border-green-500 pl-4 py-3 bg-green-50 rounded-lg">
                    <h4 className="font-bold text-green-700 text-lg mb-3">{commodity}</h4>
                    <div className="space-y-2">
                      {records.map(record => (
                        <div key={record.year} className="bg-white p-3 rounded shadow-sm flex justify-between items-center">
                          <div>
                            <p className="text-sm text-gray-600">Année {record.year}</p>
                            <p className="text-xs text-gray-500">{record.faostat_domain} - {record.element_label}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-xl font-bold text-green-600">
                              {record.value.toLocaleString()}
                            </p>
                            <Badge variant="outline" className="text-xs">
                              {record.unit}
                            </Badge>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </>
      ) : (
        <Card>
          <CardContent className="text-center py-12 text-gray-500">
            Aucune donnée agricole disponible pour ce pays.
          </CardContent>
        </Card>
      )}
    </div>
  );
}

export default ProductionAgriculture;
