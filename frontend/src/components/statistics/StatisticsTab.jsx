import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { ResponsiveContainer, BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import StatisticsZaubaStyle from '../StatisticsZaubaStyle';
import TradeComparison from '../TradeComparison';
import TradeProductsTable from '../TradeProductsTable';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function StatisticsTab({ language = 'fr' }) {
  const [statistics, setStatistics] = useState(null);

  const texts = {
    fr: {
      topExporters: "Top 10 Pays Exportateurs (2023-2024)",
      topImporters: "Top 10 Pays Importateurs (2023-2024)",
      exportsEvolution: "Évolution des exportations en milliards USD",
      importsVolume: "Volume des importations en milliards USD",
      exports: "Exportations (USD)",
      imports: "Importations (USD)"
    },
    en: {
      topExporters: "Top 10 Exporting Countries (2023-2024)",
      topImporters: "Top 10 Importing Countries (2023-2024)",
      exportsEvolution: "Export evolution in billion USD",
      importsVolume: "Import volume in billion USD",
      exports: "Exports (USD)",
      imports: "Imports (USD)"
    }
  };

  const t = texts[language];

  useEffect(() => {
    fetchStatistics();
  }, []);

  const fetchStatistics = async () => {
    try {
      const response = await axios.get(`${API}/statistics`);
      setStatistics(response.data);
    } catch (error) {
      console.error('Error loading statistics:', error);
    }
  };

  return (
    <div className="space-y-6">
      {/* Nouveau composant Style Zauba */}
      <StatisticsZaubaStyle language={language} />
      
      <div className="my-8"></div>
      
      {/* Top 20 Trade Products Tables */}
      <TradeProductsTable language={language} />
      
      <div className="my-8"></div>
      
      {/* Intégration du composant Comparaisons dans Statistiques */}
      <TradeComparison language={language} />
      
      {/* Top 10 Exporters and Importers Charts */}
      {statistics && statistics.top_exporters_2024 && statistics.top_importers_2024 && (
        <div className="mt-8 space-y-6">
          <Card className="shadow-2xl">
            <CardHeader className="bg-gradient-to-r from-green-50 to-emerald-100">
              <CardTitle className="text-2xl font-bold text-green-700 flex items-center gap-2">
                <span>📤</span>
                <span>Top 10 Pays Exportateurs (2023-2024)</span>
              </CardTitle>
              <CardDescription className="font-semibold">Évolution des exportations en milliards USD</CardDescription>
            </CardHeader>
            <CardContent className="pt-6">
              <div style={{ minHeight: '420px' }}>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart
                    data={statistics.top_exporters_2024}
                    margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="country" />
                    <YAxis />
                    <Tooltip 
                      formatter={(value) => `$${(value / 1000000000).toFixed(1)}B`}
                      contentStyle={{ backgroundColor: '#fff', borderRadius: '8px' }}
                    />
                    <Legend />
                    <Bar dataKey="exports" name="Exportations (USD)" fill="#10b981" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-2xl">
            <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-100">
              <CardTitle className="text-2xl font-bold text-blue-700 flex items-center gap-2">
                <span>📥</span>
                <span>Top 10 Pays Importateurs (2023-2024)</span>
              </CardTitle>
              <CardDescription className="font-semibold">Volume des importations en milliards USD</CardDescription>
            </CardHeader>
            <CardContent className="pt-6">
              <div style={{ minHeight: '420px' }}>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart
                    data={statistics.top_importers_2024}
                    margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="country" />
                    <YAxis />
                    <Tooltip 
                      formatter={(value) => `$${(value / 1000000000).toFixed(1)}B`}
                      contentStyle={{ backgroundColor: '#fff', borderRadius: '8px' }}
                    />
                    <Legend />
                    <Bar dataKey="imports" name="Importations (USD)" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
