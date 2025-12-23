import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Badge } from '../ui/badge';
import { Separator } from '../ui/separator';
import { Progress } from '../ui/progress';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../ui/table';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
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

export default function CalculatorTab({ countries, language = 'fr' }) {
  const [originCountry, setOriginCountry] = useState('');
  const [destinationCountry, setDestinationCountry] = useState('');
  const [hsCode, setHsCode] = useState('');
  const [value, setValue] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const texts = {
    fr: {
      originCountry: "Pays d'origine",
      partnerCountry: "Pays partenaire",
      hsCodeLabel: "Code SH6 (6 chiffres)",
      valueLabel: "Valeur de la marchandise (USD)",
      calculateBtn: "Calculer avec Données Officielles",
      calculatorTitle: "Calculateur ZLECAf Complet",
      calculatorDesc: "Calculs basés sur les données officielles des organismes internationaux",
      rulesOrigin: "Règles d'Origine ZLECAf"
    },
    en: {
      originCountry: "Origin Country",
      partnerCountry: "Partner Country",
      hsCodeLabel: "HS6 Code (6 digits)",
      valueLabel: "Merchandise Value (USD)",
      calculateBtn: "Calculate with Official Data",
      calculatorTitle: "Complete AfCFTA Calculator",
      calculatorDesc: "Calculations based on official data from international organizations",
      rulesOrigin: "AfCFTA Rules of Origin"
    }
  };

  const t = texts[language];

  const getSectorName = (hsCode) => {
    const sector = hsCode.substring(0, 2);
    // Simple mapping for display purposes - extend as needed
    const sectorNames = {
      '01': 'Animaux vivants', '02': 'Viandes', '03': 'Poissons', '04': 'Lait & Œufs',
      '05': 'Autres produits animaux', '06': 'Plantes', '07': 'Légumes', '08': 'Fruits',
      '09': 'Café/Thé', '10': 'Céréales', '27': 'Combustibles minéraux', '84': 'Machines',
      '85': 'Électrique', '87': 'Véhicules'
    };
    return sectorNames[sector] || `Secteur ${sector}`;
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const getCountryName = (code) => {
    const country = countries.find(c => c.code === code);
    return country ? country.name : code;
  };

  const calculateTariff = async () => {
    if (!originCountry || !destinationCountry || !hsCode || !value) {
      toast({
        title: "Champs manquants",
        description: "Veuillez remplir tous les champs",
        variant: "destructive"
      });
      return;
    }

    if (hsCode.length !== 6) {
      toast({
        title: "Code SH6 invalide",
        description: "Le code SH6 doit contenir exactement 6 chiffres",
        variant: "destructive"
      });
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API}/calculate-tariff`, {
        origin_country: originCountry,
        destination_country: destinationCountry,
        hs_code: hsCode,
        value: parseFloat(value)
      });
      
      setResult(response.data);
      
      toast({
        title: "Calcul réussi",
        description: `Économie potentielle: ${formatCurrency(response.data.savings)}`,
      });
    } catch (error) {
      console.error('Erreur lors du calcul:', error);
      toast({
        title: "Erreur de calcul",
        description: error.response?.data?.detail || "Erreur lors du calcul",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6" style={{ minHeight: '600px' }}>
      {/* Formulaire de calcul */}
      <Card className="shadow-2xl border-t-4 border-t-green-600" style={{ minHeight: '400px' }}>
        <CardHeader className="bg-gradient-to-r from-green-50 to-yellow-50">
          <CardTitle className="flex items-center space-x-2 text-2xl text-green-700">
            <span>📊</span>
            <span>{t.calculatorTitle}</span>
          </CardTitle>
          <CardDescription className="text-gray-700 font-semibold">
            {t.calculatorDesc}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="origin">{t.originCountry}</Label>
              <Select value={originCountry} onValueChange={setOriginCountry}>
                <SelectTrigger>
                  <SelectValue placeholder={t.originCountry} />
                </SelectTrigger>
                <SelectContent>
                  {countries.map((country) => (
                    <SelectItem key={country.code} value={country.code}>
                      {countryFlags[country.code]} {country.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="destination">{t.partnerCountry}</Label>
              <Select value={destinationCountry} onValueChange={setDestinationCountry}>
                <SelectTrigger>
                  <SelectValue placeholder={t.partnerCountry} />
                </SelectTrigger>
                <SelectContent>
                  {countries.map((country) => (
                    <SelectItem key={country.code} value={country.code}>
                      {countryFlags[country.code]} {country.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="hs-code">{t.hsCodeLabel}</Label>
            <Input
              id="hs-code"
              value={hsCode}
              onChange={(e) => setHsCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
              placeholder="Ex : 010121, 180100..."
              maxLength={6}
            />
            {hsCode.length >= 2 && (
              <p className="text-sm text-blue-600">
                {getSectorName(hsCode)}
              </p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="value">{t.valueLabel}</Label>
            <Input
              id="value"
              type="number"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              placeholder="100000"
              min="0"
            />
          </div>

          <Button 
            onClick={calculateTariff}
            disabled={loading}
            className="w-full bg-gradient-to-r from-red-600 via-yellow-500 to-green-600 text-white font-bold text-lg py-6 shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all"
          >
            {loading ? '⏳ Calcul en cours...' : `🧮 ${t.calculateBtn}`}
          </Button>
        </CardContent>
      </Card>

      {/* Résultats complets avec visualisations */}
      {result && (
        <div className="space-y-4">
          <Card className="border-l-4 border-l-green-500 shadow-xl bg-gradient-to-br from-white to-green-50">
            <CardHeader className="bg-gradient-to-r from-green-600 to-yellow-500 text-white rounded-t-lg">
              <CardTitle className="flex items-center space-x-2 text-2xl">
                <span>💰</span>
                <span>Résultats Détaillés</span>
              </CardTitle>
              <CardDescription className="text-yellow-100 font-semibold">
                {countryFlags[result.origin_country]} {getCountryName(result.origin_country)} → {countryFlags[result.destination_country]} {getCountryName(result.destination_country)}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6 pt-6">
              {/* Graphique comparaison complète avec TOUTES les taxes */}
              <div className="bg-white p-4 rounded-lg shadow-md" style={{ minHeight: '320px' }}>
                <h4 className="font-bold text-lg mb-4 text-gray-800">📊 Comparaison Complète: Valeur + DD + TVA + Autres Taxes</h4>
                <ResponsiveContainer width="100%" height={280} debounce={300}>
                  <BarChart data={[
                    { 
                      name: 'Tarif NPF', 
                      'Valeur marchandise': result.value,
                      'Droits douane': result.normal_tariff_amount,
                      'TVA': result.normal_vat_amount,
                      'Autres taxes': result.normal_other_taxes_total
                    },
                    { 
                      name: 'Tarif ZLECAf', 
                      'Valeur marchandise': result.value,
                      'Droits douane': result.zlecaf_tariff_amount,
                      'TVA': result.zlecaf_vat_amount,
                      'Autres taxes': result.zlecaf_other_taxes_total
                    }
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip formatter={(value) => formatCurrency(value)} />
                    <Legend />
                    <Bar dataKey="Valeur marchandise" stackId="a" fill="#60a5fa" />
                    <Bar dataKey="Droits douane" stackId="a" fill="#ef4444" />
                    <Bar dataKey="TVA" stackId="a" fill="#f59e0b" />
                    <Bar dataKey="Autres taxes" stackId="a" fill="#8b5cf6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Économies TOTALES */}
              <div className="text-center bg-gradient-to-r from-yellow-100 via-orange-100 to-red-100 p-8 rounded-2xl shadow-lg border-4 border-yellow-400">
                <p className="text-lg font-bold text-gray-700 mb-2">💰 ÉCONOMIE TOTALE (avec toutes les taxes)</p>
                <p className="text-5xl font-extrabold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent mb-3">
                  {formatCurrency(result.total_savings_with_taxes)}
                </p>
                <Badge className="text-xl px-6 py-2 bg-gradient-to-r from-green-600 to-blue-600 text-white shadow-lg">
                  🎉 {result.total_savings_percentage.toFixed(1)}% d'économie totale
                </Badge>
                <Progress value={result.total_savings_percentage} className="w-full mt-4 h-3" />
                <p className="text-sm text-gray-600 mt-3">
                  Sur un coût total de {formatCurrency(result.normal_total_cost)} (NPF) vs {formatCurrency(result.zlecaf_total_cost)} (ZLECAf)
                </p>
              </div>

              {/* Journal de calcul détaillé */}
              {result.normal_calculation_journal && (
                <Card className="shadow-lg border-t-4 border-t-purple-500">
                  <CardHeader className="bg-gradient-to-r from-purple-50 to-pink-50">
                    <CardTitle className="text-xl font-bold text-purple-700 flex items-center gap-2">
                      <span>📋</span>
                      <span>Journal de Calcul Détaillé (Ordre Officiel)</span>
                    </CardTitle>
                    <CardDescription className="font-semibold">
                      {result.computation_order_ref}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pt-4">
                    <div className="overflow-x-auto">
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>Étape</TableHead>
                            <TableHead>Composant</TableHead>
                            <TableHead>Base</TableHead>
                            <TableHead>Taux</TableHead>
                            <TableHead>Montant</TableHead>
                            <TableHead>Cumulatif</TableHead>
                            <TableHead>Référence Légale</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {result.normal_calculation_journal.map((entry, index) => (
                            <TableRow key={index} className={index % 2 === 0 ? 'bg-gray-50' : ''}>
                              <TableCell className="font-bold">{entry.step}</TableCell>
                              <TableCell className="font-semibold">{entry.component}</TableCell>
                              <TableCell>{formatCurrency(entry.base)}</TableCell>
                              <TableCell>{entry.rate > 0 ? `${entry.rate.toFixed(2)}%` : '-'}</TableCell>
                              <TableCell className="font-bold text-blue-600">{formatCurrency(entry.amount)}</TableCell>
                              <TableCell className="font-bold">{formatCurrency(entry.cumulative)}</TableCell>
                              <TableCell className="text-xs">
                                {entry.legal_ref_url ? (
                                  <a href={entry.legal_ref_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                                    {entry.legal_ref}
                                  </a>
                                ) : (
                                  entry.legal_ref
                                )}
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Règles d'origine avec style africain */}
              <div className="bg-gradient-to-r from-amber-100 to-orange-100 p-6 rounded-xl border-l-4 border-orange-500 shadow-lg">
                <h4 className="font-bold text-xl text-orange-800 mb-3 flex items-center gap-2">
                  <span>📜</span> {t.rulesOrigin}
                </h4>
                <div className="bg-white p-4 rounded-lg space-y-2">
                  <p className="text-sm text-amber-800 font-semibold">
                    <strong className="text-orange-600">Type:</strong> {result.rules_of_origin.rule}
                  </p>
                  <p className="text-sm text-amber-800 font-semibold">
                    <strong className="text-orange-600">Exigence:</strong> {result.rules_of_origin.requirement}
                  </p>
                  <div className="mt-3">
                    <Progress 
                      value={result.rules_of_origin.regional_content} 
                      className="w-full h-3"
                    />
                    <p className="text-sm text-amber-700 mt-2 font-bold text-center">
                      🌍 Contenu régional minimum: {result.rules_of_origin.regional_content}% africain
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
