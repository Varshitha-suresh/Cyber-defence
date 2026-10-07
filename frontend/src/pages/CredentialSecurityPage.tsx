import React, { useState } from 'react';
import { api } from '../services/api';
import { CredentialResult } from '../types';
import { KeyRound, Search, ShieldCheck, AlertTriangle, CheckCircle2, Lock } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const CredentialSecurityPage: React.FC = () => {
  const { user } = useAuth();
  const [email, setEmail] = useState(user?.email || '');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CredentialResult | null>(null);

  const handleCheck = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      const res = await api.post('/credentials/check', { email });
      setResult(res.data);
    } catch (err) {
      console.error('Credential exposure check failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#0e1628] p-6 rounded-2xl border border-slate-800">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
            <KeyRound className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight">Credential & Breach Intelligence</h1>
            <p className="text-xs text-slate-400">
              Proactive monitoring against circulating dark web dumps & credential stuffing attacks
            </p>
          </div>
        </div>

        <form onSubmit={handleCheck} className="mt-6 flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3.5" />
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter email to verify breach exposure"
              className="w-full bg-[#0a0e18] border border-slate-700/80 rounded-xl pl-9 pr-3 py-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 text-white rounded-xl text-xs font-semibold tracking-wide transition shadow-sm"
          >
            {loading ? 'Checking Intelligence...' : 'CHECK EXPOSURE'}
          </button>
        </form>

        <div className="mt-3 p-3 bg-[#0a0e18] border border-slate-800/80 rounded-xl text-[11px] text-slate-400 flex items-center gap-2">
          <Lock className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>Privacy Guarantee: We never ask for or store passwords. Queries inspect registered email exposure hashes only.</span>
        </div>
      </div>

      {result && (
        <div className="bg-[#0e1628] rounded-2xl border border-slate-800 p-6 space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
            <div>
              <div className="flex items-center gap-2">
                <span
                  className={`text-xs px-3 py-1 rounded-full font-bold uppercase border ${
                    result.status === 'EXPOSED'
                      ? 'bg-red-950/40 text-red-400 border-red-800/40'
                      : result.status === 'CLEAN'
                      ? 'bg-emerald-950/40 text-emerald-400 border-emerald-800/40'
                      : 'bg-amber-950/40 text-amber-400 border-amber-800/40'
                  }`}
                >
                  {result.status}
                </span>
                <span className="text-xs text-slate-400 font-mono">
                  Source: {result.source}
                </span>
              </div>
              <p className="text-sm font-semibold text-white mt-2">{result.email}</p>
            </div>

            <div className="text-right">
              <p className="text-[10px] text-slate-400 uppercase">Confirmed Breach Records</p>
              <p className="text-2xl font-extrabold text-white">{result.breach_count}</p>
            </div>
          </div>

          {result.affected_services.length > 0 && (
            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
                Compromised External Platforms
              </h3>
              <div className="flex flex-wrap gap-2">
                {result.affected_services.map((svc, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1.5 bg-[#0a0e18] border border-red-900/50 text-red-300 text-xs rounded-lg font-medium"
                  >
                    {svc}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Remediation Guidelines</h3>
            <ul className="space-y-1.5 text-xs text-slate-300">
              {result.recommended_actions.map((act, idx) => (
                <li key={idx} className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-blue-400 shrink-0" />
                  <span>{act}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};
