import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { toast } from '../../hooks/use-toast';
import { MapContainer, TileLayer, Marker, Popup, Tooltip } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Custom Icon for Free Zones (Orange/Industrial)
const freeZoneIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

export default function FreeZonesTab() {
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCountry, setSelectedCountry] = useState('ALL');
  const [viewMode, setViewMode] = useState('map');

  useEffect(() => {
    fetchZones(selectedCountry);
  }, [selectedCountry]);

  const fetchZones = async (countryIso) => {
    setLoading(true);
    try {
      const url = countryIso && countryIso !== 'ALL'
        ? `${API}/logistics/free-zones?country_iso=${countryIso}`
        : `${API}/logistics/free-zones`;
      
      const response = await axios.get(url);
      setZones(response.data.zones || []);
    } catch (error) {
      console.error('Error fetching free zones:', error);
      toast({
        title: "Erreur",
        description: "Impossible de charger les données des zones franches",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gradient-to-r from-orange-600 to-red-600 text-white shadow-xl">
        <CardHeader>
          <CardTitle className="text-3xl font-bold flex items-center gap-3">
            <span>🏭</span>
            <span>Zones Franches & Industrielles</span>
          </CardTitle>
          <CardDescription className="text-orange-100 text-lg">
            Cartographie des pôles de compétitivité, zones franches d'exportation et hubs industriels
          </CardDescription>
        </CardHeader>
      </Card>

      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            <div className="flex items-center gap-3 w-full md:w-auto">
              <span className="text-sm font-semibold text-gray-700">Filtrer par pays:</span>
              <Select value={selectedCountry} onValueChange={setSelectedCountry}>
                <SelectTrigger className="w-64">
                  <SelectValue placeholder="Tous les pays" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="ALL">🌍 Tous les pays</SelectItem>
                  <SelectItem value="MAR">🇲🇦 Maroc</SelectItem>
                  <SelectItem value="DZA">🇩🇿 Algérie</SelectItem>
                  <SelectItem value="EGY">🇪🇬 Égypte</SelectItem>
                  <SelectItem value="NGA">🇳🇬 Nigéria</SelectItem>
                  <SelectItem value="DJI">🇩🇯 Djibouti</SelectItem>
                  <SelectItem value="GAB">🇬🇦 Gabon</SelectItem>
                  <SelectItem value="SEN">🇸🇳 Sénégal</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center gap-2">
              <Button
                onClick={() => setViewMode('map')}
                variant={viewMode === 'map' ? 'default' : 'outline'}
                className={viewMode === 'map' ? 'bg-orange-600 hover:bg-orange-700' : ''}
              >
                🗺️ Carte
              </Button>
              <Button
                onClick={() => setViewMode('list')}
                variant={viewMode === 'list' ? 'default' : 'outline'}
                className={viewMode === 'list' ? 'bg-orange-600 hover:bg-orange-700' : ''}
              >
                📋 Liste
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {viewMode === 'map' ? (
        <Card className="h-[600px] overflow-hidden border-2 border-orange-100">
          <MapContainer center={[5.0, 20.0]} zoom={3} style={{ height: '100%', width: '100%' }}>
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {zones.map((zone) => (
              <Marker 
                key={zone.id} 
                position={[zone.location.lat, zone.location.lon]}
                icon={freeZoneIcon}
              >
                <Popup>
                  <div className="p-2 min-w-[250px]">
                    <h3 className="font-bold text-lg text-orange-700 mb-1">{zone.name}</h3>
                    <Badge className="bg-orange-100 text-orange-800 mb-2">{zone.type}</Badge>
                    <p className="text-sm text-gray-600 mb-2">{zone.country}</p>
                    <div className="text-xs space-y-1">
                      <p><strong>🏗️ Industries:</strong> {zone.industries.join(', ')}</p>
                      <p><strong>📏 Surface:</strong> {zone.surface_ha} ha</p>
                      <p><strong>🔗 Connexion:</strong> {zone.connection}</p>
                    </div>
                  </div>
                </Popup>
                <Tooltip>{zone.name}</Tooltip>
              </Marker>
            ))}
          </MapContainer>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {zones.map((zone) => (
            <Card key={zone.id} className="hover:shadow-lg transition-shadow border-t-4 border-t-orange-500">
              <CardHeader className="pb-3">
                <div className="flex justify-between items-start">
                  <Badge variant="outline" className="text-xs">{zone.country}</Badge>
                  <Badge className={zone.status.includes('Opérationnel') ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}>
                    {zone.status}
                  </Badge>
                </div>
                <CardTitle className="text-xl mt-2">{zone.name}</CardTitle>
                <CardDescription>{zone.type}</CardDescription>
              </CardHeader>
              <CardContent className="text-sm space-y-4">
                <div>
                  <p className="font-semibold text-gray-700 mb-1">Industries Clés:</p>
                  <div className="flex flex-wrap gap-1">
                    {zone.industries.map((ind, i) => (
                      <Badge key={i} variant="secondary" className="bg-gray-100 text-gray-600 text-xs">
                        {ind}
                      </Badge>
                    ))}
                  </div>
                </div>
                
                <div className="bg-orange-50 p-3 rounded-lg border border-orange-100">
                  <p className="font-semibold text-orange-800 mb-1">💡 Incitations:</p>
                  <p className="text-xs text-orange-700">{zone.incentives}</p>
                </div>

                <div className="space-y-1 text-gray-600">
                  <p><strong>🏢 Locataires clés:</strong> {zone.key_tenants.join(', ')}</p>
                  <p><strong>🌍 Impact:</strong> {zone.impact}</p>
                  <p><strong>⚓ Connexion:</strong> {zone.connection}</p>
                </div>

                {zone.authority && (
                  <div className="bg-blue-50 p-3 rounded-lg border border-blue-200 mt-3">
                    <p className="font-semibold text-blue-800 mb-2">🏛️ Autorité Gérante:</p>
                    <div className="text-xs text-blue-700 space-y-1">
                      <p className="font-medium">{zone.authority.name}</p>
                      {zone.authority.address && (
                        <p>📍 {zone.authority.address}</p>
                      )}
                      {zone.authority.phone && (
                        <p>📞 <a href={`tel:${zone.authority.phone}`} className="hover:underline">{zone.authority.phone}</a></p>
                      )}
                      {zone.authority.email && (
                        <p>✉️ <a href={`mailto:${zone.authority.email}`} className="text-blue-600 hover:underline">{zone.authority.email}</a></p>
                      )}
                      {zone.authority.website && (
                        <p>🌐 <a href={zone.authority.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">{zone.authority.website}</a></p>
                      )}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
