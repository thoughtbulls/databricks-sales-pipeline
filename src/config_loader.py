import yaml
from typing import Dict

import yaml
from typing import Dict

def load_config_from_string(raw: str) -> Dict:
    return yaml.safe_load(raw)

