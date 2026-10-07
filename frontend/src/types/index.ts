export interface User {
  id: string;
  name: string;
  email: string;
  professional_type: string;
  mfa_enabled: boolean;
  telemetry_consent: boolean;
}

export interface Finding {
  id?: string;
  category: string;
  title: string;
  description: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  evidence?: string;
  confidence: number;
  score_impact: number;
  recommendation?: string;
  is_demo?: boolean;
}

export interface Recommendation {
  id: string;
  title: string;
  category: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  priority: number;
  why_it_matters: string;
  recommended_action: string;
  estimated_risk_reduction: number;
  status: "OPEN" | "IN PROGRESS" | "RESOLVED";
  is_demo: boolean;
  created_at: string;
  resolved_at?: string;
}

export interface SecurityAssessment {
  id: string;
  user_id: string;
  overall_score: number;
  risk_level: "LOW" | "MODERATE" | "HIGH" | "CRITICAL";
  category_scores: {
    device_security: number;
    network_security: number;
    credential_security: number;
    phishing_risk: number;
    behavioural_risk: number;
  };
  weighted_contributions: Record<string, number>;
  score_explanation: string;
  findings: Finding[];
  recommendations: Recommendation[];
  data_sources: string[];
  module_status: Record<string, string>;
  is_demo: boolean;
  created_at: string;
}

export interface DeviceScanData {
  device_name: string;
  os: string;
  os_version: string;
  patch_status: string;
  firewall_status: string;
  antivirus_status: string;
  disk_encryption_status: string;
  browser_extension_count: number;
  findings: Finding[];
  device_score: number;
}

export interface NetworkScanData {
  network_type: string;
  wifi_security: string;
  local_ip: string;
  dns_servers: string[];
  gateway: string;
  exposure_indicators: string[];
  findings: Finding[];
  network_score: number;
}

export interface PhishingResult {
  url: string;
  classification: "LEGITIMATE" | "PHISHING";
  phishing_probability: number;
  risk_score: number;
  confidence: number;
  indicators: Array<{ name: string; description: string; severity: string }>;
  model_name: string;
  model_version: string;
  prediction_timestamp: string;
}

export interface CredentialResult {
  email: string;
  status: "CLEAN" | "EXPOSED" | "UNAVAILABLE";
  breach_count: number;
  affected_services: string[];
  source: string;
  mfa_status: string;
  recommended_actions: string[];
  last_checked: string;
}

export interface BehaviourResult {
  status: "NORMAL" | "ANOMALOUS";
  anomaly_score: number;
  risk_contribution: number;
  explanation: string;
  indicators: string[];
  model_version: string;
}

export interface SecurityEventItem {
  id: string;
  event_type: string;
  category: string;
  severity: string;
  message: string;
  source: string;
  status: string;
  is_demo: boolean;
  timestamp: string;
}

export interface SystemStatusData {
  database: string;
  ml_model_overall: string;
  phishing_classifier: string;
  anomaly_detector: string;
  breach_api: string;
  device_collector: string;
  network_collector: string;
  platform_os: string;
  environment: string;
}
