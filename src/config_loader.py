import yaml
from typing import Dict

BASE_PATH = "/Volumes/dev_catalog/pipelines/configs"

def load_config(env: str) -> Dict:
    path = f"{BASE_PATH}/{env}.yaml"

    raw = dbutils.fs.head(path)
    return yaml.safe_load(raw)
