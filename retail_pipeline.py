import subprocess
import sys
from datetime import datetime
import os
import shutil

# ---------------- CONFIG ----------------
PROJECT_DIR = r"C:\Users\sneha\Desktop\Infotact Internship"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "Week2_RFM.py")

# Folder where Week2_RFM.py generates CSVs
SOURCE_OUTPUT_DIR = PROJECT_DIR

# Folder that Power BI reads from (FINAL SINGLE SOURCE)
FINAL_OUTPUT_DIR = os.path.join(PROJECT_DIR, "FINAL_OUTPUT")

# Expected output files
OUTPUT_FILES = [
    "rfm_customer_segments.csv",
    "association_rules_cleaned.csv"
]

# ---------------------------------------
def log(msg):
    print(f"[{datetime.now()}] {msg}")

# ---------------------------------------
def run_rfm_and_association():
    log("Starting RFM & Association Rule pipeline")

    result = subprocess.run(
        [sys.executable, SCRIPT_PATH],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )

    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception("Week2_RFM.py failed")

    log("RFM & Association Rule pipeline completed")

# ---------------------------------------
def move_outputs_to_final_folder():
    log("Syncing output files to FINAL_OUTPUT folder")

    # Create FINAL_OUTPUT folder if not exists
    os.makedirs(FINAL_OUTPUT_DIR, exist_ok=True)

    for file in OUTPUT_FILES:
        src = os.path.join(SOURCE_OUTPUT_DIR, file)
        dst = os.path.join(FINAL_OUTPUT_DIR, file)

        if not os.path.exists(src):
            raise FileNotFoundError(f"Missing output file: {file}")

        shutil.copy(src, dst)
        log(f"Updated file: {file}")

# ---------------------------------------
def main():
    try:
        log("ETL started")

        # Run analytics
        run_rfm_and_association()

        # Sync outputs for Power BI
        move_outputs_to_final_folder()

        log("ETL completed successfully")
        sys.exit(0)   # SUCCESS

    except Exception as e:
        log(f"ETL failed: {e}")
        sys.exit(1)   # FAILURE

# ---------------------------------------
if __name__ == "__main__":
    main()
