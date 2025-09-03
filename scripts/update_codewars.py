import re
import sys
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

USERNAME = "yukaberry"
README_PATH = Path("README.md")
START = "<!--CW_PERCENTILE-->"
END = "<!--CW_PERCENTILE_END-->"

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

# Match e.g. <b>Honor Percentile:</b>Top 1.915%
PATTERN = re.compile(
    r"<b>\s*Honor\s*Percentile:\s*</b>\s*Top\s*([0-9]+(?:[.,][0-9]+)?)\s*%",
    re.IGNORECASE,
)

def fetch_html(url: str) -> str:
    req = Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.8"})
    with urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")

def get_percentile(username: str) -> str:
    url = f"https://www.codewars.com/users/{username}/stats"
    html = fetch_html(url)

    m = PATTERN.search(html)
    if not m:
        raise RuntimeError("Honor Percentile not found in stats page HTML.")
    return m.group(1).replace(",", ".")

def replace_between_markers(text: str, start: str, end: str, replacement: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    return pattern.sub(f"{start}{replacement}{end}", text)

def main():
    percentile = get_percentile(USERNAME)
    md = README_PATH.read_text(encoding="utf-8")
    new_md = replace_between_markers(md, START, END, f"{percentile}%")
    if new_md != md:
        README_PATH.write_text(new_md, encoding="utf-8")
        print(f"Updated README with Honor Percentile: Top {percentile}%")
    else:
        print("README already up to date.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
