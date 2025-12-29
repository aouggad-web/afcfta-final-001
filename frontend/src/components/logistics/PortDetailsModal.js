import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Button } from '../ui/button';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  LineChart, Line, Legend, AreaChart, Area 
} from 'recharts';

function PortDetailsModal({ isOpen, onClose, port }) {
  if (!port) return null;

  const getEfficiencyColor = (grade) => {
    switch (grade) {
      case 'A+': return 'bg-emerald-600';
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
  const authority = port.port_authority;
  const trs = port.trs_analysis;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-5xl max-h-[90vh] overflow-y-auto">
        <DialogHeader className="bg-gradient-to-r from-blue-700 to-indigo-800 text-white p-6 rounded-t-lg -mx-6 -mt-6 shadow-lg">
          <div className="flex flex-col md:flex-row justify-between items-start gap-4">
            <div>
              <div className="flex items-center gap-3">
                <span className="text-4xl">⚓</span>
                <div>
                  <DialogTitle className="text-3xl font-bold text-white">
                    {port.port_name}
                  </DialogTitle>
                  <DialogDescription className="text-blue-100 mt-1 text-lg flex items-center gap-2">
                    <span>📍 {port.city}, {port.country_name}</span>
                    {port.un_locode && <Badge variant="outline" className="text-white border-white/30 text-xs">{port.un_locode}</Badge>}
                  </DialogDescription>
                </div>
              </div>
            </div>
            <div className="flex flex-col items-end gap-2">
              <Badge className="bg-white/20 hover:bg-white/30 text-white border-0 px-3 py-1">
                {port.port_type}
              </Badge>
              {metrics.efficiency_grade && (
                <Badge className={`${getEfficiencyColor(metrics.efficiency_grade)} text-white font-bold px-4 py-1 text-base shadow-sm border border-white/20`}>
                  Grade {metrics.efficiency_grade}
                </Badge>
              )}
            </div>
          </div>
        </DialogHeader>

        <Tabs defaultValue="overview" className="mt-6">
          <TabsList className="grid w-full grid-cols-3 bg-blue-50/50 p-1 rounded-lg">
            <TabsTrigger value="overview" className="data-[state=active]:bg-white data-[state=active]:shadow-sm">Vue d'ensemble</TabsTrigger>
            <TabsTrigger value="performance" className="data-[state=active]:bg-white data-[state=active]:shadow-sm">Performance & TRS (WCO)</TabsTrigger>
            <TabsTrigger value="connectivity" className="data-[state=active]:bg-white data-[state=active]:shadow-sm">Connectivité & Réseau</TabsTrigger>
          </TabsList>

          {/* ONGLET VUE D'ENSEMBLE */}
          <TabsContent value="overview" className="space-y-6 mt-6">
            
            {/* Port Authority Section (if available) */}
            {authority && (
              <Card className="border-l-4 border-l-blue-800 bg-gradient-to-r from-blue-50 to-white">
                <CardContent className="pt-6">
                  <div className="flex flex-col md:flex-row justify-between items-start gap-4">
                    <div>
                      <h4 className="text-sm font-bold text-blue-800 uppercase tracking-wide mb-1">🏛️ Autorité Portuaire</h4>
                      <h3 className="text-xl font-bold text-gray-900">{authority.name}</h3>
                      {authority.address && <p className="text-sm text-gray-600 mt-1">📍 {authority.address}</p>}
                    </div>
                  </div>
                  
                  {/* Contact Details Grid */}
                  <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                    {authority.website && authority.website !== 'N/A' && authority.website !== 'Non disponible' && (
                      <a 
                        href={authority.website.startsWith('http') ? authority.website : `https://${authority.website}`}
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 p-3 bg-white rounded-lg border border-blue-200 hover:bg-blue-50 hover:border-blue-400 transition-colors"
                      >
                        <span className="text-xl">🌐</span>
                        <div>
                          <p className="text-xs text-gray-500 font-medium">Site Web</p>
                          <p className="text-sm text-blue-600 font-semibold truncate max-w-[150px]">
                            {authority.website.replace('https://', '').replace('http://', '')}
                          </p>
                        </div>
                      </a>
                    )}
                    
                    {authority.contact_phone && authority.contact_phone !== 'Voir site officiel' && authority.contact_phone !== '' && (
                      <a 
                        href={`tel:${authority.contact_phone.replace(/\s/g, '')}`}
                        className="flex items-center gap-2 p-3 bg-white rounded-lg border border-green-200 hover:bg-green-50 hover:border-green-400 transition-colors"
                      >
                        <span className="text-xl">📞</span>
                        <div>
                          <p className="text-xs text-gray-500 font-medium">Téléphone</p>
                          <p className="text-sm text-green-700 font-semibold">{authority.contact_phone}</p>
                        </div>
                      </a>
                    )}
                    
                    {authority.contact_email && authority.contact_email !== 'contact@authority.com' && authority.contact_email !== '' && (
                      <a 
                        href={`mailto:${authority.contact_email}`}
                        className="flex items-center gap-2 p-3 bg-white rounded-lg border border-orange-200 hover:bg-orange-50 hover:border-orange-400 transition-colors"
                      >
                        <span className="text-xl">✉️</span>
                        <div>
                          <p className="text-xs text-gray-500 font-medium">Email</p>
                          <p className="text-sm text-orange-700 font-semibold truncate max-w-[150px]">{authority.contact_email}</p>
                        </div>
                      </a>
                    )}
                    
                    {authority.address && (
                      <a 
                        href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(authority.address)}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 p-3 bg-white rounded-lg border border-purple-200 hover:bg-purple-50 hover:border-purple-400 transition-colors"
                      >
                        <span className="text-xl">📍</span>
                        <div>
                          <p className="text-xs text-gray-500 font-medium">Localisation</p>
                          <p className="text-sm text-purple-700 font-semibold">Voir sur Google Maps</p>
                        </div>
                      </a>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card className="bg-blue-50 border-blue-200">
                <CardContent className="pt-6 text-center">
                  <p className="text-sm font-semibold text-blue-600 mb-1">Trafic Annuel (TEU)</p>
                  <p className="text-3xl font-bold text-blue-800">
                    {(port.latest_stats?.container_throughput_teu || 0).toLocaleString()}
                  </p>
                  <p className="text-xs text-blue-500 mt-1">{port.latest_stats?.year || 2024}</p>
                </CardContent>
              </Card>
              <Card className="bg-indigo-50 border-indigo-200">
                <CardContent className="pt-6 text-center">
                  <p className="text-sm font-semibold text-indigo-600 mb-1">Tonnage Global</p>
                  <p className="text-3xl font-bold text-indigo-800">
                    {(port.latest_stats?.cargo_throughput_tons || 0).toLocaleString()}
                  </p>
                  <p className="text-xs text-indigo-500 mt-1">tonnes</p>
                </CardContent>
              </Card>
              <Card className="bg-teal-50 border-teal-200">
                <CardContent className="pt-6 text-center">
                  <p className="text-sm font-semibold text-teal-600 mb-1">Escales Navires</p>
                  <p className="text-3xl font-bold text-teal-800">
                    {(port.latest_stats?.vessel_calls || 0).toLocaleString()}
                  </p>
                  <p className="text-xs text-teal-500 mt-1">navires</p>
                </CardContent>
              </Card>
            </div>

            {/* Evolution Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg text-gray-700 flex items-center gap-2">
                  📉 Évolution du Trafic (2020-2024)
                </CardTitle>
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

          {/* ONGLET PERFORMANCE & TRS */}
          <TabsContent value="performance" className="space-y-6 mt-6">
            
            {/* WCO TRS SECTION - DONNÉES OFFICIELLES */}
            <Card className="border-t-4 border-t-purple-600 shadow-md">
              <CardHeader className="bg-purple-50">
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-xl text-purple-900 flex items-center gap-2">
                      ⏱️ Temps de Séjour Conteneur (Dwell Time)
                    </CardTitle>
                    <CardDescription>
                      Données officielles - Étude TRS (Time Release Study) WCO
                    </CardDescription>
                  </div>
                  {trs?.container_dwell_time_days && trs.container_dwell_time_days !== "NA" ? (
                    <Badge className="bg-purple-600 text-white text-lg px-4 py-2">
                      {trs.container_dwell_time_days} Jours
                    </Badge>
                  ) : (
                    <Badge className="bg-gray-400 text-white text-lg px-4 py-2">
                      NA
                    </Badge>
                  )}
                </div>
              </CardHeader>
              <CardContent className="pt-6">
                {trs?.container_dwell_time_days && trs.container_dwell_time_days !== "NA" ? (
                  <div className="space-y-4">
                    {/* Données disponibles */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="bg-purple-50 p-4 rounded-lg text-center">
                        <p className="text-xs font-semibold text-purple-600">Dwell Time</p>
                        <p className="text-2xl font-bold text-purple-800">{trs.container_dwell_time_days}</p>
                        <p className="text-xs text-purple-500">jours</p>
                      </div>
                      {trs.vessel_turnaround_hours && trs.vessel_turnaround_hours !== "NA" && (
                        <div className="bg-blue-50 p-4 rounded-lg text-center">
                          <p className="text-xs font-semibold text-blue-600">Rotation Navire</p>
                          <p className="text-2xl font-bold text-blue-800">{trs.vessel_turnaround_hours}</p>
                          <p className="text-xs text-blue-500">heures</p>
                        </div>
                      )}
                      {trs.cppi_rank && trs.cppi_rank !== "NA" && (
                        <div className="bg-green-50 p-4 rounded-lg text-center">
                          <p className="text-xs font-semibold text-green-600">Rang CPPI</p>
                          <p className="text-2xl font-bold text-green-800">#{trs.cppi_rank}</p>
                          <p className="text-xs text-green-500">{trs.cppi_year || ''}</p>
                        </div>
                      )}
                      <div className="bg-orange-50 p-4 rounded-lg text-center">
                        <p className="text-xs font-semibold text-orange-600">Année Données</p>
                        <p className="text-2xl font-bold text-orange-800">{trs.data_year}</p>
                        <p className="text-xs text-orange-500">officiel</p>
                      </div>
                    </div>
                    
                    {/* Source et méthodologie */}
                    <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div>
                          <p className="font-semibold text-gray-700">📊 Source:</p>
                          <p className="text-gray-600">{trs.source}</p>
                        </div>
                        <div>
                          <p className="font-semibold text-gray-700">📋 Méthodologie:</p>
                          <p className="text-gray-600">{trs.methodology}</p>
                        </div>
                      </div>
                      {trs.notes && (
                        <div className="mt-3 pt-3 border-t border-gray-200">
                          <p className="text-xs text-gray-500">💡 {trs.notes}</p>
                        </div>
                      )}
                      {trs.wco_report_url && (
                        <a 
                          href={trs.wco_report_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="mt-3 inline-flex items-center gap-2 text-sm text-purple-600 hover:text-purple-800"
                        >
                          📄 Voir le rapport TRS officiel
                        </a>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <div className="text-6xl mb-4">📊</div>
                    <h3 className="text-lg font-semibold text-gray-700 mb-2">Données TRS Non Disponibles</h3>
                    <p className="text-sm text-gray-500 max-w-md mx-auto mb-4">
                      Aucune étude officielle TRS (Time Release Study) de l'Organisation Mondiale des Douanes (WCO) 
                      n'a été publiée pour ce port.
                    </p>
                    {trs?.wco_trs_status === "En cours" && (
                      <Badge className="bg-yellow-100 text-yellow-800 border border-yellow-300">
                        ⏳ Étude TRS en cours
                      </Badge>
                    )}
                    {trs?.notes && trs.notes !== "Aucune étude TRS (Time Release Study) officielle publiée pour ce port." && (
                      <p className="text-xs text-gray-400 mt-4">{trs.notes}</p>
                    )}
                    
                    {/* Benchmarks de comparaison */}
                    {port.global_benchmarks && (
                      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200 text-left">
                        <p className="text-sm font-semibold text-blue-800 mb-2">📈 Benchmarks de référence (UNCTAD 2023)</p>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <p className="text-blue-600">Moyenne Afrique:</p>
                            <p className="font-bold text-blue-800">{port.global_benchmarks.africa_avg_dwell_days_2023} jours</p>
                          </div>
                          <div>
                            <p className="text-blue-600">Médiane Mondiale:</p>
                            <p className="font-bold text-blue-800">{port.global_benchmarks.global_median_dwell_days_h2_2023} jour</p>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Waiting Times (Ship) */}
              <Card className="border-l-4 border-l-yellow-500 shadow-md">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2">
                    ⏳ Temps d'Attente Navire
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    <div>
                      <div className="flex justify-between mb-2">
                        <span className="text-sm font-medium text-gray-700">Attente au mouillage</span>
                        <span className="text-sm font-bold text-yellow-700">{metrics.avg_waiting_time_hours || 0} heures</span>
                      </div>
                      <Progress value={Math.min((metrics.avg_waiting_time_hours / 48) * 100, 100)} className="h-3 bg-gray-100" indicatorClassName="bg-yellow-500" />
                      <p className="text-xs text-gray-500 mt-1">Indicateur de congestion nautique</p>
                    </div>
                    
                    <div className="pt-4 border-t bg-gray-50 -mx-6 px-6 pb-2 mt-4">
                      <div className="flex justify-between items-center py-2">
                        <span className="text-base font-bold text-gray-700">Temps Total de Rotation</span>
                        <span className="text-2xl font-extrabold text-blue-800">{metrics.avg_port_stay_hours || 0} h</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Productivity Indicators */}
              <Card className="border-l-4 border-l-green-500 shadow-md">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2">
                    🏗️ Productivité
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="bg-green-50 p-4 rounded-lg flex items-center justify-between border border-green-100">
                    <div>
                      <p className="text-sm text-green-800 font-semibold">Mouvements / Heure</p>
                      <p className="text-3xl font-bold text-green-900">
                        {port.latest_stats?.berth_productivity_moves_per_hour || (port.port_type === 'Hub Transhipment' ? '45+' : '25-30')}
                      </p>
                    </div>
                    <div className="text-3xl">🏗️</div>
                  </div>
                  
                  <div className="bg-blue-50 p-4 rounded-lg flex items-center justify-between border border-blue-100">
                    <div>
                      <p className="text-sm text-blue-800 font-semibold">Connectivité LSCI</p>
                      <p className="text-3xl font-bold text-blue-900">
                        {port.lsci?.value || (port.port_type === 'Hub Transhipment' ? 'High' : 'Medium')}
                      </p>
                      {port.lsci?.world_rank && <p className="text-xs text-blue-600">Rang mondial: #{port.lsci.world_rank}</p>}
                    </div>
                    <div className="text-3xl">🌍</div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* ONGLET CONNECTIVITÉ */}
          <TabsContent value="connectivity" className="space-y-6 mt-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              
              {/* Lignes Régulières */}
              <Card className="shadow-md h-full">
                <CardHeader className="bg-gray-50 border-b">
                  <CardTitle className="text-lg flex items-center gap-2">
                    🚢 Lignes Régulières & Itinéraires
                  </CardTitle>
                  <CardDescription>
                    Connexions directes et rotations
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-4 max-h-[500px] overflow-y-auto">
                  <ul className="space-y-4">
                    {(port.services || port.connectivity?.liner_services || []).map((service, idx) => (
                      <li key={idx} className="bg-white border border-gray-200 rounded-lg p-3 hover:shadow-sm transition-shadow">
                        {typeof service === 'object' ? (
                          <>
                            <div className="flex justify-between items-start mb-2">
                              <span className="font-bold text-blue-800">{service.service_name || service.carrier}</span>
                              <Badge variant="secondary" className="text-xs">{service.frequency || 'Régulier'}</Badge>
                            </div>
                            <div className="text-sm text-gray-600 mb-1">
                              <span className="font-semibold">Armateur:</span> {service.carrier}
                            </div>
                            {service.rotation && (
                              <div className="text-xs bg-gray-50 p-2 rounded mt-2 border-l-2 border-blue-400">
                                <span className="font-semibold text-gray-700 block mb-1">Rotation:</span>
                                <span className="text-gray-600 leading-relaxed">{service.rotation}</span>
                              </div>
                            )}
                          </>
                        ) : (
                          <div className="flex items-center gap-2">
                            <span className="text-blue-500">●</span>
                            <span className="font-medium text-gray-700">{service}</span>
                          </div>
                        )}
                      </li>
                    ))}
                    {(!port.services && !port.connectivity?.liner_services) && (
                      <p className="text-gray-500 italic text-center py-4">Aucune donnée de ligne régulière disponible.</p>
                    )}
                  </ul>
                </CardContent>
              </Card>

              {/* Agents Maritimes */}
              <Card className="shadow-md h-full">
                <CardHeader className="bg-gray-50 border-b">
                  <CardTitle className="text-lg flex items-center gap-2">
                    🏢 Agents Maritimes
                  </CardTitle>
                  <CardDescription>
                    Représentants et contacts locaux
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-4 max-h-[500px] overflow-y-auto">
                  <ul className="space-y-3">
                    {(port.agents || port.connectivity?.shipping_agents || []).map((agent, idx) => (
                      <li key={idx} className="bg-white border border-gray-200 rounded-lg p-3 hover:shadow-sm transition-shadow">
                        {typeof agent === 'object' ? (
                          <div>
                            <div className="flex justify-between items-start">
                              <span className="font-bold text-gray-800">{agent.agent_name}</span>
                              {agent.group && <Badge variant="outline" className="text-xs text-gray-500">{agent.group}</Badge>}
                            </div>
                            
                            {agent.address && (
                              <div className="flex items-start gap-2 mt-2 text-xs text-gray-600">
                                <span>📍</span>
                                <span>{agent.address}</span>
                              </div>
                            )}
                            
                            <div className="flex flex-wrap gap-3 mt-3">
                              {agent.website && agent.website !== 'Non disponible' && agent.website !== 'N/A' && (
                                <a 
                                  href={agent.website.startsWith('http') ? agent.website : `https://${agent.website}`}
                                  target="_blank" 
                                  rel="noopener noreferrer" 
                                  className="text-xs text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-1 bg-blue-50 px-2 py-1 rounded"
                                >
                                  🌐 Site Web
                                </a>
                              )}
                              {agent.contact && agent.contact !== 'N/A' && (
                                <a 
                                  href={`tel:${agent.contact.replace(/\s/g, '')}`}
                                  className="text-xs text-green-600 hover:text-green-800 flex items-center gap-1 bg-green-50 px-2 py-1 rounded"
                                >
                                  📞 {agent.contact}
                                </a>
                              )}
                              {agent.email && (
                                <a 
                                  href={`mailto:${agent.email}`}
                                  className="text-xs text-orange-600 hover:text-orange-800 flex items-center gap-1 bg-orange-50 px-2 py-1 rounded"
                                >
                                  ✉️ Email
                                </a>
                              )}
                            </div>
                          </div>
                        ) : (
                          <div className="flex items-center gap-2">
                            <span className="text-green-500">●</span>
                            <span className="font-medium text-gray-700">{agent}</span>
                          </div>
                        )}
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
