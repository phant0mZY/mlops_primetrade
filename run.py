import argparse
import yaml
import numpy as np
import pandas as pd
import os
import sys
import time
import logging
import json

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# CLI_args
parser = argparse.ArgumentParser()
parser.add_argument("--config", required=True)
parser.add_argument("--input", required=True)
parser.add_argument("--log-file", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()

start_time = time.perf_counter()

# Logging
logging.basicConfig(
    filename=args.log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

config_version = "v1"

try:
    logger.info("Job started")

  
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)
    
    seed = config.get("seed")
    window = config.get("window")
    config_version = config.get("version", "v1")
    
    if seed is None or window is None:
        raise ValueError("Missing seed or window in config")

    np.random.seed(seed)
    logger.info(f"Config loaded: seed={seed}, window={window}, version={config_version}")


    if not os.path.exists(args.input):
        raise FileNotFoundError(f"File not found: {args.input}")
    
    df = pd.read_csv(args.input)
    if df.empty: raise ValueError("CSV is empty")
    if "close" not in df.columns: raise ValueError("Missing 'close' column")
    
    logger.info(f"Data loaded: {len(df)} rows")

    #Rolling_Mean 
    df["rolling_mean"] = df["close"].rolling(window=window, min_periods=1).mean()
    logger.info(f"Rolling mean calculated with window={window}")

    df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
    logger.info("Signals generated")

   
    rows_processed = len(df)
    signal_rate = float(df["signal"].mean())
    latency_ms = int((time.perf_counter() - start_time) * 1000)

    output_json = {
        "version": config_version,
        "rows_processed": rows_processed,
        "metric": "signal_rate",
        "value": round(signal_rate, 4),
        "latency_ms": latency_ms,
        "seed": seed,
        "status": "success"
    }

    save_json(args.output, output_json)
    
    
    print(json.dumps(output_json, indent=4))
    
    logger.info(f"Metrics: signal_rate={round(signal_rate,4)}, rows_processed={rows_processed}")
    logger.info(f"Job completed successfully in {latency_ms}ms")
    sys.exit(0)

except Exception as e:
    err_msg = str(e)
    error_json = {"version": config_version, "status": "error", "error_message": err_msg}
    
    logger.error(err_msg)
    if 'args' in locals():
        save_json(args.output, error_json)
    
    print(json.dumps(error_json, indent=4))
    sys.exit(1)