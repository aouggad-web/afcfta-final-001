import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Badge } from '../ui/badge';
import ProductionMacro from './ProductionMacro';
import ProductionAgriculture from './ProductionAgriculture';
import ProductionManufacturing from './ProductionManufacturing';
import ProductionMining from './ProductionMining';

function ProductionTab() {
  const [activeSubTab, setActiveSubTab] = useState('macro');

  return (
    <div className="space-y-6">
      {/* Main Header */}
      <Card className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white shadow-2xl">
        <CardHeader>
          <CardTitle className="text-4xl font-bold flex items-center gap-3">
            <span>📈</span>
            <span>Capacité de Production Africaine</span>
          </CardTitle>
          <CardDescription className="text-purple-100 text-lg font-semibold">
            Analyse multi-dimensionnelle de la production économique : Macro, Agriculture, Industrie et Mines (2021-2024)
          </CardDescription>
          <div className="flex gap-2 mt-3">
            <Badge className="bg-white text-purple-700 hover:bg-purple-50 text-sm px-3 py-1">
              🌍 10 pays pilotes
            </Badge>
            <Badge className="bg-white text-purple-700 hover:bg-purple-50 text-sm px-3 py-1">
              📊 4 dimensions
            </Badge>
            <Badge className="bg-white text-purple-700 hover:bg-purple-50 text-sm px-3 py-1">
              📅 2021-2024
            </Badge>
          </div>
        </CardHeader>
      </Card>

      {/* Data Sources Info */}
      <Card className="border-l-4 border-l-blue-500 bg-blue-50">
        <CardContent className="pt-4">
          <h3 className="font-bold text-blue-900 mb-2 flex items-center gap-2">
            <span>ℹ️</span>
            <span>Sources de Données Officielles</span>
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
            <div className="bg-white p-3 rounded shadow-sm">
              <p className="font-semibold text-purple-700">📊 Macro</p>
              <p className="text-gray-600">World Bank WDI</p>
              <p className="text-gray-600">IMF WEO</p>
            </div>
            <div className="bg-white p-3 rounded shadow-sm">
              <p className="font-semibold text-green-700">🌾 Agriculture</p>
              <p className="text-gray-600">FAO FAOSTAT</p>
              <p className="text-gray-600">Production Domain</p>
            </div>
            <div className="bg-white p-3 rounded shadow-sm">
              <p className="font-semibold text-blue-700">🏭 Manufacturing</p>
              <p className="text-gray-600">UNIDO INDSTAT4</p>
              <p className="text-gray-600">ISIC Rev.4</p>
            </div>
            <div className="bg-white p-3 rounded shadow-sm">
              <p className="font-semibold text-amber-700">⛏️ Mining</p>
              <p className="text-gray-600">USGS MCS</p>
              <p className="text-gray-600">Commodity Summaries</p>
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
            <span>Macro</span>
            <span className="text-xs opacity-80">Valeur Ajoutée</span>
          </TabsTrigger>
          <TabsTrigger 
            value="agriculture" 
            className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-green-600 data-[state=active]:to-emerald-600 data-[state=active]:text-white font-bold py-3 flex flex-col items-center gap-1"
          >
            <span className="text-2xl">🌾</span>
            <span>Agriculture</span>
            <span className="text-xs opacity-80">FAOSTAT</span>
          </TabsTrigger>
          <TabsTrigger 
            value="manufacturing" 
            className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-600 data-[state=active]:to-cyan-600 data-[state=active]:text-white font-bold py-3 flex flex-col items-center gap-1"
          >
            <span className="text-2xl">🏭</span>
            <span>Manufacturing</span>
            <span className="text-xs opacity-80">UNIDO</span>
          </TabsTrigger>
          <TabsTrigger 
            value="mining" 
            className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-amber-600 data-[state=active]:to-orange-600 data-[state=active]:text-white font-bold py-3 flex flex-col items-center gap-1"
          >
            <span className="text-2xl">⛏️</span>
            <span>Mining</span>
            <span className="text-xs opacity-80">USGS</span>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="macro">
          <ProductionMacro />
        </TabsContent>

        <TabsContent value="agriculture">
          <ProductionAgriculture />
        </TabsContent>

        <TabsContent value="manufacturing">
          <ProductionManufacturing />
        </TabsContent>

        <TabsContent value="mining">
          <ProductionMining />
        </TabsContent>
      </Tabs>

      {/* Footer Note */}
      <Card className="bg-gradient-to-r from-gray-50 to-slate-50 border-t-4 border-t-purple-500">
        <CardContent className="pt-4">
          <p className="text-sm text-gray-600 text-center">
            <strong>Note:</strong> Les données présentées couvrent actuellement 10 pays pilotes. 
            L'expansion à l'ensemble des 55 pays africains est prévue dans les prochaines phases (stratégie ETL complète).
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

export default ProductionTab;
