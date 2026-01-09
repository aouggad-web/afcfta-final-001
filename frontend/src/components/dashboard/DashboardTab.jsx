import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  LayoutDashboard, Settings, GripVertical, X, Plus, 
  TrendingUp, Ship, Factory, MapPin, Calculator, FileText 
} from 'lucide-react';

const WIDGET_TYPES = {
  trade_stats: {
    id: 'trade_stats',
    title: { fr: 'Statistiques Commerciales', en: 'Trade Statistics' },
    icon: TrendingUp,
    color: 'from-green-500 to-emerald-600',
    size: 'large'
  },
  port_traffic: {
    id: 'port_traffic',
    title: { fr: 'Trafic Portuaire', en: 'Port Traffic' },
    icon: Ship,
    color: 'from-blue-500 to-cyan-600',
    size: 'medium'
  },
  production: {
    id: 'production',
    title: { fr: 'Production', en: 'Production' },
    icon: Factory,
    color: 'from-purple-500 to-violet-600',
    size: 'medium'
  },
  country_focus: {
    id: 'country_focus',
    title: { fr: 'Pays Focus', en: 'Country Focus' },
    icon: MapPin,
    color: 'from-orange-500 to-red-600',
    size: 'small'
  },
  calculator_quick: {
    id: 'calculator_quick',
    title: { fr: 'Calculateur Rapide', en: 'Quick Calculator' },
    icon: Calculator,
    color: 'from-amber-500 to-yellow-600',
    size: 'small'
  },
  recent_rules: {
    id: 'recent_rules',
    title: { fr: "Règles d'Origine", en: 'Rules of Origin' },
    icon: FileText,
    color: 'from-slate-500 to-gray-600',
    size: 'small'
  }
};

const DEFAULT_LAYOUT = [
  { widgetId: 'trade_stats', x: 0, y: 0, w: 2, h: 2 },
  { widgetId: 'port_traffic', x: 2, y: 0, w: 1, h: 1 },
  { widgetId: 'production', x: 3, y: 0, w: 1, h: 1 },
  { widgetId: 'country_focus', x: 2, y: 1, w: 1, h: 1 },
  { widgetId: 'calculator_quick', x: 3, y: 1, w: 1, h: 1 }
];

export default function DashboardTab({ language = 'fr' }) {
  const [layout, setLayout] = useState(() => {
    const saved = localStorage.getItem('zlecaf_dashboard_layout');
    return saved ? JSON.parse(saved) : DEFAULT_LAYOUT;
  });
  const [isEditing, setIsEditing] = useState(false);
  const [availableWidgets, setAvailableWidgets] = useState([]);

  const texts = {
    fr: {
      title: "Tableau de Bord Personnalisé",
      subtitle: "Configurez votre vue avec les widgets de votre choix",
      editMode: "Mode Édition",
      save: "Enregistrer",
      cancel: "Annuler",
      addWidget: "Ajouter Widget",
      removeWidget: "Retirer",
      resetLayout: "Réinitialiser",
      dragToMove: "Glisser pour déplacer",
      widgetAdded: "Widget ajouté",
      availableWidgets: "Widgets Disponibles",
      noWidgets: "Tous les widgets sont affichés",
      customize: "Personnaliser"
    },
    en: {
      title: "Custom Dashboard",
      subtitle: "Configure your view with widgets of your choice",
      editMode: "Edit Mode",
      save: "Save",
      cancel: "Cancel",
      addWidget: "Add Widget",
      removeWidget: "Remove",
      resetLayout: "Reset Layout",
      dragToMove: "Drag to move",
      widgetAdded: "Widget added",
      availableWidgets: "Available Widgets",
      noWidgets: "All widgets are displayed",
      customize: "Customize"
    }
  };

  const t = texts[language];

  useEffect(() => {
    // Calculate available widgets (not in current layout)
    const usedWidgetIds = layout.map(item => item.widgetId);
    const available = Object.keys(WIDGET_TYPES).filter(id => !usedWidgetIds.includes(id));
    setAvailableWidgets(available);
  }, [layout]);

  const saveLayout = () => {
    localStorage.setItem('zlecaf_dashboard_layout', JSON.stringify(layout));
    setIsEditing(false);
  };

  const resetLayout = () => {
    setLayout(DEFAULT_LAYOUT);
    localStorage.setItem('zlecaf_dashboard_layout', JSON.stringify(DEFAULT_LAYOUT));
  };

  const addWidget = (widgetId) => {
    const newItem = {
      widgetId,
      x: (layout.length % 4),
      y: Math.floor(layout.length / 4),
      w: 1,
      h: 1
    };
    setLayout([...layout, newItem]);
  };

  const removeWidget = (widgetId) => {
    setLayout(layout.filter(item => item.widgetId !== widgetId));
  };

  const renderWidget = (item) => {
    const widget = WIDGET_TYPES[item.widgetId];
    if (!widget) return null;

    const Icon = widget.icon;
    const title = widget.title[language];

    return (
      <Card 
        key={item.widgetId}
        className={`relative overflow-hidden transition-all duration-300 ${
          isEditing ? 'ring-2 ring-dashed ring-blue-400 cursor-move' : ''
        } ${item.w === 2 ? 'col-span-2' : ''} ${item.h === 2 ? 'row-span-2' : ''}`}
      >
        {/* Widget Header */}
        <div className={`bg-gradient-to-r ${widget.color} p-4 text-white`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {isEditing && <GripVertical className="w-4 h-4 opacity-60" />}
              <Icon className="w-5 h-5" />
              <span className="font-semibold">{title}</span>
            </div>
            {isEditing && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeWidget(item.widgetId)}
                className="h-6 w-6 p-0 text-white/80 hover:text-white hover:bg-white/20"
              >
                <X className="w-4 h-4" />
              </Button>
            )}
          </div>
        </div>

        {/* Widget Content */}
        <CardContent className="p-4">
          <WidgetContent widgetId={item.widgetId} language={language} />
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="bg-gradient-to-r from-slate-700 via-slate-800 to-slate-900 text-white shadow-xl">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-3xl font-bold flex items-center gap-3">
                <LayoutDashboard className="w-8 h-8" />
                {t.title}
              </CardTitle>
              <CardDescription className="text-slate-300 text-lg mt-1">
                {t.subtitle}
              </CardDescription>
            </div>
            <div className="flex gap-2">
              {isEditing ? (
                <>
                  <Button variant="outline" onClick={() => setIsEditing(false)} className="text-white border-white/30 hover:bg-white/10">
                    {t.cancel}
                  </Button>
                  <Button onClick={saveLayout} className="bg-green-600 hover:bg-green-700">
                    {t.save}
                  </Button>
                </>
              ) : (
                <Button onClick={() => setIsEditing(true)} className="bg-white/20 hover:bg-white/30">
                  <Settings className="w-4 h-4 mr-2" />
                  {t.customize}
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Edit Mode Panel */}
      {isEditing && (
        <Card className="border-2 border-blue-400 bg-blue-50">
          <CardContent className="pt-4">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div>
                <h3 className="font-bold text-blue-800 flex items-center gap-2">
                  <Plus className="w-5 h-5" />
                  {t.availableWidgets}
                </h3>
                <div className="flex flex-wrap gap-2 mt-2">
                  {availableWidgets.length > 0 ? (
                    availableWidgets.map(widgetId => {
                      const widget = WIDGET_TYPES[widgetId];
                      const Icon = widget.icon;
                      return (
                        <Button
                          key={widgetId}
                          variant="outline"
                          size="sm"
                          onClick={() => addWidget(widgetId)}
                          className="gap-2"
                        >
                          <Icon className="w-4 h-4" />
                          {widget.title[language]}
                        </Button>
                      );
                    })
                  ) : (
                    <span className="text-sm text-gray-500">{t.noWidgets}</span>
                  )}
                </div>
              </div>
              <Button variant="outline" onClick={resetLayout} className="text-red-600 border-red-300 hover:bg-red-50">
                {t.resetLayout}
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Widget Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 auto-rows-min">
        {layout.map(item => renderWidget(item))}
      </div>
    </div>
  );
}

// Widget Content Components
function WidgetContent({ widgetId, language }) {
  switch (widgetId) {
    case 'trade_stats':
      return <TradeStatsWidget language={language} />;
    case 'port_traffic':
      return <PortTrafficWidget language={language} />;
    case 'production':
      return <ProductionWidget language={language} />;
    case 'country_focus':
      return <CountryFocusWidget language={language} />;
    case 'calculator_quick':
      return <CalculatorQuickWidget language={language} />;
    case 'recent_rules':
      return <RecentRulesWidget language={language} />;
    default:
      return <div className="text-gray-500">Widget non disponible</div>;
  }
}

function TradeStatsWidget({ language }) {
  return (
    <div className="space-y-3">
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-green-50 p-3 rounded-lg">
          <p className="text-xs text-green-600 font-medium">{language === 'en' ? 'Intra-African Trade' : 'Commerce Intra-Africain'}</p>
          <p className="text-2xl font-bold text-green-700">$192.5B</p>
          <Badge className="mt-1 bg-green-100 text-green-700 text-xs">+8.2% YoY</Badge>
        </div>
        <div className="bg-blue-50 p-3 rounded-lg">
          <p className="text-xs text-blue-600 font-medium">{language === 'en' ? 'Total Exports' : 'Exports Totaux'}</p>
          <p className="text-2xl font-bold text-blue-700">$556.8B</p>
          <Badge className="mt-1 bg-blue-100 text-blue-700 text-xs">2023</Badge>
        </div>
      </div>
      <div className="bg-amber-50 p-3 rounded-lg">
        <p className="text-xs text-amber-600 font-medium">{language === 'en' ? 'AfCFTA Target 2030' : 'Objectif ZLECAf 2030'}</p>
        <p className="text-xl font-bold text-amber-700">$385B</p>
        <div className="w-full bg-amber-200 rounded-full h-2 mt-2">
          <div className="bg-amber-600 h-2 rounded-full" style={{ width: '50%' }}></div>
        </div>
      </div>
    </div>
  );
}

function PortTrafficWidget({ language }) {
  return (
    <div className="space-y-3">
      <div className="flex justify-between items-center">
        <span className="text-sm text-gray-600">{language === 'en' ? 'African Throughput' : 'Trafic Africain'}</span>
        <span className="font-bold text-blue-700">28.5M TEU</span>
      </div>
      <div className="space-y-2">
        {[
          { port: 'Tanger Med', teu: '7.8M', pct: 100 },
          { port: 'Port Said', teu: '4.2M', pct: 54 },
          { port: 'Durban', teu: '2.9M', pct: 37 },
          { port: 'Alger', teu: '1.4M', pct: 18 }
        ].map(p => (
          <div key={p.port}>
            <div className="flex justify-between text-xs">
              <span>{p.port}</span>
              <span className="font-medium">{p.teu}</span>
            </div>
            <div className="w-full bg-blue-100 rounded-full h-1.5">
              <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: `${p.pct}%` }}></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function ProductionWidget({ language }) {
  return (
    <div className="space-y-2">
      <div className="grid grid-cols-2 gap-2 text-center">
        <div className="bg-purple-50 p-2 rounded">
          <p className="text-xs text-purple-600">{language === 'en' ? 'Agriculture' : 'Agriculture'}</p>
          <p className="font-bold text-purple-700">23%</p>
        </div>
        <div className="bg-indigo-50 p-2 rounded">
          <p className="text-xs text-indigo-600">{language === 'en' ? 'Industry' : 'Industrie'}</p>
          <p className="font-bold text-indigo-700">28%</p>
        </div>
        <div className="bg-violet-50 p-2 rounded">
          <p className="text-xs text-violet-600">{language === 'en' ? 'Services' : 'Services'}</p>
          <p className="font-bold text-violet-700">49%</p>
        </div>
        <div className="bg-fuchsia-50 p-2 rounded">
          <p className="text-xs text-fuchsia-600">{language === 'en' ? 'Mining' : 'Mines'}</p>
          <p className="font-bold text-fuchsia-700">12%</p>
        </div>
      </div>
    </div>
  );
}

function CountryFocusWidget({ language }) {
  return (
    <div className="text-center space-y-2">
      <div className="text-4xl">🇩🇿</div>
      <p className="font-bold">{language === 'en' ? 'Algeria' : 'Algérie'}</p>
      <div className="text-xs text-gray-500 space-y-1">
        <p>PIB: $195B</p>
        <p>{language === 'en' ? 'Pop' : 'Pop'}: 45M</p>
        <p>LSCI: 35.6</p>
      </div>
    </div>
  );
}

function CalculatorQuickWidget({ language }) {
  return (
    <div className="space-y-2">
      <p className="text-xs text-gray-500">{language === 'en' ? 'Quick Estimate' : 'Estimation Rapide'}</p>
      <div className="flex gap-2">
        <input 
          type="text" 
          placeholder="HS Code" 
          className="flex-1 text-xs px-2 py-1 border rounded"
        />
        <Button size="sm" className="text-xs px-2">
          {language === 'en' ? 'Go' : 'OK'}
        </Button>
      </div>
      <p className="text-xs text-gray-400">Ex: 0901 (Café)</p>
    </div>
  );
}

function RecentRulesWidget({ language }) {
  return (
    <div className="space-y-2 text-xs">
      <div className="flex justify-between items-center p-2 bg-gray-50 rounded">
        <span>0901 - {language === 'en' ? 'Coffee' : 'Café'}</span>
        <Badge variant="outline" className="text-xs">40%</Badge>
      </div>
      <div className="flex justify-between items-center p-2 bg-gray-50 rounded">
        <span>8703 - {language === 'en' ? 'Vehicles' : 'Véhicules'}</span>
        <Badge variant="outline" className="text-xs">45%</Badge>
      </div>
      <div className="flex justify-between items-center p-2 bg-gray-50 rounded">
        <span>6204 - {language === 'en' ? 'Clothing' : 'Vêtements'}</span>
        <Badge variant="outline" className="text-xs">35%</Badge>
      </div>
    </div>
  );
}
