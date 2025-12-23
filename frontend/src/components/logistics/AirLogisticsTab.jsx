import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { toast } from '../../hooks/use-toast';
import AirLogisticsMap from './AirLogisticsMap';
import AirportCard from './AirportCard';
import AirportDetailsModal from './AirportDetailsModal';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function AirLogisticsTab() {
  const [airports, setAirports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAirport, setSelectedAirport] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedCountry, setSelectedCountry] = useState('ALL');
  const [viewMode, setViewMode] = useState('map'); // 'map' or 'list'

  useEffect(() => {
    fetchAirports(selectedCountry);
  }, [selectedCountry]);

  const fetchAirports = async (countryIso) => {
    setLoading(true);
    try {
      const url = countryIso && countryIso !== 'ALL'
        ? `${API}/logistics/air/airports?country_iso=${countryIso}`
        : `${API}/logistics/air/airports`;
      
      const response = await axios.get(url);
      setAirports(response.data.airports || []);
    } catch (error) {
      console.error('Error fetching airports:', error);
      toast({
        title: "Erreur",
        description: "Impossible de charger les données aéroportuaires",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAirportClick = async (airport) => {
    try {
      const response = await axios.get(`${API}/logistics/air/airports/${airport.airport_id}`);
      setSelectedAirport(response.data);
      setIsModalOpen(true);
    } catch (error) {
      console.error('Error fetching airport details:', error);
      toast({
        title: "Erreur",
        description: "Impossible de charger les détails de l'aéroport",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <Card className="bg-gradient-to-r from-sky-600 to-blue-600 text-white shadow-xl">
        <CardHeader>
          <CardTitle className="text-3xl font-bold flex items-center gap-3">
            <span>✈️</span>
            <span>Logistique Aérienne Panafricaine</span>
          </CardTitle>
          <CardDescription className="text-blue-100 text-lg">
            Visualisez les principaux aéroports cargo d'Afrique avec leurs statistiques de trafic, acteurs et routes régulières
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Controls Section */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            {/* Country Filter */}
            <div className="flex items-center gap-3 w-full md:w-auto">
              <span className="text-sm font-semibold text-gray-700">Filtrer par pays:</span>
              <select
                value={selectedCountry}
                onChange={(e) => setSelectedCountry(e.target.value)}
                className="px-4 py-2 border rounded-lg shadow-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
              >
                <option value="ALL">🌍 Tous les pays (64 aéroports)</option>
                <optgroup label="Afrique du Nord">
                  <option value="DZA">🇩🇿 Algérie (3)</option>
                  <option value="EGY">🇪🇬 Égypte (2)</option>
                  <option value="LBY">🇱🇾 Libye</option>
                  <option value="MAR">🇲🇦 Maroc (3)</option>
                  <option value="TUN">🇹🇳 Tunisie</option>
                </optgroup>
                <optgroup label="Afrique de l'Ouest">
                  <option value="BEN">🇧🇯 Bénin</option>
                  <option value="BFA">🇧🇫 Burkina Faso</option>
                  <option value="CPV">🇨🇻 Cap-Vert</option>
                  <option value="CIV">🇨🇮 Côte d'Ivoire</option>
                  <option value="GMB">🇬🇲 Gambie</option>
                  <option value="GHA">🇬🇭 Ghana</option>
                  <option value="GIN">🇬🇳 Guinée</option>
                  <option value="LBR">🇱🇷 Libéria</option>
                  <option value="MLI">🇲🇱 Mali</option>
                  <option value="MRT">🇲🇷 Mauritanie</option>
                  <option value="NER">🇳🇪 Niger</option>
                  <option value="NGA">🇳🇬 Nigéria (3)</option>
                  <option value="SEN">🇸🇳 Sénégal</option>
                  <option value="SLE">🇸🇱 Sierra Leone</option>
                  <option value="TGO">🇹🇬 Togo</option>
                </optgroup>
                <optgroup label="Afrique Centrale">
                  <option value="AGO">🇦🇴 Angola</option>
                  <option value="CMR">🇨🇲 Cameroun</option>
                  <option value="CAF">🇨🇫 Rép. Centrafricaine</option>
                  <option value="TCD">🇹🇩 Tchad</option>
                  <option value="COG">🇨🇬 Congo</option>
                  <option value="COD">🇨🇩 RD Congo (2)</option>
                  <option value="GNQ">🇬🇶 Guinée Équatoriale</option>
                  <option value="GAB">🇬🇦 Gabon</option>
                  <option value="STP">🇸🇹 São Tomé-et-Príncipe</option>
                </optgroup>
                <optgroup label="Afrique de l'Est">
                  <option value="BDI">🇧🇮 Burundi</option>
                  <option value="COM">🇰🇲 Comores</option>
                  <option value="DJI">🇩🇯 Djibouti</option>
                  <option value="ERI">🇪🇷 Érythrée</option>
                  <option value="ETH">🇪🇹 Éthiopie</option>
                  <option value="KEN">🇰🇪 Kenya (2)</option>
                  <option value="MDG">🇲🇬 Madagascar</option>
                  <option value="MWI">🇲🇼 Malawi</option>
                  <option value="MUS">🇲🇺 Maurice</option>
                  <option value="RWA">🇷🇼 Rwanda</option>
                  <option value="SYC">🇸🇨 Seychelles</option>
                  <option value="SOM">🇸🇴 Somalie</option>
                  <option value="SSD">🇸🇸 Soudan du Sud</option>
                  <option value="SDN">🇸🇩 Soudan</option>
                  <option value="TZA">🇹🇿 Tanzanie (2)</option>
                  <option value="UGA">🇺🇬 Ouganda</option>
                </optgroup>
                <optgroup label="Afrique Australe">
                  <option value="BWA">🇧🇼 Botswana</option>
                  <option value="LSO">🇱🇸 Lesotho</option>
                  <option value="MOZ">🇲🇿 Mozambique</option>
                  <option value="NAM">🇳🇦 Namibie</option>
                  <option value="ZAF">🇿🇦 Afrique du Sud (2)</option>
                  <option value="SWZ">🇸🇿 Eswatini</option>
                  <option value="ZMB">🇿🇲 Zambie</option>
                  <option value="ZWE">🇿🇼 Zimbabwe</option>
                </optgroup>
              </select>
            </div>

            {/* View Mode Toggle */}
            <div className="flex items-center gap-2">
              <Button
                onClick={() => setViewMode('map')}
                variant={viewMode === 'map' ? 'default' : 'outline'}
                className={viewMode === 'map' ? 'bg-sky-600 hover:bg-sky-700' : ''}
              >
                🗺️ Carte
              </Button>
              <Button
                onClick={() => setViewMode('list')}
                variant={viewMode === 'list' ? 'default' : 'outline'}
                className={viewMode === 'list' ? 'bg-sky-600 hover:bg-sky-700' : ''}
              >
                📋 Liste
              </Button>
            </div>

            {/* Airport Count Badge */}
            <Badge variant="secondary" className="text-lg px-4 py-2">
              {airports.length} aéroport{airports.length > 1 ? 's' : ''}
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* Map or List View */}
      {loading ? (
        <Card>
          <CardContent className="py-12">
            <div className="flex flex-col items-center justify-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-sky-600"></div>
              <p className="mt-4 text-gray-600">Chargement des données aéroportuaires...</p>
            </div>
          </CardContent>
        </Card>
      ) : viewMode === 'map' ? (
        <AirLogisticsMap
          onAirportClick={handleAirportClick}
          selectedCountry={selectedCountry}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {airports.map((airport) => (
            <AirportCard
              key={airport.airport_id}
              airport={airport}
              onOpenDetails={handleAirportClick}
            />
          ))}
        </div>
      )}

      {/* Airport Details Modal */}
      <AirportDetailsModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        airport={selectedAirport}
      />
    </div>
  );
}
