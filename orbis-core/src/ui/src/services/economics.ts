import apiClient from './client';

export interface EconomicIndicator {
  indicator: string;
  country: string;
  value: number;
  unit: string;
  date: string;
  previous_value?: number;
  change?: number;
}

export interface EconomicTimeSeries {
  date: string;
  value: number;
}

/**
 * Get Consumer Price Index (CPI) data
 */
export const getCPIData = async (country = 'US'): Promise<EconomicTimeSeries[]> => {
  const response = await apiClient.get('/economics/cpi', {
    params: { country }
  });
  return response.data;
};

/**
 * Get GDP data
 */
export const getGDPData = async (country = 'US'): Promise<EconomicTimeSeries[]> => {
  const response = await apiClient.get('/economics/gdp', {
    params: { country }
  });
  return response.data;
};

/**
 * Get unemployment rate
 */
export const getUnemploymentData = async (country = 'US'): Promise<EconomicTimeSeries[]> => {
  const response = await apiClient.get('/economics/unemployment', {
    params: { country }
  });
  return response.data;
};

/**
 * Get economic indicators overview
 */
export const getEconomicOverview = async (country = 'US'): Promise<EconomicIndicator[]> => {
  const response = await apiClient.get('/economics/overview', {
    params: { country }
  });
  return response.data;
};