import apiClient from './client';

export interface CryptoData {
  symbol: string;
  name: string;
  price: number;
  change_24h: number;
  change_percent_24h: number;
  market_cap: number;
  volume_24h: number;
  circulating_supply?: number;
}

export interface CryptoHistory {
  timestamp: string;
  price: number;
  volume: number;
}

/**
 * Get cryptocurrency data by symbol
 */
export const getCryptoData = async (symbol: string): Promise<CryptoData> => {
  const response = await apiClient.get(`/crypto/${symbol}`);
  return response.data;
};

/**
 * Get top cryptocurrencies by market cap
 */
export const getTopCryptos = async (limit = 10): Promise<CryptoData[]> => {
  const response = await apiClient.get('/crypto/top', {
    params: { limit }
  });
  return response.data;
};

/**
 * Get historical cryptocurrency data
 */
export const getCryptoHistory = async (
  symbol: string, 
  period = '7d'
): Promise<CryptoHistory[]> => {
  const response = await apiClient.get(`/crypto/${symbol}/history`, {
    params: { period }
  });
  return response.data;
};