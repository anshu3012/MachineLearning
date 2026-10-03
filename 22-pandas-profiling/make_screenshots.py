"""Screenshots of the real profiling report (titanic_report.html, made by notebook.ipynb) for the Note.

Opens the report in the system Chrome, headless (the same way kaleido does), clicks the tabs we need,
and saves each part as images/<name>.png. Run it after the notebook: python make_screenshots.py
"""
import asyncio
import base64
from pathlib import Path

import choreographer as choreo

here = Path(__file__).parent
REPORT = (here / "titanic_report.html").resolve().as_uri()

# JS helpers: find a variable block by its column name, click a button, measure an element (or a section)
HELPERS = """
window.varBlock = n => [...document.querySelectorAll('.variable')]
    .find(e => e.innerText.trim().split(/\\s/)[0] === n);
window.click = sel => { document.querySelector(sel).click(); };
window.rectOf = (els, pad) => {
  const rs = els.map(e => e.getBoundingClientRect());
  const x = Math.min(...rs.map(r => r.left)) - pad, y = Math.min(...rs.map(r => r.top)) + scrollY - pad;
  const w = Math.max(...rs.map(r => r.right)) + pad - x, h = Math.max(...rs.map(r => r.bottom)) + scrollY + pad - y;
  return {x, y, width: w, height: h};
};
window.section = id => { const h = document.getElementById(id); return [h, h.nextElementSibling]; };
"""

# name: (JS run first, JS expression giving the list of elements to capture)
SHOTS = {
    "report_overview": ("", "[document.getElementById('tab-pane-overview-dataset_overview')]"),
    "report_alerts": ("click('#tab-overview-alerts')",
                      "[document.getElementById('tab-pane-overview-alerts')]"),
    "report_sex": ("", "[varBlock('Sex')]"),
    "report_age": ("", "[varBlock('Age')]"),
    "report_age_details": ("varBlock('Age').querySelector('.collapse-toggle, [data-bs-toggle=collapse]').click()",
                           "[varBlock('Age').querySelector('.collapse.show .tab-pane.active')]"),
    "report_interactions": ("click('#tab-interactions-interactions_age');"
                            "click('#tab-interactions_age-interactions_age_fare')",
                            "section('interactions')"),
    "report_correlations": ("click('#tab-correlations_tab-pearson_diagram_table')",
                            "[document.getElementById('tab-pane-pearson_diagram_table-pearson_diagram')]"),
    "report_missing_count": ("", "[document.getElementById('tab-pane-missing-bar')]"),
    "report_missing_matrix": ("click('#tab-missing-matrix')",
                              "[document.getElementById('tab-pane-missing-matrix')]"),
}


async def main():
    async with choreo.Browser(headless=True) as browser:
        tab = await browser.create_tab(REPORT)
        await tab.send_command("Emulation.setDeviceMetricsOverride",
                               params={"width": 1100, "height": 900, "deviceScaleFactor": 2, "mobile": False})
        await asyncio.sleep(3)

        async def js(expr):
            r = await tab.send_command("Runtime.evaluate", params={"expression": expr, "returnByValue": True})
            if "exceptionDetails" in r["result"]:
                raise RuntimeError(f"{expr}: {r['result']['exceptionDetails']}")
            return r["result"]["result"].get("value")

        await js(HELPERS)
        for name, (action, target) in SHOTS.items():
            if action:
                await js(action)
                await asyncio.sleep(1)  # let the tab fade-in finish
            clip = await js(f"rectOf({target}, 8)")
            shot = await tab.send_command("Page.captureScreenshot", params={
                "format": "png", "captureBeyondViewport": True, "clip": {**clip, "scale": 1}})
            (here / "images" / f"{name}.png").write_bytes(base64.b64decode(shot["result"]["data"]))
            print(name, round(clip["width"]), "x", round(clip["height"]))


asyncio.run(main())
