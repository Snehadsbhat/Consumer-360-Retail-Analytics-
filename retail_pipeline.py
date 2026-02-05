import subprocess
import sys
from datetime import datetime

def log(msg):
    print(f"[{datetime.now()}] {msg}")

def run_rfm_and_association():
    log("Starting RFM & Association Rule pipeline")

    
    script_path = r"C:\Users\sneha\Desktop\Infotact Internship\Week2_RFM.py"
    working_dir = r"C:\Users\sneha\Desktop\Infotact Internship"

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        cwd=working_dir
    )

    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception("Week2_RFM.py failed")

    log("RFM & Association Rule pipeline completed")

def main():
    try:
        log("ETL started")

        # Since data is already cleaned, we directly run analytics
        run_rfm_and_association()

        log("ETL completed successfully")
        sys.exit(0)

    except Exception as e:
        log(f"ETL failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
