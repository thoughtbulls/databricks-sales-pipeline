import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--env", required=True)
args = parser.parse_args()

cfg = yaml.safe_load(open("configs/{args.env}.yaml"))
# cfg = yaml.safe_load(open("configs/dev.yaml"))
tpl = open("workflows/job.json.tpl").read()

tpl = tpl.replace("{{ENV}}", cfg["env"])
tpl = tpl.replace("{{JOB_NAME}}", cfg["job"]["name"])
tpl = tpl.replace("{{SPARK_VERSION}}", cfg["cluster"]["spark_version"])
tpl = tpl.replace("{{NODE_TYPE_ID}}", cfg["cluster"]["node_type_id"])
tpl = tpl.replace("{{NUM_WORKERS}}", str(cfg["cluster"]["num_workers"]))

open("workflows/job.json", "w").write(tpl)