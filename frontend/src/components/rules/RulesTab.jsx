import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Separator } from '../ui/separator';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function RulesTab() {
  const [hsCode, setHsCode] = useState('');
  const [rulesOfOrigin, setRulesOfOrigin] = useState(null);

  const fetchRulesOfOrigin = async (code) => {
    try {
      const response = await axios.get(`${API}/rules-of-origin/${code}`);
      setRulesOfOrigin(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des règles d\'origine:', error);
    }
  };

  const getSectorName = (code) => {
    const sector = code.substring(0, 2);
    // This mapping could be more extensive or imported from a shared constant
    return `Secteur ${sector}`; 
  };

  return (
    <div className="space-y-6">
      <Card className="shadow-xl border-t-4 border-t-orange-500">
        <CardHeader className="bg-gradient-to-r from-orange-50 to-red-50">
          <CardTitle className="text-2xl font-bold text-orange-700 flex items-center gap-2">
            <span>📜</span>
            <span>Règles d'Origine ZLECAf</span>
          </CardTitle>
          <CardDescription className="font-semibold text-gray-700">
            Entrez un code SH6 pour consulter les règles d'origine spécifiques
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex space-x-2">
            <Input
              placeholder="Code SH6 (ex: 010121)"
              value={hsCode}
              onChange={(e) => setHsCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
              maxLength={6}
              className="text-lg font-semibold border-2 border-orange-300 focus:border-orange-500"
            />
            <Button 
              onClick={() => fetchRulesOfOrigin(hsCode)} 
              disabled={hsCode.length !== 6}
              className="bg-gradient-to-r from-orange-600 to-red-600 text-white font-bold px-6"
            >
              🔍 Consulter
            </Button>
          </div>
        </CardContent>
      </Card>

      {rulesOfOrigin && (
        <Card className="shadow-2xl border-l-4 border-l-amber-500">
          <CardHeader className="bg-gradient-to-r from-amber-100 to-yellow-100">
            <CardTitle className="text-xl font-bold text-amber-800">Règles pour le Code SH {rulesOfOrigin.hs_code}</CardTitle>
            <CardDescription className="font-semibold text-amber-700">
              Secteur: {getSectorName(rulesOfOrigin.hs_code)}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 pt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-semibold mb-2">Type de Règle</h4>
                <Badge variant="secondary" className="text-lg px-3 py-1">
                  {rulesOfOrigin.rules.rule}
                </Badge>
              </div>
              
              <div>
                <h4 className="font-semibold mb-2">Exigence</h4>
                <p className="text-sm">{rulesOfOrigin.rules.requirement}</p>
              </div>
            </div>

            <div>
              <h4 className="font-semibold mb-2">Contenu Régional Minimum</h4>
              <Progress value={rulesOfOrigin.rules.regional_content} className="w-full" />
              <p className="text-sm text-gray-600 mt-1">
                {rulesOfOrigin.rules.regional_content}% de contenu africain requis
              </p>
            </div>

            <Separator />

            <div>
              <h4 className="font-semibold mb-3">Documentation Requise</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {rulesOfOrigin.explanation.documentation_required.map((doc, index) => (
                  <Badge key={index} variant="outline">
                    {doc}
                  </Badge>
                ))}
              </div>
            </div>

            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="font-semibold text-blue-800 mb-2">Informations Administratives</h4>
              <div className="space-y-1 text-sm text-blue-700">
                <p><strong>Période de validité:</strong> {rulesOfOrigin.explanation.validity_period}</p>
                <p><strong>Autorité émettrice:</strong> {rulesOfOrigin.explanation.issuing_authority}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
