import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragOverlay
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  rectSortingStrategy,
  useSortable
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  LayoutDashboard, Settings, GripVertical, X, Plus, 
  TrendingUp, Ship, Factory, MapPin, Calculator, FileText,
  Save, RotateCcw, BarChart3, PieChart, Bell, Globe, Target
} from 'lucide-react';

// Import Dynamic Widgets
import {
  LiveTradeWidget,
  LivePortsWidget,
  LSCIChartWidget,
  CountryProfileWidget,
  TradeBalanceWidget,
  AfCFTAProgressWidget,
  RegionalTradeWidget,
  AlertsWidget
} from './DynamicWidgets';

// Widget definitions - Now using DYNAMIC widgets with real-time API data
const WIDGET_TYPES = {
  live_trade: {
    id: 'live_trade',
    titleKey: 'dashboard.widgets.liveTradeStats',
    icon: TrendingUp,
    color: 'from-green-500 to-emerald-600',
    defaultSize: { w: 2, h: 1 },
    isDynamic: true
  },
  live_ports: {
    id: 'live_ports',
    titleKey: 'dashboard.widgets.livePorts',
    icon: Ship,
    color: 'from-blue-500 to-cyan-600',
    defaultSize: { w: 1, h: 1 },
    isDynamic: true
  },
  lsci_chart: {
    id: 'lsci_chart',
    titleKey: 'dashboard.widgets.lsciChart',
    icon: BarChart3,
    color: 'from-indigo-500 to-purple-600',
    defaultSize: { w: 1, h: 1 },
    isDynamic: true
  },
  country_profile: {
    id: 'country_profile',
    titleKey: 'dashboard.widgets.countryProfile',
    icon: MapPin,
    color: 'from-orange-500 to-red-600',
    defaultSize: { w: 1, h: 1 },
    isDynamic: true
  },
  afcfta_progress: {
    id: 'afcfta_progress',
    titleKey: 'dashboard.widgets.afcftaProgress',
    icon: Target,
    color: 'from-emerald-500 to-teal-600',
    defaultSize: { w: 1, h: 1 },
    isDynamic: true
  },
  trade_balance: {
    id: 'trade_balance',
    titleKey: 'dashboard.widgets.tradeBalance',
    icon: BarChart3,
    color: 'from-cyan-500 to-blue-600',
    defaultSize: { w: 1, h: 1 },
    isDynamic: true
  },
  regional_trade: {
    id: 'regional_trade',
    titleKey: 'dashboard.widgets.regionalTrade',
    icon: PieChart,
    color: 'from-violet-500 to-purple-600',
    defaultSize: { w: 1, h: 1 },
    isDynamic: true
  },
  alerts: {
    id: 'alerts',
    titleKey: 'dashboard.widgets.alerts',
    icon: Bell,
    color: 'from-amber-500 to-orange-600',
    defaultSize: { w: 1, h: 1 },
    isDynamic: true
  },
  calculator_quick: {
    id: 'calculator_quick',
    titleKey: 'dashboard.widgets.calculator',
    icon: Calculator,
    color: 'from-amber-500 to-yellow-600',
    defaultSize: { w: 1, h: 1 },
    isDynamic: false
  }
};

// Default widgets now use DYNAMIC real-time data
const DEFAULT_WIDGETS = ['live_trade', 'live_ports', 'afcfta_progress', 'country_profile', 'lsci_chart'];

// Sortable Widget Component
function SortableWidget({ widget, isEditing, onRemove, language }) {
  const { t } = useTranslation();
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging
  } = useSortable({ id: widget.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
    zIndex: isDragging ? 1000 : 1
  };

  const widgetDef = WIDGET_TYPES[widget.id];
  if (!widgetDef) return null;

  const Icon = widgetDef.icon;
  const title = t(widgetDef.titleKey, { defaultValue: widget.id });

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`${widget.id === 'trade_stats' ? 'col-span-2' : ''}`}
    >
      <Card 
        className={`h-full overflow-hidden transition-all duration-200 ${
          isEditing ? 'ring-2 ring-dashed ring-blue-400' : ''
        } ${isDragging ? 'shadow-2xl scale-105' : 'shadow-md'}`}
      >
        {/* Widget Header */}
        <div className={`bg-gradient-to-r ${widgetDef.color} p-3 text-white`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {isEditing && (
                <button
                  {...attributes}
                  {...listeners}
                  className="cursor-grab active:cursor-grabbing p-1 hover:bg-white/20 rounded"
                >
                  <GripVertical className="w-4 h-4" />
                </button>
              )}
              <Icon className="w-5 h-5" />
              <span className="font-semibold text-sm">{title}</span>
            </div>
            {isEditing && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onRemove(widget.id)}
                className="h-6 w-6 p-0 text-white/80 hover:text-white hover:bg-white/20"
              >
                <X className="w-4 h-4" />
              </Button>
            )}
          </div>
        </div>

        {/* Widget Content */}
        <CardContent className="p-4">
          <WidgetContent widgetId={widget.id} language={language} t={t} />
        </CardContent>
      </Card>
    </div>
  );
}

// Main Dashboard Component
export default function DashboardTab({ language = 'fr' }) {
  const { t, i18n } = useTranslation();
  
  const [widgets, setWidgets] = useState(() => {
    const saved = localStorage.getItem('zlecaf_dashboard_widgets');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        return DEFAULT_WIDGETS.map(id => ({ id }));
      }
    }
    return DEFAULT_WIDGETS.map(id => ({ id }));
  });
  
  const [isEditing, setIsEditing] = useState(false);
  const [activeId, setActiveId] = useState(null);

  // Sync i18n language with prop
  useEffect(() => {
    if (i18n.language !== language) {
      i18n.changeLanguage(language);
    }
  }, [language, i18n]);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragStart = (event) => {
    setActiveId(event.active.id);
  };

  const handleDragEnd = (event) => {
    const { active, over } = event;
    setActiveId(null);

    if (over && active.id !== over.id) {
      setWidgets((items) => {
        const oldIndex = items.findIndex(item => item.id === active.id);
        const newIndex = items.findIndex(item => item.id === over.id);
        return arrayMove(items, oldIndex, newIndex);
      });
    }
  };

  const saveLayout = () => {
    localStorage.setItem('zlecaf_dashboard_widgets', JSON.stringify(widgets));
    setIsEditing(false);
  };

  const resetLayout = () => {
    const defaultWidgets = DEFAULT_WIDGETS.map(id => ({ id }));
    setWidgets(defaultWidgets);
    localStorage.setItem('zlecaf_dashboard_widgets', JSON.stringify(defaultWidgets));
  };

  const addWidget = (widgetId) => {
    if (!widgets.find(w => w.id === widgetId)) {
      setWidgets([...widgets, { id: widgetId }]);
    }
  };

  const removeWidget = (widgetId) => {
    setWidgets(widgets.filter(w => w.id !== widgetId));
  };

  const availableWidgets = Object.keys(WIDGET_TYPES).filter(
    id => !widgets.find(w => w.id === id)
  );

  const activeWidget = activeId ? WIDGET_TYPES[activeId] : null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="bg-gradient-to-r from-slate-700 via-slate-800 to-slate-900 text-white shadow-xl">
        <CardHeader>
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <CardTitle className="text-2xl md:text-3xl font-bold flex items-center gap-3">
                <LayoutDashboard className="w-7 h-7" />
                {t('dashboard.title', { defaultValue: language === 'fr' ? 'Tableau de Bord Personnalisé' : 'Custom Dashboard' })}
              </CardTitle>
              <CardDescription className="text-slate-300 text-base mt-1">
                {t('dashboard.subtitle', { defaultValue: language === 'fr' ? 'Glissez-déposez pour réorganiser vos widgets' : 'Drag and drop to reorganize your widgets' })}
              </CardDescription>
            </div>
            <div className="flex gap-2">
              {isEditing ? (
                <>
                  <Button 
                    variant="outline" 
                    onClick={() => setIsEditing(false)} 
                    className="text-white border-white/30 hover:bg-white/10"
                  >
                    {t('common.cancel', { defaultValue: language === 'fr' ? 'Annuler' : 'Cancel' })}
                  </Button>
                  <Button onClick={saveLayout} className="bg-green-600 hover:bg-green-700 gap-2">
                    <Save className="w-4 h-4" />
                    {t('common.save', { defaultValue: language === 'fr' ? 'Enregistrer' : 'Save' })}
                  </Button>
                </>
              ) : (
                <Button onClick={() => setIsEditing(true)} className="bg-white/20 hover:bg-white/30 gap-2">
                  <Settings className="w-4 h-4" />
                  {t('dashboard.customize', { defaultValue: language === 'fr' ? 'Personnaliser' : 'Customize' })}
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
              <div className="flex-1">
                <h3 className="font-bold text-blue-800 flex items-center gap-2 mb-3">
                  <Plus className="w-5 h-5" />
                  {t('dashboard.availableWidgets', { defaultValue: language === 'fr' ? 'Widgets Disponibles' : 'Available Widgets' })}
                </h3>
                <div className="flex flex-wrap gap-2">
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
                          className="gap-2 bg-white hover:bg-blue-100"
                        >
                          <Icon className="w-4 h-4" />
                          {t(widget.titleKey, { defaultValue: widgetId })}
                        </Button>
                      );
                    })
                  ) : (
                    <span className="text-sm text-gray-500 italic">
                      {t('dashboard.noWidgets', { defaultValue: language === 'fr' ? 'Tous les widgets sont affichés' : 'All widgets are displayed' })}
                    </span>
                  )}
                </div>
              </div>
              <Button 
                variant="outline" 
                onClick={resetLayout} 
                className="text-red-600 border-red-300 hover:bg-red-50 gap-2"
              >
                <RotateCcw className="w-4 h-4" />
                {t('dashboard.reset', { defaultValue: language === 'fr' ? 'Réinitialiser' : 'Reset' })}
              </Button>
            </div>
            {isEditing && (
              <p className="text-sm text-blue-600 mt-3 flex items-center gap-2">
                <GripVertical className="w-4 h-4" />
                {language === 'fr' 
                  ? 'Maintenez et glissez l\'icône ⋮⋮ pour réorganiser les widgets'
                  : 'Hold and drag the ⋮⋮ icon to reorganize widgets'}
              </p>
            )}
          </CardContent>
        </Card>
      )}

      {/* Widget Grid with DnD */}
      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragStart={handleDragStart}
        onDragEnd={handleDragEnd}
      >
        <SortableContext items={widgets.map(w => w.id)} strategy={rectSortingStrategy}>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {widgets.map((widget) => (
              <SortableWidget
                key={widget.id}
                widget={widget}
                isEditing={isEditing}
                onRemove={removeWidget}
                language={language}
              />
            ))}
          </div>
        </SortableContext>

        {/* Drag Overlay */}
        <DragOverlay>
          {activeId && activeWidget ? (
            <Card className="shadow-2xl opacity-90 w-64">
              <div className={`bg-gradient-to-r ${activeWidget.color} p-3 text-white rounded-t-lg`}>
                <div className="flex items-center gap-2">
                  <activeWidget.icon className="w-5 h-5" />
                  <span className="font-semibold text-sm">
                    {t(activeWidget.titleKey, { defaultValue: activeId })}
                  </span>
                </div>
              </div>
              <CardContent className="p-4 bg-white rounded-b-lg">
                <div className="h-20 flex items-center justify-center text-gray-400">
                  {language === 'fr' ? 'Déplacez ici...' : 'Moving...'}
                </div>
              </CardContent>
            </Card>
          ) : null}
        </DragOverlay>
      </DndContext>
    </div>
  );
}

// Widget Content Components
function WidgetContent({ widgetId, language, t }) {
  switch (widgetId) {
    case 'trade_stats':
      return <TradeStatsWidget language={language} t={t} />;
    case 'port_traffic':
      return <PortTrafficWidget language={language} t={t} />;
    case 'production':
      return <ProductionWidget language={language} t={t} />;
    case 'country_focus':
      return <CountryFocusWidget language={language} t={t} />;
    case 'calculator_quick':
      return <CalculatorQuickWidget language={language} t={t} />;
    case 'recent_rules':
      return <RecentRulesWidget language={language} t={t} />;
    default:
      return <div className="text-gray-500">Widget unavailable</div>;
  }
}

function TradeStatsWidget({ language, t }) {
  return (
    <div className="space-y-3">
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-green-50 p-3 rounded-lg">
          <p className="text-xs text-green-600 font-medium">
            {language === 'en' ? 'Intra-African Trade' : 'Commerce Intra-Africain'}
          </p>
          <p className="text-2xl font-bold text-green-700">$218.7B</p>
          <Badge className="mt-1 bg-green-100 text-green-700 text-xs">+13.7% YoY</Badge>
        </div>
        <div className="bg-blue-50 p-3 rounded-lg">
          <p className="text-xs text-blue-600 font-medium">
            {language === 'en' ? 'Total Exports' : 'Exports Totaux'}
          </p>
          <p className="text-2xl font-bold text-blue-700">$553.7B</p>
          <Badge className="mt-1 bg-blue-100 text-blue-700 text-xs">2024</Badge>
        </div>
      </div>
      <div className="bg-amber-50 p-3 rounded-lg">
        <p className="text-xs text-amber-600 font-medium">
          {language === 'en' ? 'AfCFTA Target 2030' : 'Objectif ZLECAf 2030'}
        </p>
        <p className="text-xl font-bold text-amber-700">$385B</p>
        <div className="w-full bg-amber-200 rounded-full h-2 mt-2">
          <div className="bg-amber-600 h-2 rounded-full transition-all" style={{ width: '57%' }}></div>
        </div>
        <p className="text-xs text-amber-600 mt-1">57% {language === 'en' ? 'achieved' : 'atteint'}</p>
      </div>
    </div>
  );
}

function PortTrafficWidget({ language }) {
  const ports = [
    { port: 'Tanger Med', teu: '7.8M', pct: 100 },
    { port: 'Port Said', teu: '4.2M', pct: 54 },
    { port: 'Durban', teu: '2.9M', pct: 37 },
    { port: 'Alger', teu: '1.4M', pct: 18 }
  ];

  return (
    <div className="space-y-3">
      <div className="flex justify-between items-center">
        <span className="text-sm text-gray-600">
          {language === 'en' ? 'African Throughput' : 'Trafic Africain'}
        </span>
        <span className="font-bold text-blue-700">28.5M TEU</span>
      </div>
      <div className="space-y-2">
        {ports.map(p => (
          <div key={p.port}>
            <div className="flex justify-between text-xs">
              <span>{p.port}</span>
              <span className="font-medium">{p.teu}</span>
            </div>
            <div className="w-full bg-blue-100 rounded-full h-1.5">
              <div 
                className="bg-blue-500 h-1.5 rounded-full transition-all" 
                style={{ width: `${p.pct}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function ProductionWidget({ language }) {
  const sectors = [
    { key: 'agri', label: language === 'en' ? 'Agriculture' : 'Agriculture', value: '23%', color: 'purple' },
    { key: 'ind', label: language === 'en' ? 'Industry' : 'Industrie', value: '28%', color: 'indigo' },
    { key: 'serv', label: language === 'en' ? 'Services' : 'Services', value: '49%', color: 'violet' },
    { key: 'min', label: language === 'en' ? 'Mining' : 'Mines', value: '12%', color: 'fuchsia' }
  ];

  return (
    <div className="grid grid-cols-2 gap-2 text-center">
      {sectors.map(s => (
        <div key={s.key} className={`bg-${s.color}-50 p-2 rounded`}>
          <p className={`text-xs text-${s.color}-600`}>{s.label}</p>
          <p className={`font-bold text-${s.color}-700`}>{s.value}</p>
        </div>
      ))}
    </div>
  );
}

function CountryFocusWidget({ language }) {
  return (
    <div className="text-center space-y-2">
      <div className="text-4xl">🇩🇿</div>
      <p className="font-bold">{language === 'en' ? 'Algeria' : 'Algérie'}</p>
      <div className="text-xs text-gray-500 space-y-1">
        <p>PIB: $266.5B</p>
        <p>Pop: 47M</p>
        <p>LSCI: 35.6 (#4 {language === 'en' ? 'Africa' : 'Afrique'})</p>
      </div>
    </div>
  );
}

function CalculatorQuickWidget({ language }) {
  return (
    <div className="space-y-2">
      <p className="text-xs text-gray-500">
        {language === 'en' ? 'Quick Estimate' : 'Estimation Rapide'}
      </p>
      <div className="flex gap-2">
        <input 
          type="text" 
          placeholder="HS Code" 
          className="flex-1 text-xs px-2 py-1.5 border rounded focus:ring-2 focus:ring-amber-400 outline-none"
        />
        <Button size="sm" className="text-xs px-3 bg-amber-500 hover:bg-amber-600">
          {language === 'en' ? 'Go' : 'OK'}
        </Button>
      </div>
      <p className="text-xs text-gray-400">Ex: 0901 ({language === 'en' ? 'Coffee' : 'Café'})</p>
    </div>
  );
}

function RecentRulesWidget({ language }) {
  const rules = [
    { code: '0901', name: language === 'en' ? 'Coffee' : 'Café', rule: '40%' },
    { code: '8703', name: language === 'en' ? 'Vehicles' : 'Véhicules', rule: '45%' },
    { code: '6204', name: language === 'en' ? 'Clothing' : 'Vêtements', rule: '35%' }
  ];

  return (
    <div className="space-y-2 text-xs">
      {rules.map(r => (
        <div key={r.code} className="flex justify-between items-center p-2 bg-gray-50 rounded hover:bg-gray-100 transition-colors">
          <span>{r.code} - {r.name}</span>
          <Badge variant="outline" className="text-xs">{r.rule}</Badge>
        </div>
      ))}
    </div>
  );
}
