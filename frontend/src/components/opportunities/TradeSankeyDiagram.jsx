/**
 * Trade Sankey Diagram Component
 * Visualizes trade flows between countries and products
 * 
 * Shows: Source Countries → Products → Destination Countries
 * Interactive: Click nodes to filter flows
 */
import React, { useMemo, useState, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { ResponsiveContainer, Sankey, Tooltip } from 'recharts';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { X } from 'lucide-react';

// Color palettes for different node types
const SOURCE_COLORS = ['#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe'];
const MIDDLE_COLORS = ['#10b981', '#34d399', '#6ee7b7', '#a7f3d0'];
const SINK_COLORS = ['#f97316', '#fb923c', '#fdba74', '#fed7aa'];

// Generate consistent color from string
const colorHash = (str) => {
  let hash = 0;
  if (!str) return 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  return hash;
};

const getColor = (type, name) => {
  const index = Math.abs(colorHash(name));
  switch (type) {
    case 'source': return SOURCE_COLORS[index % SOURCE_COLORS.length];
    case 'middle': return MIDDLE_COLORS[index % MIDDLE_COLORS.length];
    case 'sink': return SINK_COLORS[index % SINK_COLORS.length];
    default: return '#8884d8';
  }
};

// Format currency
const formatValue = (value) => {
  if (!value || isNaN(value)) return '$0';
  if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
  if (value >= 1e6) return `$${(value / 1e6).toFixed(1)}M`;
  if (value >= 1e3) return `$${(value / 1e3).toFixed(0)}K`;
  return `$${value.toLocaleString()}`;
};

// Custom Tooltip
const CustomSankeyTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const { source, target, value, payload: linkPayload } = payload[0];
    if (!source?.payload || !target?.payload) return null;

    return (
      <div className="bg-white/95 p-3 border border-slate-200 rounded-lg shadow-xl text-xs">
        <div className="flex justify-between items-center mb-1 gap-4">
          <span className="font-bold text-slate-900">{source.payload.name}</span>
          <span className="text-slate-400">→</span>
          <span className="font-bold text-slate-900">{target.payload.name}</span>
        </div>
        <p className="font-semibold text-emerald-600">
          Valeur: {formatValue(value)}
        </p>
      </div>
    );
  }
  return null;
};

// Custom Node Component
const CustomSankeyNode = (props) => {
  const { x, y, width, height, payload, containerWidth, onNodeClick } = props;
  if (!payload || !payload.name) return null;
  if (height < 1) return null;

  const isSource = x < containerWidth / 3;
  const isSink = x > containerWidth * 2 / 3;
  const isDimmed = payload.isDimmed;
  const isActive = payload.isActive;
  const color = payload.color || '#8884d8';

  const handleClick = () => {
    const filterType = isSource ? 'source' : isSink ? 'destination' : 'product';
    onNodeClick(filterType, payload.name);
  };

  return (
    <g
      onClick={handleClick}
      className="cursor-pointer transition-all hover:opacity-100 opacity-90"
    >
      <rect
        x={x} y={y} width={width} height={height}
        fill={color}
        fillOpacity={isDimmed ? 0.15 : 1}
        stroke={isActive ? '#000' : 'none'}
        strokeWidth={isActive ? 2 : 0}
        rx={2}
      />
      {height > 10 && (
        <text
          x={isSource ? x - 6 : isSink ? x + width + 6 : x + width / 2}
          y={y + height / 2}
          dy="0.35em"
          textAnchor={isSource ? 'end' : isSink ? 'start' : 'middle'}
          fontSize="10"
          fontWeight={isActive ? "900" : "600"}
          fill={isDimmed ? '#9ca3af' : '#374151'}
          style={{ pointerEvents: 'none' }}
        >
          {payload.name.length > 20 ? payload.name.substring(0, 17) + '...' : payload.name}
        </text>
      )}
    </g>
  );
};

// Filter Badge Component
const FilterBadge = ({ label, value, color, onClear }) => {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-700 border-blue-200',
    emerald: 'bg-emerald-100 text-emerald-700 border-emerald-200',
    orange: 'bg-orange-100 text-orange-700 border-orange-200'
  };

  return (
    <span className={`inline-flex items-center px-2 py-1 rounded text-[10px] font-bold uppercase border ${colorClasses[color]}`}>
      {value.length > 20 ? value.substring(0, 17) + '...' : value}
      <button onClick={onClear} className="ml-2 hover:opacity-70">
        <X className="h-3 w-3" />
      </button>
    </span>
  );
};

// Main Component
export default function TradeSankeyDiagram({ 
  opportunities = [],
  mode = 'substitution', // 'substitution' | 'export' | 'product'
  language = 'fr'
}) {
  const { t } = useTranslation();
  const [activeFilters, setActiveFilters] = useState({
    source: '',
    product: '',
    destination: ''
  });

  const hasAnyFilter = activeFilters.source || activeFilters.product || activeFilters.destination;

  // Handle node click for filtering
  const handleNodeClick = useCallback((filterType, value) => {
    setActiveFilters(prev => ({
      ...prev,
      [filterType]: prev[filterType] === value ? '' : value
    }));
  }, []);

  // Clear all filters
  const clearAllFilters = useCallback(() => {
    setActiveFilters({ source: '', product: '', destination: '' });
  }, []);

  // Build Sankey data from opportunities
  const data = useMemo(() => {
    const nodes = [];
    const links = [];
    const nodeMap = new Map();

    const getNodeIndex = (name, type) => {
      const key = `${name}-${type}`;
      const isActive = (type === 'source' && activeFilters.source === name) ||
                       (type === 'middle' && activeFilters.product === name) ||
                       (type === 'sink' && activeFilters.destination === name);

      if (!nodeMap.has(key)) {
        nodeMap.set(key, nodes.length);
        nodes.push({ 
          name, 
          type, 
          color: getColor(type, name), 
          isActive,
          isDimmed: hasAnyFilter && !isActive
        });
      }
      return nodeMap.get(key);
    };

    // Process opportunities
    opportunities.forEach(opp => {
      const imported = opp.imported_product || opp.exportable_product || {};
      const suppliers = opp.african_suppliers || opp.target_markets || [];
      
      const productName = imported.name || imported.hs_code || 'Unknown';
      const importerName = mode === 'substitution' 
        ? (opp.importer_name || 'Importer')
        : (opp.exporter_name || 'Exporter');
      
      // Apply filters
      if (activeFilters.product && activeFilters.product !== productName) return;
      if (activeFilters.destination && activeFilters.destination !== importerName) return;

      suppliers.forEach(supplier => {
        const supplierName = supplier.country_name || supplier.country_iso3;
        
        if (activeFilters.source && activeFilters.source !== supplierName) return;

        const value = supplier.export_value || supplier.capture_potential || 
                      supplier.production_capacity || opp.substitution_potential || 1000000;

        if (value <= 0) return;

        const srcIdx = getNodeIndex(supplierName, 'source');
        const midIdx = getNodeIndex(productName, 'middle');
        const snkIdx = getNodeIndex(importerName, 'sink');

        // Create links: Source → Product → Destination
        links.push({ source: srcIdx, target: midIdx, value: value / 2 });
        links.push({ source: midIdx, target: snkIdx, value: value / 2 });
      });
    });

    return { nodes, links };
  }, [opportunities, activeFilters, hasAnyFilter, mode]);

  const texts = {
    fr: {
      noData: "Aucune donnée à afficher",
      tip: "Astuce: Cliquez sur un nœud pour filtrer les flux",
      clearAll: "Réinitialiser",
      source: "Source",
      product: "Produit",
      destination: "Destination"
    },
    en: {
      noData: "No data to display",
      tip: "Tip: Click a node to filter flows",
      clearAll: "Reset",
      source: "Source",
      product: "Product",
      destination: "Destination"
    }
  };

  const txt = texts[language] || texts.fr;

  // Empty state
  if (data.nodes.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-64 bg-slate-50 rounded-xl border border-dashed border-slate-300">
        <p className="text-slate-500 italic mb-4">{txt.noData}</p>
        {hasAnyFilter && (
          <Button variant="ghost" size="sm" onClick={clearAllFilters}>
            {txt.clearAll}
          </Button>
        )}
      </div>
    );
  }

  return (
    <div className="w-full" data-testid="trade-sankey-diagram">
      {/* Filters Bar */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <div className="flex flex-wrap gap-2">
          {activeFilters.source && (
            <FilterBadge 
              label={txt.source}
              value={activeFilters.source}
              color="blue"
              onClear={() => handleNodeClick('source', '')}
            />
          )}
          {activeFilters.product && (
            <FilterBadge 
              label={txt.product}
              value={activeFilters.product}
              color="emerald"
              onClear={() => handleNodeClick('product', '')}
            />
          )}
          {activeFilters.destination && (
            <FilterBadge 
              label={txt.destination}
              value={activeFilters.destination}
              color="orange"
              onClear={() => handleNodeClick('destination', '')}
            />
          )}
          {hasAnyFilter && (
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={clearAllFilters}
              className="text-[10px] font-bold uppercase text-slate-400 hover:text-slate-600"
            >
              {txt.clearAll}
            </Button>
          )}
          {!hasAnyFilter && (
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider italic">
              {txt.tip}
            </span>
          )}
        </div>
      </div>

      {/* Sankey Diagram */}
      <div className="h-[450px] bg-white rounded-xl border border-slate-200 p-4">
        <ResponsiveContainer width="100%" height="100%">
          <Sankey
            data={data}
            node={<CustomSankeyNode containerWidth={800} onNodeClick={handleNodeClick} />}
            nodePadding={30}
            nodeWidth={10}
            margin={{ top: 10, right: 120, bottom: 10, left: 120 }}
            link={{ stroke: '#cbd5e1', strokeOpacity: 0.3 }}
          >
            <Tooltip content={<CustomSankeyTooltip />} />
          </Sankey>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="flex justify-center gap-6 mt-4 text-xs">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-blue-500" />
          <span className="text-slate-600">Pays fournisseurs</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-emerald-500" />
          <span className="text-slate-600">Produits</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-orange-500" />
          <span className="text-slate-600">Pays importateurs</span>
        </div>
      </div>
    </div>
  );
}
