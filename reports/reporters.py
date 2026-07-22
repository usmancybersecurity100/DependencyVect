import json
import csv
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from scanner.models import ScanResult
from config.settings import OUTPUT_DIR

class ReportGenerator:
    def __init__(self, result: ScanResult):
        self.result = result
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_filename = f"VectReport_{self.timestamp}"

    def generate_all(self):
        self.to_json()
        self.to_csv()
        self.to_html()
        self.to_pdf()

    def to_json(self):
        path = OUTPUT_DIR / f"{self.base_filename}.json"
        
        # Serialize dataclasses manually for clean output
        data = {
            "target": self.result.target_file,
            "ecosystem": self.result.ecosystem,
            "risk_level": self.result.risk_level,
            "risk_score": self.result.risk_score,
            "metrics": {
                "total": self.result.total_dependencies,
                "vulnerable": self.result.vulnerable_dependencies,
                "critical": self.result.critical_count
            },
            "findings": []
        }
        
        for dep in self.result.dependencies:
            if dep.is_vulnerable:
                dep_data = {"package": dep.name, "version": dep.version, "cves": []}
                for v in dep.vulnerabilities:
                    dep_data["cves"].append({"id": v.cve_id, "severity": v.severity, "score": v.cvss_score})
                data["findings"].append(dep_data)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return path

    def to_csv(self):
        path = OUTPUT_DIR / f"{self.base_filename}.csv"
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Package Name", "Version", "CVE ID", "Severity", "CVSS Score"])
            for dep in self.result.dependencies:
                if dep.is_vulnerable:
                    for v in dep.vulnerabilities:
                        writer.writerow([dep.name, dep.version, v.cve_id, v.severity, v.cvss_score])
        return path

    def to_html(self):
        path = OUTPUT_DIR / f"{self.base_filename}.html"
        html_content = f"""
        <html>
        <head>
            <title>DependencyVect Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1, h2 {{ color: #2C3E50; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #2C3E50; color: white; }}
                .risk {{ font-weight: bold; padding: 10px; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px; width: 250px;}}
            </style>
        </head>
        <body>
            <h1>DependencyVect Security Audit</h1>
            <div class="risk">Risk Score: {self.result.risk_score} | Level: {self.result.risk_level}</div>
            <p>Target: {self.result.target_file} ({self.result.ecosystem})</p>
            <p>Vulnerable Packages: {self.result.vulnerable_dependencies} / {self.result.total_dependencies}</p>
            <h2>Vulnerability Details</h2>
            <table>
                <tr><th>Package</th><th>Version</th><th>CVE</th><th>Severity</th></tr>
        """
        for dep in self.result.dependencies:
            for v in dep.vulnerabilities:
                html_content += f"<tr><td>{dep.name}</td><td>{dep.version}</td><td>{v.cve_id}</td><td>{v.severity}</td></tr>"
        
        html_content += "</table></body></html>"
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return path

    def to_pdf(self):
        path = OUTPUT_DIR / f"{self.base_filename}.pdf"
        doc = SimpleDocTemplate(str(path), pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        elements.append(Paragraph("DependencyVect Security Audit Report", styles['Title']))
        elements.append(Spacer(1, 12))

        # Executive Summary
        elements.append(Paragraph("Executive Summary", styles['Heading2']))
        summary = f"Scanned {self.result.target_file}. Found {self.result.vulnerable_dependencies} vulnerable packages out of {self.result.total_dependencies} total dependencies. Overall Risk Score: {self.result.risk_score} ({self.result.risk_level})."
        elements.append(Paragraph(summary, styles['Normal']))
        elements.append(Spacer(1, 12))

        # Table Data
        data = [["Package", "Version", "CVE ID", "Severity"]]
        for dep in self.result.dependencies:
            for v in dep.vulnerabilities:
                data.append([dep.name, dep.version, v.cve_id, v.severity])

        if len(data) > 1:
            table = Table(data, colWidths=[120, 80, 150, 80])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
        else:
            elements.append(Paragraph("No vulnerabilities detected.", styles['Normal']))

        doc.build(elements)
        return path
