import apiClient from './client';

export interface StockData {
  symbol: string;
  price: number;
  change: number;
  change_percent: number;
  volume: number;
  market_cap?: number;
}

export interface StockHistory {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

/**
 * Fetch stock information by symbol
 */
export const getStockData = async (symbol: string): Promise<StockData> => {
  const response = await apiClient.get(`/stocks/${symbol}`);
  return response.data;
};

/**
 * Fetch historical stock data
 */
export const getStockHistory = async (symbol: string, period = '1y'): Promise<StockHistory[]> => {
  const response = await apiClient.get(`/stocks/${symbol}/history`, {
    params: { period }
  });
  return response.data;
};

/**
 * Search stocks by query
 */
export const searchStocks = async (query: string): Promise<StockData[]> => {
  const response = await apiClient.get('/stocks/search', {
    params: { q: query }
  });
  return response.data;
};