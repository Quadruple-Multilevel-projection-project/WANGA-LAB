#!/usr/bin/env python3
"""Generate one Excel-compatible CSV per 175x14 matrix unit and a ZIP bundle."""
import argparse, csv, pathlib, zipfile
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",default="data/matrix_2450.csv")
    p.add_argument("--out",default="build/units")
    a=p.parse_args()
    source=pathlib.Path(a.input); out=pathlib.Path(a.out); out.mkdir(parents=True,exist_ok=True)
    with source.open(encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    ids=set()
    for row in rows:
        uid=row["unit_id"]
        if uid in ids: raise SystemExit(f"duplicate unit_id: {uid}")
        ids.add(uid)
        path=out/f"{uid}.csv"
        with path.open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(row.keys())); w.writeheader(); w.writerow(row)
    if len(rows)!=2450: raise SystemExit(f"expected 2450 units, got {len(rows)}")
    archive=out.parent/"impression-units-2450.zip"
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
        for path in sorted(out.glob("*.csv")): z.write(path,path.name)
    print(f"PASS: {len(rows)} unique unit CSV files; ZIP={archive}")
if __name__=="__main__": main()
