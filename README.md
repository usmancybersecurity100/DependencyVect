# DependencyVect 🛡️

**Software Supply Chain CVE Auditor**

DependencyVect is a powerful DevSecOps Command Line Interface (CLI) tool designed to secure your software supply chain. It actively scans software dependency manifests (such as `requirements.txt` for Python and `package.json` for NodeJS) and cross-references them against the official [OSV.dev](https://osv.dev) (Open Source Vulnerabilities) database. By doing so, it detects known CVEs (Common Vulnerabilities and Exposures) prior to deployment, ensuring your applications remain secure.

## 🌟 Core Features

* **Fast & Accurate Scanning:** Efficiently parses multiple dependency manifest formats.
* **Real-time OSV API Integration:** Leverages the official Google OSV database for the latest vulnerability data.
* **Risk Scoring Engine:** Calculates a comprehensive 0-100 risk score based on CVSS mappings.
* **Rich CLI UI:** Provides an interactive terminal dashboard complete with progress bars and colorized output tables.
* **Automated Reporting:** Generates detailed audit reports instantly in PDF, HTML, CSV, and JSON formats.

---

## 📁 Project Structure

* `config/` - Contains configuration files for scanner settings and API limits.
* `reports/` - The destination folder where all generated vulnerability reports are saved.
* `samples/` - Includes sample `requirements.txt` and `package.json` files for testing.
* `scanner/` - The core engine responsible for parsing manifests and querying the OSV database.
* `utils/` - Helper scripts, UI formatters, and secondary functions.
* `main.py` - The primary entry point for executing the DependencyVect tool.

---

## 🛠️ Prerequisites & Installation

**1. Clone the repository:**
```bash
git clone https://github.com/usmancybersecurity100/DependencyVect.git
```

**2. Navigate into the project directory:**
```bash
cd DependencyVect
```

**3. Install the required dependencies:**
*(Ensure you have Python 3.11+ installed)*
```bash
pip install -r requirements.txt
```

---

## 🚀 Comprehensive Usage Guide

DependencyVect is highly customizable through various command-line flags. Below is the complete guide on how to operate the tool effectively.

### ⚙️ Command-Line Arguments (Flags)

| Short Flag | Long Flag | Description | Required? |
| :--- | :--- | :--- | :--- |
| `-f` | `--file` | Path to the dependency file you want to scan. | **Yes** |
| `-o` | `--output` | Format of the report to generate (`pdf`, `html`, `json`, `csv`). | No |
| `-v` | `--verbose` | Enable verbose output for detailed scanning logs. | No |
| `-h` | `--help` | Display the help menu with all available commands. | No |

### 📖 Practical Examples

**1. Standard Terminal Scan:**
The most basic command. It scans your Python dependencies and prints the vulnerabilities in a colorized table directly in your terminal.
```bash
python main.py -f requirements.txt
```

**2. Scan a NodeJS Project:**
You can easily switch the target file to scan Node dependencies.
```bash
python main.py -f package.json
```

**3. Generate an Audit Report (PDF / HTML):**
If you need to send the results to your management or save them for compliance, use the output flag. The generated file will be saved in the `reports/` directory.
```bash
python main.py -f requirements.txt --output pdf
```
*To generate an HTML report instead:*
```bash
python main.py -f requirements.txt --output html
```

**4. Run with Verbose Logging (Debugging):**
If you want to see exactly what the tool is doing in the background (API calls, parsing steps), turn on verbose mode.
```bash
python main.py -f requirements.txt -v
```

**5. Need Help?**
If you ever forget a command, just pull up the help menu:
```bash
python main.py --help
```

---

## 🔒 Security & Compliance
DependencyVect is designed for educational and defensive purposes to assist developers and security researchers in identifying vulnerabilities within their own software pipelines. Always ensure you have authorization before scanning third-party environments.

