import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, Legend } from 'recharts';

function PortDetailsModal({ isOpen, onClose, port }) {
  if (!port) return null;

  const getEfficiencyColor = (grade) => {
    switch (grade) {
      case 'A': return 'bg-green-500';
      case 'B': return 'bg-blue-500';
      case 'B-': return 'bg-yellow-500';
      case 'C': return 'bg-orange-500';
      case 'D': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const metrics = port.performance_metrics || {};
  const history = port.traffic_evolution || [];

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6 rounded-t-lg -mx-6 -mt-6">
          <div className="flex justify-between items-start">
            <div>
              <DialogTitle className="text-3xl font-bold flex items-center gap-3">
                <span>⚓</span>
                {port.port_name}
              </DialogTitle>
              <DialogDescription className="text-blue-100 mt-2 text-lg">
                {port.city}, {port.country_name}
              </DialogDescription>
            </div>
            <div className="flex flex-col items-end gap-2">
              <Badge variant="outline" className="bg-white text-blue-700 font-bold px-3 py-1 text-sm">
                {port.port_type}
              </Badge>
              {metrics.efficiency_grade && (
                <Badge className={`${getEfficiencyColor(metrics.efficiency_grade)} text-white font-bold px-3 py-1`}>
                  Grade {metrics.efficiency_grade}
                </Badge>
              )}
            </div>
          </div>
        </DialogHeader>

        <Tabs defaultValue="overview" className="mt-6">
          <TabsList className="grid w-full grid-cols-3 bg-blue-50">
            <TabsTrigger value="overview">Vue d'ensemble</TabsTrigger>
            <TabsTrigger value="performance">Performance & Délais</TabsTrigger>
            <TabsTrigger value="connectivity">Connectivité</TabsTrigger>
          </TabsList>

          {/* ONGLET VUE D'ENSEMBLE */}
          <TabsContent value="overview" className="space-y-6 mt-4">
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card className="bg-blue-50 border-blue-200">
                <CardContent className="pt-6 text-center">
                  <p className="text-sm font-semibold text-blue-600 mb-1">Trafic Annuel (TEU)</p>
                  <p className="text-3xl font-bold text-blue-800">
                    {(port.latest_stats?.container_throughput_teu || 0).toLocaleString()}
                  </p>
                </CardContent>
              </Card>
              <Card className="bg-indigo-50 border-indigo-200">
                <CardContent className="pt-6 text-center">
                  <p className="text-sm font-semibold text-indigo-600 mb-1">Tonnage Global</p>
                  <p className="text-3xl font-bold text-indigo-800">
                    {(port.latest_stats?.cargo_throughput_tons || 0).toLocaleString()}
                  </p>
                </CardContent>
              </Card>
              <Card className="bg-teal-50 border-teal-200">
                <CardContent className="pt-6 text-center">
                  <p className="text-sm font-semibold text-teal-600 mb-1">Escales Navires</p>
                  <p className="text-3xl font-bold text-teal-800">
                    {(port.latest_stats?.vessel_calls || 0).toLocaleString()}
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Evolution Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg text-gray-700">📈 Évolution du Trafic (2020-2024)</CardTitle>
              </CardHeader>
              <CardContent className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={history}>
                    <defs>
                      <linearGradient id="colorTeu" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip 
                      formatter={(value) => value.toLocaleString()}
                      contentStyle={{ backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #e2e8f0' }}
                    />
                    <Area 
                      type="monotone" 
                      dataKey="teu" 
                      stroke="#2563eb" 
                      fillOpacity={1} 
                      fill="url(#colorTeu)" 
                      name="Trafic TEU"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>

          {/* ONGLET PERFORMANCE */}
          <TabsContent value="performance" className="space-y-6 mt-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Waiting Times */}
              <Card className="border-l-4 border-l-yellow-500 shadow-md">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2">
                    ⏳ Temps d'Attente
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between mb-1">
                        <span className="text-sm font-medium">Attente au mouillage</span>
                        <span className="text-sm font-bold">{metrics.avg_waiting_time_hours || 0} h</span>
                      </div>
                      <Progress value={Math.min((metrics.avg_waiting_time_hours / 72) * 100, 100)} className="h-2 bg-gray-100" indicatorClassName="bg-yellow-500" />
                      <p className="text-xs text-gray-500 mt-1">Moyenne régionale: 48h</p>
                    </div>
                    
                    <div>
                      <div className="flex justify-between mb-1">
                        <span className="text-sm font-medium">Temps à quai (Opérations)</span>
                        <span className="text-sm font-bold">{metrics.berth_productivity || 0} h</span>
                      </div>
                      <Progress value={Math.min((metrics.berth_productivity / 48) * 100, 100)} className="h-2 bg-gray-100" indicatorClassName="bg-blue-500" />
                    </div>

                    <div className="pt-4 border-t">
                      <div className="flex justify-between items-center">
                        <span className="text-base font-bold text-gray-700">Temps Total au Port</span>
                        <span className="text-2xl font-extrabold text-blue-700">{metrics.avg_port_stay_hours || 0} h</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Productivity Indicators */}
              <Card className="border-l-4 border-l-green-500 shadow-md">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2">
                    🏗️ Productivité & Efficacité
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="bg-gray-50 p-4 rounded-lg flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Mouvements / Heure</p>
                      <p className="text-2xl font-bold text-gray-800">
                        {port.port_type === 'Hub Transhipment' ? '45+' : '25-30'}
                      </p>
                    </div>
                    <Badge variant="secondary">Est.</Badge>
                  </div>
                  
                  <div className="bg-gray-50 p-4 rounded-lg flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Connectivité LSCI</p>
                      <p className="text-2xl font-bold text-gray-800">
                        {port.port_type === 'Hub Transhipment' ? 'High' : 'Medium'}
                      </p>
                    </div>
                    <div className="text-2xl">🌍</div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Waiting Time Evolution Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg text-gray-700">📉 Historique des temps d'attente</CardTitle>
              </CardHeader>
              <CardContent className="h-[250px]">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={history}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="avg_wait_time" 
                      name="Temps d'attente (h)" 
                      stroke="#f59e0b" 
                      strokeWidth={3}
                      dot={{ r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>

          {/* ONGLET CONNECTIVITÉ */}
          <TabsContent value="connectivity" className="space-y-6 mt-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">🚢 Lignes Régulières</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {(port.connectivity?.liner_services || ['Service MSC West Africa', 'CMA CGM Africa Express', 'Maersk Euraf']).map((service, idx) => (
                      <li key={idx} className="flex items-center gap-2 p-2 bg-gray-50 rounded hover:bg-gray-100">
                        <span className="text-blue-500">●</span>
                        <span className="font-medium text-gray-700">{service}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">🏢 Agents Maritimes</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {(port.connectivity?.shipping_agents || ['Bolloré Transport', 'CMA CGM Agency', 'Maersk Logistics']).map((agent, idx) => (
                      <li key={idx} className="flex items-center gap-2 p-2 bg-gray-50 rounded hover:bg-gray-100">
                        <span className="text-green-500">●</span>
                        <span className="font-medium text-gray-700">{agent}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}

export default PortDetailsModal;
