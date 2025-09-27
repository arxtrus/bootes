import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Search from './pages/Search';
import Indicators from './pages/Indicators';

/**
 * Main application component with routing and layout
 */
function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Global Navigation */}
      <Navbar />
      
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/search" element={<Search />} />
          <Route path="/indicators" element={<Indicators />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;