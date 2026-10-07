import React, { useState } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  ShieldAlert,
  LayoutDashboard,
  Laptop,
  Wifi,
  MailCheck,
  KeyRound,
  Activity,
  CheckSquare,
  History,
  AlertTriangle,
  Settings as SettingsIcon,
  LogOut,
  ChevronRight,
  Menu,
  X,
  Server
} from 'lucide-react';

export const MainLayout: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navLinks = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Device Security', path: '/device', icon: Laptop },
    { name: 'Network Security', path: '/network', icon: Wifi },
    { name: 'Phishing Analyzer', path: '/phishing', icon: MailCheck },
    { name: 'Credential Security', path: '/credentials', icon: KeyRound },
    { name: 'Behavioural Security', path: '/behaviour', icon: Activity },
    { name: 'Recommendations', path: '/recommendations', icon: CheckSquare },
    { name: 'Risk History', path: '/history', icon: History },
    { name: 'Security Events', path: '/events', icon: AlertTriangle },
    { name: 'Settings & Status', path: '/settings', icon: SettingsIcon },
  ];

  return (
    <div className="flex h-screen bg-[#0b0f19] text-slate-100 overflow-hidden font-sans">
      {/* Sidebar for Desktop */}
      <aside className="hidden md:flex flex-col w-64 bg-[#0d1322] border-r border-slate-800/80">
        <div className="p-5 flex items-center gap-3 border-b border-slate-800/80">
          <div className="p-2 bg-blue-600/20 text-blue-400 rounded-lg border border-blue-500/30">
            <ShieldAlert className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <h1 className="text-sm font-bold tracking-wide uppercase text-slate-200">Cyber Defence</h1>
            <p className="text-[10px] text-slate-400">Remote Pro Risk Engine</p>
          </div>
        </div>

        <nav className="flex-1 overflow-y-auto p-3 space-y-1">
          {navLinks.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-blue-600 text-white font-semibold shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`
                }
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>

        {/* User Card & Logout */}
        <div className="p-4 border-t border-slate-800/80 bg-[#0a0e18]">
          <div className="flex items-center justify-between">
            <div className="truncate">
              <p className="text-xs font-semibold text-slate-200 truncate">{user?.name || 'Remote Professional'}</p>
              <p className="text-[11px] text-slate-400 truncate">{user?.email}</p>
              <span className="inline-block mt-1 px-1.5 py-0.5 text-[9px] font-mono bg-blue-900/40 text-blue-300 rounded border border-blue-700/40">
                {user?.professional_type || 'Contractor'}
              </span>
            </div>
            <button
              onClick={handleLogout}
              title="Sign Out"
              className="p-1.5 text-slate-400 hover:text-red-400 hover:bg-slate-800 rounded transition"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Navbar */}
        <header className="h-14 bg-[#0d1322]/90 border-b border-slate-800/80 px-6 flex items-center justify-between">
          <div className="flex items-center gap-3 md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-1.5 rounded-lg bg-slate-800 text-slate-300"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            <span className="text-sm font-bold text-slate-200">Cyber Defence System</span>
          </div>

          <div className="hidden md:flex items-center gap-2 text-xs text-slate-400">
            <span>Security Operations</span>
            <ChevronRight className="w-3.5 h-3.5 text-slate-600" />
            <span className="text-slate-200 font-medium">NIST CSF Aligned Assessment</span>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-2.5 py-1 bg-emerald-950/40 border border-emerald-800/40 text-emerald-400 text-[11px] rounded-full">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              <span>DEFENCE ENGINE ACTIVE</span>
            </div>
          </div>
        </header>

        {/* Mobile Navigation Drawer */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-[#0d1322] border-b border-slate-800 p-4 space-y-1">
            {navLinks.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={() => setMobileMenuOpen(false)}
                className="flex items-center gap-3 px-3 py-2 rounded text-xs text-slate-300 hover:bg-slate-800"
              >
                <item.icon className="w-4 h-4" />
                <span>{item.name}</span>
              </NavLink>
            ))}
            <button
              onClick={handleLogout}
              className="flex items-center gap-3 w-full px-3 py-2 text-xs text-red-400 hover:bg-slate-800 rounded mt-2"
            >
              <LogOut className="w-4 h-4" />
              <span>Sign Out</span>
            </button>
          </div>
        )}

        {/* View Page Body */}
        <main className="flex-1 overflow-y-auto p-6 bg-[#0b0f19]">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
