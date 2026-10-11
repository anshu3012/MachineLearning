// Glossary codes in the text ("G-2040") open their definition under the line. site/glossary_terms.py writes each
// code as <button class="gloss" data-g> and its hidden <span class="gloss-def" data-g> box after the bracket;
// this script toggles the box. A link to another Note opens a box as well: the box of the code right after it,
// or the <span class="gloss-def" data-link> box the build put after it, which links to the section. Ctrl/Cmd-click
// still follows the link. Renders nothing itself: it only carries the script and the style.
// build-content.sh copies this file to quartz/components/; quartz.layout.ts imports it.
import { QuartzComponent, QuartzComponentConstructor } from "./types"

const GlossaryTerms: QuartzComponent = () => null

GlossaryTerms.afterDOMLoaded = `
document.addEventListener("nav", () => {
  for (const btn of document.querySelectorAll("article button.gloss")) {
    const block = btn.closest("p, li, td, th, blockquote, div") || btn.parentElement
    const def = block.querySelector('.gloss-def[data-g="' + btn.dataset.g + '"]')
    if (!def) continue
    btn.setAttribute("aria-label", "Show the meaning of " + btn.dataset.g)
    const toggle = () => {
      const open = btn.getAttribute("aria-expanded") !== "true"
      def.hidden = !open
      btn.setAttribute("aria-expanded", String(open))
    }
    btn.addEventListener("click", toggle)
    window.addCleanup?.(() => btn.removeEventListener("click", toggle))
  }
  for (const a of document.querySelectorAll("article a")) {
    const next = a.nextElementSibling
    const gap = a.nextSibling
    const btn = next && next.matches("button.gloss") && gap && gap.nodeType === 3 && gap.textContent.trim() === "(" ? next : null
    const box = next && next.matches(".gloss-def[data-link]") ? next : null
    if (!btn && !box) continue
    a.setAttribute("aria-expanded", "false")
    const open = (e) => {
      if (e.ctrlKey || e.metaKey || e.shiftKey || e.button !== 0) return
      e.preventDefault()
      e.stopPropagation()
      if (btn) btn.click()
      else box.hidden = !box.hidden
      a.setAttribute("aria-expanded", String(btn ? btn.getAttribute("aria-expanded") === "true" : !box.hidden))
    }
    a.addEventListener("click", open)
    window.addCleanup?.(() => a.removeEventListener("click", open))
  }
})
`

GlossaryTerms.css = `
button.gloss {
  display: inline;
  padding: 0;
  border: 0;
  background: none;
  color: var(--secondary);
  font: inherit;
  text-decoration: underline dotted;
  text-underline-offset: 3px;
  cursor: pointer;
}
button.gloss[aria-expanded="true"] { text-decoration-style: solid; }
button.gloss:focus-visible { outline: 2px solid var(--secondary); outline-offset: 2px; }
.gloss-def {
  display: block;
  margin: 0.4rem 0 0.6rem;
  padding: 0.5rem 0.75rem;
  border-left: 3px solid var(--secondary);
  border-radius: 6px;
  background: var(--highlight);
  font-size: 0.92rem;
  line-height: 1.5;
}
.gloss-def[hidden] { display: none; }
`

export default (() => GlossaryTerms) satisfies QuartzComponentConstructor
