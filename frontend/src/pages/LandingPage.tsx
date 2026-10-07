import React from 'react';
import { Link } from 'react-router-dom';
import {
  ShieldAlert,
  Lock,
  Cpu,
  Wifi,
  Eye,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  Fingerprint,
  FileText,
  UserCheck,
  Activity
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#0b0f19] text-slate-100 font-sans selection:bg-blue-600 selection:text-white">
      {/* Top Header */}
      <header className="border-b border-slate-800/80 bg-[#0d1322]/80 backdrop-blur sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-600/20 text-blue-400 rounded-lg border border-blue-500/30">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <span className="font-bold text-base tracking-wide uppercase text-white">Cyber Defence System</span>
            <span className="text-[10px] block text-slate-400 font-mono">FOR REMOTE PROFESSIONALS</span>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <Link
            to="/login"
            className="text-xs font-semibold px-4 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition"
          >
            Sign In
          </Link>
          <Link
            to="/register"
            className="text-xs font-semibold px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white shadow-sm transition"
          >
            Deploy Defence
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-6 pt-20 pb-16 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-950/60 border border-blue-800/50 text-blue-400 text-xs font-medium mb-6">
          <span className="w-2 h-2 rounded-full bg-blue-400 animate-ping" />
          <span>Continuous Cyber-Risk Intelligence for Gig Workers & Freelancers</span>
        </div>
        <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight">
          Enterprise-Grade Threat Assessment for{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-300 to-cyan-400">
            Zero-Trust Remote Work
          </span>
        </h1>
        <p className="mt-6 text-base md:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
          Remote employees, contractors, and freelancers use personal PCs, home networks, and public Wi-Fi without
          corporate security firewalls. Our AI calculates a deterministic, explainable Cyber Risk Index (0–100) with prioritized remediation.
        </p>

        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            to="/register"
            className="w-full sm:w-auto flex items-center justify-center gap-2 px-6 py-3.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold shadow-lg shadow-blue-900/30 transition"
          >
            <span>Start Free Security Evaluation</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            to="/login"
            className="w-full sm:w-auto flex items-center justify-center gap-2 px-6 py-3.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-200 text-sm font-semibold border border-slate-700/60 transition"
          >
            <span>Explore Demo Scenarios</span>
          </Link>
        </div>
      </section>

      {/* What the System Protects */}
      <section className="max-w-6xl mx-auto px-6 py-16 border-t border-slate-800/80">
        <div className="text-center mb-12">
          <h2 className="text-2xl font-bold text-white">Comprehensive 5-Layer Threat Shield</h2>
          <p className="text-sm text-slate-400 mt-2">Continuous evaluation calibrated across NIST CSF core domains</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
          <div className="p-5 rounded-xl bg-[#0e1628] border border-slate-800/80 hover:border-blue-500/50 transition">
            <Cpu className="w-6 h-6 text-blue-400 mb-3" />
            <h3 className="text-sm font-bold text-white">Device Security</h3>
            <p className="text-xs text-slate-400 mt-1">Host firewall, OS patch currency, EDR presence, and storage encryption.</p>
          </div>
          <div className="p-5 rounded-xl bg-[#0e1628] border border-slate-800/80 hover:border-cyan-500/50 transition">
            <Wifi className="w-6 h-6 text-cyan-400 mb-3" />
            <h3 className="text-sm font-bold text-white">Network Security</h3>
            <p className="text-xs text-slate-400 mt-1">Local Wi-Fi encryption (WPA2/3), cleartext DNS leakage, and exposed services.</p>
          </div>
          <div className="p-5 rounded-xl bg-[#0e1628] border border-slate-800/80 hover:border-indigo-500/50 transition">
            <Lock className="w-6 h-6 text-indigo-400 mb-3" />
            <h3 className="text-sm font-bold text-white">Credential Shield</h3>
            <p className="text-xs text-slate-400 mt-1">Dark web breach exposure detection, credential stuffing defense & MFA auditing.</p>
          </div>
          <div className="p-5 rounded-xl bg-[#0e1628] border border-slate-800/80 hover:border-amber-500/50 transition">
            <Eye className="w-6 h-6 text-amber-400 mb-3" />
            <h3 className="text-sm font-bold text-white">Phishing AI</h3>
            <p className="text-xs text-slate-400 mt-1">Supervised machine learning analysis of suspicious hyperlinks and fake login traps.</p>
          </div>
          <div className="p-5 rounded-xl bg-[#0e1628] border border-slate-800/80 hover:border-emerald-500/50 transition">
            <Activity className="w-6 h-6 text-emerald-400 mb-3" />
            <h3 className="text-sm font-bold text-white">Behaviour Anomaly</h3>
            <p className="text-xs text-slate-400 mt-1">Isolation Forest behavioral detection of unusual login hours and network shifts.</p>
          </div>
        </div>
      </section>

      {/* Cyber Risk Index Formula Explanation */}
      <section className="max-w-6xl mx-auto px-6 py-16 border-t border-slate-800/80 bg-[#0d1424]/40 rounded-2xl my-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <div>
            <h2 className="text-2xl font-bold text-white">Deterministic & Explainable Scoring</h2>
            <p className="text-sm text-slate-400 mt-3 leading-relaxed">
              Unlike opaque black-box systems, the Cyber Risk Index uses an auditable, NIST CSF-aligned weighted mathematical formulation. 
              You always know exactly why your score changed.
            </p>
            <div className="mt-6 space-y-2 font-mono text-xs text-slate-300">
              <div className="p-2.5 bg-[#0a0e18] rounded border border-slate-800">
                Risk Index = (Device × 25%) + (Network × 20%) + (Credential × 20%) + (Phishing × 20%) + (Behaviour × 15%)
              </div>
            </div>
            <div className="mt-4 flex gap-3 text-xs">
              <span className="px-2.5 py-1 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800/40">0–24: LOW</span>
              <span className="px-2.5 py-1 rounded bg-blue-950/60 text-blue-400 border border-blue-800/40">25–49: MODERATE</span>
              <span className="px-2.5 py-1 rounded bg-amber-950/60 text-amber-400 border border-amber-800/40">50–74: HIGH</span>
              <span className="px-2.5 py-1 rounded bg-red-950/60 text-red-400 border border-red-800/40">75–100: CRITICAL</span>
            </div>
          </div>
          <div className="bg-[#0b0f1a] p-6 rounded-xl border border-slate-800 space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">Strict Privacy Principles</h4>
            <div className="flex items-start gap-3">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <p className="text-xs text-slate-300">Never collects or asks for account passwords or private keys.</p>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <p className="text-xs text-slate-300">Zero packet interception or private file scanning on host drives.</p>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <p className="text-xs text-slate-300">Safe, non-invasive local telemetry only with explicit user consent.</p>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <p className="text-xs text-slate-300">Strict defensive posture: zero exploit or port-scanning payloads.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-8 text-center text-xs text-slate-500">
        <p>Cyber Defence System for Remote Professionals — Academic Project & Production Architecture Prototype.</p>
      </footer>
    </div>
  );
};
