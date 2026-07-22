import requests
import time
from typing import List, Dict, Any
from config.settings import OSV_API_URL, API_TIMEOUT, MAX_RETRIES
from utils.logger import setup_logger

logger = setup_logger(__name__)

class OSVClient:
    def __init__(self):
        self.url = OSV_API_URL
        self.session = requests.Session()

    def query_package(self, name: str, version: str, ecosystem: str) -> List[Dict[str, Any]]:
        payload = {
            "version": version,
            "package": {
                "name": name,
                "ecosystem": ecosystem
            }
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.post(self.url, json=payload, timeout=API_TIMEOUT)
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("vulns", [])
                elif response.status_code == 429:
                    logger.warning(f"Rate limited by OSV API. Retrying in {attempt + 1} seconds...")
                    time.sleep(attempt + 1)
                    continue
                else:
                    logger.error(f"OSV API error {response.status_code} for package {name}")
                    return []
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error querying OSV API for {name}: {str(e)}")
                if attempt == MAX_RETRIES - 1:
                    return []
                time.sleep(1)
        return []

    def extract_vulnerability_data(self, vuln_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts and normalizes data from the complex OSV JSON response."""
        cve_id = vuln_data.get("id", "UNKNOWN")
        if "aliases" in vuln_data and vuln_data["aliases"]:
            cve_id = vuln_data["aliases"][0] # Prefer CVE format if available

        summary = vuln_data.get("summary", vuln_data.get("details", "No summary provided."))[:150] + "..."
        
        # Determine Severity and CVSS
        severity = "UNKNOWN"
        cvss_score = 0.0
        if "severity" in vuln_data:
            for sev in vuln_data["severity"]:
                if sev["type"] == "CVSS_V3":
                    # Simple CVSS parser (extracts score from vector string if needed, or defaults)
                    # OSV usually provides the score directly in some formats, but we assume default high if flagged
                    severity = "HIGH" 
                    cvss_score = 7.5

        # In a real-world scenario, parsing the exact CVSS vector from OSV is required. 
        # For simplicity, if OSV flags it without a score, we map it as High severity.
        
        return {
            "cve_id": cve_id,
            "summary": summary.replace("\n", " "),
            "severity": severity,
            "cvss_score": cvss_score,
            "affected_versions": [], # Simplified for this version
            "fixed_version": "Check OSV", 
            "reference_urls": [ref.get("url") for ref in vuln_data.get("references", [])]
        }
