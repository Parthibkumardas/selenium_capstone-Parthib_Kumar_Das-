"""HTML reporting for the unittest suite (pytest uses pytest-html).

HtmlTestResult records every test outcome; write_html_report() renders a
self-contained HTML file with failure screenshots embedded as base64.
"""
import base64
import html
import time
import unittest
from datetime import datetime
from pathlib import Path


class HtmlTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []
        self._started = 0.0

    def startTest(self, test):
        self._started = time.time()
        super().startTest(test)

    def _record(self, test, status, detail=""):
        self.records.append({
            "test": test,  # kept so screenshot_path can be read once tearDown has run
            "name": test.id(),
            "status": status,
            "detail": detail,
            "duration": time.time() - self._started,
        })

    def addSuccess(self, test):
        super().addSuccess(test)
        self._record(test, "PASS")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._record(test, "FAIL", self._exc_info_to_string(err, test))

    def addError(self, test, err):
        super().addError(test, err)
        self._record(test, "ERROR", self._exc_info_to_string(err, test))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._record(test, "SKIP", reason)


_CSS = """
body{font-family:Segoe UI,Arial,sans-serif;margin:24px;color:#222}
.summary span{display:inline-block;margin-right:16px;padding:6px 14px;border-radius:6px;color:#fff;font-weight:600}
.total{background:#455a64}.PASS{background:#2e7d32}.FAIL,.ERROR{background:#c62828}.SKIP{background:#ef6c00}
table{border-collapse:collapse;width:100%;margin-top:18px}
th,td{border:1px solid #ddd;padding:8px;text-align:left;vertical-align:top}
th{background:#eceff1}td.status{font-weight:700;color:#fff;text-align:center;width:70px}
pre{white-space:pre-wrap;font-size:12px;background:#fafafa;padding:8px;margin:6px 0}
img{max-width:520px;border:1px solid #bbb;margin-top:6px}
"""


def _embed_screenshot(path):
    if not path or not Path(path).exists():
        return ""
    encoded = base64.b64encode(Path(path).read_bytes()).decode()
    return f'<div><b>Screenshot</b><br><img src="data:image/png;base64,{encoded}"></div>'


def write_html_report(records, report_path, title="Unittest Execution Report"):
    counts = {"PASS": 0, "FAIL": 0, "ERROR": 0, "SKIP": 0}
    for record in records:
        counts[record["status"]] += 1

    rows = []
    for index, record in enumerate(records, start=1):
        extra = ""
        if record["detail"]:
            extra += f"<pre>{html.escape(record['detail'])}</pre>"
        extra += _embed_screenshot(getattr(record["test"], "screenshot_path", None))
        rows.append(
            f"<tr><td>{index}</td><td>{html.escape(record['name'])}</td>"
            f"<td class='status {record['status']}'>{record['status']}</td>"
            f"<td>{record['duration']:.2f}s</td><td>{extra}</td></tr>"
        )

    document = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>{_CSS}</style></head><body>
<h1>{html.escape(title)}</h1>
<p>Generated: {datetime.now():%Y-%m-%d %H:%M:%S}</p>
<div class="summary">
<span class="total">Total: {len(records)}</span><span class="PASS">Passed: {counts['PASS']}</span>
<span class="FAIL">Failed: {counts['FAIL']}</span><span class="ERROR">Errors: {counts['ERROR']}</span>
<span class="SKIP">Skipped: {counts['SKIP']}</span></div>
<table><tr><th>#</th><th>Test</th><th>Status</th><th>Time</th><th>Details</th></tr>
{''.join(rows)}</table></body></html>"""

    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(document, encoding="utf-8")
    return report_path
