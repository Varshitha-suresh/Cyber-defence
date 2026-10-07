import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { SystemStatusData } from '../types';
import { Settings as SettingsIcon, Server, Shield, CheckCircle2, AlertCircle, User, Lock } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const { user } = useAuth();
  const [status, setStatus] = useState<SystemStatusData | null>(null);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [pwdMsg, setPwdMsg] = useState<string | null>(null);
  const [pwdError, setPwdError] = useState<string | null>(null);

  useEffect(() => {
    api.get('/system/status').then((res) => setStatus(res.data)).catch(console.error);
  }, []);

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPwdMsg(null);
    setPwdError(null);

    try {
      await api.post('/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword,
      });
      setPwdMsg('Password updated successfully.');
      setCurrentPassword('');
      setNewPassword('');
    } catch (err: any) {
      setPwdError(err.response?.data?.detail || 'Failed to update password.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#0e1628] p-6 rounded-2xl border border-slate-800">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
            <SettingsIcon className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight">System Configuration & Health</h1>
            <p className="text-xs text-slate-400">
              Diagnostic verification of ML engines, database layers, and account security
            </p>
          </div>
        </div>
      </div>

      {/* System Diagnostic Status Grid */}
      <div className="bg-[#0e1628] p-6 rounded-2xl border border-slate-800 space-y-4">
        <div className="flex items-center gap-2">
          <Server className="w-4 h-4 text-blue-400" />
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Defence Engine & Subsystem Diagnostics
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-3 bg-[#0a0e18] rounded-xl border border-slate-800">
            <span className="text-[11px] text-slate-400">PostgreSQL / SQLite Database</span>
            <p className="text-xs font-bold text-emerald-400 mt-1">{status?.database || 'CONNECTING...'}</p>
          </div>
          <div className="p-3 bg-[#0a0e18] rounded-xl border border-slate-800">
            <span className="text-[11px] text-slate-400">Phishing Supervised ML Model</span>
            <p className="text-xs font-bold text-emerald-400 mt-1">{status?.phishing_classifier || 'CHECKING...'}</p>
          </div>
          <div className="p-3 bg-[#0a0e18] rounded-xl border border-slate-800">
            <span className="text-[11px] text-slate-400">Isolation Forest Anomaly Model</span>
            <p className="text-xs font-bold text-emerald-400 mt-1">{status?.anomaly_detector || 'CHECKING...'}</p>
          </div>
          <div className="p-3 bg-[#0a0e18] rounded-xl border border-slate-800">
            <span className="text-[11px] text-slate-400">Breach Intelligence Provider</span>
            <p className="text-xs font-bold text-blue-400 mt-1">{status?.breach_api || 'CHECKING...'}</p>
          </div>
          <div className="p-3 bg-[#0a0e18] rounded-xl border border-slate-800">
            <span className="text-[11px] text-slate-400">Device Telemetry Collector</span>
            <p className="text-xs font-bold text-emerald-400 mt-1">{status?.device_collector || 'CHECKING...'}</p>
          </div>
          <div className="p-3 bg-[#0a0e18] rounded-xl border border-slate-800">
            <span className="text-[11px] text-slate-400">Network Interface Collector</span>
            <p className="text-xs font-bold text-emerald-400 mt-1">{status?.network_collector || 'CHECKING...'}</p>
          </div>
        </div>
      </div>

      {/* User Security & Password Update */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-[#0e1628] p-6 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center gap-2">
            <User className="w-4 h-4 text-blue-400" />
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-300">
              User Profile & Consent Preferences
            </h2>
          </div>
          <div className="space-y-2 text-xs">
            <p><span className="text-slate-400">Name:</span> <span className="text-white font-medium">{user?.name}</span></p>
            <p><span className="text-slate-400">Email:</span> <span className="text-white font-medium">{user?.email}</span></p>
            <p><span className="text-slate-400">Classification:</span> <span className="text-white font-medium">{user?.professional_type}</span></p>
            <p><span className="text-slate-400">Telemetry Consent:</span> <span className="text-emerald-400 font-medium">Active (Safe Local Only)</span></p>
          </div>
        </div>

        <div className="bg-[#0e1628] p-6 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center gap-2">
            <Lock className="w-4 h-4 text-blue-400" />
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-300">
              Update Password
            </h2>
          </div>

          {pwdMsg && <p className="text-xs text-emerald-400">{pwdMsg}</p>}
          {pwdError && <p className="text-xs text-red-400">{pwdError}</p>}

          <form onSubmit={handleChangePassword} className="space-y-3">
            <input
              type="password"
              required
              placeholder="Current Password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              className="w-full bg-[#0a0e18] border border-slate-700 rounded-lg p-2 text-xs text-white"
            />
            <input
              type="password"
              required
              minLength={8}
              placeholder="New Password (min 8 characters)"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="w-full bg-[#0a0e18] border border-slate-700 rounded-lg p-2 text-xs text-white"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold"
            >
              Update Password
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
