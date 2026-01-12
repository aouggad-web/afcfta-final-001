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
import UNCTADDataPanel from './UNCTADDataPanel';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function MaritimeLogisticsTab({ language = 'fr' }) {
  const [ports, setPorts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPort, setSelectedPort] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedCountry, setSelectedCountry] = useState('ALL');
  const [viewMode, setViewMode] = useState('map');

  const texts = {
    fr: {
      title: "Logistique Maritime Panafricaine",
      subtitle: "Visualisez les 68 principaux ports d'Afrique avec leurs statistiques de trafic, temps d'attente (TRS) et connectivité",
      filterByCountry: "Filtrer par pays:",
      allCountries: "Tous les pays",
      portsDisplayed: "port(s) affiché(s)",
      map: "Carte",
      list: "Liste",
      loading: "Chargement des données portuaires...",
      errorTitle: "Erreur",
      errorLoad: "Impossible de charger les données des ports",
      errorDetails: "Impossible de charger les détails du port",
      // Country names
      algeria: "Algérie",
      morocco: "Maroc",
      egypt: "Égypte",
      southAfrica: "Afrique du Sud",
      nigeria: "Nigéria",
      kenya: "Kenya",
      tanzania: "Tanzanie",
      ivoryCoast: "Côte d'Ivoire",
      ghana: "Ghana",
      senegal: "Sénégal",
      angola: "Angola",
      cameroon: "Cameroun",
      djibouti: "Djibouti"
    },
    en: {
      title: "Pan-African Maritime Logistics",
      subtitle: "View the 68 main African ports with traffic statistics, waiting times (TRS) and connectivity",
      filterByCountry: "Filter by country:",
      allCountries: "All countries",
      portsDisplayed: "port(s) displayed",
      map: "Map",
      list: "List",
      loading: "Loading port data...",
      errorTitle: "Error",
      errorLoad: "Unable to load port data",
      errorDetails: "Unable to load port details",
      // Country names
      algeria: "Algeria",
      morocco: "Morocco",
      egypt: "Egypt",
      southAfrica: "South Africa",
      nigeria: "Nigeria",
      kenya: "Kenya",
      tanzania: "Tanzania",
      ivoryCoast: "Côte d'Ivoire",
      ghana: "Ghana",
      senegal: "Senegal",
      angola: "Angola",
      cameroon: "Cameroon",
      djibouti: "Djibouti"
    }
  };

  const t = texts[language];

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
        title: t.errorTitle,
        description: t.errorLoad,
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
        title: t.errorTitle,
        description: t.errorDetails,
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
            <span>{t.title}</span>
          </CardTitle>
          <CardDescription className="text-blue-100 text-lg">
            {t.subtitle}
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Controls */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-wrap items-center justify-between gap-4">
            {/* Country Filter */}
            <div className="flex items-center gap-3">
              <Label htmlFor="country-filter" className="font-semibold">{t.filterByCountry}</Label>
              <Select value={selectedCountry} onValueChange={setSelectedCountry}>
                <SelectTrigger className="w-64">
                  <SelectValue placeholder={t.allCountries} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="ALL">🌍 {t.allCountries}</SelectItem>
                  <SelectItem value="DZA">🇩🇿 {t.algeria}</SelectItem>
                  <SelectItem value="MAR">🇲🇦 {t.morocco}</SelectItem>
                  <SelectItem value="EGY">🇪🇬 {t.egypt}</SelectItem>
                  <SelectItem value="ZAF">🇿🇦 {t.southAfrica}</SelectItem>
                  <SelectItem value="NGA">🇳🇬 {t.nigeria}</SelectItem>
                  <SelectItem value="KEN">🇰🇪 {t.kenya}</SelectItem>
                  <SelectItem value="TZA">🇹🇿 {t.tanzania}</SelectItem>
                  <SelectItem value="CIV">🇨🇮 {t.ivoryCoast}</SelectItem>
                  <SelectItem value="GHA">🇬🇭 {t.ghana}</SelectItem>
                  <SelectItem value="SEN">🇸🇳 {t.senegal}</SelectItem>
                  <SelectItem value="AGO">🇦🇴 {t.angola}</SelectItem>
                  <SelectItem value="CMR">🇨🇲 {t.cameroon}</SelectItem>
                  <SelectItem value="DJI">🇩🇯 {t.djibouti}</SelectItem>
                </SelectContent>
              </Select>
              <Badge variant="outline" className="text-sm">
                {ports.length} {t.portsDisplayed}
              </Badge>
            </div>

            {/* View Mode Toggle */}
            <div className="flex gap-2">
              <Button
                variant={viewMode === 'map' ? 'default' : 'outline'}
                onClick={() => setViewMode('map')}
                className="flex items-center gap-2"
              >
                🗺️ {t.map}
              </Button>
              <Button
                variant={viewMode === 'list' ? 'default' : 'outline'}
                onClick={() => setViewMode('list')}
                className="flex items-center gap-2"
              >
                📋 {t.list}
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
              <p className="mt-4 text-gray-600">{t.loading}</p>
            </div>
          </CardContent>
        </Card>
      ) : viewMode === 'map' ? (
        <LogisticsMap
          onPortClick={handlePortClick}
          selectedCountry={selectedCountry}
          language={language}
        />
      ) : (
        <div className="max-h-[550px] overflow-y-auto rounded-lg border border-gray-200 p-4 bg-gray-50">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {ports.map((port) => (
              <PortCard
                key={port.port_id}
                port={port}
                onOpenDetails={handlePortClick}
                language={language}
              />
            ))}
          </div>
        </div>
      )}

      {/* Port Details Modal */}
      <PortDetailsModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        port={selectedPort}
        language={language}
      />

      {/* UNCTAD Data Panel */}
      <UNCTADDataPanel language={language} />
    </div>
  );
}
