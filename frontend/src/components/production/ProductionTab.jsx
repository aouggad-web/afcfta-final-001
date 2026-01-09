import React, { useState, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Badge } from '../ui/badge';
import ProductionMacro from './ProductionMacro';
import ProductionAgriculture from './ProductionAgriculture';
import ProductionManufacturing from './ProductionManufacturing';
import ProductionMining from './ProductionMining';
import { PDFExportButton } from '../common/ExportTools';

function ProductionTab({ language = 'fr' }) {
  const [activeSubTab, setActiveSubTab] = useState('macro');
  const contentRef = useRef(null);

  const texts = {
    fr: {
      title: "Capacité de Production Africaine",
      subtitle: "Analyse multi-dimensionnelle de la production économique : Macro, Agriculture, Industrie et Mines (2021-2024)",
      badge1: "54 pays africains",
      badge2: "4 dimensions",
      badge3: "2021-2024",
      sourcesTitle: "Sources de Données Officielles",
      macroTitle: "Macro",
      macroSubtitle: "Valeur Ajoutée",
      macroSource1: "World Bank WDI",
      macroSource2: "IMF WEO",
      agricultureTitle: "Agriculture",
      agricultureSubtitle: "FAOSTAT",
      agricultureSource1: "FAO FAOSTAT",
      agricultureSource2: "Production Domain",
      manufacturingTitle: "Manufacturing",
      manufacturingSubtitle: "UNIDO",
      manufacturingSource1: "UNIDO INDSTAT4",
      manufacturingSource2: "ISIC Rev.4",
      miningTitle: "Mining",
      miningSubtitle: "USGS",
      miningSource1: "USGS MCS",
      miningSource2: "Commodity Summaries",
      footerText: "Les données de production couvrent maintenant les 54 pays africains membres de la ZLECAf sur les 4 dimensions économiques (Macro, Agriculture, Manufacturing, Mining) pour la période 2021-2024. Données basées sur World Bank, FAO, UNIDO et USGS.",
      coverageLabel: "Couverture complète:"
    },
    en: {
      title: "African Production Capacity",
      subtitle: "Multi-dimensional analysis of economic production: Macro, Agriculture, Industry and Mining (2021-2024)",
      badge1: "54 African countries",
      badge2: "4 dimensions",
      badge3: "2021-2024",
      sourcesTitle: "Official Data Sources",
      macroTitle: "Macro",
      macroSubtitle: "Value Added",
      macroSource1: "World Bank WDI",
      macroSource2: "IMF WEO",
      agricultureTitle: "Agriculture",
      agricultureSubtitle: "FAOSTAT",
      agricultureSource1: "FAO FAOSTAT",
      agricultureSource2: "Production Domain",
      manufacturingTitle: "Manufacturing",
      manufacturingSubtitle: "UNIDO",
      manufacturingSource1: "UNIDO INDSTAT4",
      manufacturingSource2: "ISIC Rev.4",
      miningTitle: "Mining",
      miningSubtitle: "USGS",
      miningSource1: "USGS MCS",
      miningSource2: "Commodity Summaries",
      footerText: "Production data now covers all 54 African countries members of the AfCFTA across 4 economic dimensions (Macro, Agriculture, Manufacturing, Mining) for the period 2021-2024. Data based on World Bank, FAO, UNIDO and USGS.",
      coverageLabel: "Full coverage:"
    }
  };

  const t = texts[language];

  return (
    <div className="space-y-6">
      {/* Main Header */}
      <Card className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white shadow-2xl">
        <CardHeader>
          <CardTitle className="text-4xl font-bold flex items-center gap-3">
            <span>📈</span>
            <span>{t.title}</span>
          </CardTitle>
          <CardDescription className="text-purple-100 text-lg font-semibold">
            {t.subtitle}
          </CardDescription>
          <div className="flex gap-2 mt-3">
            <Badge className="bg-white text-purple-700 hover:bg-purple-50 text-sm px-3 py-1">
              🌍 {t.badge1}
            </Badge>
            <Badge className="bg-white text-purple-700 hover:bg-purple-50 text-sm px-3 py-1">
              📊 {t.badge2}
            </Badge>
            <Badge className="bg-white text-purple-700 hover:bg-purple-50 text-sm px-3 py-1">
              📅 {t.badge3}
            </Badge>
          </div>
        </CardHeader>
      </Card>

      {/* Data Sources Info */}
      <Card className="border-l-4 border-l-blue-500 bg-blue-50">
        <CardContent className="pt-4">
          <h3 className="font-bold text-blue-900 mb-2 flex items-center gap-2">
            <span>ℹ️</span>
            <span>{t.sourcesTitle}</span>
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
            <div className="bg-white p-3 rounded shadow-sm">
              <p className="font-semibold text-purple-700">📊 {t.macroTitle}</p>
              <p className="text-gray-600">{t.macroSource1}</p>
              <p className="text-gray-600">{t.macroSource2}</p>
            </div>
            <div className="bg-white p-3 rounded shadow-sm">
              <p className="font-semibold text-green-700">🌾 {t.agricultureTitle}</p>
              <p className="text-gray-600">{t.agricultureSource1}</p>
              <p className="text-gray-600">{t.agricultureSource2}</p>
            </div>
            <div className="bg-white p-3 rounded shadow-sm">
              <p className="font-semibold text-blue-700">🏭 {t.manufacturingTitle}</p>
              <p className="text-gray-600">{t.manufacturingSource1}</p>
              <p className="text-gray-600">{t.manufacturingSource2}</p>
            </div>
            <div className="bg-white p-3 rounded shadow-sm">
              <p className="font-semibold text-amber-700">⛏️ {t.miningTitle}</p>
              <p className="text-gray-600">{t.miningSource1}</p>
              <p className="text-gray-600">{t.miningSource2}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Sub-tabs Navigation */}
      <Tabs value={activeSubTab} onValueChange={setActiveSubTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-4 bg-gradient-to-r from-purple-100 via-indigo-100 to-blue-100 p-2 shadow-lg h-auto">
          <TabsTrigger 
            value="macro" 
            className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-600 data-[state=active]:to-indigo-600 data-[state=active]:text-white font-bold py-3 flex flex-col items-center gap-1"
          >
            <span className="text-2xl">📊</span>
            <span>{t.macroTitle}</span>
            <span className="text-xs opacity-80">{t.macroSubtitle}</span>
          </TabsTrigger>
          <TabsTrigger 
            value="agriculture" 
            className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-green-600 data-[state=active]:to-emerald-600 data-[state=active]:text-white font-bold py-3 flex flex-col items-center gap-1"
          >
            <span className="text-2xl">🌾</span>
            <span>{t.agricultureTitle}</span>
            <span className="text-xs opacity-80">{t.agricultureSubtitle}</span>
          </TabsTrigger>
          <TabsTrigger 
            value="manufacturing" 
            className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-600 data-[state=active]:to-cyan-600 data-[state=active]:text-white font-bold py-3 flex flex-col items-center gap-1"
          >
            <span className="text-2xl">🏭</span>
            <span>{t.manufacturingTitle}</span>
            <span className="text-xs opacity-80">{t.manufacturingSubtitle}</span>
          </TabsTrigger>
          <TabsTrigger 
            value="mining" 
            className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-amber-600 data-[state=active]:to-orange-600 data-[state=active]:text-white font-bold py-3 flex flex-col items-center gap-1"
          >
            <span className="text-2xl">⛏️</span>
            <span>{t.miningTitle}</span>
            <span className="text-xs opacity-80">{t.miningSubtitle}</span>
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

      {/* Footer Note */}
      <Card className="bg-gradient-to-r from-gray-50 to-slate-50 border-t-4 border-t-purple-500">
        <CardContent className="pt-4">
          <p className="text-sm text-gray-600 text-center">
            <strong>📊 {t.coverageLabel}</strong> {t.footerText}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

export default ProductionTab;
