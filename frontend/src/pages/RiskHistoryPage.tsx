import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { SecurityAssessment } from '../types';
import { History, ShieldAlert, Calendar, ArrowRight } from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from 'recharts';

export const RiskHistoryPage: React.FC = () => {
  const [history, setHistory] = useState<SecurityAssessment[]>([]);
  const [selectedAssessment, setSelectedAssessment] = useState<SecurityAssessment | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const res = await api.get('/assessment/history?limit=30');
      setHistory(res.data || []);
      if (res.data && res.data.length > 0) {
        setSelectedAssessment(res.data[0]);
      }
    } catch (err) {
      console.error('Failed to load risk history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const chartData = history
    .slice()
    .reverse()
    .map((item, index) => ({
      index: `#${index + 1}`,
      date: new Date(item.created_at).toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit' }),
      overall: item.overall_score,
      device: item.category_scores.device_security,
      network: item.category_scores.network_security,
      credential: item.category_scores.credential_security,
      phishing: item.category_scores.phishing_risk,
      behaviour: item.category_scores.behavioural_risk,
    }));

  return (
    <div className="space-y-6">
      <div className="bg-[#0e1628] p-6 rounded-2xl border border-slate-800">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
            <History className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight">Risk Trajectory & Historical Audit</h1>
            <p className="text-xs text-slate-400">
              Longitudinal tracking of Cyber Risk Index and multi-vector category fluctuations
            </p>
          </div>
        </div>
      </div>

      {/* Multi-vector Trend Chart */}
      <div className="bg-[#0e1628] p-6 rounded-2xl border border-slate-800 space-y-4">
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">Historical Risk Trajectory</h2>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
              <XAxis dataKey="date" stroke="#64748b" fontSize={11} tickLine={false} />
              <YAxis stroke="#64748b" fontSize={11} domain={[0, 100]} tickLine={false} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0d1322', borderColor: '#334155', fontSize: '12px' }}
                labelStyle={{ color: '#94a3b8' }}
              />
              <Line type="monotone" dataKey="overall" name="Overall Index" stroke="#38bdf8" strokeWidth={3} dot={{ r: 4 }} />
              <Line type="monotone" dataKey="device" name="Device" stroke="#818cf8" strokeWidth={1.5} dot={false} />
              <Line type="monotone" dataKey="network" name="Network" stroke="#34d399" strokeWidth={1.5} dot={false} />
              <Line type="monotone" dataKey="credential" name="Credential" stroke="#f472b6" strokeWidth={1.5} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Assessment Audit List */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-[#0e1628] p-6 rounded-2xl border border-slate-800 space-y-3">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Past Assessments</h2>
          <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
            {history.map((a) => (
              <div
                key={a.id}
                onClick={() => setSelectedAssessment(a)}
                className={`p-3 rounded-xl border cursor-pointer transition ${
                  selectedAssessment?.id === a.id
                    ? 'bg-blue-950/40 border-blue-500'
                    : 'bg-[#0a0e18] border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-bold text-white">{a.overall_score} / 100</span>
                  <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded border border-slate-700 text-slate-300">
                    {a.risk_level}
                  </span>
                </div>
                <div className="flex items-center justify-between mt-2 text-[10px] text-slate-400">
                  <span>{new Date(a.created_at).toLocaleString()}</span>
                  {a.is_demo && <span className="text-amber-400 font-mono">DEMO</span>}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Selected Assessment Detailed Inspector */}
        <div className="lg:col-span-2 bg-[#0e1628] p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">Assessment Detail Inspector</h2>
          {selectedAssessment ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-[#0a0e18] rounded-xl border border-slate-800">
                <div>
                  <span className="text-xs text-slate-400">Cyber Risk Index</span>
                  <p className="text-3xl font-extrabold text-white mt-1">{selectedAssessment.overall_score} / 100</p>
                </div>
                <div className="text-right">
                  <span className="text-xs text-slate-400">Classification</span>
                  <p className="text-lg font-bold text-blue-400 mt-1">{selectedAssessment.risk_level} RISK</p>
                </div>
              </div>

              <div className="p-4 bg-[#0a0e18] rounded-xl border border-slate-800">
                <span className="text-xs font-bold text-slate-300">Scoring Engine Explanation</span>
                <p className="text-xs text-slate-400 mt-2 leading-relaxed">{selectedAssessment.score_explanation}</p>
              </div>

              <div>
                <span className="text-xs font-bold text-slate-300">Category Vectors</span>
                <div className="grid grid-cols-5 gap-2 mt-2 text-center">
                  <div className="p-2 bg-[#0a0e18] rounded border border-slate-800">
                    <p className="text-[10px] text-slate-400">Device</p>
                    <p className="text-xs font-bold text-white">{selectedAssessment.category_scores.device_security}</p>
                  </div>
                  <div className="p-2 bg-[#0a0e18] rounded border border-slate-800">
                    <p className="text-[10px] text-slate-400">Network</p>
                    <p className="text-xs font-bold text-white">{selectedAssessment.category_scores.network_security}</p>
                  </div>
                  <div className="p-2 bg-[#0a0e18] rounded border border-slate-800">
                    <p className="text-[10px] text-slate-400">Credential</p>
                    <p className="text-xs font-bold text-white">{selectedAssessment.category_scores.credential_security}</p>
                  </div>
                  <div className="p-2 bg-[#0a0e18] rounded border border-slate-800">
                    <p className="text-[10px] text-slate-400">Phishing</p>
                    <p className="text-xs font-bold text-white">{selectedAssessment.category_scores.phishing_risk}</p>
                  </div>
                  <div className="p-2 bg-[#0a0e18] rounded border border-slate-800">
                    <p className="text-[10px] text-slate-400">Behaviour</p>
                    <p className="text-xs font-bold text-white">{selectedAssessment.category_scores.behavioural_risk}</p>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-xs text-slate-500">Select an assessment to view details.</p>
          )}
        </div>
      </div>
    </div>
  );
};
