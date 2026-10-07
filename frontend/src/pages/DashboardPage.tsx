import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { SecurityAssessment, SecurityEventItem } from '../types';
import {
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  RotateCw,
  Cpu,
  Wifi,
  Lock,
  Eye,
  Activity,
  ArrowRight,
  TrendingDown,
  Clock,
  Layers,
  CheckCircle2,
  XCircle,
  FileWarning
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  LineChart,
  Line,
  CartesianGrid
} from 'recharts';

export const DashboardPage: React.FC = () => {
  const [assessment, setAssessment] = useState<SecurityAssessment | null>(null);
  const [history, setHistory] = useState<SecurityAssessment[]>([]);
  const [events, setEvents] = useState<SecurityEventItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [selectedScenario, setSelectedScenario] = useState<string>('REAL');

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [latestRes, historyRes, eventsRes] = await Promise.all([
        api.get('/assessment/latest'),
        api.get('/assessment/history?limit=10'),
        api.get('/security-events'),
      ]);
      setAssessment(latestRes.data);
      setHistory(historyRes.data || []);
      setEvents(eventsRes.data || []);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleRunAssessment = async () => {
    try {
      setScanning(true);
      const payload = selectedScenario === 'REAL' ? {} : { scenario: selectedScenario };
      const res = await api.post('/assessment/run', payload);
      setAssessment(res.data);
      // Refresh history & events
      fetchDashboardData();
    } catch (err) {
      console.error('Assessment execution failed:', err);
    } finally {
      setScanning(false);
    }
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'LOW':
        return 'text-emerald-400 bg-emerald-950/40 border-emerald-800/40';
      case 'MODERATE':
        return 'text-blue-400 bg-blue-950/40 border-blue-800/40';
      case 'HIGH':
        return 'text-amber-400 bg-amber-950/40 border-amber-800/40';
      case 'CRITICAL':
        return 'text-red-400 bg-red-950/40 border-red-800/40';
      default:
        return 'text-slate-400 bg-slate-900 border-slate-700';
    }
  };

  const categoryBarData = assessment
    ? [
        { name: 'Device', score: assessment.category_scores.device_security },
        { name: 'Network', score: assessment.category_scores.network_security },
        { name: 'Credential', score: assessment.category_scores.credential_security },
        { name: 'Phishing', score: assessment.category_scores.phishing_risk },
        { name: 'Behaviour', score: assessment.category_scores.behavioural_risk },
      ]
    : [];

  const trendData = history
    .slice()
    .reverse()
    .map((item, index) => ({
      index: `#${index + 1}`,
      date: new Date(item.created_at).toLocaleDateString([], { month: 'short', day: 'numeric' }),
      score: item.overall_score,
    }));

  return (
    <div className="space-y-6">
      {/* Top Banner & Assessment Execution Bar */}
      <div className="bg-[#0e1628] border border-slate-800/80 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold text-white tracking-tight">Security Posture Dashboard</h1>
            {assessment?.is_demo && (
              <span className="px-2 py-0.5 text-[10px] font-mono uppercase bg-amber-950/60 text-amber-400 border border-amber-800/40 rounded">
                DEMO DATA
              </span>
            )}
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Last Evaluated:{' '}
            {assessment?.created_at ? new Date(assessment.created_at).toLocaleString() : 'Never'}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-1.5 bg-[#0a0e18] px-2.5 py-1.5 rounded-lg border border-slate-800 text-xs">
            <span className="text-slate-400 text-[11px]">Execution Profile:</span>
            <select
              value={selectedScenario}
              onChange={(e) => setSelectedScenario(e.target.value)}
              className="bg-transparent text-slate-200 text-xs font-semibold focus:outline-none"
            >
              <option value="REAL" className="bg-[#0e1628]">Real Local Machine Telemetry</option>
              <option value="SECURE" className="bg-[#0e1628]">Scenario 1: Secure Baseline (Low)</option>
              <option value="MODERATE" className="bg-[#0e1628]">Scenario 2: Moderate Risk</option>
              <option value="CRITICAL" className="bg-[#0e1628]">Scenario 3: Critical Threat Exposure</option>
            </select>
          </div>

          <button
            onClick={handleRunAssessment}
            disabled={scanning}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 text-white text-xs font-semibold rounded-lg shadow-sm transition"
          >
            <RotateCw className={`w-3.5 h-3.5 ${scanning ? 'animate-spin' : ''}`} />
            <span>{scanning ? 'Analyzing Pipeline...' : 'RUN SECURITY ASSESSMENT'}</span>
          </button>
        </div>
      </div>

      {/* Main Grid: Cyber Risk Index Score & Category Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cyber Risk Index Card */}
        <div className="bg-[#0e1628] border border-slate-800/80 rounded-2xl p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Cyber Risk Index</span>
              <span
                className={`text-xs px-2.5 py-0.5 rounded-full font-bold uppercase border ${getRiskColor(
                  assessment?.risk_level || 'LOW'
                )}`}
              >
                {assessment?.risk_level || 'EVALUATING'} RISK
              </span>
            </div>

            <div className="mt-6 flex items-baseline gap-2">
              <span className="text-5xl font-extrabold text-white">
                {assessment ? assessment.overall_score : '--'}
              </span>
              <span className="text-slate-500 font-mono text-lg">/ 100</span>
            </div>

            <div className="w-full bg-slate-800 rounded-full h-2.5 mt-4 overflow-hidden">
              <div
                className={`h-2.5 rounded-full transition-all duration-500 ${
                  (assessment?.overall_score || 0) < 25
                    ? 'bg-emerald-400'
                    : (assessment?.overall_score || 0) < 50
                    ? 'bg-blue-400'
                    : (assessment?.overall_score || 0) < 75
                    ? 'bg-amber-400'
                    : 'bg-red-500'
                }`}
                style={{ width: `${Math.min(100, assessment?.overall_score || 0)}%` }}
              />
            </div>

            <p className="text-xs text-slate-400 mt-4 leading-relaxed">
              {assessment?.score_explanation ||
                'Run an assessment to compute risk across device, network, credentials, phishing, and behavioural telemetry.'}
            </p>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-500">
            <span>Formula: NIST CSF Deterministic Weighted</span>
            <span>Scale: 0 (Secure) - 100 (Critical)</span>
          </div>
        </div>

        {/* Category Breakdown Chart */}
        <div className="lg:col-span-2 bg-[#0e1628] border border-slate-800/80 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Category Risk Vector Breakdown (0–100)
            </h2>
            <span className="text-[11px] text-slate-500 font-mono">Lower is safer</span>
          </div>
          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categoryBarData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis dataKey="name" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} domain={[0, 100]} tickLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0d1322', borderColor: '#334155', fontSize: '12px' }}
                  labelStyle={{ color: '#94a3b8' }}
                />
                <Bar dataKey="score" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          {/* Quick Metrics Badges */}
          <div className="grid grid-cols-5 gap-2 mt-4 pt-3 border-t border-slate-800/80 text-center">
            <div>
              <p className="text-[10px] text-slate-400">Device</p>
              <p className="text-xs font-bold text-white">{assessment?.category_scores?.device_security ?? '--'}</p>
            </div>
            <div>
              <p className="text-[10px] text-slate-400">Network</p>
              <p className="text-xs font-bold text-white">{assessment?.category_scores?.network_security ?? '--'}</p>
            </div>
            <div>
              <p className="text-[10px] text-slate-400">Credential</p>
              <p className="text-xs font-bold text-white">{assessment?.category_scores?.credential_security ?? '--'}</p>
            </div>
            <div>
              <p className="text-[10px] text-slate-400">Phishing</p>
              <p className="text-xs font-bold text-white">{assessment?.category_scores?.phishing_risk ?? '--'}</p>
            </div>
            <div>
              <p className="text-[10px] text-slate-400">Behaviour</p>
              <p className="text-xs font-bold text-white">{assessment?.category_scores?.behavioural_risk ?? '--'}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Second Row: Top Prioritized Recommendations & Risk History Trend */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Recommendations */}
        <div className="bg-[#0e1628] border border-slate-800/80 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Prioritized Remediation Actions
              </h2>
              <span className="px-1.5 py-0.5 rounded text-[10px] bg-blue-900/40 text-blue-300 font-mono">
                {assessment?.recommendations?.length || 0} Open
              </span>
            </div>
          </div>

          <div className="space-y-3">
            {assessment?.recommendations && assessment.recommendations.length > 0 ? (
              assessment.recommendations.slice(0, 3).map((rec) => (
                <div key={rec.id} className="p-3 bg-[#0a0e18] border border-slate-800 rounded-xl space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-white">{rec.title}</span>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase border ${getRiskColor(
                        rec.severity
                      )}`}
                    >
                      {rec.severity}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 leading-relaxed">{rec.recommended_action}</p>
                  <div className="flex items-center justify-between text-[10px] text-slate-500 pt-1">
                    <span>Est. Risk Reduction: -{rec.estimated_risk_reduction}%</span>
                    <span className="text-blue-400 font-semibold">{rec.status}</span>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-xs text-slate-500">
                No active recommendations. Endpoint posture is compliant.
              </div>
            )}
          </div>
        </div>

        {/* Risk Trend Chart */}
        <div className="bg-[#0e1628] border border-slate-800/80 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Risk Trend Over Time
            </h2>
            <span className="text-[11px] text-slate-500 font-mono">Past Assessments</span>
          </div>

          <div className="h-52 w-full">
            {trendData.length > 1 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                  <XAxis dataKey="date" stroke="#64748b" fontSize={11} tickLine={false} />
                  <YAxis stroke="#64748b" fontSize={11} domain={[0, 100]} tickLine={false} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0d1322', borderColor: '#334155', fontSize: '12px' }}
                    labelStyle={{ color: '#94a3b8' }}
                  />
                  <Line
                    type="monotone"
                    dataKey="score"
                    stroke="#38bdf8"
                    strokeWidth={2}
                    dot={{ fill: '#38bdf8', r: 3 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-500">
                Run multiple assessments to render historical trend trajectory.
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Third Row: Recent Security Events */}
      <div className="bg-[#0e1628] border border-slate-800/80 rounded-2xl p-6">
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">
          Audit Trail & Security Events
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-[#0a0e18] text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-2.5 px-3">Event Type</th>
                <th className="py-2.5 px-3">Category</th>
                <th className="py-2.5 px-3">Severity</th>
                <th className="py-2.5 px-3">Message</th>
                <th className="py-2.5 px-3">Source</th>
                <th className="py-2.5 px-3">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              {events.slice(0, 5).map((evt) => (
                <tr key={evt.id} className="hover:bg-slate-800/30 transition">
                  <td className="py-2 px-3 font-semibold text-white">{evt.event_type}</td>
                  <td className="py-2 px-3 text-slate-400">{evt.category}</td>
                  <td className="py-2 px-3">
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${getRiskColor(evt.severity)}`}>
                      {evt.severity}
                    </span>
                  </td>
                  <td className="py-2 px-3 text-slate-300 truncate max-w-xs">{evt.message}</td>
                  <td className="py-2 px-3 font-mono text-[10px] text-slate-400">{evt.source}</td>
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
