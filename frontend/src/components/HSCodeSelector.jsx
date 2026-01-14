import React, { useState, useEffect, useCallback, useRef } from 'react';
import { createPortal } from 'react-dom';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Search, X, Package, ChevronDown, ChevronRight, Loader2 } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const texts = {
  fr: {
    title: "Codes SH6 - Système Harmonisé",
    searchPlaceholder: "Rechercher un produit ou code HS...",
    chapters: "Chapitres",
    allChapters: "Tous les chapitres",
    results: "résultats",
    noResults: "Aucun résultat pour",
    loading: "Chargement...",
    selectCode: "Sélectionner",
    selectedCode: "Code sélectionné",
    clearSelection: "Effacer",
    browseByChapter: "Parcourir par chapitre",
    topChapters: "Chapitres principaux",
    recentSearches: "Recherches récentes"
  },
  en: {
    title: "HS6 Codes - Harmonized System",
    searchPlaceholder: "Search product or HS code...",
    chapters: "Chapters",
    allChapters: "All chapters",
    results: "results",
    noResults: "No results for",
    loading: "Loading...",
    selectCode: "Select",
    selectedCode: "Selected code",
    clearSelection: "Clear",
    browseByChapter: "Browse by chapter",
    topChapters: "Main chapters",
    recentSearches: "Recent searches"
  }
};

// Composant de recherche rapide (inline)
export function HSCodeSearch({ value, onChange, language = 'fr', placeholder }) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dropdownPosition, setDropdownPosition] = useState({ top: 0, left: 0, width: 0 });
  const inputRef = useRef(null);
  const dropdownRef = useRef(null);
  
  const t = texts[language] || texts.fr;

  const searchCodes = useCallback(async (query) => {
    if (query.length < 2) {
      setResults([]);
      return;
    }
    
    setLoading(true);
    try {
      const response = await axios.get(`${API}/hs-codes/search`, {
        params: { q: query, language, limit: 15 }
      });
      setResults(response.data.results || []);
    } catch (error) {
      console.error('Error searching HS codes:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, [language]);

  useEffect(() => {
    const debounce = setTimeout(() => {
      if (searchTerm) {
        searchCodes(searchTerm);
      }
    }, 300);
    return () => clearTimeout(debounce);
  }, [searchTerm, searchCodes]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      const rect = inputRef.current.getBoundingClientRect();
      setDropdownPosition({
        top: rect.bottom + window.scrollY + 4,
        left: rect.left + window.scrollX,
        width: rect.width
      });
    }
  }, [isOpen]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target) &&
          inputRef.current && !inputRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (code) => {
    onChange(code);
    setIsOpen(false);
    setSearchTerm('');
  };

  const selectedCode = value ? results.find(r => r.code === value) : null;

  return (
    <div className="relative">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
        <Input
          ref={inputRef}
          type="text"
          placeholder={placeholder || t.searchPlaceholder}
          value={searchTerm || (value ? `${value} - ${selectedCode?.label || ''}` : '')}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          className="pl-10 pr-10"
          data-testid="hs-code-search-input"
        />
        {value && (
          <button
            onClick={() => {
              onChange('');
              setSearchTerm('');
            }}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {isOpen && (searchTerm.length >= 2 || results.length > 0) && createPortal(
        <div
          ref={dropdownRef}
          className="bg-white rounded-lg shadow-xl border border-gray-200 max-h-80 overflow-y-auto"
          style={{
            position: 'absolute',
            top: dropdownPosition.top,
            left: dropdownPosition.left,
            width: dropdownPosition.width,
            zIndex: 99999
          }}
        >
          {loading ? (
            <div className="p-4 text-center text-gray-500">
              <Loader2 className="w-5 h-5 animate-spin mx-auto mb-2" />
              <span className="text-sm">{t.loading}</span>
            </div>
          ) : results.length > 0 ? (
            <div className="py-1">
              <div className="px-3 py-2 text-xs text-gray-500 border-b">
                {results.length} {t.results}
              </div>
              {results.map((item) => (
                <button
                  key={item.code}
                  onClick={() => handleSelect(item.code)}
                  className={`w-full px-3 py-2 text-left hover:bg-green-50 transition-colors flex items-start gap-3 ${
                    value === item.code ? 'bg-green-100' : ''
                  }`}
                >
                  <Badge variant="outline" className="font-mono text-xs shrink-0 bg-blue-50 text-blue-700">
                    {item.code}
                  </Badge>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-800 truncate">{item.label}</p>
                    <p className="text-xs text-gray-500">Ch. {item.chapter} - {item.chapter_name}</p>
                  </div>
                </button>
              ))}
            </div>
          ) : searchTerm.length >= 2 ? (
            <div className="p-4 text-center text-gray-500">
              <Package className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p className="text-sm">{t.noResults} "{searchTerm}"</p>
            </div>
          ) : null}
        </div>,
        document.body
      )}
    </div>
  );
}

// Composant de navigation par chapitres (panel complet)
export function HSCodeBrowser({ onSelect, language = 'fr' }) {
  const [chapters, setChapters] = useState([]);
  const [selectedChapter, setSelectedChapter] = useState(null);
  const [chapterCodes, setChapterCodes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  
  const t = texts[language] || texts.fr;

  useEffect(() => {
    fetchChapters();
    fetchStats();
  }, []);

  const fetchChapters = async () => {
    try {
      const response = await axios.get(`${API}/hs-codes/chapters`);
      setChapters(Object.entries(response.data.chapters || {}).map(([code, labels]) => ({
        code,
        label_fr: labels.fr,
        label_en: labels.en,
        label: language === 'en' ? labels.en : labels.fr
      })));
    } catch (error) {
      console.error('Error fetching chapters:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API}/hs-codes/statistics`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const fetchChapterCodes = async (chapter) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/hs-codes/chapter/${chapter}`, {
        params: { language }
      });
      setChapterCodes(response.data.codes || []);
    } catch (error) {
      console.error('Error fetching chapter codes:', error);
      setChapterCodes([]);
    } finally {
      setLoading(false);
    }
  };

  const handleChapterClick = (chapter) => {
    if (selectedChapter === chapter) {
      setSelectedChapter(null);
      setChapterCodes([]);
    } else {
      setSelectedChapter(chapter);
      fetchChapterCodes(chapter);
    }
  };

  const searchCodes = async (query) => {
    if (query.length < 2) {
      setSearchResults([]);
      return;
    }
    try {
      const response = await axios.get(`${API}/hs-codes/search`, {
        params: { q: query, language, limit: 20 }
      });
      setSearchResults(response.data.results || []);
    } catch (error) {
      console.error('Error searching:', error);
    }
  };

  useEffect(() => {
    const debounce = setTimeout(() => {
      if (searchTerm) {
        searchCodes(searchTerm);
      } else {
        setSearchResults([]);
      }
    }, 300);
    return () => clearTimeout(debounce);
  }, [searchTerm, language]);

  return (
    <Card className="shadow-lg">
      <CardHeader className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white rounded-t-lg">
        <CardTitle className="flex items-center gap-2">
          <Package className="w-5 h-5" />
          {t.title}
        </CardTitle>
        {stats && (
          <p className="text-blue-100 text-sm">
            {stats.total_chapters} {t.chapters} • {stats.total_codes} codes SH6
          </p>
        )}
      </CardHeader>
      <CardContent className="p-4">
        {/* Search */}
        <div className="mb-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <Input
              type="text"
              placeholder={t.searchPlaceholder}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
              data-testid="hs-browser-search"
            />
          </div>
        </div>

        {/* Search Results */}
        {searchResults.length > 0 && (
          <div className="mb-4 border rounded-lg max-h-60 overflow-y-auto">
            <div className="px-3 py-2 text-xs text-gray-500 bg-gray-50 border-b sticky top-0">
              {searchResults.length} {t.results}
            </div>
            {searchResults.map((item) => (
              <button
                key={item.code}
                onClick={() => onSelect && onSelect(item)}
                className="w-full px-3 py-2 text-left hover:bg-green-50 transition-colors flex items-start gap-3 border-b last:border-0"
              >
                <Badge variant="outline" className="font-mono text-xs shrink-0 bg-blue-50 text-blue-700">
                  {item.code}
                </Badge>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-800">{item.label}</p>
                  <p className="text-xs text-gray-500">Ch. {item.chapter}</p>
                </div>
              </button>
            ))}
          </div>
        )}

        {/* Top Chapters */}
        {stats && !searchTerm && (
          <div className="mb-4">
            <h4 className="text-sm font-semibold text-gray-700 mb-2">{t.topChapters}</h4>
            <div className="flex flex-wrap gap-2">
              {stats.top_chapters?.slice(0, 6).map((ch) => (
                <Badge
                  key={ch.chapter}
                  variant="outline"
                  className="cursor-pointer hover:bg-blue-50"
                  onClick={() => handleChapterClick(ch.chapter)}
                >
                  {ch.chapter} - {ch.chapter_name_fr?.slice(0, 20)}...
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Chapters List */}
        {!searchTerm && (
          <div>
            <h4 className="text-sm font-semibold text-gray-700 mb-2">{t.browseByChapter}</h4>
            <div className="border rounded-lg max-h-80 overflow-y-auto">
              {chapters.map((chapter) => (
                <div key={chapter.code} className="border-b last:border-0">
                  <button
                    onClick={() => handleChapterClick(chapter.code)}
                    className={`w-full px-3 py-2 text-left hover:bg-gray-50 transition-colors flex items-center gap-2 ${
                      selectedChapter === chapter.code ? 'bg-blue-50' : ''
                    }`}
                  >
                    {selectedChapter === chapter.code ? (
                      <ChevronDown className="w-4 h-4 text-blue-600" />
                    ) : (
                      <ChevronRight className="w-4 h-4 text-gray-400" />
                    )}
                    <Badge variant="outline" className="font-mono text-xs bg-gray-100">
                      {chapter.code}
                    </Badge>
                    <span className="text-sm text-gray-700 flex-1 truncate">
                      {language === 'en' ? chapter.label_en : chapter.label_fr}
                    </span>
                  </button>
                  
                  {/* Chapter codes */}
                  {selectedChapter === chapter.code && (
                    <div className="bg-gray-50 border-t">
                      {loading ? (
                        <div className="p-4 text-center">
                          <Loader2 className="w-5 h-5 animate-spin mx-auto" />
                        </div>
                      ) : (
                        <div className="max-h-60 overflow-y-auto">
                          {chapterCodes.map((code) => (
                            <button
                              key={code.code}
                              onClick={() => onSelect && onSelect(code)}
                              className="w-full px-4 py-2 text-left hover:bg-green-100 transition-colors flex items-start gap-2 border-b border-gray-100 last:border-0"
                            >
                              <Badge className="font-mono text-xs bg-green-600 text-white shrink-0">
                                {code.code}
                              </Badge>
                              <span className="text-sm text-gray-700">{code.label}</span>
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default HSCodeSearch;
