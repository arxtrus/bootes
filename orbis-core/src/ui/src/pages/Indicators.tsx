import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { useCPIData, useGDPData, useEconomicOverview } from '../hooks/useApi';

// Dummy data for when API is not available
const dummyCPIData = [
  { date: '2023-01', value: 6.4 },
  { date: '2023-02', value: 6.0 },
  { date: '2023-03', value: 5.0 },
  { date: '2023-04', value: 4.9 },
  { date: '2023-05', value: 4.0 },
  { date: '2023-06', value: 3.0 },
  { date: '2023-07', value: 3.2 },
  { date: '2023-08', value: 3.7 },
  { date: '2023-09', value: 3.7 },
  { date: '2023-10', value: 3.2 },
  { date: '2023-11', value: 3.1 },
  { date: '2023-12', value: 3.4 },
];

const dummyGDPData = [
  { quarter: 'Q1 2023', value: 2.1 },
  { quarter: 'Q2 2023', value: 2.4 },
  { quarter: 'Q3 2023', value: 2.2 },
  { quarter: 'Q4 2023', value: 3.1 },
  { quarter: 'Q1 2024', value: 2.8 },
  { quarter: 'Q2 2024', value: 3.2 },
];

/**
 * Indicators page showing economic indicators and charts
 */
export default function Indicators() {
  // These hooks will attempt to fetch real data, but we'll fall back to dummy data
  const { data: cpiData, isLoading: cpiLoading, error: cpiError } = useCPIData();
  const { data: gdpData, isLoading: gdpLoading, error: gdpError } = useGDPData();
  const { error: overviewError } = useEconomicOverview();

  // Use dummy data if API calls fail
  const displayCPIData = cpiData || dummyCPIData;
  const displayGDPData = gdpData || dummyGDPData;

  const indicators = [
    {
      name: 'Consumer Price Index (CPI)',
      value: '3.1%',
      change: '+0.2%',
      trend: 'up',
      description: 'Year-over-year inflation rate'
    },
    {
      name: 'GDP Growth Rate',
      value: '3.2%',
      change: '+0.4%',
      trend: 'up',
      description: 'Quarterly annualized growth'
    },
    {
      name: 'Unemployment Rate',
      value: '3.8%',
      change: '-0.1%',
      trend: 'down',
      description: 'Current unemployment level'
    },
    {
      name: 'Federal Funds Rate',
      value: '5.25%',
      change: '0.0%',
      trend: 'neutral',
      description: 'Current federal funds target rate'
    }
  ];

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return '📈';
      case 'down':
        return '📉';
      default:
        return '➡️';
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'up':
        return 'text-green-600';
      case 'down':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Economic Indicators</h1>
        <p className="text-gray-600">Key economic metrics and trends</p>
      </div>

      {/* API Status Indicator */}
      {(cpiError || gdpError || overviewError) && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <span className="text-yellow-400 text-xl">ℹ️</span>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">Using Demo Data</h3>
              <p className="text-sm text-yellow-700 mt-1">
                Unable to connect to live data API. Displaying sample economic indicators.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Key Indicators Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {indicators.map((indicator, index) => (
          <div key={index} className="bg-white p-6 rounded-lg border shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-600">{indicator.name}</h3>
              <span className="text-lg">{getTrendIcon(indicator.trend)}</span>
            </div>
            <div className="space-y-2">
              <p className="text-2xl font-bold text-gray-900">{indicator.value}</p>
              <p className={`text-sm font-medium ${getTrendColor(indicator.trend)}`}>
                {indicator.change} from previous period
              </p>
              <p className="text-xs text-gray-500">{indicator.description}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* CPI Chart */}
        <div className="bg-white p-6 rounded-lg border shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Consumer Price Index (CPI)</h2>
            {cpiLoading && (
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            )}
          </div>
          <p className="text-sm text-gray-600 mb-4">Monthly year-over-year inflation rate</p>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={displayCPIData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip 
                formatter={(value: number) => [`${value}%`, 'CPI YoY']}
                labelFormatter={(label) => `Date: ${label}`}
              />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#dc2626" 
                strokeWidth={2}
                dot={{ fill: '#dc2626', strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* GDP Chart */}
        <div className="bg-white p-6 rounded-lg border shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">GDP Growth Rate</h2>
            {gdpLoading && (
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            )}
          </div>
          <p className="text-sm text-gray-600 mb-4">Quarterly annualized growth rate</p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={displayGDPData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="quarter" />
              <YAxis />
              <Tooltip 
                formatter={(value: number) => [`${value}%`, 'GDP Growth']}
                labelFormatter={(label) => `Quarter: ${label}`}
              />
              <Bar 
                dataKey="value" 
                fill="#059669" 
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Data Sources */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <h3 className="text-sm font-medium text-gray-900 mb-2">Data Sources</h3>
        <p className="text-sm text-gray-600">
          Economic indicators are sourced from the Bureau of Labor Statistics (BLS), 
          Bureau of Economic Analysis (BEA), and Federal Reserve Economic Data (FRED). 
          Data is updated monthly or quarterly depending on the indicator.
        </p>
      </div>

      {/* Additional Information */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <span className="text-blue-400 text-xl">💡</span>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-blue-800">Understanding Economic Indicators</h3>
            <div className="text-sm text-blue-700 mt-2 space-y-1">
              <p><strong>CPI:</strong> Measures inflation by tracking changes in prices of goods and services</p>
              <p><strong>GDP Growth:</strong> Indicates the health and size of the economy</p>
              <p><strong>Unemployment:</strong> Shows the percentage of labor force that is unemployed</p>
              <p><strong>Fed Funds Rate:</strong> The interest rate at which banks lend to each other overnight</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}