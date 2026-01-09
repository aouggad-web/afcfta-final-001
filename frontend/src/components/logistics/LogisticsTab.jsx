import React, { useRef } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Badge } from '../ui/badge';
import MaritimeLogisticsTab from './MaritimeLogisticsTab';
import AirLogisticsTab from './AirLogisticsTab';
import LandLogisticsTab from './LandLogisticsTab';
import FreeZonesTab from './FreeZonesTab';
import { PDFExportButton } from '../common/ExportTools';

export default function LogisticsTab({ language = 'fr' }) {
  const contentRef = useRef(null);
  
  const texts = {
    fr: {
      title: "Plateforme Logistique Multimodale",
      subtitle: "Analyse intégrée des corridors maritimes, aériens, terrestres et zones franches de la ZLECAf",
      maritime: "Maritime (Ports)",
      air: "Aérien (Fret)",
      land: "Terrestre (Corridors)",
      zones: "Zones Franches",
      dataSourcesTitle: "Sources de Données",
      trsTitle: "Données TRS (Time Release Study)",
      trsDesc: "Temps de dédouanement officiels - Organisation Mondiale des Douanes (OMD)",
      unctadTitle: "Données UNCTAD",
      unctadDesc: "Statistiques maritimes et portuaires - UNCTAD Maritime Transport Review",
      wcoTitle: "Données OMD/WCO",
      wcoDesc: "Facilitation des échanges - Temps de passage aux frontières",
      sourceLabel: "Source:",
      estimated: "Estimé",
      official: "Officiel"
    },
    en: {
      title: "Multimodal Logistics Platform",
      subtitle: "Integrated analysis of maritime, air, land corridors and free zones of the AfCFTA",
      maritime: "Maritime (Ports)",
      air: "Air (Freight)",
      land: "Land (Corridors)",
      zones: "Free Zones",
      dataSourcesTitle: "Data Sources",
      trsTitle: "TRS Data (Time Release Study)",
      trsDesc: "Official customs clearance times - World Customs Organization (WCO)",
      unctadTitle: "UNCTAD Data",
      unctadDesc: "Maritime and port statistics - UNCTAD Maritime Transport Review",
      wcoTitle: "WCO Data",
      wcoDesc: "Trade facilitation - Border crossing times",
      sourceLabel: "Source:",
      estimated: "Estimated",
      official: "Official"
    }
  };

  const t = texts[language];

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="bg-gradient-to-r from-blue-700 to-indigo-800 text-white shadow-xl">
        <CardHeader>
          <CardTitle className="text-3xl font-bold flex items-center gap-3">
            <span>🌍</span>
            <span>{t.title}</span>
          </CardTitle>
          <CardDescription className="text-blue-100 text-lg">
            {t.subtitle}
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Data Sources Card */}
      <Card className="border-l-4 border-l-cyan-500 bg-cyan-50">
        <CardContent className="pt-4">
          <h3 className="font-bold text-cyan-900 flex items-center gap-2 mb-4">
            <span>📊</span>
            <span>{t.dataSourcesTitle}</span>
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="bg-white p-3 rounded shadow-sm border-l-2 border-l-orange-400">
              <p className="font-semibold text-orange-700">⏱️ {t.trsTitle}</p>
              <p className="text-gray-600 text-xs">{t.trsDesc}</p>
              <Badge className="mt-2 bg-orange-100 text-orange-700 text-xs">{t.estimated}</Badge>
            </div>
            <div className="bg-white p-3 rounded shadow-sm border-l-2 border-l-blue-400">
              <p className="font-semibold text-blue-700">🚢 {t.unctadTitle}</p>
              <p className="text-gray-600 text-xs">{t.unctadDesc}</p>
              <Badge className="mt-2 bg-blue-100 text-blue-700 text-xs">{t.official}</Badge>
            </div>
            <div className="bg-white p-3 rounded shadow-sm border-l-2 border-l-green-400">
              <p className="font-semibold text-green-700">🛃 {t.wcoTitle}</p>
              <p className="text-gray-600 text-xs">{t.wcoDesc}</p>
              <Badge className="mt-2 bg-green-100 text-green-700 text-xs">{t.official}</Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Tabs */}
      <Tabs defaultValue="maritime" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4 bg-white shadow-md p-1 h-14">
          <TabsTrigger value="maritime" className="text-base font-semibold data-[state=active]:bg-blue-100 data-[state=active]:text-blue-800">
            🚢 {t.maritime}
          </TabsTrigger>
          <TabsTrigger value="air" className="text-base font-semibold data-[state=active]:bg-sky-100 data-[state=active]:text-sky-800">
            ✈️ {t.air}
          </TabsTrigger>
          <TabsTrigger value="land" className="text-base font-semibold data-[state=active]:bg-slate-100 data-[state=active]:text-slate-800">
            🚛 {t.land}
          </TabsTrigger>
          <TabsTrigger value="zones" className="text-base font-semibold data-[state=active]:bg-orange-100 data-[state=active]:text-orange-800">
            🏭 {t.zones}
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

      {/* Footer with Source Indicator */}
      <Card className="bg-gray-50 border-gray-200">
        <CardContent className="py-3">
          <p className="text-xs text-gray-500 text-center">
            {t.sourceLabel} UNCTAD Maritime Transport Review 2023 | World Customs Organization (WCO) TRS Database | AfCFTA Secretariat
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
