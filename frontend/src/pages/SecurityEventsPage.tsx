import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { SecurityEventItem } from '../types';
import { AlertTriangle, ShieldAlert, CheckCircle2, Clock } from 'lucide-react';

export const SecurityEventsPage: React.FC = () => {
  const [events, setEvents] = useState<SecurityEventItem[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchEvents = async () => {
    try {
      setLoading(true);
      const res = await api.get('/security-events');
      setEvents(res.data || []);
    } catch (err) {
      console.error('Failed to load events:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  return (
    <div className="space-y-6">
      <div className="bg-[#0e1628] p-6 rounded-2xl border border-slate-800">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
            <AlertTriangle className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight">Security Audit Log & Alerts</h1>
            <p className="text-xs text-slate-400">
              Chronological log of multi-module threat telemetry, anomaly detections and system actions
            </p>
          </div>
        </div>
      </div>

      <div className="bg-[#0e1628] rounded-2xl border border-slate-800 p-6">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-[#0a0e18] text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-2.5 px-3">Event Type</th>
                <th className="py-2.5 px-3">Category</th>
                <th className="py-2.5 px-3">Severity</th>
                <th className="py-2.5 px-3">Message</th>
                <th className="py-2.5 px-3">Source</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              {events.map((evt) => (
                <tr key={evt.id} className="hover:bg-slate-800/30 transition">
                  <td className="py-2.5 px-3 font-semibold text-white">{evt.event_type}</td>
                  <td className="py-2.5 px-3 text-slate-400">{evt.category}</td>
                  <td className="py-2.5 px-3">
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                        evt.severity === 'CRITICAL'
                          ? 'bg-red-950/40 text-red-400 border-red-800/40'
                          : evt.severity === 'HIGH'
                          ? 'bg-amber-950/40 text-amber-400 border-amber-800/40'
                          : evt.severity === 'MODERATE'
                          ? 'bg-blue-950/40 text-blue-400 border-blue-800/40'
                          : 'bg-emerald-950/40 text-emerald-400 border-emerald-800/40'
                      }`}
                    >
                      {evt.severity}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 text-slate-300 max-w-sm truncate">{evt.message}</td>
                  <td className="py-2.5 px-3 font-mono text-[10px] text-slate-400">{evt.source}</td>
                  <td className="py-2.5 px-3 font-mono text-[10px] text-slate-400">{evt.status}</td>
                  <td className="py-2.5 px-3 text-[10px] text-slate-400">
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
