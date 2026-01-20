import yaml
from typing import Dict

BASE_PATH = "dbfs:/pipelines/databricks-sales-pipeline/configs"

def load_config(env: str) -> Dict:
    path = f"{BASE_PATH}/{env}.yaml"

    raw = dbutils.fs.head(path)
    return yaml.safe_load(raw)
