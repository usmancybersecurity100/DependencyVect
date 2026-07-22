import json
import re
from pathlib import Path
from typing import List, Tuple
from utils.logger import setup_logger

logger = setup_logger(__name__)

class DependencyParser:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def validate_file(self) -> bool:
        if not self.file_path.exists() or not self.file_path.is_file():
            logger.error(f"File not found or invalid: {self.file_path}")
            return False
        return True

    def parse(self) -> Tuple[str, List[Tuple[str, str]]]:
        """Returns ecosystem and a list of (package_name, version) tuples."""
        if not self.validate_file():
            raise FileNotFoundError(f"Cannot process {self.file_path}")

        file_name = self.file_path.name
        if file_name == "requirements.txt":
            return "PyPI", self._parse_requirements_txt()
        elif file_name == "package.json":
            return "npm", self._parse_package_json()
        else:
            raise ValueError(f"Unsupported file format: {file_name}")

    def _parse_requirements_txt(self) -> List[Tuple[str, str]]:
        dependencies = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    # Split by common version specifiers
                    match = re.split(r'==|>=|<=|~=|<|>', line)
                    if len(match) >= 2:
                        name, version = match[0].strip(), match[1].strip()
                        dependencies.append((name, version))
                    else:
                        logger.warning(f"Could not parse version for: {line}")
            return dependencies
        except Exception as e:
            logger.error(f"Error parsing requirements.txt: {str(e)}")
            raise

    def _parse_package_json(self) -> List[Tuple[str, str]]:
        dependencies = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            deps = data.get("dependencies", {})
            dev_deps = data.get("devDependencies", {})
            all_deps = {**deps, **dev_deps}

            for name, version in all_deps.items():
                # Clean semantic versioning characters for OSV accuracy
                clean_version = re.sub(r'[\^\~]', '', version).strip()
                dependencies.append((name, clean_version))
            
            return dependencies
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in package.json: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error parsing package.json: {str(e)}")
            raise
