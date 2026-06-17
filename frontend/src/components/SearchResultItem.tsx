import React from 'react';
import { SearchResult } from '../types';
import { sanitizeUrl } from '../utils/formatting';

interface SearchResultItemProps {
  result: SearchResult;
  onResultClick?: (pageId: number) => void;
}

const SearchResultItem: React.FC<SearchResultItemProps> = ({ result, onResultClick }) => {
  return (
    <div className="mb-6 pb-6 border-b border-gray-200 last:border-b-0">
      <a
        href={result.url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 hover:text-blue-800 hover:underline text-sm"
      >
        {sanitizeUrl(result.url)}
      </a>
      <h3 className="text-xl font-bold text-blue-600 hover:text-blue-800 cursor-pointer mt-1">
        <a href={result.url} target="_blank" rel="noopener noreferrer">
          {result.title || 'Untitled'}
        </a>
      </h3>
      <p className="text-gray-600 text-sm mt-2 leading-relaxed">{result.snippet}</p>
      <div className="text-xs text-gray-500 mt-2">Relevance: {(result.score * 100).toFixed(1)}%</div>
    </div>
  );
};

export default SearchResultItem;
