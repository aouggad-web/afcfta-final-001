import React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import MaritimeLogisticsTab from './MaritimeLogisticsTab';
import AirLogisticsTab from './AirLogisticsTab';
import LandLogisticsTab from './LandLogisticsTab';

export default function LogisticsTab() {
  return (
    <div className="space-y-6">
      <Card className="bg-gradient-to-r from-blue-700 to-indigo-800 text-white shadow-xl">
        <CardHeader>
          <CardTitle className="text-3xl font-bold flex items-center gap-3">
            <span>🌍</span>
            <span>Plateforme Logistique Multimodale</span>
          </CardTitle>
          <CardDescription className="text-blue-100 text-lg">
            Analyse intégrée des corridors maritimes, aériens et terrestres de la ZLECAf
          </CardDescription>
        </CardHeader>
      </Card>

      <Tabs defaultValue="maritime" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3 bg-white shadow-md p-1 h-14">
          <TabsTrigger value="maritime" className="text-base font-semibold data-[state=active]:bg-blue-100 data-[state=active]:text-blue-800">
            🚢 Maritime (Ports)
          </TabsTrigger>
          <TabsTrigger value="air" className="text-base font-semibold data-[state=active]:bg-sky-100 data-[state=active]:text-sky-800">
            ✈️ Aérien (Fret)
          </TabsTrigger>
          <TabsTrigger value="land" className="text-base font-semibold data-[state=active]:bg-slate-100 data-[state=active]:text-slate-800">
            🚛 Terrestre (Corridors)
          </TabsTrigger>
        </TabsList>

        <TabsContent value="maritime" className="mt-6">
          <MaritimeLogisticsTab />
        </TabsContent>

        <TabsContent value="air" className="mt-6">
          <AirLogisticsTab />
        </TabsContent>

        <TabsContent value="land" className="mt-6">
          <LandLogisticsTab />
        </TabsContent>
      </Tabs>
    </div>
  );
}
