import yaml
from typing import Dict

import yaml
from typing import Dict

def load_config(path: str) -> Dict:
    """
    Load YAML config from loacal file system.
    (Used by local test + CI)
    """
    with open(path, "r") as f:
        return yaml.safe_load(f)
