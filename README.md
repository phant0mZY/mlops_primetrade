

MLOps Technical Assessment

This repository contains a containerized batch processing pipeline for generating trading signals from OHLCV data. The system is designed for reproducibility and structured observability.

Setup Instructions
To set up the environment locally, use the following command:

Install dependencies:

pip install -r requirements.txt
Local Execution Instructions
The script requires specific CLI arguments for input, configuration, and output paths:

Run locally:

python run.py --input data.csv --config config.yaml \
    --output metrics.json --log-file run.log

Docker Instructions:
The application is fully containerized to ensure environment consistency:


 Build the Docker image:
docker build -t mlops-task .

 Run the container:
docker run --rm mlops-task

Expected Output:
The application generates a machine-readable JSON file at the specified output path. The structure is as follows:

(JSON)
{
    "version": "v1",
    "rows_processed": 10000,
    "metric": "signal_rate",
    "value": 0.5037,
    "latency_ms": 28,
    "seed": 42,
    "status": "success"
}


Dependencies:

The pipeline relies on the following Python packages:

pandas

numpy

pyyaml

