import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { DeviceScanData } from '../types';
import { Laptop, Shield, ShieldAlert, CheckCircle2, RotateCw, AlertTriangle, Cpu } from 'lucide-react';

export const DeviceSecurityPage: React.FC = () => {
  const [data, setData] = useState<DeviceScanData | null>(null);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);

  const fetchDeviceData = async () => {
    try {
      setLoading(true);
      const res = await api.get('/device/security');
      setData(res.data);
    } catch (err) {
      console.error('Failed to load device security info:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDeviceData();
  }, []);

  const handleScan = async () => {
    try {
      setScanning(true);
      const res = await api.post('/device/scan');
      setData(res.data);
    } catch (err) {
      console.error('Failed to run device scan:', err);
    } finally {
      setScanning(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-[#0e1628] p-6 rounded-2xl border border-slate-800">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
              <Laptop className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white tracking-tight">Endpoint Device Security</h1>
              <p className="text-xs text-slate-400">Non-invasive host telemetry & configuration auditing</p>
            </div>
          </div>
        </div>

        <button
          onClick={handleScan}
          disabled={scanning}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 text-white text-xs font-semibold rounded-lg shadow-sm transition"
        >
          <RotateCw className={`w-3.5 h-3.5 ${scanning ? 'animate-spin' : ''}`} />
          <span>{scanning ? 'Auditing Host...' : 'SCAN DEVICE'}</span>
        </button>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 bg-[#0e1628] rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400">Operating System</p>
          <p className="text-sm font-bold text-white mt-1">{data?.os || 'Detecting...'} {data?.os_version}</p>
        </div>
        <div className="p-4 bg-[#0e1628] rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400">Host Firewall</p>
          <p className="text-sm font-bold text-emerald-400 mt-1">{data?.firewall_status || 'Scanning...'}</p>
        </div>
        <div className="p-4 bg-[#0e1628] rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400">Endpoint Protection / Antivirus</p>
          <p className="text-sm font-bold text-blue-400 mt-1 truncate">{data?.antivirus_status || 'Scanning...'}</p>
        </div>
        <div className="p-4 bg-[#0e1628] rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400">Device Risk Score</p>
          <p className="text-xl font-bold text-white mt-1">{data?.device_score ?? '--'} <span className="text-xs text-slate-500 font-normal">/ 100</span></p>
        </div>
      </div>

      {/* Device Findings */}
      <div className="bg-[#0e1628] rounded-2xl border border-slate-800 p-6 space-y-4">
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">Endpoint Security Findings</h2>
        <div className="space-y-3">
          {data?.findings.map((f, idx) => (
            <div key={idx} className="p-4 bg-[#0a0e18] border border-slate-800/80 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-white">{f.title}</span>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase border ${
                  f.severity === 'LOW' ? 'bg-emerald-950/40 text-emerald-400 border-emerald-800/40' :
                  f.severity === 'MEDIUM' ? 'bg-amber-950/40 text-amber-400 border-amber-800/40' :
                  'bg-red-950/40 text-red-400 border-red-800/40'
                }`}>
                  {f.severity}
                </span>
              </div>
              <p className="text-xs text-slate-400">{f.description}</p>
              {f.evidence && (
                <div className="text-[11px] font-mono bg-slate-900/60 p-2 rounded text-slate-300 border border-slate-800/60">
                  <span className="text-slate-500">Evidence: </span>{f.evidence}
                </div>
              )}
              {f.recommendation && (
                <p className="text-[11px] text-blue-400 font-medium">
                  Recommendation: {f.recommendation}
                </p>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
