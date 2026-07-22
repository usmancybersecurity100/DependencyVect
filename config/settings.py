import logging
from pathlib import Path

# ==========================================
# PATH CONFIGURATIONS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

# Ensure output and log directories exist
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# ==========================================
# API CONFIGURATIONS
# ==========================================
OSV_API_URL = "https://api.osv.dev/v1/query"
API_TIMEOUT = 10  # Seconds before timing out
MAX_RETRIES = 3

# ==========================================
# LOGGING CONFIGURATIONS
# ==========================================
LOG_FILE = LOG_DIR / "dependencyvect.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO

# ==========================================
# RISK ENGINE THRESHOLDS
# ==========================================
# CVSS Score thresholds
SEVERITY_CRITICAL = 9.0
SEVERITY_HIGH = 7.0
SEVERITY_MEDIUM = 4.0
SEVERITY_LOW = 0.1

# ==========================================
# SUPPORTED ECOSYSTEMS
# ==========================================
# Maps file names to OSV ecosystem identifiers
SUPPORTED_FILES = {
    "requirements.txt": "PyPI",
    "package.json": "npm"
}
