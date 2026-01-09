import React, { useState, useMemo, useRef, useEffect, useCallback } from 'react';
import { Input } from '../ui/input';
import { Badge } from '../ui/badge';
import { Search, ChevronDown, X, Globe, Star } from 'lucide-react';
import { getCountriesByRegion, getAllCountries, getCountryName } from '../../utils/translations';

// Grandes économies à mettre en avant
const MAJOR_ECONOMIES = ['ZAF', 'NGA', 'EGY', 'KEN', 'GHA', 'ETH', 'MAR', 'DZA', 'TZA', 'CIV'];

function EnhancedCountrySelector({ value, onChange, label, variant = "default", language = 'fr' }) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const dropdownRef = useRef(null);
  const inputRef = useRef(null);

  // Get translated countries based on language
  const AFRICAN_COUNTRIES_BY_REGION = useMemo(() => getCountriesByRegion(language), [language]);
  
  // Translated labels
  const texts = {
    fr: {
      selectCountry: "Sélectionner un pays",
      searchPlaceholder: "Rechercher un pays...",
      majorEconomies: "Grandes économies",
      noResults: "Aucun pays trouvé"
    },
    en: {
      selectCountry: "Select a country",
      searchPlaceholder: "Search for a country...",
      majorEconomies: "Major economies",
      noResults: "No country found"
    }
  };
  const t = texts[language] || texts.fr;
  const displayLabel = label || t.selectCountry;

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
        setSearchTerm('');
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Focus input when dropdown opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  }, [isOpen]);

  // Obtenir tous les pays dans une liste plate
  const allCountries = useMemo(() => {
    const countries = [];
    Object.values(AFRICAN_COUNTRIES_BY_REGION).forEach(region => {
      countries.push(...region);
    });
    return countries;
  }, []);

  // Trouver le pays sélectionné
  const selectedCountry = useMemo(() => {
    return allCountries.find(c => c.code === value);
  }, [value, allCountries]);

  // Filtrer les pays selon la recherche
  const filteredRegions = useMemo(() => {
    if (!searchTerm) return AFRICAN_COUNTRIES_BY_REGION;

    const normalizedSearch = searchTerm.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    const filtered = {};
    Object.entries(AFRICAN_COUNTRIES_BY_REGION).forEach(([region, countries]) => {
      const matchedCountries = countries.filter(country => {
        const normalizedName = country.name.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
        return normalizedName.includes(normalizedSearch) ||
               country.code.toLowerCase().includes(normalizedSearch);
      });
      if (matchedCountries.length > 0) {
        filtered[region] = matchedCountries;
      }
    });
    return filtered;
  }, [searchTerm]);

  // Grandes économies filtrées
  const majorEconomiesFiltered = useMemo(() => {
    const majors = allCountries.filter(c => MAJOR_ECONOMIES.includes(c.code));
    if (!searchTerm) return majors;
    const normalizedSearch = searchTerm.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    return majors.filter(country => {
      const normalizedName = country.name.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
      return normalizedName.includes(normalizedSearch) ||
             country.code.toLowerCase().includes(normalizedSearch);
    });
  }, [searchTerm, allCountries]);

  const handleToggle = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsOpen(prev => !prev);
  }, []);

  const handleSelect = useCallback((country) => {
    onChange(country.code);
    setIsOpen(false);
    setSearchTerm('');
  }, [onChange]);

  const handleClear = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    onChange('');
    setSearchTerm('');
  }, [onChange]);

  const handleSearchChange = useCallback((e) => {
    e.stopPropagation();
    setSearchTerm(e.target.value);
  }, []);

  const handleSearchClick = useCallback((e) => {
    e.stopPropagation();
  }, []);

  // Style variants
  const isProminent = variant === "prominent";

  return (
    <div className="relative w-full" ref={dropdownRef} style={{ zIndex: isOpen ? 9999 : 1 }}>
      {/* Label */}
      <label className="block text-sm font-bold text-gray-700 mb-2 flex items-center gap-2">
        <Globe className="w-4 h-4" />
        {displayLabel}
      </label>
      
      {/* Main selector button */}
      <button
        type="button"
        onClick={handleToggle}
        className={`
          w-full text-left cursor-pointer rounded-xl border-2 transition-all duration-200
          ${isOpen 
            ? 'border-green-500 ring-4 ring-green-100 shadow-lg' 
            : 'border-gray-200 hover:border-green-300 hover:shadow-md'
          }
          ${isProminent 
            ? 'bg-gradient-to-r from-green-50 to-emerald-50 p-4' 
            : 'bg-white p-3'
          }
        `}
      >
        <div className="flex items-center justify-between">
          {selectedCountry ? (
            <div className="flex items-center gap-3">
              <span className="text-3xl">{selectedCountry.flag}</span>
              <div>
                <p className={`font-bold ${isProminent ? 'text-lg' : 'text-base'} text-gray-800`}>
                  {selectedCountry.name}
                </p>
                <p className="text-xs text-gray-500">Code: {selectedCountry.code}</p>
              </div>
              {MAJOR_ECONOMIES.includes(selectedCountry.code) && (
                <Badge className="bg-amber-100 text-amber-700 ml-2">
                  <Star className="w-3 h-3 mr-1" /> Top 10
                </Badge>
              )}
            </div>
          ) : (
            <div className="flex items-center gap-2 text-gray-400">
              <Search className="w-5 h-5" />
              <span className={isProminent ? 'text-base' : 'text-sm'}>Rechercher un pays africain...</span>
            </div>
          )}
          <div className="flex items-center gap-2">
            {selectedCountry && (
              <span
                onClick={handleClear}
                className="p-1 hover:bg-gray-100 rounded-full transition-colors cursor-pointer"
              >
                <X className="w-4 h-4 text-gray-400" />
              </span>
            )}
            <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
          </div>
        </div>
      </button>

      {/* Dropdown - Rendered as overlay */}
      {isOpen && (
        <>
          {/* Backdrop to capture clicks */}
          <div 
            className="fixed inset-0" 
            style={{ zIndex: 99998 }}
            onClick={() => setIsOpen(false)}
          />
          <div 
            className="absolute left-0 right-0 mt-2 bg-white rounded-xl shadow-2xl border border-gray-200"
            style={{ 
              zIndex: 99999,
              position: 'absolute',
              top: '100%'
            }}
          >
            {/* Search input */}
            <div className="p-3 border-b border-gray-100 bg-gray-50" onClick={handleSearchClick}>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
                <input
                  ref={inputRef}
                  type="text"
                  placeholder={t.searchPlaceholder}
                  value={searchTerm}
                  onChange={handleSearchChange}
                  onClick={handleSearchClick}
                  className="w-full pl-10 pr-4 py-2 border border-green-200 rounded-lg focus:border-green-500 focus:ring-2 focus:ring-green-200 focus:outline-none text-sm"
                />
              </div>
              <p className="text-xs text-gray-500 mt-2 flex items-center gap-1">
                <Globe className="w-3 h-3" />
                {allCountries.length} {language === 'en' ? 'African countries available' : 'pays africains disponibles'}
                {searchTerm && ` • ${Object.values(filteredRegions).flat().length} ${language === 'en' ? 'results' : 'résultats'}`}
              </p>
            </div>

            {/* Scrollable list */}
            <div className="max-h-64 overflow-y-auto bg-white" style={{ overflowY: 'auto' }}>
            {/* Major economies section - only show when no search */}
            {!searchTerm && majorEconomiesFiltered.length > 0 && (
              <div className="p-2">
                <div className="flex items-center gap-2 px-3 py-2 text-xs font-bold text-amber-700 bg-amber-50 rounded-lg mb-2">
                  <Star className="w-4 h-4" />
                  Grandes Économies Africaines
                </div>
                <div className="grid grid-cols-2 gap-1">
                  {majorEconomiesFiltered.map(country => (
                    <button
                      key={country.code}
                      type="button"
                      onClick={() => handleSelect(country)}
                      className={`
                        flex items-center gap-2 px-3 py-2 rounded-lg text-left transition-colors
                        ${value === country.code 
                          ? 'bg-green-100 text-green-800' 
                          : 'hover:bg-gray-50'
                        }
                      `}
                    >
                      <span className="text-xl">{country.flag}</span>
                      <span className="text-sm font-medium truncate">{country.name}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Divider */}
            {!searchTerm && <div className="border-t border-gray-100 my-2" />}

            {/* Filtered Regions */}
            {Object.entries(filteredRegions).map(([region, countries]) => (
              <div key={region} className="p-2">
                <div className="flex items-center gap-2 px-3 py-1 text-xs font-semibold text-gray-600 bg-gray-50 rounded-lg mb-1">
                  {region} ({countries.length})
                </div>
                <div className="space-y-0.5">
                  {countries.map(country => (
                    <button
                      key={country.code}
                      type="button"
                      onClick={() => handleSelect(country)}
                      className={`
                        w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left transition-colors
                        ${value === country.code 
                          ? 'bg-green-100 text-green-800 font-medium' 
                          : 'hover:bg-gray-50'
                        }
                      `}
                    >
                      <span className="text-xl">{country.flag}</span>
                      <span className="flex-1 text-sm">{country.name}</span>
                      <Badge variant="outline" className="text-xs text-gray-400 font-mono">
                        {country.code}
                      </Badge>
                    </button>
                  ))}
                </div>
              </div>
            ))}

            {/* No results */}
            {Object.keys(filteredRegions).length === 0 && (
              <div className="p-8 text-center text-gray-500">
                <Search className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>Aucun pays trouvé pour "{searchTerm}"</p>
              </div>
            )}
          </div>
        </div>
        </>
      )}
    </div>
  );
}

export default EnhancedCountrySelector;
