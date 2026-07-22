# DependencyVect 🛡️
**Software Supply Chain CVE Auditor**

DependencyVect is a powerful DevSecOps CLI tool designed to scan software dependency manifests (`requirements.txt`, `package.json`) and cross-reference them against the official [OSV.dev](https://osv.dev/) vulnerability database to detect known CVEs prior to deployment.

## Features
- **Fast & Accurate Scanning:** Parses Python and NodeJS manifests.
- **OSV API Integration:** Leverages the official Google OSV database.
- **Risk Scoring Engine:** Calculates 0-100 risk score based on CVSS mappings.
- **Rich CLI UI:** Interactive terminal dashboard with progress bars and colorized tables.
- **Automated Reporting:** Generates PDF, HTML, CSV, and JSON audit reports instantly.

## Installation
1. Clone the repository.
2. Ensure you have Python 3.11+ installed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
