import React, { useState, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Badge } from '../ui/badge';
import ProductionMacro from './ProductionMacro';
import ProductionAgriculture from './ProductionAgriculture';
import ProductionManufacturing from './ProductionManufacturing';
import ProductionMining from './ProductionMining';
import { PDFExportButton } from '../common/ExportTools';

function ProductionTab({ language = 'fr' }) {
  const { t } = useTranslation();
  const [activeSubTab, setActiveSubTab] = useState('macro');
  const contentRef = useRef(null);

  return (
    <div className="space-y-6">
      {/* Export Button */}
      <div className="flex justify-end">
        <PDFExportButton
          targetRef={contentRef}
          filename="production"
          title={t('production.title')}
          language={language}
        />
      </div>

      <div ref={contentRef}>
      {/* Main Header - Compact */}
      <Card className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white shadow-xl">
        <CardHeader className="py-3">
          <CardTitle className="text-xl font-bold flex items-center gap-2">
            <span>📈</span>
            <span>{t('production.title')}</span>
          </CardTitle>
          <CardDescription className="text-purple-100 text-sm">
            {t('production.subtitle')}
          </CardDescription>
          <div className="flex gap-2 mt-2">
            <Badge className="bg-white text-purple-700 hover:bg-purple-50 text-xs px-2 py-0.5">
              🌍 {t('production.badge1')}
            </Badge>
            <Badge className="bg-white text-purple-700 hover:bg-purple-50 text-xs px-2 py-0.5">
              📊 {t('production.badge2')}
            </Badge>
            <Badge className="bg-white text-purple-700 hover:bg-purple-50 text-xs px-2 py-0.5">
              📅 {t('production.badge3')}
            </Badge>
          </div>
        </CardHeader>
      </Card>

      {/* Sub-tabs Navigation - Compact */}
      <Tabs value={activeSubTab} onValueChange={setActiveSubTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4 bg-gradient-to-r from-purple-100 via-indigo-100 to-blue-100 p-1 shadow-md h-auto">
          <TabsTrigger 
            value="macro" 
            className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-600 data-[state=active]:to-indigo-600 data-[state=active]:text-white font-semibold py-2 flex flex-col items-center gap-0.5 text-sm"
          >
            <span className="text-lg">📊</span>
            <span>{t('production.macro.title')}</span>
          </TabsTrigger>
          <TabsTrigger 
            value="agriculture" 
            className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-green-600 data-[state=active]:to-emerald-600 data-[state=active]:text-white font-semibold py-2 flex flex-col items-center gap-0.5 text-sm"
          >
            <span className="text-lg">🌾</span>
            <span>{t('production.agriculture.title')}</span>
          </TabsTrigger>
          <TabsTrigger 
            value="manufacturing" 
            className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-600 data-[state=active]:to-cyan-600 data-[state=active]:text-white font-semibold py-2 flex flex-col items-center gap-0.5 text-sm"
          >
            <span className="text-lg">🏭</span>
            <span>{t('production.manufacturing.title')}</span>
          </TabsTrigger>
          <TabsTrigger 
            value="mining" 
            className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-amber-600 data-[state=active]:to-orange-600 data-[state=active]:text-white font-semibold py-2 flex flex-col items-center gap-0.5 text-sm"
          >
            <span className="text-lg">⛏️</span>
            <span>{t('production.mining.title')}</span>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="macro">
          <ProductionMacro language={language} />
        </TabsContent>

        <TabsContent value="agriculture">
          <ProductionAgriculture language={language} />
        </TabsContent>

        <TabsContent value="manufacturing">
          <ProductionManufacturing language={language} />
        </TabsContent>

        <TabsContent value="mining">
          <ProductionMining language={language} />
        </TabsContent>
      </Tabs>

      {/* Data Sources Info - Moved to bottom */}
      <Card className="border-l-4 border-l-blue-500 bg-blue-50">
        <CardContent className="pt-4">
          <h3 className="font-bold text-blue-900 mb-2 flex items-center gap-2">
            <span>ℹ️</span>
            <span>{t('production.sourcesTitle')}</span>
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
            <div className="bg-white p-3 rounded shadow-sm">
              <p className="font-semibold text-purple-700">📊 {t('production.macro.title')}</p>
              <p className="text-gray-600">{t('production.macro.source1')}</p>
              <p className="text-gray-600">{t('production.macro.source2')}</p>
            </div>
            <div className="bg-white p-3 rounded shadow-sm">
              <p className="font-semibold text-green-700">🌾 {t('production.agriculture.title')}</p>
              <p className="text-gray-600">{t('production.agriculture.source1')}</p>
              <p className="text-gray-600">{t('production.agriculture.source2')}</p>
            </div>
            <div className="bg-white p-3 rounded shadow-sm">
              <p className="font-semibold text-blue-700">🏭 {t('production.manufacturing.title')}</p>
              <p className="text-gray-600">{t('production.manufacturing.source1')}</p>
              <p className="text-gray-600">{t('production.manufacturing.source2')}</p>
            </div>
            <div className="bg-white p-3 rounded shadow-sm">
              <p className="font-semibold text-amber-700">⛏️ {t('production.mining.title')}</p>
              <p className="text-gray-600">{t('production.mining.source1')}</p>
              <p className="text-gray-600">{t('production.mining.source2')}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Footer Note */}
      <Card className="bg-gradient-to-r from-gray-50 to-slate-50 border-t-4 border-t-purple-500">
        <CardContent className="pt-4">
          <p className="text-sm text-gray-600 text-center">
            <strong>📊 {t('production.coverageLabel')}</strong> {t('production.footerText')}
          </p>
        </CardContent>
      </Card>
      </div>
    </div>
  );
}

export default ProductionTab;
