import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Badge } from '../ui/badge';
import { 
  TrendingUp, Ship, Globe, Target, BarChart3, RefreshCw
} from 'lucide-react';
import NewsDashboard from './NewsDashboard';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Mini Widget Component
const MiniWidget = ({ title, value, subtitle, icon: Icon, color, trend }) => (
  <Card className={`shadow-md hover:shadow-lg transition-shadow bg-gradient-to-br ${color}`}>
    <CardContent className="p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs text-white/80 font-medium">{title}</p>
          <p className="text-2xl font-bold text-white">{value}</p>
          <p className="text-xs text-white/70">{subtitle}</p>
        </div>
        <div className="p-3 bg-white/20 rounded-full">
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
      {trend && (
        <div className={`mt-2 text-xs ${trend > 0 ? 'text-green-200' : 'text-red-200'}`}>
          {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}% vs 2023
        </div>
      )}
    </CardContent>
  </Card>
);

// Traductions
const translations = {
  fr: {
    overview: "Vue d'ensemble ZLECAf",
    totalGdp: "PIB Combiné Afrique",
    intraAfricanTrade: "Commerce Intra-Africain",
    majorPorts: "Ports Majeurs",
    afcftaProgress: "Progression ZLECAf",
    countries: "pays membres",
    billion: "milliards USD",
    growth: "Croissance 2024",
    source: "Source: FMI WEO Oct 2025, UNCTAD"
  },
  en: {
    overview: "AfCFTA Overview",
    totalGdp: "Combined Africa GDP",
    intraAfricanTrade: "Intra-African Trade",
    majorPorts: "Major Ports",
    afcftaProgress: "AfCFTA Progress",
    countries: "member countries",
    billion: "billion USD",
    growth: "Growth 2024",
    source: "Source: IMF WEO Oct 2025, UNCTAD"
  }
};

const DashboardTabNew = ({ language = 'fr' }) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const t = translations[language] || translations.fr;

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch(`${API}/statistics`);
        const data = await response.json();
        setStats(data);
      } catch (error) {
        console.error('Error fetching stats:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="space-y-6 p-4">
      {/* En-tête avec statistiques clés */}
      <div className="mb-6">
        <h2 className="text-xl font-bold text-gray-800 mb-1 flex items-center gap-2">
          <Globe className="w-6 h-6 text-green-600" />
          {t.overview}
        </h2>
        <p className="text-sm text-gray-500">{t.source}</p>
      </div>

      {/* Widgets statistiques clés - Compact */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MiniWidget
          title={t.totalGdp}
          value="$2.7T"
          subtitle={`54 ${t.countries}`}
          icon={BarChart3}
          color="from-green-600 to-emerald-700"
        />
        <MiniWidget
          title={t.intraAfricanTrade}
          value="$235B"
          subtitle={t.growth + ": +7.7%"}
          icon={TrendingUp}
          color="from-blue-600 to-cyan-700"
          trend={7.7}
        />
        <MiniWidget
          title={t.majorPorts}
          value="68"
          subtitle="35.5M TEU/an"
          icon={Ship}
          color="from-indigo-600 to-purple-700"
          trend={8.1}
        />
        <MiniWidget
          title={t.afcftaProgress}
          value="57%"
          subtitle="Phase 2 en cours"
          icon={Target}
          color="from-amber-600 to-orange-700"
        />
      </div>

      {/* Section principale: Fil d'actualités */}
      <NewsDashboard language={language} />
    </div>
  );
};

export default DashboardTabNew;
