from scanner.models import ScanResult
from config.settings import SEVERITY_CRITICAL, SEVERITY_HIGH, SEVERITY_MEDIUM

class RiskEngine:
    @staticmethod
    def calculate_risk(result: ScanResult) -> ScanResult:
        total = result.total_dependencies
        if total == 0:
            return result

        vuln_count = result.vulnerable_dependencies
        
        # Tally severities
        for dep in result.dependencies:
            for vuln in dep.vulnerabilities:
                score = vuln.cvss_score
                if score >= SEVERITY_CRITICAL:
                    result.critical_count += 1
                elif score >= SEVERITY_HIGH:
                    result.high_count += 1
                elif score >= SEVERITY_MEDIUM:
                    result.medium_count += 1
                else:
                    result.low_count += 1

        # Calculate weighted score (0-100 scale)
        weight = (result.critical_count * 10) + (result.high_count * 7) + (result.medium_count * 4) + (result.low_count * 1)
        raw_score = (weight / (total * 10)) * 100
        result.risk_score = min(round(raw_score, 2), 100.0)

        # Determine level
        if result.risk_score >= 70:
            result.risk_level = "CRITICAL"
        elif result.risk_score >= 40:
            result.risk_level = "HIGH"
        elif result.risk_score >= 15:
            result.risk_level = "MEDIUM"
        elif result.risk_score > 0:
            result.risk_level = "LOW"
        else:
            result.risk_level = "SECURE"

        return result
