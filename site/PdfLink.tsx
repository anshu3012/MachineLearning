// "Open as PDF" link under the title of every Note page (and the course map, which is the home page).
// The site's page path mirrors the repo's pdf/ folder (ML/07-classification/ML-085-knn -> pdf/ML/07-classification/
// ML-085-knn.pdf). The PDFs are linked on GitHub, not copied to the site: they are 260 MB and the site must stay
// under GitHub Pages' 1 GB limit. GitHub shows a PDF in its own viewer, on a phone too.
// build-content.sh copies this file to quartz/components/; quartz.layout.ts imports it.
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const REPO = "https://github.com/anshu3012/MachineLearning/blob/main/pdf/"

const PdfLink: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  const slug = fileData.slug ?? ""
  const path = slug === "index" ? "00-course-map" : /(^|\/)[A-Z]{2}-\d{3}-[^/]+$/.test(slug) ? slug : null
  if (!path) return null
  return (
    <p class="pdf-link">
      <a href={`${REPO}${path}.pdf`} target="_blank" rel="noopener">
        Open as PDF
      </a>
    </p>
  )
}

PdfLink.css = `
.pdf-link { margin: 0.25rem 0 0.5rem; font-size: 0.95rem; }
.pdf-link a { display: inline-flex; align-items: center; min-height: 44px; }
`

export default (() => PdfLink) satisfies QuartzComponentConstructor
