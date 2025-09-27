import { Link, useLocation } from 'react-router-dom';

/**
 * Navigation bar component with links to main sections
 */
export default function Navbar() {
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: '📊' },
    { name: 'Search', path: '/search', icon: '🔍' },
    { name: 'Indicators', path: '/indicators', icon: '📈' },
  ];

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <nav className="bg-white border-b border-gray-200 px-4 py-3 shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <div className="text-2xl font-bold text-blue-600">🌐 Orbis</div>
          <span className="text-sm text-gray-500">Financial Data Platform</span>
        </div>

        {/* Navigation Links */}
        <div className="flex space-x-1">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                isActive(item.path)
                  ? 'bg-blue-100 text-blue-700 border border-blue-200'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <span className="mr-2">{item.icon}</span>
              {item.name}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}