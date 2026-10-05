import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"
import { Options } from "./quartz/components/Explorer"
import InteractiveFigures from "./quartz/components/InteractiveFigures"
import PdfLink from "./quartz/components/PdfLink"

// CampusX Notes layout. Copied over Quartz's quartz.layout.ts by site/build-content.sh.

// Explorer: order by slug (file name), so chapters and Notes follow their numbers, folders first.
const sortFn: Options["sortFn"] = (a, b) => {
  if (a.isFolder !== b.isFolder) return a.isFolder ? -1 : 1
  return a.slug.localeCompare(b.slug)
}

// Explorer: show the number in front of the title ("06 Regression", "ML-049 Simple Linear Regression ...").
const mapFn: Options["mapFn"] = (node) => {
  const seg = node.slugSegment ?? ""            // the root node has no segment: guard it, or the tree never builds
  const m = seg.match(/^(\d{2}|[A-Z]{2}-\d{3})-/)
  if (m && node.displayName !== seg) node.displayName = `${m[1]} ${node.displayName}`
}

const explorer = Component.Explorer({ sortFn, mapFn, folderClickBehavior: "collapse" })

export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [Component.TagList()], // tags after the text, not between the title and the first line
  footer: Component.Footer({
    links: {
      "Source on GitHub": "https://github.com/anshu3012/MachineLearning",
    },
  }),
}

// single Note pages
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    PdfLink(), // "Open as PDF" (GitHub) under the title of each Note
    InteractiveFigures(), // "Make interactive" button under each interactive figure
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        { Component: Component.Search(), grow: true },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
    explorer,
  ],
  // Graph: Quartz's defaults (local graph of depth 1; the corner icon opens the global graph). Not on the
  // home page: the course map links every Note, so its local graph is one solid blob.
  right: [
    Component.DesktopOnly(Component.TableOfContents()),
    Component.ConditionalRender({
      component: Component.Graph(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.Backlinks(),
  ],
}

// folder (chapter) and tag listing pages
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [{ Component: Component.Search(), grow: true }, { Component: Component.Darkmode() }],
    }),
    explorer,
  ],
  right: [],
}
