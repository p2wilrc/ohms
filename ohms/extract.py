"""
Extract more human-readable things from the XML files in OHMS data
"""

import argparse
import csv
import logging
import os
import shutil
from pathlib import Path

from lxml import etree

LOGGER = logging.getLogger(Path(__file__).stem)
THISDIR = Path(__file__).parent
CSSFILE = THISDIR / "ohms.css"
XSLTFILE = THISDIR / "ohms2html.xsl"
with open(XSLTFILE) as infh:
    TRANSFORM = etree.XSLT(etree.parse(infh))
NS = "{https://www.weareavp.com/nunncenter/ohms}"
FIELDS = [
    "title",
    "duration",
    "interviewee",
    "interviewer",
    "collection_name",
    "series_name",
    "repository",
]


def extract(inpath: Path, outpath: Path) -> dict:
    with open(inpath, "rt") as infh:
        tree = etree.parse(infh)
    # use XSL to get a basic HTML
    html = TRANSFORM(tree)
    htmlpath = outpath.with_suffix(".html")
    LOGGER.info("%s -> %s", inpath, htmlpath)
    html.write_output(htmlpath)
    # transcript (cursed namespaces!)
    record = tree.find(f".//{NS}record")
    transcript = record.find(f"{NS}transcript")
    if transcript.text:
        txtpath = outpath.with_suffix(".txt")
        LOGGER.info("    -> %s", txtpath)
        with open(txtpath, "wt") as outfh:
            outfh.write(transcript.text)
    # collect individual bits of info for the spreadsheet
    info = {}
    for item in FIELDS:
        el = record.find(f"{NS}{item}")
        if el is not None and el.text is not None:
            info[item] = el.text
    # date tag is different (replicate XSL here...)
    date = record.find(f"{NS}date")
    info["date"] = date.get("value")
    if not info["date"]:
        date = record.find(f"{NS}date_nonpreferred_format")
        info["date"] = date.text
    return info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("indir", help="Directory with OHMS XML input files", type=Path)
    parser.add_argument("outdir", help="Directory for output", type=Path)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    args.outdir.mkdir(parents=True, exist_ok=True)
    records = []
    for path, dirs, files in os.walk(args.indir, topdown=True):
        fpath = Path(path)
        rpath = fpath.relative_to(args.indir)
        opath = args.outdir / rpath
        opath.mkdir(exist_ok=True)
        shutil.copy(CSSFILE, opath / CSSFILE.name)
        for f in files:
            fpath = Path(path) / f
            rpath = fpath.relative_to(args.indir)
            opath = args.outdir / rpath
            info = extract(fpath, opath)
            info["filename"] = rpath
            records.append(info)
    with open(args.outdir / "files.csv", "wt") as outfh:
        writer = csv.DictWriter(outfh, fieldnames=["filename", "date",] + FIELDS)
        writer.writeheader()
        for row in records:
            writer.writerow(row)


if __name__ == "__main__":
    main()
