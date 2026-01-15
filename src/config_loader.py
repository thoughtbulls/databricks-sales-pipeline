import yaml
from typing import Dict

BASE_PATH = "/Workspace/Shared/databricks-sales-pipeline"

def load_config(env: str) -> Dict:
    config_path = f"{BASE_PATH}/configs/{env}.yaml"

    with open(config_path, "r") as f:
        return yaml.safe_load(f)
