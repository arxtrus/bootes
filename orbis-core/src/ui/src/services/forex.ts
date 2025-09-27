import apiClient from './client';

export interface ForexRate {
  from_currency: string;
  to_currency: string;
  rate: number;
  timestamp: string;
  change: number;
  change_percent: number;
}

export interface ForexHistory {
  date: string;
  rate: number;
}

/**
 * Get current exchange rate between two currencies
 */
export const getForexRate = async (from: string, to: string): Promise<ForexRate> => {
  const response = await apiClient.get(`/forex/${from}/${to}`);
  return response.data;
};

/**
 * Get major currency pairs rates
 */
export const getMajorPairs = async (): Promise<ForexRate[]> => {
  const response = await apiClient.get('/forex/major-pairs');
  return response.data;
};

/**
 * Get historical forex data
 */
export const getForexHistory = async (
  from: string, 
  to: string, 
  period = '1m'
): Promise<ForexHistory[]> => {
  const response = await apiClient.get(`/forex/${from}/${to}/history`, {
    params: { period }
  });
  return response.data;
};