import React, { useState } from 'react';
import { api } from '../services/api';
import { PhishingResult } from '../types';
import { MailCheck, Search, AlertTriangle, CheckCircle2, ShieldAlert, Cpu } from 'lucide-react';

export const PhishingAnalyzerPage: React.FC = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PhishingResult | null>(null);
  const [verifiedOverride, setVerifiedOverride] = useState(false);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    try {
      setLoading(true);
      setVerifiedOverride(false);
      const res = await api.post('/phishing/analyze', { url });
      setResult(res.data);
    } catch (err) {
      console.error('Error during phishing inference:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadSample = (sampleUrl: string) => {
    setUrl(sampleUrl);
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#0e1628] p-6 rounded-2xl border border-slate-800">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
            <MailCheck className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight">AI Phishing URL Analyzer</h1>
            <p className="text-xs text-slate-400">
              Supervised Machine Learning Model trained on UCI & PhishTank verified corpora
            </p>
          </div>
        </div>

        <form onSubmit={handleAnalyze} className="mt-6 flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3.5" />
            <input
              type="text"
              required
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste suspicious link (e.g., http://192.168.1.100/paypal-update/...)"
              className="w-full bg-[#0a0e18] border border-slate-700/80 rounded-xl pl-9 pr-3 py-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 text-white rounded-xl text-xs font-semibold tracking-wide transition shadow-sm"
          >
            {loading ? 'Evaluating ML Features...' : 'ANALYZE URL'}
          </button>
        </form>

        <div className="mt-4 flex flex-wrap items-center gap-2 text-[11px] text-slate-400">
          <span>Quick Benchmark Samples:</span>
          <button
            type="button"
            onClick={() => loadSample('http://192.168.1.100/paypal-update/verification/login.php?cmd=_login-run')}
            className="px-2 py-1 bg-slate-800 hover:bg-slate-700 rounded text-red-300 font-mono"
          >
            [Phishing Trap: PayPal Fake]
          </button>
          <button
            type="button"
            onClick={() => loadSample('https://bit.ly/3xSecLoginRedirectToBankingPort148')}
            className="px-2 py-1 bg-slate-800 hover:bg-slate-700 rounded text-amber-300 font-mono"
          >
            [Obfuscated: Bitly Shortener]
          </button>
          <button
            type="button"
            onClick={() => loadSample('https://github.com/torvalds/linux')}
            className="px-2 py-1 bg-slate-800 hover:bg-slate-700 rounded text-emerald-300 font-mono"
          >
            [Legitimate: GitHub Repository]
          </button>
        </div>
      </div>

      {result && (
        <div className="bg-[#0e1628] rounded-2xl border border-slate-800 p-6 space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
            <div>
              <div className="flex items-center gap-2">
                <span
                  className={`text-xs px-3 py-1 rounded-full font-bold uppercase border ${
                    result.classification === 'PHISHING'
                      ? 'bg-red-950/40 text-red-400 border-red-800/40'
                      : 'bg-emerald-950/40 text-emerald-400 border-emerald-800/40'
                  }`}
                >
                  {result.classification}
                </span>
                <span className="text-xs text-slate-400 font-mono">
                  Confidence: {(result.confidence * 100).toFixed(1)}%
                </span>
              </div>
              <p className="text-xs font-mono text-slate-300 mt-2 break-all">{result.url}</p>
            </div>

            <div className="flex items-center gap-6">
              <div className="text-right">
                <p className="text-[10px] text-slate-400 uppercase">Phishing Probability</p>
                <p className="text-xl font-bold text-white">{(result.phishing_probability * 100).toFixed(1)}%</p>
              </div>
              <div className="text-right">
                <p className="text-[10px] text-slate-400 uppercase">Risk Contribution</p>
                <p className="text-xl font-bold text-white">{result.risk_score} / 100</p>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
              Lexical & Structural Indicators Detected
            </h3>
            {result.indicators.length > 0 ? (
              <div className="space-y-2">
                {result.indicators.map((ind, i) => (
                  <div key={i} className="p-3 bg-[#0a0e18] border border-slate-800/80 rounded-xl flex items-start gap-3">
                    <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                    <div>
                      <span className="text-xs font-bold text-slate-200">{ind.name}</span>
                      <p className="text-[11px] text-slate-400 mt-0.5">{ind.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-3 bg-[#0a0e18] border border-slate-800/80 rounded-xl flex items-center gap-2 text-xs text-emerald-400">
                <CheckCircle2 className="w-4 h-4" />
                <span>Zero hostile lexical indicators found. Domain structure aligns with legitimate services.</span>
              </div>
            )}
          </div>

          <div className="mt-6 border-t border-slate-800 pt-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
              Device Protection
            </h3>
            {result.classification === 'PHISHING' ? (
              <div className="bg-red-950/20 border border-red-900/50 rounded-xl p-4">
                <div className="flex items-center gap-3 mb-3 text-red-400">
                  <ShieldAlert className="w-5 h-5" />
                  <span className="text-sm font-bold">CONNECTION BLOCKED: HIGH RISK</span>
                </div>
                <p className="text-xs text-slate-300 mb-4">
                  The AI has determined this site is highly likely to be malicious. For your safety, the connection has been restricted.
                </p>
                
                <div className="flex items-center gap-2 mb-4">
                  <input 
                    type="checkbox" 
                    id="override" 
                    checked={verifiedOverride}
                    onChange={(e) => setVerifiedOverride(e.target.checked)}
                    className="w-4 h-4 rounded border-slate-700 bg-slate-800 text-red-500 focus:ring-red-500"
                  />
                  <label htmlFor="override" className="text-xs text-slate-400 select-none cursor-pointer">
                    I verify I understand the risks and want to unblock this connection.
                  </label>
                </div>
                
                <button 
                  disabled={!verifiedOverride}
                  className="px-4 py-2 bg-red-600 hover:bg-red-500 disabled:bg-slate-800 disabled:text-slate-500 text-white rounded text-xs font-bold transition"
                  onClick={() => window.open(result.url, '_blank')}
                >
                  Unblock & Proceed Anyway
                </button>
              </div>
            ) : (
              <div className="bg-emerald-950/20 border border-emerald-900/50 rounded-xl p-4 flex justify-between items-center">
                <div className="flex items-center gap-3 text-emerald-400">
                  <CheckCircle2 className="w-5 h-5" />
                  <span className="text-sm font-bold">CONNECTION ALLOWED</span>
                </div>
                <button 
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-bold transition"
                  onClick={() => window.open(result.url, '_blank')}
                >
                  Proceed to Site
                </button>
              </div>
            )}
          </div>

          <div className="text-[11px] font-mono text-slate-500 pt-4 mt-2 flex items-center justify-between border-t border-slate-800">
            <span>Model: {result.model_name} (v{result.model_version})</span>
            <span>Note: Probabilistic classification. Always verify sender identity.</span>
          </div>
        </div>
      )}
    </div>
  );
};
