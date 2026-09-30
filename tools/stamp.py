"""Stamp index.html's scripts and style sheets with a new version (?v=YYYYMMDDHHMM), so browsers fetch the new files
instead of mixing cached old ones with new ones. Run it before each deploy:

    python3 tools/stamp.py
"""
import datetime
import os
import re

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html")
html = open(path).read()
version = datetime.datetime.now().strftime("%Y%m%d%H%M")
# every local .js and .css reference (src="js/…" or href="css/…"), with or without an old ?v=
stamped, n = re.subn(r'((?:src|href)="(?:js|css|fonts)/[^"?]+\.(?:js|css))(?:\?v=\d+)?"', rf'\1?v={version}"', html)
open(path, "w").write(stamped)
print(f"stamped {n} files in index.html with v={version}")
