{
  "name": "sales_pipeline_${ENV}",
  "tasks": [
    {
      "task_key": "bronze",
      "spark_python_task": {
        "python_file": "/Shared/databricks-sales-pipeline/notebooks/01_bronze_ingestion.py",
        "parameters": ["--env", "${ENV}"]
      },

      "job_cluster_key": "sales_cluster",
      "libraries": [
          { "pypi": { "package": "pyyaml" } }
        ]
    },
    {
      "task_key": "silver",
      "depends_on": [{ "task_key": "bronze" }],
      "spark_python_task": {
        "python_file": "/Workspace/Shared/databricks-sales-pipeline/notebooks/02_silver_transformation.py",
        "parameters": ["--env", "${ENV}"]
      },

      "job_cluster_key": "sales_cluster",
      "libraries": [
        { "pypi": { "package": "pyyaml" } }
      ]
    },
    {
      "task_key": "gold",
      "depends_on": [{ "task_key": "silver" }],
      "spark_python_task": {
        "python_file": "/Workspace/Shared/databricks-sales-pipeline/notebooks/03_gold_aggregation.py",
        "parameters": ["--env", "${ENV}"]
      },

      "job_cluster_key": "sales_cluster",
      "libraries": [
        { "pypi": { "package": "pyyaml" } }
      ]
    }
  ],
  "job_clusters": [
    {
      "job_cluster_key": "sales_cluster",
      "new_cluster": {
        "spark_version": "13.3.x-scala2.12",
        "node_type_id": "m4.large",
        "num_workers": 1,

        "libraries": [
          { "pypi": { "package": "pyyaml" } }
        ], 

        "data_security_mode": "SINGLE_USER",
        "runtime_engine": "STANDARD",

        "aws_attributes": {
          "ebs_volume_type": "GENERAL_PURPOSE_SSD",
          "ebs_volume_count": 1,
          "ebs_volume_size": 50
        }
      }
    }
  ]
}
