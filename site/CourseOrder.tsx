// "Course order" in the left sidebar, above the MA / ML / DL folders: the whole course as one reading path,
// in Stages (CONTEXT.md "Course order"). The data is course_map/course_order.json, written by
// course_map/build_map.py; build-content.sh copies it next to this file. The current Note is marked and its Stage
// opens. On a phone it moves into the ☰ menu, above the folders. Open by default; a reader who closes it keeps it
// closed (remembered in this browser).
// build-content.sh copies this file to quartz/components/; quartz.layout.ts imports it.
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { resolveRelative, FullSlug } from "../util/path"
import data from "./course_order.json"

type Stage = { stage: string; notes: { label: string; title: string; slug: string }[] }

const CourseOrder: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  const here = fileData.slug as FullSlug
  return (
    <details class="course-order">
      <summary>Course order</summary>
      <div class="co-panel">
        <p class="co-intro">Read the course in this order: each Note comes after everything it builds on.</p>
        <ol class="co-stages">
          {(data as Stage[]).map((s, i) => (
            <li>
              <details class="co-stage" open={s.notes.some((n) => n.slug === here)}>
                <summary>
                  {i + 1}. {s.stage}
                </summary>
                <ul>
                  {s.notes.map((n) => (
                    <li class={n.slug === here ? "co-here" : ""}>
                      <a href={resolveRelative(here, n.slug as FullSlug)} data-for={n.slug}>
                        <span class="co-label">{n.label}</span> {n.title}
                      </a>
                    </li>
                  ))}
                </ul>
              </details>
            </li>
          ))}
        </ol>
      </div>
    </details>
  )
}

CourseOrder.css = `
.course-order { margin: 0.5rem 0 1rem; }
.course-order > summary { cursor: pointer; font-weight: 600; color: var(--dark); min-height: 44px;
  display: flex; align-items: center; }
.course-order .co-intro { font-size: 0.85rem; color: var(--gray); margin: 0 0 0.5rem; }
.course-order ol, .course-order ul { list-style: none; padding-left: 0; margin: 0; }
.course-order .co-stage > summary { cursor: pointer; font-size: 0.9rem; padding: 0.35rem 0; }
.course-order .co-stage ul { padding-left: 0.75rem; border-left: 1px solid var(--lightgray); margin-bottom: 0.4rem; }
.course-order .co-stage li a { display: block; font-size: 0.85rem; padding: 0.25rem 0; text-decoration: none; }
.course-order .co-label { color: var(--gray); font-variant-numeric: tabular-nums; }
.course-order .co-here a { font-weight: 700; color: var(--secondary); }
.explorer-content .course-order { padding: 0 0.5rem; }
/* the list is long: the sidebar (computer) and the ☰ menu (phone) must scroll as a whole */
@media (min-width: 801px) {
  .left.sidebar:has(.course-order) { overflow-y: auto; overscroll-behavior: contain; }   /* not on a phone: it clips the ☰ menu */
}
.explorer .explorer-content:has(.course-order) { overflow-y: auto; overscroll-behavior: contain; }
`

// On every page change: on a phone, move the list into the ☰ menu; open it unless the reader closed it; mark the
// current Note and open its Stage.
CourseOrder.afterDOMLoaded = `
document.addEventListener("nav", (e) => {
  const slug = e.detail.url
  let closed = false
  try { closed = localStorage.getItem("co-closed") === "1" } catch {}
  for (const box of document.querySelectorAll(".course-order")) {
    if (window.matchMedia("(max-width: 800px)").matches) {
      const menu = document.querySelector(".explorer .explorer-content")
      if (menu && box.parentElement !== menu) menu.prepend(box)
    }
    box.open = !closed
    box.querySelector(":scope > summary").onclick = () => {
      try { localStorage.setItem("co-closed", box.open ? "1" : "0") } catch {}
    }
    for (const li of box.querySelectorAll("li.co-here")) li.classList.remove("co-here")
    const a = box.querySelector('a[data-for="' + slug + '"]')
    if (a) {
      a.parentElement.classList.add("co-here")
      a.closest("details.co-stage").open = true
    }
  }
})
`

export default (() => CourseOrder) satisfies QuartzComponentConstructor
