import math
import re
from urllib.parse import urlparse
from typing import Dict, Any, List

def calculate_entropy(text: str) -> float:
    if not text:
        return 0.0
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    entropy = 0.0
    total = len(text)
    for count in freq.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

class URLFeatureExtractor:
    """
    Extracts lexical, structural, and behavioral features from a URL for phishing classification.
    Produces both numeric vector for scikit-learn ML models and explainable indicator flags.
    """
    FEATURE_NAMES = [
        "url_length",
        "hostname_length",
        "path_length",
        "query_length",
        "num_dots",
        "num_subdomains",
        "num_hyphens",
        "num_digits",
        "num_special_chars",
        "has_ip_address",
        "has_at_symbol",
        "is_https",
        "has_suspicious_token",
        "is_shortened",
        "digit_ratio",
        "entropy"
    ]

    SUSPICIOUS_TOKENS = [
        "login", "verify", "secure", "account", "banking", "update", "confirm",
        "password", "wallet", "support", "service", "signin", "authenticate", "paypal",
        "appleid", "recovery", "security", "bill", "invoice", "ebay", "netflix", "microsoft"
    ]

    SHORTENERS = [
        "bit.ly", "tinyurl.com", "goo.gl", "t.co", "is.gd", "buff.ly", "ow.ly",
        "rb.gy", "cutt.ly", "shorturl.at"
    ]

    def extract_features(self, url: str) -> Dict[str, Any]:
        url = url.strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            parsed_url = urlparse("http://" + url)
            full_url = "http://" + url
        else:
            parsed_url = urlparse(url)
            full_url = url

        hostname = parsed_url.netloc or ""
        path = parsed_url.path or ""
        query = parsed_url.query or ""

        # Remove port if present in hostname
        if ":" in hostname:
            hostname = hostname.split(":")[0]

        # 1. URL length
        url_length = len(full_url)
        # 2. Hostname length
        hostname_length = len(hostname)
        # 3. Path length
        path_length = len(path)
        # 4. Query length
        query_length = len(query)

        # 5. Number of dots
        num_dots = full_url.count(".")
        # 6. Number of subdomains
        host_parts = hostname.split(".")
        num_subdomains = max(0, len(host_parts) - 2) if len(host_parts) > 1 else 0

        # 7. Number of hyphens
        num_hyphens = full_url.count("-")

        # 8. Number of digits
        num_digits = sum(c.isdigit() for c in full_url)

        # 9. Number of special characters
        special_chars = ["-", "_", "?", "=", "&", "%", "@", "!", "$", "*", "+", ";", "~"]
        num_special_chars = sum(full_url.count(c) for c in special_chars)

        # 10. Presence of IP address
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        has_ip_address = 1 if re.match(ip_pattern, hostname) else 0

        # 11. Has '@' symbol (often used to obscure destination)
        has_at_symbol = 1 if "@" in full_url else 0

        # 12. HTTPS usage
        is_https = 1 if parsed_url.scheme.lower() == "https" else 0

        # 13. Suspicious tokens
        has_suspicious_token = 1 if any(token in full_url.lower() for token in self.SUSPICIOUS_TOKENS) else 0

        # 14. Shortener service
        is_shortened = 1 if any(s in hostname.lower() for s in self.SHORTENERS) else 0

        # 15. Digit ratio
        digit_ratio = (num_digits / url_length) if url_length > 0 else 0.0

        # 16. Shannon Entropy
        entropy = calculate_entropy(full_url)

        feature_dict = {
            "url_length": float(url_length),
            "hostname_length": float(hostname_length),
            "path_length": float(path_length),
            "query_length": float(query_length),
            "num_dots": float(num_dots),
            "num_subdomains": float(num_subdomains),
            "num_hyphens": float(num_hyphens),
            "num_digits": float(num_digits),
            "num_special_chars": float(num_special_chars),
            "has_ip_address": float(has_ip_address),
            "has_at_symbol": float(has_at_symbol),
            "is_https": float(is_https),
            "has_suspicious_token": float(has_suspicious_token),
            "is_shortened": float(is_shortened),
            "digit_ratio": float(digit_ratio),
            "entropy": float(entropy)
        }

        # Human-readable detected indicators for explainability
        indicators: List[Dict[str, Any]] = []
        if has_ip_address:
            indicators.append({
                "name": "Raw IP Hostname",
                "description": "The destination URL uses a numeric IP address instead of a registered domain name.",
                "severity": "CRITICAL"
            })
        if is_shortened:
            indicators.append({
                "name": "URL Shortener Masking",
                "description": "URL leverages link shortening which masks the ultimate landing domain.",
                "severity": "HIGH"
            })
        if has_at_symbol:
            indicators.append({
                "name": "Embedded Credentials/Redirect Syntax (@)",
                "description": "The URL contains an '@' character, frequently used to disguise credential theft destinations.",
                "severity": "CRITICAL"
            })
        if num_subdomains >= 3:
            indicators.append({
                "name": "Excessive Subdomains",
                "description": f"URL contains {num_subdomains} subdomains designed to mimic legitimate domain hierarchies.",
                "severity": "HIGH"
            })
        if url_length > 75:
            indicators.append({
                "name": "Abnormally Long URL Structure",
                "description": f"Length of {url_length} characters is unusually high, often used for token injection or obfuscation.",
                "severity": "MEDIUM"
            })
        if not is_https:
            indicators.append({
                "name": "Insecure Cleartext Transport (HTTP)",
                "description": "Traffic is not encrypted with TLS/SSL certificate.",
                "severity": "MEDIUM"
            })
        if has_suspicious_token and (num_hyphens > 2 or num_subdomains > 1):
            indicators.append({
                "name": "Targeted Brand Impersonation Keyword",
                "description": "Contains high-value target keywords (login, auth, secure, banking) alongside complex subdomain structure.",
                "severity": "HIGH"
            })

        return {
            "features": feature_dict,
            "vector": [feature_dict[name] for name in self.FEATURE_NAMES],
            "indicators": indicators
        }

url_extractor = URLFeatureExtractor()
