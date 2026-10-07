import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Recommendation } from '../types';
import { CheckSquare, CheckCircle2, Clock, AlertTriangle, ShieldCheck } from 'lucide-react';

export const RecommendationsPage: React.FC = () => {
  const [recs, setRecs] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchRecs = async () => {
    try {
      setLoading(true);
      const res = await api.get('/recommendations');
      setRecs(res.data || []);
    } catch (err) {
      console.error('Failed to load recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecs();
  }, []);

  const handleStatusChange = async (id: string, newStatus: string) => {
    try {
      const res = await api.patch(`/recommendations/${id}`, { status: newStatus });
      setRecs(recs.map((r) => (r.id === id ? res.data : r)));
    } catch (err) {
      console.error('Failed to update recommendation status:', err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#0e1628] p-6 rounded-2xl border border-slate-800">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
            <CheckSquare className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight">Prioritized Remediation Action Plan</h1>
            <p className="text-xs text-slate-400">
              Ranked recommendations with estimated risk reductions & status tracking
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {recs.map((rec) => (
          <div
            key={rec.id}
            className={`p-5 rounded-2xl border transition-all ${
              rec.status === 'RESOLVED'
                ? 'bg-[#0a0e18]/60 border-slate-800/50 opacity-75'
                : 'bg-[#0e1628] border-slate-800'
            }`}
          >
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <span
                  className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase border ${
                    rec.severity === 'CRITICAL'
                      ? 'bg-red-950/40 text-red-400 border-red-800/40'
                      : rec.severity === 'HIGH'
                      ? 'bg-amber-950/40 text-amber-400 border-amber-800/40'
                      : 'bg-blue-950/40 text-blue-400 border-blue-800/40'
                  }`}
                >
                  {rec.severity}
                </span>
                <span className="text-xs font-mono text-slate-400">Priority #{rec.priority}</span>
                <span className="text-xs font-mono text-blue-400 bg-blue-950/40 px-2 py-0.5 rounded border border-blue-800/40">
                  {rec.category}
                </span>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400">Est. Risk Reduction:</span>
                <span className="text-xs font-bold text-emerald-400">-{rec.estimated_risk_reduction}%</span>

                <select
                  value={rec.status}
                  onChange={(e) => handleStatusChange(rec.id, e.target.value)}
                  className="ml-3 bg-[#0a0e18] border border-slate-700 rounded-lg px-2.5 py-1 text-xs font-semibold text-white focus:outline-none"
                >
                  <option value="OPEN">OPEN</option>
                  <option value="IN PROGRESS">IN PROGRESS</option>
                  <option value="RESOLVED">RESOLVED</option>
                </select>
              </div>
            </div>

            <div className="mt-3">
              <h3 className="text-sm font-bold text-white">{rec.title}</h3>
              <p className="text-xs text-slate-400 mt-1 leading-relaxed">{rec.why_it_matters}</p>
            </div>

            <div className="mt-3 p-3 bg-[#0a0e18] rounded-xl border border-slate-800/80 text-xs text-slate-300">
              <span className="font-semibold text-blue-400">Recommended Action: </span>
              {rec.recommended_action}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
