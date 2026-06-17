import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import SearchBox from '../components/SearchBox';
import SearchResultItem from '../components/SearchResultItem';
import Pagination from '../components/Pagination';
import { SearchResponse } from '../types';
import apiService from '../services/api';

const RESULTS_PER_PAGE = 10;

const SearchResultsPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get('q') || '';
  const page = parseInt(searchParams.get('page') || '1');

  const [results, setResults] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (query.trim()) {
      const fetchResults = async () => {
        try {
          setLoading(true);
          setError(null);
          const offset = (page - 1) * RESULTS_PER_PAGE;
          const data = await apiService.search(query, RESULTS_PER_PAGE, offset);
          setResults(data);
        } catch (err) {
          setError(err instanceof Error ? err.message : 'Search failed');
          setResults(null);
        } finally {
          setLoading(false);
        }
      };

      fetchResults();
    }
  }, [query, page]);

  const handleSearch = (newQuery: string) => {
    setSearchParams({ q: newQuery, page: '1' });
  };

  const handlePageChange = (newPage: number) => {
    setSearchParams({ q: query, page: newPage.toString() });
    window.scrollTo(0, 0);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b border-gray-200 py-4">
        <div className="max-w-4xl mx-auto px-4">
          <SearchBox initialQuery={query} onSearch={handleSearch} />
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center text-gray-500 py-8">
            <p className="text-lg">Searching...</p>
          </div>
        ) : results && results.results.length > 0 ? (
          <>
            <div className="text-gray-600 mb-6">
              About {results.total} results ({((results.offset + results.results.length) / results.total * 100).toFixed(1)}% shown)
            </div>
            <div>
              {results.results.map((result) => (
                <SearchResultItem key={result.page_id} result={result} />
              ))}
            </div>
            {results.total > RESULTS_PER_PAGE && (
              <Pagination
                currentPage={page}
                totalResults={results.total}
                resultsPerPage={RESULTS_PER_PAGE}
                onPageChange={handlePageChange}
              />
            )}
          </>
        ) : query && !loading ? (
          <div className="text-center text-gray-600 py-8">
            <p className="text-lg">No results found for "{query}"</p>
            <p className="text-sm mt-2">Try different keywords or check back later</p>
          </div>
        ) : null}
      </div>
    </div>
  );
};

export default SearchResultsPage;
