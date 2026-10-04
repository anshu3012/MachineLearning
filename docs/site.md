# The Notes website

**URL:** https://anshu3012.github.io/MachineLearning/

The Notes are published as a static site with [Quartz 4](https://quartz.jzhao.xyz). Quartz is not stored in this repo; GitHub Actions fetches it on every build.

## How a build works

Workflow: `.github/workflows/site.yml`. It runs on every push to `main` that touches `MA/`, `ML/`, `DL/`, `00-course-map/`, `glossary.md` or `site/`, and can also be started by hand (Actions tab, "Publish site", "Run workflow").

1. Check out this repo.
2. Shallow-clone `jackyzha0/quartz` (branch `v4`) into `quartz/`.
3. `site/build-content.sh quartz` fills `quartz/content/`:
   - copies only `*.md` and `images/*.{png,gif,svg,jpg}`; no data, notebooks, `.py`, `.tex`, `.pdf`, logs;
   - flattens each Note to `XX/NN-chapter/XX-NNN-slug.md` (images stay in `XX-NNN-slug/images/`), so the Explorer shows Subject > Chapter > Note;
   - copies each chapter index `NN-chapter.md` to `NN-chapter/index.md` (Quartz's folder page), turning its `# Title` into front matter;
   - copies `00-course-map.md` to `index.md`, so the home page is the course map;
   - edits the copies: strips pandoc `{height=..}`/`{width=..}` after images (Quartz would print them as text), turns Note links into bare names (Quartz resolves them by unique file name), makes image paths root-absolute;
   - copies `site/quartz.config.ts` and `site/quartz.layout.ts` over Quartz's defaults.
4. `npm ci && npx quartz build` in `quartz/` (about 1 minute for 318 pages).
5. `actions/configure-pages` (with `enablement: true`), `upload-pages-artifact`, `deploy-pages`.

Repo files are never modified; all edits happen on the copies in `quartz/content/`.

## Site configuration

- `site/quartz.config.ts`: title, `baseUrl`, plugins (KaTeX maths, folder pages sorted by file name, no OG images, no RSS, no dates).
- `site/quartz.layout.ts`: Explorer (sorted by file name, number prefixed to each title), Search, Table of contents, Backlinks; Graph is off.

## Testing a build locally

```bash
git clone --depth 1 --branch v4 https://github.com/jackyzha0/quartz.git /tmp/quartz
bash site/build-content.sh /tmp/quartz
cd /tmp/quartz && npm ci && npx quartz build --serve   # http://localhost:8080
```

Needs Node 22 or newer.

## If a build fails

Open the repo's **Actions** tab, click the failed "Publish site" run, then the `build` job; the failing step is expanded in red.

- Fails in "Copy Notes and config into Quartz": a Note or folder breaks the naming scheme (`XX-NNN-slug/XX-NNN-slug.md`, `NN-chapter/NN-chapter.md`).
- Fails in "Build": usually a Markdown or maths parse problem; the log names the file. Reproduce locally with the steps above.
- Fails in "configure-pages" with a permissions error: see the manual step below.
- Fails in `deploy` with an environment-protection error: Settings > Environments, delete `github-pages`, re-run the workflow (it recreates it).

## One manual step

Pages must be enabled with the source set to GitHub Actions. The workflow tries to do this itself (`enablement: true`); if that step fails, do it once by hand: repo **Settings > Pages > Build and deployment > Source: GitHub Actions**, then re-run the workflow.

## Known limits

- The site is about 680 MB, nearly all GIFs and PNGs; GitHub Pages allows 1 GB. The deploy step takes a few minutes because of this.
- The `prerequisites:` front-matter list (`[[XX-NNN-slug]]`) is not shown on the page; Quartz ignores unknown front matter. The "Where this fits" box carries the same links.
- Each chapter page shows the chapter's own reading-order list followed by Quartz's automatic list of the same Notes.
