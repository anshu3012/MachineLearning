// Per-figure "Make interactive" buttons. build-content.sh writes each figure that has a plotly twin as
// <iframe data-src hidden> + <img class="static-fig">, and each playground / 3D map as <iframe data-src hidden>.
// build-content.sh also writes the button under each (so nothing shifts as the page loads); this script wires it:
// tapping it swaps that one figure to its interactive page (loading it
// then, not before) and back. Every figure starts as the plain image on every visit; nothing is remembered.
// Renders nothing itself: it only carries the script and the button style.
// build-content.sh copies this file to quartz/components/; quartz.layout.ts imports it.
import { QuartzComponent, QuartzComponentConstructor } from "./types"

const InteractiveFigures: QuartzComponent = () => null

// data-src is a root path ("/ML/.../images/x.htm"); the page's slug depth turns it into a relative URL, which also
// works under the /MachineLearning/ prefix on GitHub Pages.
InteractiveFigures.afterDOMLoaded = `
document.addEventListener("nav", () => {
  const depth = (document.body.dataset.slug || "").split("/").length - 1
  const prefix = depth > 0 ? "../".repeat(depth) : "./"
  for (const f of document.querySelectorAll("article iframe[data-src]")) {
    const img = f.nextElementSibling && f.nextElementSibling.matches("img.static-fig") ? f.nextElementSibling : null
    const btn = (img || f).nextElementSibling
    if (!btn || !btn.matches("button.fig-toggle")) continue
    const off = btn.textContent
    const toggle = () => {
      const on = btn.getAttribute("aria-pressed") !== "true"
      if (on && !f.getAttribute("src")) f.setAttribute("src", prefix + f.dataset.src.replace(/^\\//, ""))
      f.hidden = !on
      if (img) img.hidden = on
      btn.setAttribute("aria-pressed", String(on))
      btn.textContent = on ? (img ? "Back to image" : "Close") : off
    }
    btn.addEventListener("click", toggle)
    window.addCleanup?.(() => btn.removeEventListener("click", toggle))
  }
})
`

InteractiveFigures.css = `
.fig-toggle {
  display: block;
  min-height: 44px;
  margin: -0.5rem auto 0;
  padding: 0.4rem 1rem;
  border: 1px solid var(--lightgray);
  border-radius: 999px;
  background: var(--light);
  color: var(--secondary);
  font: inherit;
  font-size: 0.9rem;
  cursor: pointer;
}
.fig-toggle[aria-pressed="true"] { color: var(--darkgray); }
.fig-toggle:focus-visible { outline: 2px solid var(--secondary); outline-offset: 2px; }
`

export default (() => InteractiveFigures) satisfies QuartzComponentConstructor
