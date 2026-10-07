from typing import List, Dict, Any

class RecommendationEngine:
    """
    Synthesizes findings from Device, Network, Credential, Phishing, and Behavioural layers
    into prioritized, actionable, human-readable remediation steps.
    Calculates estimated risk reduction percentages.
    """
    def generate_recommendations(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        recommendations = []
        seen_titles = set()

        # Severity sorting weight
        severity_rank = {
            "CRITICAL": 1,
            "HIGH": 2,
            "MEDIUM": 3,
            "LOW": 4
        }

        # Sort input findings by severity priority first
        sorted_findings = sorted(findings, key=lambda f: severity_rank.get(f.get("severity", "LOW"), 5))

        for finding in sorted_findings:
            title = finding.get("title", "")
            if title in seen_titles:
                continue
            seen_titles.add(title)

            sev = finding.get("severity", "LOW")
            cat = finding.get("category", "General Security")
            rec_action = finding.get("recommendation", "Review and remediate identified configuration.")
            evidence = finding.get("evidence", "")

            # Estimate reduction based on severity
            reduction = 15.0 if sev == "CRITICAL" else (10.0 if sev == "HIGH" else (5.0 if sev == "MEDIUM" else 2.0))
            priority = severity_rank.get(sev, 4)

            why_it_matters = (
                f"Addresses identified {sev.lower()}-severity issue in {cat}. "
                f"Evidence observed: {evidence if evidence else 'Detected security telemetry anomaly'}."
            )

            recommendations.append({
                "title": f"Remediate: {title}",
                "category": cat,
                "severity": sev,
                "priority": priority,
                "why_it_matters": why_it_matters,
                "recommended_action": rec_action,
                "estimated_risk_reduction": reduction,
                "status": "OPEN",
                "is_demo": finding.get("is_demo", False)
            })

        # If zero negative findings exist, provide proactive hygiene recommendations
        if not recommendations:
            recommendations.append({
                "title": "Establish Regular Backup & Verification Schedule",
                "category": "Device Security",
                "severity": "LOW",
                "priority": 4,
                "why_it_matters": "Proactive protection against ransomware and drive hardware failure.",
                "recommended_action": "Configure encrypted 3-2-1 backup strategy for crucial client work files.",
                "estimated_risk_reduction": 3.0,
                "status": "OPEN",
                "is_demo": False
            })

        return recommendations

recommendation_engine = RecommendationEngine()
