"""
ONS Data Downloader — Process Automation
Author: Gaurav Indora
Purpose: Automate discovery and download of ONS CSV datasets.
Usage:  python automation/ons_downloader.py
Skills: Process Automation, Python
"""
import requests, os, re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_DIR = os.path.join(ROOT,"data","raw","ONS")
os.makedirs(SAVE_DIR,exist_ok=True)

ONS_DATASETS = {
    "EMP01_Employment":     "https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/lf24/lms",
    "UNEM01_Unemployment":  "https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peoplenotinwork/unemployment/timeseries/mgsx/lms",
    "VACS01_Vacancies":     "https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/jp9z/unem",
    "CPI_Inflation":        "https://www.ons.gov.uk/generator?format=csv&uri=/economy/inflationandpriceindices/timeseries/d7g7/mm23",
    "GDP_Quarterly":        "https://www.ons.gov.uk/generator?format=csv&uri=/economy/grossdomesticproductgdp/timeseries/ihyq/pn2",
}

headers = {"User-Agent":"Mozilla/5.0 (compatible; UKJobMarketAnalysis/1.0)"}

def download_dataset(name, url):
    """Download an ONS CSV dataset and save locally."""
    print(f"  Downloading {name}...")
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            fname = f"{SAVE_DIR}/{name}_{datetime.now().strftime('%Y%m%d')}.csv"
            with open(fname,"wb") as f: f.write(r.content)
            lines = len(r.content.decode("utf-8","ignore").splitlines())
            print(f"    ✓ Saved: {fname} ({lines} lines)")
            return True
        else:
            print(f"    ✗ HTTP {r.status_code} — will use locally stored data")
            return False
    except Exception as e:
        print(f"    ✗ Error: {e} — will use locally stored data")
        return False

def check_existing():
    """List all currently downloaded raw ONS files."""
    print("\nExisting ONS data files:")
    files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".csv")]
    for f in sorted(files):
        size = os.path.getsize(os.path.join(SAVE_DIR,f))
        print(f"  • {f}  ({size:,} bytes)")
    return files

if __name__ == "__main__":
    print("="*60)
    print("ONS DATA DOWNLOADER — UK Job Market Analysis")
    print(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    success=0
    for name,url in ONS_DATASETS.items():
        if download_dataset(name,url): success+=1
    print(f"\n{success}/{len(ONS_DATASETS)} downloads successful.")
    check_existing()
    print("\nNote: If downloads fail, data is already stored in data/raw/ONS/")
    print("from the project setup. Re-run this script to refresh data.")
