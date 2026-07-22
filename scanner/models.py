from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Vulnerability:
    cve_id: str
    summary: str
    severity: str
    cvss_score: float
    affected_versions: List[str]
    fixed_version: Optional[str]
    reference_urls: List[str]

@dataclass
class Dependency:
    name: str
    version: str
    ecosystem: str
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    
    @property
    def is_vulnerable(self) -> bool:
        return len(self.vulnerabilities) > 0

@dataclass
class ScanResult:
    target_file: str
    ecosystem: str
    total_dependencies: int = 0
    vulnerable_dependencies: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    risk_score: float = 0.0
    risk_level: str = "Low"
    dependencies: List[Dependency] = field(default_factory=list)
