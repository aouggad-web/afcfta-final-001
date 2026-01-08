import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, Tooltip, useMap } from 'react-leaflet';
import L from 'leaflet';
import axios from 'axios';

// Fix for Leaflet default marker icons in React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// Fonction pour calculer le rayon du cercle en fonction du trafic TEU
const calculateRadius = (teu) => {
  if (!teu) return 5;
  // Échelle logarithmique pour une meilleure visualisation
  return Math.min(5 + Math.log(teu / 1000) * 2, 30);
};

// Fonction pour déterminer la couleur selon le type de port
const getPortColor = (portType) => {
  switch (portType) {
    case 'Hub Transhipment':
      return '#ef4444'; // Rouge pour les grands hubs
    case 'Hub Regional':
      return '#f59e0b'; // Orange pour les hubs régionaux
    case 'Maritime Commercial':
      return '#3b82f6'; // Bleu pour les ports commerciaux
    default:
      return '#6b7280'; // Gris par défaut
  }
};

// Composant pour centrer la carte sur un pays
function MapController({ countryIso }) {
  const map = useMap();
  
  useEffect(() => {
    if (countryIso && countryIso !== 'ALL') {
      // Coordonnées approximatives des pays (centres)
      const countryCoordinates = {
        'DZA': [28.0, 2.0],
        'MAR': [32.0, -6.0],
        'EGY': [26.0, 30.0],
        'NGA': [9.0, 8.0],
        'ZAF': [-29.0, 24.0],
        'KEN': [-1.0, 38.0],
        // Ajoutez d'autres pays si nécessaire
      };
      
      const coords = countryCoordinates[countryIso];
      if (coords) {
        map.flyTo(coords, 6, { duration: 1.5 });
      }
    } else {
      // Vue panafricaine par défaut
      map.flyTo([5, 20], 4, { duration: 1.5 });
    }
  }, [countryIso, map]);
  
  return null;
}

export default function LogisticsMap({ onPortClick, selectedCountry = 'ALL', language = 'fr' }) {
  const [ports, setPorts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const texts = {
    fr: {
      loading: "Chargement de la carte...",
      loadError: "Impossible de charger les données des ports",
      portsDisplayed: "Ports Affichés",
      hubTransshipment: "Hub Transbordement",
      hubRegional: "Hub Régional",
      commercial: "Commercial",
      sizeTraffic: "Taille = Trafic TEU",
      teuYear: "TEU/an",
      tonsYear: "Tonnes/an",
      portTime: "Temps Port",
      hours: "h"
    },
    en: {
      loading: "Loading map...",
      loadError: "Unable to load port data",
      portsDisplayed: "Ports Displayed",
      hubTransshipment: "Transshipment Hub",
      hubRegional: "Regional Hub",
      commercial: "Commercial",
      sizeTraffic: "Size = TEU Traffic",
      teuYear: "TEU/year",
      tonsYear: "Tons/year",
      portTime: "Port Time",
      hours: "h"
    }
  };

  const t = texts[language];

  useEffect(() => {
    const fetchPorts = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
        const url = selectedCountry && selectedCountry !== 'ALL'
          ? `${API_URL}/api/logistics/ports?country_iso=${selectedCountry}`
          : `${API_URL}/api/logistics/ports`;
        
        const response = await axios.get(url);
        setPorts(response.data.ports || []);
      } catch (err) {
        console.error('Error fetching ports:', err);
        setError('Impossible de charger les données des ports');
      } finally {
        setLoading(false);
      }
    };

    fetchPorts();
  }, [selectedCountry]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96 bg-gray-100 rounded-lg">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">{t.loading}</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-96 bg-red-50 rounded-lg">
        <div className="text-center text-red-600">
          <p className="font-bold">❌ {t.loadError}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative rounded-lg overflow-hidden shadow-xl border-4 border-blue-200">
      <MapContainer
        center={[5, 20]}
        zoom={4}
        style={{ height: '600px', width: '100%' }}
        className="z-0"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <MapController countryIso={selectedCountry} />

        {ports.map((port) => (
          <CircleMarker
            key={port.port_id}
            center={[port.geo_lat, port.geo_lon]}
            radius={calculateRadius(port.latest_stats?.container_throughput_teu)}
            fillColor={getPortColor(port.port_type)}
            color={getPortColor(port.port_type)}
            weight={2}
            fillOpacity={0.6}
            eventHandlers={{
              click: () => {
                if (onPortClick) {
                  onPortClick(port);
                }
              },
            }}
          >
            <Tooltip direction="top" offset={[0, -10]} opacity={0.9}>
              <div className="text-center">
                <strong className="text-sm">{port.port_name}</strong>
                <br />
                <span className="text-xs text-gray-600">{port.country_name}</span>
                <br />
                <span className="text-xs">
                  📦 {port.latest_stats?.container_throughput_teu?.toLocaleString('fr-FR') || 'N/A'} TEU
                </span>
              </div>
            </Tooltip>
          </CircleMarker>
        ))}
      </MapContainer>

      {/* Légende */}
      <div className="absolute bottom-4 right-4 bg-white p-3 rounded-lg shadow-lg z-10 border border-gray-300">
        <p className="text-xs font-bold text-gray-700 mb-2">Type de Port</p>
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-red-500"></div>
            <span className="text-xs">Hub Transhipment</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-orange-500"></div>
            <span className="text-xs">Hub Régional</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-blue-500"></div>
            <span className="text-xs">Commercial</span>
          </div>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Taille = Trafic TEU
        </p>
      </div>

      {/* Info bulle nombre de ports */}
      <div className="absolute top-4 left-4 bg-blue-600 text-white p-3 rounded-lg shadow-lg z-10">
        <p className="text-sm font-bold">🚢 {ports.length} Ports Affichés</p>
      </div>
    </div>
  );
}
