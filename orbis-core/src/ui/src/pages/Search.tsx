import { useState } from 'react';
import { useStockData } from '../hooks/useApi';

/**
 * Search page for looking up stock symbols and displaying data
 */
export default function Search() {
  const [symbol, setSymbol] = useState('');
  const [searchSymbol, setSearchSymbol] = useState('');
  
  // Only fetch data when searchSymbol is set (after search is triggered)
  const { data: stockData, isLoading, error, isError } = useStockData(searchSymbol);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (symbol.trim()) {
      setSearchSymbol(symbol.trim().toUpperCase());
    }
  };

  const handleClear = () => {
    setSymbol('');
    setSearchSymbol('');
  };

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US', { 
      minimumFractionDigits: 2, 
      maximumFractionDigits: 2 
    }).format(num);
  };

  const formatCurrency = (num: number) => {
    return new Intl.NumberFormat('en-US', { 
      style: 'currency', 
      currency: 'USD' 
    }).format(num);
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Search</h1>
        <p className="text-gray-600">Look up stock symbols and view detailed information</p>
      </div>

      {/* Search Form */}
      <div className="bg-white p-6 rounded-lg border shadow-sm">
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1">
            <label htmlFor="symbol" className="block text-sm font-medium text-gray-700 mb-2">
              Stock Symbol
            </label>
            <input
              type="text"
              id="symbol"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              placeholder="Enter symbol (e.g., AAPL, GOOGL, TSLA)"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div className="flex items-end gap-2">
            <button
              type="submit"
              disabled={!symbol.trim() || isLoading}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Searching...' : 'Search'}
            </button>
            <button
              type="button"
              onClick={handleClear}
              className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
              Clear
            </button>
          </div>
        </form>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="bg-white p-6 rounded-lg border">
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-gray-600">Loading stock data...</span>
          </div>
        </div>
      )}

      {/* Error State */}
      {isError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <span className="text-red-400 text-xl">⚠️</span>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error fetching data</h3>
              <p className="text-sm text-red-700 mt-1">
                {error instanceof Error ? error.message : 'Unable to fetch stock data. Please try again.'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {stockData && !isLoading && (
        <div className="bg-white rounded-lg border shadow-sm">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">
              {stockData.symbol} Stock Information
            </h2>
          </div>
          
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Price Information */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900">Price Information</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Current Price:</span>
                    <span className="font-semibold text-lg">
                      {formatCurrency(stockData.price)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Change:</span>
                    <span className={`font-semibold ${
                      stockData.change >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {stockData.change >= 0 ? '+' : ''}{formatCurrency(stockData.change)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Change %:</span>
                    <span className={`font-semibold ${
                      stockData.change_percent >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {stockData.change_percent >= 0 ? '+' : ''}{formatNumber(stockData.change_percent)}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Volume Information */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900">Trading Information</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Volume:</span>
                    <span className="font-semibold">
                      {new Intl.NumberFormat('en-US').format(stockData.volume)}
                    </span>
                  </div>
                  {stockData.market_cap && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Market Cap:</span>
                      <span className="font-semibold">
                        {formatCurrency(stockData.market_cap)}
                      </span>
                    </div>
                  )}
                </div>
              </div>

              {/* Status Indicator */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900">Status</h3>
                <div className="p-4 rounded-lg border">
                  <div className="flex items-center">
                    <div className={`w-3 h-3 rounded-full mr-3 ${
                      stockData.change >= 0 ? 'bg-green-500' : 'bg-red-500'
                    }`}></div>
                    <span className="text-sm font-medium">
                      {stockData.change >= 0 ? 'Up' : 'Down'} for the day
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* No Results Message */}
      {searchSymbol && !stockData && !isLoading && !isError && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
          <div className="text-center">
            <span className="text-gray-400 text-4xl">📊</span>
            <h3 className="text-lg font-medium text-gray-900 mt-2">No data found</h3>
            <p className="text-gray-600 mt-1">
              No data available for symbol "{searchSymbol}". Please try a different symbol.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}