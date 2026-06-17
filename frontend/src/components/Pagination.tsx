import React from 'react';

interface PaginationProps {
  currentPage: number;
  totalResults: number;
  resultsPerPage: number;
  onPageChange: (page: number) => void;
}

const Pagination: React.FC<PaginationProps> = ({ currentPage, totalResults, resultsPerPage, onPageChange }) => {
  const totalPages = Math.ceil(totalResults / resultsPerPage);

  if (totalPages <= 1) return null;

  const pages = [];
  const maxPagesToShow = 5;
  let startPage = Math.max(1, currentPage - Math.floor(maxPagesToShow / 2));
  let endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);

  if (endPage - startPage < maxPagesToShow - 1) {
    startPage = Math.max(1, endPage - maxPagesToShow + 1);
  }

  if (startPage > 1) {
    pages.push(
      <button
        key={1}
        onClick={() => onPageChange(1)}
        className="px-2 py-1 text-blue-600 hover:underline"
      >
        1
      </button>
    );
    if (startPage > 2) {
      pages.push(<span key="ellipsis-start" className="px-2">...</span>);
    }
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(
      <button
        key={i}
        onClick={() => onPageChange(i)}
        className={`px-2 py-1 ${
          i === currentPage
            ? 'bg-blue-500 text-white rounded'
            : 'text-blue-600 hover:underline'
        }`}
      >
        {i}
      </button>
    );
  }

  if (endPage < totalPages) {
    if (endPage < totalPages - 1) {
      pages.push(<span key="ellipsis-end" className="px-2">...</span>);
    }
    pages.push(
      <button
        key={totalPages}
        onClick={() => onPageChange(totalPages)}
        className="px-2 py-1 text-blue-600 hover:underline"
      >
        {totalPages}
      </button>
    );
  }

  return (
    <div className="flex justify-center gap-1 mt-8">
      <button
        onClick={() => onPageChange(Math.max(1, currentPage - 1))}
        disabled={currentPage === 1}
        className="px-3 py-1 text-blue-600 hover:underline disabled:text-gray-400"
      >
        ← Previous
      </button>
      <div className="flex gap-1">{pages}</div>
      <button
        onClick={() => onPageChange(Math.min(totalPages, currentPage + 1))}
        disabled={currentPage === totalPages}
        className="px-3 py-1 text-blue-600 hover:underline disabled:text-gray-400"
      >
        Next →
      </button>
    </div>
  );
};

export default Pagination;
