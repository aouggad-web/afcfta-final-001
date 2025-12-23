import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Label } from '../ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Badge } from '../ui/badge';
import { toast } from '../../hooks/use-toast';
import LogisticsMap from './LogisticsMap';
import PortCard from './PortCard';
import PortDetailsModal from './PortDetailsModal';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function LogisticsTab() {
  const [ports, setPorts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPort, setSelectedPort] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedCountry, setSelectedCountry] = useState('ALL');
  const [viewMode, setViewMode] = useState('map'); // 'map' or 'list'

  useEffect(() => {
    fetchPorts(selectedCountry);
  }, [selectedCountry]);

  const fetchPorts = async (countryIso) => {
    setLoading(true);
    try {
      const url = countryIso && countryIso !== 'ALL'
        ? `${API}/logistics/ports?country_iso=${countryIso}`
        : `${API}/logistics/ports`;
      
      const response = await axios.get(url);
      setPorts(response.data.ports || []);
    } catch (error) {
      console.error('Error fetching ports:', error);
      toast({
        title: "Erreur",
        description: "Impossible de charger les données des ports",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handlePortClick = async (port) => {
    try {
      const response = await axios.get(`${API}/logistics/ports/${port.port_id}`);
      setSelectedPort(response.data);
      setIsModalOpen(true);
    } catch (error) {
      console.error('Error fetching port details:', error);
      toast({
        title: "Erreur",
        description: "Impossible de charger les détails du port",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <Card className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-xl">
        <CardHeader>
          <CardTitle className="text-3xl font-bold flex items-center gap-3">
            <span>🚢</span>
            <span>Logistique Maritime Panafricaine</span>
          </CardTitle>
          <CardDescription className="text-blue-100 text-lg">
            Visualisez les 68 principaux ports d'Afrique avec leurs statistiques de trafic, temps d'attente (TRS) et connectivité
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Controls */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-wrap items-center justify-between gap-4">
            {/* Country Filter */}
            <div className="flex items-center gap-3">
              <Label htmlFor="country-filter" className="font-semibold">Filtrer par pays:</Label>
              <Select value={selectedCountry} onValueChange={setSelectedCountry}>
                <SelectTrigger className="w-64">
                  <SelectValue placeholder="Tous les pays" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="ALL">🌍 Tous les pays</SelectItem>
                  <SelectItem value="DZA">🇩🇿 Algérie</SelectItem>
                  <SelectItem value="MAR">🇲🇦 Maroc</SelectItem>
                  <SelectItem value="EGY">🇪🇬 Égypte</SelectItem>
                  <SelectItem value="ZAF">🇿🇦 Afrique du Sud</SelectItem>
                  <SelectItem value="NGA">🇳🇬 Nigéria</SelectItem>
                  <SelectItem value="KEN">🇰🇪 Kenya</SelectItem>
                  <SelectItem value="TZA">🇹🇿 Tanzanie</SelectItem>
                  <SelectItem value="CIV">🇨🇮 Côte d'Ivoire</SelectItem>
                  <SelectItem value="GHA">🇬🇭 Ghana</SelectItem>
                  <SelectItem value="SEN">🇸🇳 Sénégal</SelectItem>
                  <SelectItem value="AGO">🇦🇴 Angola</SelectItem>
                  <SelectItem value="CMR">🇨🇲 Cameroun</SelectItem>
                  <SelectItem value="DJI">🇩🇯 Djibouti</SelectItem>
                </SelectContent>
              </Select>
              <Badge variant="outline" className="text-sm">
                {ports.length} port(s) affiché(s)
              </Badge>
            </div>

            {/* View Mode Toggle */}
            <div className="flex gap-2">
              <Button
                variant={viewMode === 'map' ? 'default' : 'outline'}
                onClick={() => setViewMode('map')}
                className="flex items-center gap-2"
              >
                🗺️ Carte
              </Button>
              <Button
                variant={viewMode === 'list' ? 'default' : 'outline'}
                onClick={() => setViewMode('list')}
                className="flex items-center gap-2"
              >
                📋 Liste
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Map or List View */}
      {loading ? (
        <Card>
          <CardContent className="flex items-center justify-center h-96">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Chargement des données portuaires...</p>
            </div>
          </CardContent>
        </Card>
      ) : viewMode === 'map' ? (
        <LogisticsMap
          onPortClick={handlePortClick}
          selectedCountry={selectedCountry}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {ports.map((port) => (
            <PortCard
              key={port.port_id}
              port={port}
              onOpenDetails={handlePortClick}
            />
          ))}
        </div>
      )}

      {/* Port Details Modal */}
      <PortDetailsModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        port={selectedPort}
      />
    </div>
  );
}
