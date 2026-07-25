# OS/endpoint dataset

`raw/` is gitignored.

**Option A — real dataset:** Kaggle — search **"ADFA-LD dataset"** (public OS-level system call logs).

**Option B — synthetic dataset:** run `python3 generate_logs.py` to produce `raw/os_logs.csv` (~5,000 normal rows + ~500 attack rows).
