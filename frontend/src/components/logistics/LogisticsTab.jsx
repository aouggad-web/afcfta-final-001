import React, { useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Badge } from '../ui/badge';
import MaritimeLogisticsTab from './MaritimeLogisticsTab';
import AirLogisticsTab from './AirLogisticsTab';
import LandLogisticsTab from './LandLogisticsTab';
import FreeZonesTab from './FreeZonesTab';
import { PDFExportButton } from '../common/ExportTools';

export default function LogisticsTab({ language = 'fr' }) {
  const { t } = useTranslation();
  const contentRef = useRef(null);

  return (
    <div className="space-y-6" data-testid="logistics-tab">
      {/* Export Button */}
      <div className="flex justify-end">
        <PDFExportButton
          targetRef={contentRef}
          filename="logistics"
          title={t('logistics.title')}
          language={language}
        />
      </div>

      <div ref={contentRef}>
      {/* Header - Compact */}
      <Card className="bg-gradient-to-r from-blue-700 to-indigo-800 text-white shadow-xl">
        <CardHeader className="py-3">
          <CardTitle className="text-xl font-bold flex items-center gap-2">
            <span>🌍</span>
            <span>{t('logistics.title')}</span>
          </CardTitle>
          <CardDescription className="text-blue-100 text-sm">
            {t('logistics.subtitle')}
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Main Tabs - Compact */}
      <Tabs defaultValue="maritime" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4 bg-white shadow-md p-1 h-10">
          <TabsTrigger value="maritime" className="text-sm font-semibold data-[state=active]:bg-blue-100 data-[state=active]:text-blue-800" data-testid="maritime-tab-trigger">
            🚢 {t('logistics.maritime')}
          </TabsTrigger>
          <TabsTrigger value="air" className="text-sm font-semibold data-[state=active]:bg-sky-100 data-[state=active]:text-sky-800" data-testid="air-tab-trigger">
            ✈️ {t('logistics.air')}
          </TabsTrigger>
          <TabsTrigger value="land" className="text-sm font-semibold data-[state=active]:bg-slate-100 data-[state=active]:text-slate-800" data-testid="land-tab-trigger">
            🚛 {t('logistics.land')}
          </TabsTrigger>
          <TabsTrigger value="zones" className="text-sm font-semibold data-[state=active]:bg-orange-100 data-[state=active]:text-orange-800" data-testid="zones-tab-trigger">
            🏭 {t('logistics.freeZones')}
          </TabsTrigger>
        </TabsList>

        <TabsContent value="maritime" className="mt-6">
          <MaritimeLogisticsTab language={language} />
        </TabsContent>

        <TabsContent value="air" className="mt-6">
          <AirLogisticsTab language={language} />
        </TabsContent>

        <TabsContent value="land" className="mt-6">
          <LandLogisticsTab language={language} />
        </TabsContent>

        <TabsContent value="zones" className="mt-6">
          <FreeZonesTab language={language} />
        </TabsContent>
      </Tabs>

      {/* Data Sources Card - Moved to bottom */}
      <Card className="border-l-4 border-l-cyan-500 bg-cyan-50">
        <CardContent className="pt-4">
          <h3 className="font-bold text-cyan-900 flex items-center gap-2 mb-4">
            <span>📊</span>
            <span>{t('logistics.dataSourcesTitle')}</span>
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="bg-white p-3 rounded shadow-sm border-l-2 border-l-orange-400">
              <p className="font-semibold text-orange-700">⏱️ {t('logistics.trsTitle')}</p>
              <p className="text-gray-600 text-xs">{t('logistics.trsDesc')}</p>
              <Badge className="mt-2 bg-orange-100 text-orange-700 text-xs">{t('common.estimated')}</Badge>
            </div>
            <div className="bg-white p-3 rounded shadow-sm border-l-2 border-l-blue-400">
              <p className="font-semibold text-blue-700">🚢 {t('logistics.unctad.title')}</p>
              <p className="text-gray-600 text-xs">{t('logistics.unctad.desc')}</p>
              <Badge className="mt-2 bg-blue-100 text-blue-700 text-xs">{t('common.official')}</Badge>
            </div>
            <div className="bg-white p-3 rounded shadow-sm border-l-2 border-l-green-400">
              <p className="font-semibold text-green-700">🛃 {t('logistics.wcoTitle')}</p>
              <p className="text-gray-600 text-xs">{t('logistics.wcoDesc')}</p>
              <Badge className="mt-2 bg-green-100 text-green-700 text-xs">{t('common.official')}</Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Footer with Source Indicator */}
      <Card className="bg-gray-50 border-gray-200">
        <CardContent className="py-3">
          <p className="text-xs text-gray-500 text-center">
            {t('logistics.sourceLabel')} UNCTAD Maritime Transport Review 2023 | World Customs Organization (WCO) TRS Database | AfCFTA Secretariat
          </p>
        </CardContent>
      </Card>
      </div>
    </div>
  );
}
