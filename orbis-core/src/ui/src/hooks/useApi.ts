import { useQuery } from '@tanstack/react-query';
import { getStockData, getStockHistory } from '../services/stocks';
import { getCryptoData, getTopCryptos } from '../services/crypto';
import { getForexRate, getMajorPairs } from '../services/forex';
import { getCPIData, getGDPData, getEconomicOverview } from '../services/economics';

/**
 * Hook for fetching stock data
 */
export const useStockData = (symbol: string) => {
  return useQuery({
    queryKey: ['stock', symbol],
    queryFn: () => getStockData(symbol),
    enabled: !!symbol,
    staleTime: 30000, // 30 seconds
  });
};

/**
 * Hook for fetching stock history
 */
export const useStockHistory = (symbol: string, period = '1y') => {
  return useQuery({
    queryKey: ['stockHistory', symbol, period],
    queryFn: () => getStockHistory(symbol, period),
    enabled: !!symbol,
    staleTime: 300000, // 5 minutes
  });
};

/**
 * Hook for fetching crypto data
 */
export const useCryptoData = (symbol: string) => {
  return useQuery({
    queryKey: ['crypto', symbol],
    queryFn: () => getCryptoData(symbol),
    enabled: !!symbol,
    staleTime: 30000,
  });
};

/**
 * Hook for fetching top cryptocurrencies
 */
export const useTopCryptos = (limit = 10) => {
  return useQuery({
    queryKey: ['topCryptos', limit],
    queryFn: () => getTopCryptos(limit),
    staleTime: 60000, // 1 minute
  });
};

/**
 * Hook for fetching forex rates
 */
export const useForexRate = (from: string, to: string) => {
  return useQuery({
    queryKey: ['forex', from, to],
    queryFn: () => getForexRate(from, to),
    enabled: !!from && !!to,
    staleTime: 30000,
  });
};

/**
 * Hook for fetching major currency pairs
 */
export const useMajorPairs = () => {
  return useQuery({
    queryKey: ['majorPairs'],
    queryFn: getMajorPairs,
    staleTime: 60000,
  });
};

/**
 * Hook for fetching CPI data
 */
export const useCPIData = (country = 'US') => {
  return useQuery({
    queryKey: ['cpi', country],
    queryFn: () => getCPIData(country),
    staleTime: 3600000, // 1 hour
  });
};

/**
 * Hook for fetching GDP data
 */
export const useGDPData = (country = 'US') => {
  return useQuery({
    queryKey: ['gdp', country],
    queryFn: () => getGDPData(country),
    staleTime: 3600000,
  });
};

/**
 * Hook for fetching economic overview
 */
export const useEconomicOverview = (country = 'US') => {
  return useQuery({
    queryKey: ['economicOverview', country],
    queryFn: () => getEconomicOverview(country),
    staleTime: 3600000,
  });
};