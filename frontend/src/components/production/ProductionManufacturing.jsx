import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import CountrySelector from './CountrySelector';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function ProductionManufacturing() {
  const [selectedCountry, setSelectedCountry] = useState('ZAF');
  const [manufData, setManufData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedCountry) {
      fetchManufData(selectedCountry);
    }
  }, [selectedCountry]);

  const fetchManufData = async (countryIso3) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/production/manufacturing/${countryIso3}`);
      setManufData(response.data);
    } catch (error) {
      console.error('Error fetching manufacturing data:', error);
    } finally {
      setLoading(false);
    }
  };

  const prepareChartData = () => {
    if (!manufData || !manufData.data_by_isic) return [];

    const years = [2021, 2022, 2023, 2024];
    return years.map(year => {
      const dataPoint = { year };
      
      Object.entries(manufData.data_by_isic).forEach(([isic, records]) => {
        const yearRecord = records.find(r => r.year === year);
        if (yearRecord) {
          dataPoint[isic] = yearRecord.value / 1000000000; // Convert to billions
        }
      });
      
      return dataPoint;
    });
  };

  const formatBillions = (num) => {
    return `$${num.toFixed(2)}B`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-xl">
        <CardHeader>
          <CardTitle className="text-3xl font-bold flex items-center gap-3">
            <span>🏭</span>
            <span>Production Manufacturière (UNIDO)</span>
          </CardTitle>
          <CardDescription className="text-blue-100 text-lg">
            Valeur ajoutée par secteur industriel ISIC Rev.4 (2021-2024)
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
            {manufData && (
              <Badge variant="outline" className="text-sm">
                {manufData.total_records} enregistrements
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
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Chargement des données industrielles...</p>
            </div>
          </CardContent>
        </Card>
      ) : manufData && manufData.data_by_isic ? (
        <>
          {/* Line Chart: Evolution */}
          <Card className="shadow-lg">
            <CardHeader className="bg-gradient-to-r from-blue-50 to-cyan-50">
              <CardTitle className="text-xl text-blue-700">
                📈 Évolution de la Valeur Ajoutée Manufacturière (milliards USD)
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={prepareChartData()}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis 
                    label={{ value: 'Valeur Ajoutée (Md USD)', angle: -90, position: 'insideLeft' }}
                  />
                  <Tooltip 
                    formatter={(value) => formatBillions(value)}
                  />
                  <Legend />
                  {Object.keys(manufData.data_by_isic).map((isic, index) => (
                    <Line 
                      key={isic}
                      type="monotone" 
                      dataKey={isic} 
                      stroke={['#3b82f6', '#0ea5e9', '#06b6d4'][index % 3]}
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
            <CardHeader className="bg-gradient-to-r from-cyan-50 to-sky-50">
              <CardTitle className="text-xl text-cyan-700">
                📊 Production par Secteur ISIC et Année
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={prepareChartData()}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis 
                    label={{ value: 'Valeur Ajoutée (Md USD)', angle: -90, position: 'insideLeft' }}
                  />
                  <Tooltip 
                    formatter={(value) => formatBillions(value)}
                  />
                  <Legend />
                  {Object.keys(manufData.data_by_isic).map((isic, index) => (
                    <Bar 
                      key={isic}
                      dataKey={isic} 
                      fill={['#3b82f6', '#0ea5e9', '#06b6d4'][index % 3]}
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
                🏭 Données Détaillées par Secteur ISIC
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <div className="space-y-4">
                {Object.entries(manufData.data_by_isic).map(([isicLabel, records]) => (
                  <div key={isicLabel} className="border-l-4 border-blue-500 pl-4 py-3 bg-blue-50 rounded-lg">
                    <h4 className="font-bold text-blue-700 text-lg mb-3">{isicLabel}</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      {records.map(record => (
                        <div key={record.year} className="bg-white p-3 rounded shadow-sm">
                          <p className="text-sm text-gray-600 mb-1">Année {record.year}</p>
                          <p className="text-2xl font-bold text-blue-600">
                            ${(record.value / 1000000000).toFixed(2)}B
                          </p>
                          <Badge variant="outline" className="text-xs mt-2">
                            Prix constants {record.price_base_year}
                          </Badge>
                          <p className="text-xs text-gray-500 mt-1">
                            {record.unido_dataset} - ISIC Rev.{record.isic_revision}
                          </p>
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
            Aucune donnée manufacturière disponible pour ce pays.
          </CardContent>
        </Card>
      )}
    </div>
  );
}

export default ProductionManufacturing;
