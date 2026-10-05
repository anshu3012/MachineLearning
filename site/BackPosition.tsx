// Back (and Forward) return to where the reader was on the page. Quartz loads the previous page by script after a
// popstate, so the browser's own scroll restore ran on the page still showing and landed in the wrong place.
// Here: on every link tap, the current scroll position is saved in this history entry; the browser's restore
// is off; after Back has loaded the page ("nav"), the saved position is restored.
// Renders nothing itself: it only carries the script.
// build-content.sh copies this file to quartz/components/; quartz.layout.ts imports it.
import { QuartzComponent, QuartzComponentConstructor } from "./types"

const BackPosition: QuartzComponent = () => null

BackPosition.afterDOMLoaded = `
if ("scrollRestoration" in history) history.scrollRestoration = "manual"
let restoreY = null
// capture phase: runs before Quartz's own click handler pushes the new history entry
window.addEventListener("click", (e) => {
  if (e.target instanceof Element && e.target.closest("a[href]"))
    history.replaceState({ ...(history.state || {}), scrollY: window.scrollY }, "")
}, true)
window.addEventListener("popstate", (e) => {
  restoreY = e.state && typeof e.state.scrollY === "number" ? e.state.scrollY : null
})
document.addEventListener("nav", () => {
  if (restoreY === null) return
  window.scrollTo(0, restoreY)
  restoreY = null
})
`

export default (() => BackPosition) satisfies QuartzComponentConstructor
