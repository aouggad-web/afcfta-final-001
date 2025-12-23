import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Badge } from '../ui/badge';
import { toast } from '../../hooks/use-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const countryFlags = {
  'DZ': '🇩🇿', 'AO': '🇦🇴', 'BJ': '🇧🇯', 'BW': '🇧🇼', 'BF': '🇧🇫', 'BI': '🇧🇮', 'CM': '🇨🇲', 'CV': '🇨🇻',
  'CF': '🇨🇫', 'TD': '🇹🇩', 'KM': '🇰🇲', 'CG': '🇨🇬', 'CD': '🇨🇩', 'CI': '🇨🇮', 'DJ': '🇩🇯', 'EG': '🇪🇬',
  'GQ': '🇬🇶', 'ER': '🇪🇷', 'SZ': '🇸🇿', 'ET': '🇪🇹', 'GA': '🇬🇦', 'GM': '🇬🇲', 'GH': '🇬🇭', 'GN': '🇬🇳',
  'GW': '🇬🇼', 'KE': '🇰🇪', 'LS': '🇱🇸', 'LR': '🇱🇷', 'LY': '🇱🇾', 'MG': '🇲🇬', 'MW': '🇲🇼', 'ML': '🇲🇱',
  'MR': '🇲🇷', 'MU': '🇲🇺', 'MA': '🇲🇦', 'MZ': '🇲🇿', 'NA': '🇳🇦', 'NE': '🇳🇪', 'NG': '🇳🇬', 'RW': '🇷🇼',
  'ST': '🇸🇹', 'SN': '🇸🇳', 'SC': '🇸🇨', 'SL': '🇸🇱', 'SO': '🇸🇴', 'ZA': '🇿🇦', 'SS': '🇸🇸', 'SD': '🇸🇩',
  'TZ': '🇹🇿', 'TG': '🇹🇬', 'TN': '🇹🇳', 'UG': '🇺🇬', 'ZM': '🇿🇲', 'ZW': '🇿🇼'
};

const formatNumber = (number) => {
  return new Intl.NumberFormat('en-US').format(number);
};

export default function CountryProfilesTab() {
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [countryProfile, setCountryProfile] = useState(null);

  useEffect(() => {
    fetchCountries();
  }, []);

  const fetchCountries = async () => {
    try {
      const response = await axios.get(`${API}/countries`);
      setCountries(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des pays:', error);
      toast({
        title: "Erreur",
        description: "Impossible de charger la liste des pays",
        variant: "destructive"
      });
    }
  };

  const fetchCountryProfile = async (countryCode) => {
    try {
      const response = await axios.get(`${API}/country-profile/${countryCode}`);
      setCountryProfile(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement du profil pays:', error);
    }
  };

  return (
    <div className="space-y-6">
      <Card className="shadow-xl border-t-4 border-t-blue-600">
        <CardHeader className="bg-gradient-to-r from-blue-50 to-cyan-50">
          <CardTitle className="text-2xl font-bold text-blue-700 flex items-center gap-2">
            <span>🌍</span>
            <span>Profils Économiques des Pays</span>
          </CardTitle>
          <CardDescription className="font-semibold text-gray-700">
            Sélectionnez un pays pour consulter son profil économique complet, ses infrastructures et ses projets structurants (2025-2030)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Select 
            value={selectedCountry} 
            onValueChange={(value) => {
              setSelectedCountry(value);
              fetchCountryProfile(value);
            }}
          >
            <SelectTrigger className="text-lg font-semibold border-2 border-blue-300 focus:border-blue-500">
              <SelectValue placeholder="🔍 Choisir un pays" />
            </SelectTrigger>
            <SelectContent>
              {countries.map((country) => (
                <SelectItem key={country.code} value={country.code}>
                  {countryFlags[country.code]} {country.name} - {country.region}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </CardContent>
      </Card>

      {countryProfile && (
        <div className="space-y-4">
          <Card className="shadow-2xl border-l-4 border-l-green-600">
            <CardHeader className="bg-gradient-to-r from-green-100 via-yellow-100 to-red-100">
              <CardTitle className="flex items-center space-x-2 text-2xl">
                <span className="text-4xl">{countryFlags[countryProfile.country_code]}</span>
                <span className="font-bold text-green-700">{countryProfile.country_name}</span>
              </CardTitle>
              <CardDescription className="text-lg font-semibold text-gray-700">
                {countryProfile.region} • 👥 Population: {formatNumber(countryProfile.population)} habitants
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-4">
              {/* Indicateurs économiques principaux - COMPACTS */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-3 mb-4">
                {countryProfile.gdp_usd && (
                  <div className="bg-gradient-to-br from-green-50 to-emerald-100 p-3 rounded-lg shadow border border-green-300 text-center">
                    <p className="text-xs font-semibold text-green-700 mb-1">💰 PIB Total</p>
                    <p className="text-2xl font-bold text-green-600">
                      ${(countryProfile.gdp_usd / 1000000000).toFixed(1)}B
                    </p>
                    <p className="text-xs text-green-600 mt-1">Rang: #{countryProfile.projections?.africa_rank || 'N/A'}</p>
                  </div>
                )}
                
                {countryProfile.gdp_per_capita && (
                  <div className="bg-gradient-to-br from-blue-50 to-cyan-100 p-3 rounded-lg shadow border border-blue-300 text-center">
                    <p className="text-xs font-semibold text-blue-700 mb-1">👤 PIB/Habitant</p>
                    <p className="text-2xl font-bold text-blue-600">
                      ${formatNumber(Math.round(countryProfile.gdp_per_capita))}
                    </p>
                    <p className="text-xs text-blue-600 mt-1">USD/personne</p>
                  </div>
                )}
                
                <div className="bg-gradient-to-br from-purple-50 to-pink-100 p-3 rounded-lg shadow border border-purple-300 text-center">
                  <p className="text-xs font-semibold text-purple-700 mb-1">📊 IDH 2024</p>
                  <p className="text-2xl font-bold text-purple-600">
                    {countryProfile.projections?.development_index || 'N/A'}
                  </p>
                  <p className="text-xs text-purple-600 mt-1">Indice Dév. Humain</p>
                </div>

                <div className="bg-gradient-to-br from-orange-50 to-amber-100 p-3 rounded-lg shadow border border-orange-300 text-center">
                  <p className="text-xs font-semibold text-orange-700 mb-1">👥 Population</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {(countryProfile.population / 1000000).toFixed(1)}M
                  </p>
                  <p className="text-xs text-orange-600 mt-1">Millions d'habitants</p>
                </div>
              </div>

              {/* Gold Reserves & GAI 2025 */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                {/* Gold Reserves */}
                {countryProfile.projections?.gold_reserves_tonnes !== undefined && (
                  <div className="bg-gradient-to-br from-yellow-50 to-amber-100 p-4 rounded-lg shadow-lg border-2 border-yellow-400">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-2xl">🥇</span>
                      <p className="text-sm font-bold text-yellow-800">Réserves d'Or</p>
                    </div>
                    <p className="text-3xl font-bold text-yellow-700 mb-2">
                      {countryProfile.projections.gold_reserves_tonnes.toFixed(1)} <span className="text-xl">tonnes</span>
                    </p>
                    <div className="flex gap-3 text-xs">
                      <span className="bg-yellow-200 text-yellow-800 px-2 py-1 rounded font-semibold">
                        🌍 Afrique: #{countryProfile.projections.gold_reserves_rank_africa}
                      </span>
                      {countryProfile.projections.gold_reserves_rank_global && (
                        <span className="bg-yellow-300 text-yellow-900 px-2 py-1 rounded font-semibold">
                          🌎 Mondial: #{countryProfile.projections.gold_reserves_rank_global}
                        </span>
                      )}
                    </div>
                  </div>
                )}

                {/* Global Attractiveness Index 2025 */}
                {countryProfile.projections?.gai_2025_score !== undefined && (
                  <div className="bg-gradient-to-br from-indigo-50 to-purple-100 p-4 rounded-lg shadow-lg border-2 border-indigo-400">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-2xl">📊</span>
                        <p className="text-sm font-bold text-indigo-800">Global Attractiveness Index 2025</p>
                      </div>
                      <span className={`px-3 py-1 rounded-full font-bold text-sm ${
                        countryProfile.projections.gai_2025_rating === 'A' ? 'bg-green-500 text-white' :
                        countryProfile.projections.gai_2025_rating?.startsWith('A') ? 'bg-green-400 text-white' :
                        countryProfile.projections.gai_2025_rating?.startsWith('B') ? 'bg-blue-400 text-white' :
                        countryProfile.projections.gai_2025_rating?.startsWith('C') ? 'bg-yellow-400 text-white' :
                        countryProfile.projections.gai_2025_rating?.startsWith('D') ? 'bg-orange-400 text-white' :
                        'bg-red-400 text-white'
                      }`}>
                        {countryProfile.projections.gai_2025_rating}
                      </span>
                    </div>
                    <div className="flex items-baseline gap-2 mb-2">
                      <p className="text-4xl font-bold text-indigo-700">
                        {countryProfile.projections.gai_2025_score.toFixed(1)}
                      </p>
                      <span className={`text-sm font-semibold px-2 py-1 rounded ${
                        countryProfile.projections.gai_2025_trend === 'improving' ? 'bg-green-200 text-green-800' :
                        countryProfile.projections.gai_2025_trend === 'declining' ? 'bg-red-200 text-red-800' :
                        'bg-gray-200 text-gray-800'
                      }`}>
                        {countryProfile.projections.gai_2025_trend === 'improving' ? '📈 En hausse' :
                         countryProfile.projections.gai_2025_trend === 'declining' ? '📉 En baisse' :
                         '➡️ Stable'}
                      </span>
                    </div>
                    <div className="flex gap-3 text-xs">
                      <span className="bg-indigo-200 text-indigo-800 px-2 py-1 rounded font-semibold">
                        🌍 Afrique: #{countryProfile.projections.gai_2025_rank_africa}
                      </span>
                      <span className="bg-purple-200 text-purple-800 px-2 py-1 rounded font-semibold">
                        🌎 Mondial: #{countryProfile.projections.gai_2025_rank_global}
                      </span>
                    </div>
                  </div>
                )}
              </div>

              {/* Section Perspectives & Projets Structurants (Nouveau) */}
              {countryProfile.ongoing_projects && countryProfile.ongoing_projects.length > 0 && (
                <div className="mb-4">
                  <Card className="shadow-xl border-t-4 border-t-emerald-600">
                    <CardHeader className="bg-gradient-to-r from-emerald-50 to-teal-50">
                      <CardTitle className="text-xl font-bold text-emerald-700 flex items-center gap-2">
                        <span>🏗️</span>
                        <span>Projets Structurants & Perspectives 2030</span>
                      </CardTitle>
                      <CardDescription className="font-semibold text-gray-700">
                        Investissements majeurs en cours de réalisation (Rail, Ports, Mines, Énergie)
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="pt-6">
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {countryProfile.ongoing_projects.map((project, index) => (
                          <div key={index} className="bg-white rounded-xl shadow-md border border-gray-200 hover:shadow-lg transition-shadow overflow-hidden flex flex-col">
                            <div className="bg-emerald-600 text-white p-3">
                              <h5 className="font-bold text-sm leading-tight">{project.titre}</h5>
                            </div>
                            <div className="p-4 flex-grow flex flex-col gap-3">
                              <div className="flex justify-between items-start">
                                <Badge variant="outline" className="bg-emerald-50 text-emerald-700 border-emerald-200">
                                  {project.secteur}
                                </Badge>
                                <span className="text-xs font-bold text-gray-500 bg-gray-100 px-2 py-1 rounded">
                                  🏁 {project.echeance}
                                </span>
                              </div>
                              
                              <div className="space-y-2 text-sm text-gray-600 flex-grow">
                                <p className="line-clamp-3">{project.description}</p>
                                
                                <div className="bg-gray-50 p-2 rounded text-xs border border-gray-100">
                                  <p><strong>💰 Budget:</strong> {project.budget}</p>
                                  <p><strong>🚀 Impact:</strong> {project.impact}</p>
                                </div>
                              </div>
                              
                              <div className="mt-auto pt-3 border-t border-gray-100 text-xs text-gray-400 flex justify-between items-center">
                                <span className="truncate max-w-[70%]">🤝 {project.partenaires}</span>
                                <span className="italic">{project.statut}</span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}

              {/* World Bank Data360 Indicators */}
              {countryProfile.projections?.life_expectancy_2023 && (
                <div className="mb-4">
                  <Card className="shadow-xl border-t-4 border-t-blue-600">
                    <CardHeader className="bg-gradient-to-r from-blue-50 to-cyan-50">
                      <CardTitle className="text-xl font-bold text-blue-700 flex items-center gap-2">
                        <span>🌐</span>
                        <span>Indicateurs World Bank Data360 (2024)</span>
                      </CardTitle>
                      <p className="text-sm text-blue-600 mt-1">
                        Données officielles de la Banque Mondiale - Mis à jour 2024
                      </p>
                    </CardHeader>
                    <CardContent className="pt-6">
                      {/* Section 1: People (Social) */}
                      <div className="mb-6">
                        <h4 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                          <span>👥</span>
                          <span>Indicateurs Sociaux</span>
                        </h4>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                          <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-3 rounded-lg border-l-4 border-green-500">
                            <p className="text-xs font-semibold text-green-700">🏥 Espérance de vie</p>
                            <p className="text-2xl font-bold text-green-600">
                              {countryProfile.projections.life_expectancy_2023}
                            </p>
                            <p className="text-xs text-gray-600">ans (2023)</p>
                          </div>
                          
                          {countryProfile.projections.gini_index_2024 && (
                            <div className="bg-gradient-to-br from-orange-50 to-amber-50 p-3 rounded-lg border-l-4 border-orange-500">
                              <p className="text-xs font-semibold text-orange-700">📊 Indice Gini</p>
                              <p className="text-2xl font-bold text-orange-600">
                                {parseFloat(countryProfile.projections.gini_index_2024).toFixed(1)}
                              </p>
                              <p className="text-xs text-gray-600">sur 100 (2024)</p>
                            </div>
                          )}
                          
                          {countryProfile.projections.poverty_rate_3usd_2024 && (
                            <div className="bg-gradient-to-br from-red-50 to-rose-50 p-3 rounded-lg border-l-4 border-red-500">
                              <p className="text-xs font-semibold text-red-700">💰 Pauvreté ($3/jour)</p>
                              <p className="text-2xl font-bold text-red-600">
                                {parseFloat(countryProfile.projections.poverty_rate_3usd_2024).toFixed(1)}%
                              </p>
                              <p className="text-xs text-gray-600">population (2024)</p>
                            </div>
                          )}
                          
                          {countryProfile.projections.urban_population_pct_2024 && (
                            <div className="bg-gradient-to-br from-purple-50 to-indigo-50 p-3 rounded-lg border-l-4 border-purple-500">
                              <p className="text-xs font-semibold text-purple-700">🏙️ Population urbaine</p>
                              <p className="text-2xl font-bold text-purple-600">
                                {parseFloat(countryProfile.projections.urban_population_pct_2024).toFixed(1)}%
                              </p>
                              <p className="text-xs text-gray-600">du total (2024)</p>
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Section 2: Digital & Infrastructure */}
                      <div className="mb-6">
                        <h4 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                          <span>💻</span>
                          <span>Digital & Connectivité</span>
                        </h4>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                          {countryProfile.projections.internet_users_pct_2024 && (
                            <div className="bg-gradient-to-br from-blue-50 to-sky-50 p-3 rounded-lg border-l-4 border-blue-500">
                              <p className="text-xs font-semibold text-blue-700">🌐 Accès Internet</p>
                              <p className="text-2xl font-bold text-blue-600">
                                {parseFloat(countryProfile.projections.internet_users_pct_2024).toFixed(1)}%
                              </p>
                              <p className="text-xs text-gray-600">population (2024)</p>
                            </div>
                          )}
                          
                          {countryProfile.projections.cybersecurity_index_2024 && (
                            <div className="bg-gradient-to-br from-indigo-50 to-purple-50 p-3 rounded-lg border-l-4 border-indigo-500">
                              <p className="text-xs font-semibold text-indigo-700">🔒 Cybersécurité</p>
                              <p className="text-2xl font-bold text-indigo-600">
                                {parseFloat(countryProfile.projections.cybersecurity_index_2024).toFixed(1)}
                              </p>
                              <p className="text-xs text-gray-600">ITU GCI (2024)</p>
                            </div>
                          )}
                          
                          {countryProfile.projections.electricity_access_2022 && (
                            <div className="bg-gradient-to-br from-yellow-50 to-amber-50 p-3 rounded-lg border-l-4 border-yellow-500">
                              <p className="text-xs font-semibold text-yellow-700">⚡ Accès Électricité</p>
                              <p className="text-2xl font-bold text-yellow-600">
                                {parseFloat(countryProfile.projections.electricity_access_2022).toFixed(0)}%
                              </p>
                              <p className="text-xs text-gray-600">population (2022)</p>
                            </div>
                          )}
                          
                          {countryProfile.projections.mobile_3g_coverage_2024 && (
                            <div className="bg-gradient-to-br from-teal-50 to-cyan-50 p-3 rounded-lg border-l-4 border-teal-500">
                              <p className="text-xs font-semibold text-teal-700">📱 Couverture 3G</p>
                              <p className="text-2xl font-bold text-teal-600">
                                {parseFloat(countryProfile.projections.mobile_3g_coverage_2024).toFixed(0)}%
                              </p>
                              <p className="text-xs text-gray-600">population (2024)</p>
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Section 3: Environment & Gender */}
                      <div>
                        <h4 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                          <span>🌍</span>
                          <span>Environnement & Égalité</span>
                        </h4>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                          {countryProfile.projections.female_labor_force_pct_2024 && (
                            <div className="bg-gradient-to-br from-pink-50 to-rose-50 p-3 rounded-lg border-l-4 border-pink-500">
                              <p className="text-xs font-semibold text-pink-700">👩‍💼 Femmes actives</p>
                              <p className="text-2xl font-bold text-pink-600">
                                {parseFloat(countryProfile.projections.female_labor_force_pct_2024).toFixed(1)}%
                              </p>
                              <p className="text-xs text-gray-600">pop. fém. (2024)</p>
                            </div>
                          )}
                          
                          {countryProfile.projections.water_stress_2022 && (
                            <div className="bg-gradient-to-br from-blue-50 to-cyan-50 p-3 rounded-lg border-l-4 border-blue-500">
                              <p className="text-xs font-semibold text-blue-700">💧 Stress hydrique</p>
                              <p className="text-2xl font-bold text-blue-600">
                                {parseFloat(countryProfile.projections.water_stress_2022).toFixed(1)}%
                              </p>
                              <p className="text-xs text-gray-600">ressources (2022)</p>
                            </div>
                          )}
                          
                          {countryProfile.projections.ghg_emissions_mt_2022 && (
                            <div className="bg-gradient-to-br from-gray-50 to-slate-50 p-3 rounded-lg border-l-4 border-gray-500">
                              <p className="text-xs font-semibold text-gray-700">🏭 Émissions GES</p>
                              <p className="text-2xl font-bold text-gray-600">
                                {parseFloat(countryProfile.projections.ghg_emissions_mt_2022).toFixed(1)}
                              </p>
                              <p className="text-xs text-gray-600">Mt CO₂e (2022)</p>
                            </div>
                          )}
                          
                          {countryProfile.projections.learning_poverty_2023 && (
                            <div className="bg-gradient-to-br from-violet-50 to-purple-50 p-3 rounded-lg border-l-4 border-violet-500">
                              <p className="text-xs font-semibold text-violet-700">📚 Pauvreté éducative</p>
                              <p className="text-2xl font-bold text-violet-600">
                                {parseFloat(countryProfile.projections.learning_poverty_2023).toFixed(1)}%
                              </p>
                              <p className="text-xs text-gray-600">enfants (2023)</p>
                            </div>
                          )}
                        </div>
                      </div>
                      
                      {/* Source footer */}
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <p className="text-xs text-gray-500 text-center">
                          Source: <strong>World Bank Data360</strong> - Données officielles de la Banque Mondiale (2024) • 
                          <a href="https://data360.worldbank.org" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline ml-1">
                            data360.worldbank.org
                          </a>
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}

              {/* Infrastructure Section (AIDI 2025 & LPI 2023) */}
              {countryProfile.infrastructure_ranking && (
                <Card className="shadow-lg border-l-4 border-l-orange-500">
                  <CardHeader className="bg-gradient-to-r from-orange-50 to-yellow-50">
                    <CardTitle className="text-xl font-bold text-orange-700 flex items-center gap-2">
                      <span>🏗️</span>
                      <span>Performance Infrastructure & Logistique</span>
                    </CardTitle>
                    <CardDescription className="font-semibold text-gray-700">
                      Classement continental (AIDI 2025) et mondial (LPI 2023)
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pt-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-purple-50 p-3 rounded-lg text-center">
                        <p className="text-xs font-semibold text-purple-700 mb-1">📊 Score IPL (LPI)</p>
                        <p className="text-2xl font-bold text-purple-600">
                          {countryProfile.infrastructure_ranking.lpi_infrastructure_score}/5
                        </p>
                        <p className="text-xs text-purple-600 mt-1">Infrastructure</p>
                        <div className="mt-2 text-xs bg-purple-100 rounded px-2 py-1">
                          Rang Mondial: <strong>#{countryProfile.infrastructure_ranking.lpi_world_rank}</strong>
                        </div>
                      </div>
                      
                      <div className="bg-orange-50 p-3 rounded-lg text-center">
                        <p className="text-xs font-semibold text-orange-700 mb-1">🏗️ Score AIDI 2025</p>
                        <p className="text-2xl font-bold text-orange-600">
                          {countryProfile.infrastructure_ranking.aidi_transport_score}/100
                        </p>
                        <p className="text-xs text-orange-600 mt-1">Indice Global</p>
                        <div className="mt-2 text-xs bg-orange-100 rounded px-2 py-1">
                          Rang Afrique: <strong>#{countryProfile.infrastructure_ranking.africa_rank}</strong>
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-4 bg-gray-50 p-3 rounded-lg">
                      <p className="text-xs text-gray-700">
                        <strong>IPL (Indice de Performance Logistique)</strong> : Évalue la qualité des infrastructures liées au commerce et au transport (Banque Mondiale).
                        <br />
                        <strong>AIDI (Africa Infrastructure Development Index)</strong> : Mesure composite du développement des infrastructures (Transport, Électricité, TIC, Eau) par la BAD.
                      </p>
                    </div>
                  </CardContent>
                </Card>
              )}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
