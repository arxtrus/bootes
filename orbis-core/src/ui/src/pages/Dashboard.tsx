import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// Dummy data for charts
const stockData = [
  { date: '2024-01', price: 150 },
  { date: '2024-02', price: 162 },
  { date: '2024-03', price: 148 },
  { date: '2024-04', price: 175 },
  { date: '2024-05', price: 188 },
  { date: '2024-06', price: 192 },
];

const gdpData = [
  { quarter: 'Q1 2023', growth: 2.1 },
  { quarter: 'Q2 2023', growth: 2.4 },
  { quarter: 'Q3 2023', growth: 2.2 },
  { quarter: 'Q4 2023', growth: 3.1 },
  { quarter: 'Q1 2024', growth: 2.8 },
  { quarter: 'Q2 2024', growth: 3.2 },
];

/**
 * Dashboard page with tabbed navigation for different asset classes
 */
export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('stocks');

  const tabs = [
    { id: 'stocks', name: 'Stocks', icon: '📈' },
    { id: 'forex', name: 'Forex', icon: '💱' },
    { id: 'crypto', name: 'Crypto', icon: '₿' },
    { id: 'economics', name: 'Economics', icon: '🏛️' },
  ];

  const renderStocksTab = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">S&P 500</h3>
          <p className="text-2xl font-bold text-green-600">4,327.54</p>
          <p className="text-sm text-green-600">+1.2% (+52.14)</p>
        </div>
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">NASDAQ</h3>
          <p className="text-2xl font-bold text-green-600">13,431.34</p>
          <p className="text-sm text-green-600">+0.8% (+105.22)</p>
        </div>
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">DOW</h3>
          <p className="text-2xl font-bold text-red-600">34,112.27</p>
          <p className="text-sm text-red-600">-0.3% (-112.45)</p>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg border">
        <h3 className="text-lg font-semibold mb-4">Sample Stock Price Trend</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={stockData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="price" stroke="#2563eb" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );

  const renderForexTab = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">EUR/USD</h3>
          <p className="text-xl font-bold">1.0842</p>
          <p className="text-sm text-green-600">+0.12%</p>
        </div>
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">GBP/USD</h3>
          <p className="text-xl font-bold">1.2734</p>
          <p className="text-sm text-red-600">-0.08%</p>
        </div>
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">USD/JPY</h3>
          <p className="text-xl font-bold">148.62</p>
          <p className="text-sm text-green-600">+0.34%</p>
        </div>
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">USD/CAD</h3>
          <p className="text-xl font-bold">1.3456</p>
          <p className="text-sm text-red-600">-0.15%</p>
        </div>
      </div>
    </div>
  );

  const renderCryptoTab = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">Bitcoin (BTC)</h3>
          <p className="text-2xl font-bold text-orange-600">$42,387.50</p>
          <p className="text-sm text-green-600">+2.1% (+$874.23)</p>
        </div>
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">Ethereum (ETH)</h3>
          <p className="text-2xl font-bold text-blue-600">$2,542.18</p>
          <p className="text-sm text-green-600">+1.8% (+$45.32)</p>
        </div>
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">Market Cap</h3>
          <p className="text-2xl font-bold">$1.67T</p>
          <p className="text-sm text-green-600">+1.5%</p>
        </div>
      </div>
    </div>
  );

  const renderEconomicsTab = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">US GDP Growth</h3>
          <p className="text-xl font-bold text-green-600">3.2%</p>
          <p className="text-sm text-gray-500">Q2 2024</p>
        </div>
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">Unemployment</h3>
          <p className="text-xl font-bold text-blue-600">3.8%</p>
          <p className="text-sm text-gray-500">Latest</p>
        </div>
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">Inflation (CPI)</h3>
          <p className="text-xl font-bold text-orange-600">3.1%</p>
          <p className="text-sm text-gray-500">YoY</p>
        </div>
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-sm font-medium text-gray-600">Fed Rate</h3>
          <p className="text-xl font-bold text-red-600">5.25%</p>
          <p className="text-sm text-gray-500">Current</p>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg border">
        <h3 className="text-lg font-semibold mb-4">GDP Growth Trend</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={gdpData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="quarter" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="growth" stroke="#059669" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'stocks':
        return renderStocksTab();
      case 'forex':
        return renderForexTab();
      case 'crypto':
        return renderCryptoTab();
      case 'economics':
        return renderEconomicsTab();
      default:
        return renderStocksTab();
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Overview of financial markets and economic indicators</p>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      {renderTabContent()}
    </div>
  );
}