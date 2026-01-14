import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Separator } from '../ui/separator';
import { HSCodeSearch, HSCodeBrowser } from '../HSCodeSelector';
import { FileText, ChevronDown, ChevronUp, Globe, CheckCircle } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function RulesTab({ language = 'fr' }) {
  const [hsCode, setHsCode] = useState('');
  const [rulesOfOrigin, setRulesOfOrigin] = useState(null);
  const [showBrowser, setShowBrowser] = useState(false);
  const [loading, setLoading] = useState(false);

  const texts = {
    fr: {
      title: "Règles d'Origine ZLECAf",
      description: "Entrez un code SH6 pour consulter les règles d'origine spécifiques",
      placeholder: "Code SH6 (ex: 010121)",
      consult: "Consulter",
      rulesForCode: "Règles pour le Code SH",
      sector: "Secteur",
      ruleType: "Type de Règle",
      requirement: "Exigence",
      minRegionalContent: "Contenu Régional Minimum",
      regionalContentRequired: "de contenu africain requis",
      requiredDocumentation: "Documentation Requise",
      adminInfo: "Informations Administratives",
      validityPeriod: "Période de validité",
      issuingAuthority: "Autorité émettrice",
      errorLoading: "Erreur lors du chargement des règles d'origine"
    },
    en: {
      title: "AfCFTA Rules of Origin",
      description: "Enter an HS6 code to consult specific rules of origin",
      placeholder: "HS6 Code (e.g., 010121)",
      consult: "Consult",
      rulesForCode: "Rules for HS Code",
      sector: "Sector",
      ruleType: "Rule Type",
      requirement: "Requirement",
      minRegionalContent: "Minimum Regional Content",
      regionalContentRequired: "African content required",
      requiredDocumentation: "Required Documentation",
      adminInfo: "Administrative Information",
      validityPeriod: "Validity period",
      issuingAuthority: "Issuing authority",
      errorLoading: "Error loading rules of origin"
    }
  };

  const t = texts[language];

  const fetchRulesOfOrigin = async (code) => {
    try {
      const response = await axios.get(`${API}/rules-of-origin/${code}?lang=${language}`);
      setRulesOfOrigin(response.data);
    } catch (error) {
      console.error(t.errorLoading, error);
    }
  };

  const getSectorName = (code) => {
    const sector = code.substring(0, 2);
    return `${t.sector} ${sector}`; 
  };

  return (
    <div className="space-y-6">
      <Card className="shadow-xl border-t-4 border-t-orange-500">
        <CardHeader className="bg-gradient-to-r from-orange-50 to-red-50">
          <CardTitle className="text-2xl font-bold text-orange-700 flex items-center gap-2">
            <span>📜</span>
            <span>{t.title}</span>
          </CardTitle>
          <CardDescription className="font-semibold text-gray-700">
            {t.description}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex space-x-2">
            <Input
              placeholder={t.placeholder}
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
              🔍 {t.consult}
            </Button>
          </div>
        </CardContent>
      </Card>

      {rulesOfOrigin && (
        <Card className="shadow-2xl border-l-4 border-l-amber-500">
          <CardHeader className="bg-gradient-to-r from-amber-100 to-yellow-100">
            <CardTitle className="text-xl font-bold text-amber-800">{t.rulesForCode} {rulesOfOrigin.hs_code}</CardTitle>
            <CardDescription className="font-semibold text-amber-700">
              {t.sector}: {getSectorName(rulesOfOrigin.hs_code)}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 pt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-semibold mb-2">{t.ruleType}</h4>
                <Badge variant="secondary" className="text-lg px-3 py-1">
                  {rulesOfOrigin.rules.rule}
                </Badge>
              </div>
              
              <div>
                <h4 className="font-semibold mb-2">{t.requirement}</h4>
                <p className="text-sm">{rulesOfOrigin.rules.requirement}</p>
              </div>
            </div>

            <div>
              <h4 className="font-semibold mb-2">{t.minRegionalContent}</h4>
              <Progress value={rulesOfOrigin.rules.regional_content} className="w-full" />
              <p className="text-sm text-gray-600 mt-1">
                {rulesOfOrigin.rules.regional_content}% {t.regionalContentRequired}
              </p>
            </div>

            <Separator />

            <div>
              <h4 className="font-semibold mb-3">{t.requiredDocumentation}</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {rulesOfOrigin.explanation.documentation_required.map((doc, index) => (
                  <Badge key={index} variant="outline">
                    {doc}
                  </Badge>
                ))}
              </div>
            </div>

            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="font-semibold text-blue-800 mb-2">{t.adminInfo}</h4>
              <div className="space-y-1 text-sm text-blue-700">
                <p><strong>{t.validityPeriod}:</strong> {rulesOfOrigin.explanation.validity_period}</p>
                <p><strong>{t.issuingAuthority}:</strong> {rulesOfOrigin.explanation.issuing_authority}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
