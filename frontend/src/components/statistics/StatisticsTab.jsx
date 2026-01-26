import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { ResponsiveContainer, BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import StatisticsZaubaStyle from '../StatisticsZaubaStyle';
import TradeComparison from '../TradeComparison';
import TradeProductsTable from '../TradeProductsTable';
import OECTradeStats from '../stats/OECTradeStats';
import { PDFExportButton } from '../common/ExportTools';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function StatisticsTab({ language = 'fr' }) {
  const { t } = useTranslation();
  const [statistics, setStatistics] = useState(null);
  const contentRef = useRef(null);

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
    <div className="space-y-6" data-testid="statistics-tab">
      {/* Export Button */}
      <div className="flex justify-end">
        <PDFExportButton
          targetRef={contentRef}
          filename="statistics"
          title={t('statistics.title')}
          language={language}
        />
      </div>

      <div ref={contentRef}>
        {/* OEC Trade Statistics - Nouveau composant moderne */}
        <OECTradeStats language={language} />
        
        <div className="my-8"></div>
        
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
          <Card className="shadow-2xl" data-testid="top-exporters-chart">
            <CardHeader className="bg-gradient-to-r from-green-50 to-emerald-100">
              <CardTitle className="text-2xl font-bold text-green-700 flex items-center gap-2">
                <span>📤</span>
                <span>{t('statistics.topExporters')}</span>
              </CardTitle>
              <CardDescription className="font-semibold">{t('statistics.exportsEvolution')}</CardDescription>
            </CardHeader>
            <CardContent className="pt-6">
              <div style={{ minHeight: '420px' }}>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart
                    data={statistics.top_exporters_2024}
                    margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis tickFormatter={(value) => `$${(value / 1000000000).toFixed(0)}B`} />
                    <Tooltip 
                      formatter={(value) => `$${(value / 1000000000).toFixed(1)}B`}
                      contentStyle={{ backgroundColor: '#fff', borderRadius: '8px' }}
                    />
                    <Legend />
                    <Bar dataKey="exports_2024" name={t('statistics.exports')} fill="#10b981" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-2xl" data-testid="top-importers-chart">
            <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-100">
              <CardTitle className="text-2xl font-bold text-blue-700 flex items-center gap-2">
                <span>📥</span>
                <span>{t('statistics.topImporters')}</span>
              </CardTitle>
              <CardDescription className="font-semibold">{t('statistics.importsVolume')}</CardDescription>
            </CardHeader>
            <CardContent className="pt-6">
              <div style={{ minHeight: '420px' }}>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart
                    data={statistics.top_importers_2024}
                    margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis tickFormatter={(value) => `$${(value / 1000000000).toFixed(0)}B`} />
                    <Tooltip 
                      formatter={(value) => `$${(value / 1000000000).toFixed(1)}B`}
                      contentStyle={{ backgroundColor: '#fff', borderRadius: '8px' }}
                    />
                    <Legend />
                    <Bar dataKey="imports_2024" name={t('statistics.imports')} fill="#3b82f6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
      </div>
    </div>
  );
}
