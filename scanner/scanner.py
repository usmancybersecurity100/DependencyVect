from scanner.parser import DependencyParser
from scanner.osv_client import OSVClient
from scanner.models import Dependency, Vulnerability, ScanResult
from scanner.risk_engine import RiskEngine
from utils.logger import setup_logger
from rich.progress import Progress

logger = setup_logger(__name__)

class DependencyScanner:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.parser = DependencyParser(file_path)
        self.client = OSVClient()

    def run_scan(self, progress: Progress, task_id) -> ScanResult:
        logger.info(f"Starting scan for {self.file_path}")
        
        # 1. Parse
        ecosystem, raw_deps = self.parser.parse()
        
        result = ScanResult(
            target_file=self.file_path,
            ecosystem=ecosystem,
            total_dependencies=len(raw_deps)
        )

        # 2. Query API & Build Models
        progress.update(task_id, total=len(raw_deps))
        
        for name, version in raw_deps:
            dep = Dependency(name=name, version=version, ecosystem=ecosystem)
            
            # Query OSV
            vulns_data = self.client.query_package(name, version, ecosystem)
            
            for v_data in vulns_data:
                extracted = self.client.extract_vulnerability_data(v_data)
                vuln = Vulnerability(
                    cve_id=extracted["cve_id"],
                    summary=extracted["summary"],
                    severity=extracted["severity"],
                    cvss_score=extracted["cvss_score"],
                    affected_versions=extracted["affected_versions"],
                    fixed_version=extracted["fixed_version"],
                    reference_urls=extracted["reference_urls"]
                )
                dep.vulnerabilities.append(vuln)
            
            if dep.is_vulnerable:
                result.vulnerable_dependencies += 1
                
            result.dependencies.append(dep)
            progress.advance(task_id)

        # 3. Calculate Risk
        result = RiskEngine.calculate_risk(result)
        logger.info(f"Scan complete. Found {result.vulnerable_dependencies} vulnerable packages.")
        
        return result
