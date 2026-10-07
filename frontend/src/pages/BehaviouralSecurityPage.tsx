import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { BehaviourResult } from '../types';
import { Activity, ShieldAlert, CheckCircle2, AlertTriangle, RotateCw } from 'lucide-react';

export const BehaviouralSecurityPage: React.FC = () => {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [simNet, setSimNet] = useState('PUBLIC_WIFI');
  const [simLoc, setSimLoc] = useState('DOMESTIC_TRAVEL');
  const [simFreq, setSimFreq] = useState(3.5);
  const [simDur, setSimDur] = useState(25.0);
  const [latestAnalysis, setLatestAnalysis] = useState<BehaviourResult | null>(null);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const res = await api.get('/behaviour/history');
      setHistory(res.data || []);
    } catch (err) {
      console.error('Failed to load behavioural history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleSimulateLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setAnalyzing(true);
      const res = await api.post('/behaviour/analyze', {
        device_id: 'WORK-LAPTOP-01',
        network_category: simNet,
        location_category: simLoc,
        login_frequency: simFreq,
        session_duration: simDur
      });
      setLatestAnalysis(res.data);
      fetchHistory();
    } catch (err) {
      console.error('Error analyzing login behaviour:', err);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#0e1628] p-6 rounded-2xl border border-slate-800">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight">Behavioural Anomaly Detection</h1>
            <p className="text-xs text-slate-400">
              Isolation Forest unsupervised machine learning model detecting atypical authentication contexts
            </p>
          </div>
        </div>

        {/* Test Authentication Context Simulation Form */}
        <form onSubmit={handleSimulateLogin} className="mt-6 p-4 bg-[#0a0e18] border border-slate-800 rounded-xl space-y-4">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Simulate or Analyze Authentication Context Event
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
            <div>
              <label className="block text-[11px] text-slate-400 mb-1">Network Category</label>
              <select
                value={simNet}
                onChange={(e) => setSimNet(e.target.value)}
                className="w-full bg-[#0d1322] border border-slate-700 rounded-lg p-2 text-xs text-white"
              >
                <option value="HOME">Home Network (Secure)</option>
                <option value="CORPORATE">Corporate VPN</option>
                <option value="PUBLIC_WIFI">Public Wi-Fi (Untrusted)</option>
                <option value="UNKNOWN">Atypical Cellular Hotspot</option>
              </select>
            </div>

            <div>
              <label className="block text-[11px] text-slate-400 mb-1">Location Category</label>
              <select
                value={simLoc}
                onChange={(e) => setSimLoc(e.target.value)}
                className="w-full bg-[#0d1322] border border-slate-700 rounded-lg p-2 text-xs text-white"
              >
                <option value="HOME_REGION">Home City/Region</option>
                <option value="DOMESTIC_TRAVEL">Domestic Travel</option>
                <option value="FOREIGN_UNTRUSTED">Foreign Untrusted IP Range</option>
              </select>
            </div>

            <div>
              <label className="block text-[11px] text-slate-400 mb-1">Login Frequency (per hr)</label>
              <input
                type="number"
                step="0.5"
                min="0.5"
                max="20"
                value={simFreq}
                onChange={(e) => setSimFreq(parseFloat(e.target.value))}
                className="w-full bg-[#0d1322] border border-slate-700 rounded-lg p-2 text-xs text-white"
              />
            </div>

            <div>
              <label className="block text-[11px] text-slate-400 mb-1">Session Duration (min)</label>
              <input
                type="number"
                min="1"
                max="480"
                value={simDur}
                onChange={(e) => setSimDur(parseFloat(e.target.value))}
                className="w-full bg-[#0d1322] border border-slate-700 rounded-lg p-2 text-xs text-white"
              />
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={analyzing}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 text-white text-xs font-semibold rounded-lg shadow-sm transition"
            >
              <RotateCw className={`w-3.5 h-3.5 ${analyzing ? 'animate-spin' : ''}`} />
              <span>{analyzing ? 'Running Isolation Forest...' : 'EVALUATE BEHAVIOUR'}</span>
            </button>
          </div>
        </form>
      </div>

      {latestAnalysis && (
        <div className="bg-[#0e1628] rounded-2xl border border-slate-800 p-6 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span
                className={`text-xs px-3 py-1 rounded-full font-bold uppercase border ${
                  latestAnalysis.status === 'ANOMALOUS'
                    ? 'bg-amber-950/40 text-amber-400 border-amber-800/40'
                    : 'bg-emerald-950/40 text-emerald-400 border-emerald-800/40'
                }`}
              >
                {latestAnalysis.status}
              </span>
              <span className="text-xs text-slate-400 font-mono">
                Anomaly Score: {latestAnalysis.anomaly_score}
              </span>
            </div>
            <span className="text-xs text-white font-bold">
              Risk Contribution: {latestAnalysis.risk_contribution} / 100
            </span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">{latestAnalysis.explanation}</p>
        </div>
      )}

      {/* Historical Authentication Log */}
      <div className="bg-[#0e1628] rounded-2xl border border-slate-800 p-6">
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">
          Authentication Event History
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-[#0a0e18] text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-2.5 px-3">Network</th>
                <th className="py-2.5 px-3">Location</th>
                <th className="py-2.5 px-3">Frequency</th>
                <th className="py-2.5 px-3">Duration</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3">Anomaly Score</th>
                <th className="py-2.5 px-3">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              {history.map((evt) => (
                <tr key={evt.id} className="hover:bg-slate-800/30 transition">
                  <td className="py-2 px-3 font-semibold text-white">{evt.network_category}</td>
                  <td className="py-2 px-3 text-slate-400">{evt.location_category}</td>
                  <td className="py-2 px-3">{evt.login_frequency}/hr</td>
                  <td className="py-2 px-3">{evt.session_duration}m</td>
                  <td className="py-2 px-3">
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                        evt.is_anomalous
                          ? 'bg-amber-950/40 text-amber-400 border-amber-800/40'
                          : 'bg-emerald-950/40 text-emerald-400 border-emerald-800/40'
                      }`}
                    >
                      {evt.is_anomalous ? 'ANOMALOUS' : 'NORMAL'}
                    </span>
                  </td>
                  <td className="py-2 px-3 font-mono">{evt.anomaly_score}</td>
                  <td className="py-2 px-3 text-[10px] text-slate-400">
                    {new Date(evt.timestamp).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
