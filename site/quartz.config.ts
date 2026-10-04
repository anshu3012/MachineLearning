import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

// CampusX Notes site. Copied over Quartz's quartz.config.ts by site/build-content.sh.
// See https://quartz.jzhao.xyz/configuration
const config: QuartzConfig = {
  configuration: {
    pageTitle: "CampusX Notes",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "en-GB",
    baseUrl: "anshu3012.github.io/MachineLearning",
    ignorePatterns: ["private", "templates", ".obsidian", "**/data", "**/*.ipynb", "**/*.py"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        // Atkinson Hyperlegible ships 400 and 700 only, so the weights are listed (Quartz would ask for 600).
        header: { name: "Atkinson Hyperlegible", weights: [400, 700] },
        body: { name: "Atkinson Hyperlegible", weights: [400, 700], includeItalic: true },
        code: "IBM Plex Mono",
      },
      colors: {
        // Text on light/lightgray is at least 4.5:1 in both modes (site/custom.scss header lists the pairs).
        // gray is a border and rule colour only; custom.scss moves Quartz's two grey text uses to tertiary.
        lightMode: {
          light: "#F8FAFC",
          lightgray: "#E2E8F0",
          gray: "#94A3B8",
          darkgray: "#475569",
          dark: "#1E293B",
          secondary: "#36679C", // the figures' blue, desaturated; 4.76:1 on lightgray
          tertiary: "#64748B",
          highlight: "rgba(54, 103, 156, 0.08)",
          textHighlight: "#fde68a88",
        },
        darkMode: {
          light: "#0F1115",
          lightgray: "#26292E",
          gray: "#6B7280",
          darkgray: "#CBD5E1",
          dark: "#E6E8EC",
          secondary: "#8AB4E8",
          tertiary: "#94A3B8",
          highlight: "rgba(138, 180, 232, 0.12)",
          textHighlight: "#b4530088",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      // No CreatedModifiedDate: content is a copy, so git/filesystem dates would just be the build time.
      Plugin.SyntaxHighlighting({
        theme: { light: "github-light", dark: "github-dark" },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      // "shortest": a link is resolved by its unique file name, so bare Note names work from anywhere.
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      // Chapter folder pages list Notes in file-name (number) order.
      Plugin.FolderPage({ sort: (a, b) => (a.slug ?? "").localeCompare(b.slug ?? "") }),
      Plugin.TagPage(),
      Plugin.ContentIndex({ enableSiteMap: true, enableRSS: false }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // CustomOgImages left out: one rendered image per page makes the build several times slower.
    ],
  },
}

export default config
