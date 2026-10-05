#!/usr/bin/env bash
# Fill a Quartz checkout with the Notes and apply our config.
# Usage: site/build-content.sh <quartz-dir>
# Only copies: *.md, images/*.{png,gif,svg,jpg}, images/*.html (interactive figures, as .htm) and tools/plotly.min.js.
# Copies are edited; repo files are never touched.
set -euo pipefail
repo=$(cd "$(dirname "$0")/.." && pwd)
quartz=$(cd "$1" && pwd)
content="$quartz/content"
rm -rf "$content" && mkdir -p "$content"

# Edits applied to every copied Markdown file ($1 = root-absolute image dir, with trailing slash, or empty):
#  1. drop pandoc size attributes after image links: ](x.png){height=40%}
#  2. Note links -> bare file name (any #section kept); Quartz resolves them by unique file name (markdownLinkResolution: shortest)
#  3. course map -> site root, glossary -> bare name
#  4. images -> root-absolute path, because "shortest" treats unknown relative paths as root-relative
#  5. our blockquote openers -> Quartz callouts: "> **Key point:** text" becomes "> [!tip] Key point" + "> text";
#     later "> ..." lines of the same blockquote stay inside the callout. "Where this fits" starts collapsed.
fix_md() {
  sed -E \
    -e 's/\)\{(width|height)=[^}]*\}/)/g' \
    -e 's|\]\(([^)]*/)?([A-Z]{2}-[0-9]{3}-[^/)#]+)\.md(#[^)]*)?\)|](\2\3)|g' \
    -e 's|\]\(([^)]*/)?00-course-map\.md(#[^)]*)?\)|](/\2)|g' \
    -e 's|\]\(([^)]*/)?glossary\.md(#[^)]*)?\)|](glossary\2)|g' \
    -e "s#\]\(images/#](/$1images/#g" \
    -e 's/^> \*\*Key point:\*\* ?(.*)$/> [!tip] Key point\n> \1/' \
    -e 's/^> \*\*Extra:\*\* ?(.*)$/> [!note] Extra\n> \1/' \
    -e 's/^> \*\*Another way to see it:\*\* ?(.*)$/> [!example] Another way to see it\n> \1/' \
    -e 's/^> \*\*Where this fits:\*\* ?(.*)$/> [!info]- Where this fits\n> \1/' |
  display_math
}

# 6. A line that is only "$$ ... $$" (the Notes' one-line display maths, which GitHub and pandoc show as display)
#    becomes a fenced block "$$" / body / "$$" with blank lines around: Quartz's remark-math renders a one-line
#    $$...$$ as inline maths, which ran every step-by-step calculation together into one paragraph.
#    The line's prefix (list indent or "> ") is kept so the block stays inside its list item or callout.
display_math() {
  awk '{ match($0, /^[> \t]*/); pre = substr($0, 1, RLENGTH); rest = substr($0, RLENGTH + 1) }
       rest ~ /^\$\$.*\$\$[ \t]*$/ {
         body = rest; sub(/^\$\$/, "", body); sub(/\$\$[ \t]*$/, "", body)
         if (body !~ /\$\$/ && body ~ /[^ \t]/) {
           blank = pre; sub(/[ \t]+$/, "", blank)
           print blank; print pre "$$"; print pre body; print pre "$$"; print blank; next
         }
       }
       { print }'
}

# Quartz shows no caption for ![caption](path). After each standalone captioned image, add a paragraph
# "Figure N: caption", N counting such images per page from 1, the same way pandoc numbers them, so the
# Notes' "Figure 3" references line up. custom.scss styles the paragraph that follows an image as a caption.
# An image indented in a list item or inside a "> " blockquote counts too (pandoc numbers those as well);
# the caption keeps the same prefix so it stays in the item or quote.
add_captions() {
  awk 'match($0, /^[> ]*!\[/) && /^[> ]*!\[.+\]\([^)]*\)[[:space:]]*$/ {
         n++; print
         pre = substr($0, 1, RLENGTH - 2); blank = pre; sub(/[ ]+$/, "", blank); print blank
         cap = $0; sub(/^[> ]*!\[/, "", cap); sub(/\]\([^)]*\)[[:space:]]*$/, "", cap)
         print pre "Figure " n ": " cap; next
       } { print }'
}

# Interactive figures. A figure script writes images/x.html (a plotly page) next to images/x.png; a Note may also
# carry a marker line "<!-- playground: images/x_playground.html -->". In the copy, run after add_captions:
#  - a standalone image whose twin exists becomes <iframe class="plotly-twin" data-src hidden> + the PNG + a
#    "Make interactive" button, written here so the page does not shift when it loads (a shift made section
#    links land short); site/InteractiveFigures.tsx wires the button, which swaps that one figure and only then loads
#    its iframe, so phones get plain images that scroll and pinch-zoom normally; the
#    "Figure N" line add_captions already wrote stays, so numbering is the same as for the PNG;
#  - the marker becomes <iframe class="playground"> + an "Open interactive playground" button, with a one-line caption.
# The iframe height is the page's own height (its "height":N / height:Npx) plus 20px for plotly's modebar.
# $1 = root-absolute image dir prefix (as fix_md), $2 = "name<TAB>height" list written by copy_images.
embed_interactive() {
  awk -v pre="/$1images/" -v twins="$2" '
    BEGIN { while ((getline l < twins) > 0) { split(l, a, "\t"); h[a[1]] = a[2] }
            BTN = "<button type=\"button\" class=\"fig-toggle\" aria-pressed=\"false\">" }
    /^!\[.*\]\(.*\/images\/[^)\/]+\.png\)[[:space:]]*$/ {
      src = $0; sub(/^!\[.*\]\(/, "", src); sub(/\)[[:space:]]*$/, "", src)
      name = src; sub(/\.png$/, "", name); sub(/.*\//, "", name)
      if (name in h) {
        cap = $0; sub(/^!\[/, "", cap); sub(/\]\([^)]*\)[[:space:]]*$/, "", cap); gsub(/"/, "\\&quot;", cap)
        twin = src; sub(/\.png$/, ".htm", twin)
        printf "<iframe class=\"plotly-twin\" data-src=\"%s\" title=\"%s\" height=\"%d\" hidden></iframe>" \
               "<img class=\"static-fig\" src=\"%s\" alt=\"%s\">" BTN "Make interactive</button>\n", \
               twin, cap, (h[name] ? h[name] : 500) + 20, src, cap
        next
      }
    }
    /^<!-- playground: images\/[^ \/]+\.html -->[[:space:]]*$/ {
      name = $0; sub(/.*images\//, "", name); sub(/\.html -->[[:space:]]*$/, "", name)
      printf "<iframe class=\"playground\" data-src=\"%s%s.htm\" title=\"Interactive playground\" height=\"%d\" hidden></iframe>" \
             BTN "Open interactive playground</button>\n" \
             "\nInteractive playground: tap Open, then move the controls.\n", \
             pre, name, (h[name] ? h[name] : 700) + 20
      next
    }
    { print }'
}

# Files without front matter: turn the first-line "# Title" into front matter so Quartz shows the right title.
h1_to_frontmatter() {
  awk 'NR==1 && /^# / { printf "---\ntitle: \"%s\"\n---\n", substr($0, 3); next } { print }'
}

# Interactive pages are copied as *.htm: Quartz's Assets emitter drops a ".html" extension (the file would be
# served without a type), ".htm" it keeps. The plotly wrapper div is fixed at 950-1200px wide; "width:100%" lets
# the figure (config responsive: true) shrink to the iframe, down to 600px (narrower, the fixed margins and legend
# leave no plot area), below which the iframe scrolls sideways, like the "Where this fits" strip.
# The twin's "../../../../tools/plotly.min.js" path still resolves because the folder depth is unchanged.
# Prints the page's height ("height:Npx" / "height":N).
copy_html() {  # $1 = source .html, $2 = destination .htm
  sed -E '0,/style="height:[0-9]+px; width:[0-9]+px;"/ s/(style="height:[0-9]+px; )width:[0-9]+px;"/\1width:100%; min-width:600px;"/' "$1" > "$2"
  grep -oE 'height:[0-9]+px|"height":[0-9]+' "$1" | head -1 | tr -dc 0-9
}

# Only files the Note references are copied (images/x.png, .gif, ...; a twin x.html when x.png is referenced; a
# playground marker's x.html): the PDF-only frame grids (x_frames.png) and old figures stay out, which keeps the
# site under GitHub Pages' 1 GB limit.
copy_images() {  # $1 = source images dir, $2 = destination dir, $3 = "name<TAB>height" list to write (truncated first),
                 # $4 = the Note's .md
  local f name refs
  : > "$3"
  [ -d "$1" ] || return 0
  mkdir -p "$2"
  refs=$(grep -oE 'images/[^]()" >]+' "$4" | sed 's#^images/##' | sort -u)
  for f in $refs; do
    case "$f" in *.png|*.gif|*.svg|*.jpg) [ -f "$1/$f" ] && cp "$1/$f" "$2/" ;; esac
  done
  for f in "$1"/*.html; do
    [ -e "$f" ] || continue
    name=$(basename "$f" .html)
    grep -qxF -e "$name.png" -e "$name.html" <<< "$refs" || continue
    printf '%s\t%s\n' "$name" "$(copy_html "$f" "$2/$name.htm")" >> "$3"
  done
}
twins=$(mktemp); trap 'rm -f "$twins"' EXIT

# Notes: XX/NN-chapter/XX-NNN-slug/XX-NNN-slug.md -> XX/NN-chapter/XX-NNN-slug.md (flat, so the Explorer shows
# Subject > Chapter > Note); images stay in XX/NN-chapter/XX-NNN-slug/images/.
for note in "$repo"/{MA,ML,DL}/*/[A-Z][A-Z]-[0-9][0-9][0-9]-*/; do
  note=${note%/}
  name=$(basename "$note")
  rel=${note#"$repo"/}
  chapter=$(dirname "$rel")
  mkdir -p "$content/$chapter"
  copy_images "$note/images" "$content/$rel/images" "$twins" "$note/$name.md"
  fix_md "$rel/" < "$note/$name.md" | add_captions | embed_interactive "$rel/" "$twins" > "$content/$chapter/$name.md"
done

# Chapter index Notes: XX/NN-chapter/NN-chapter.md -> XX/NN-chapter/index.md (Quartz's folder page).
# Only the title and the intro line are kept; Quartz's own folder listing is the list of Notes.
for idx in "$repo"/{MA,ML,DL}/*/[0-9][0-9]-*.md; do
  chapter=${idx#"$repo"/}
  chapter=${chapter%/*}
  h1_to_frontmatter < "$idx" | awk '/^- /{skip=1} !skip' | fix_md "" > "$content/$chapter/index.md"
done

# Course map -> home page (images under 00-course-map/, where the twins' "../../tools/plotly.min.js" resolves),
# with the 3D concept map embedded at the end of its first section, after the concept playground (marker in the Note).
copy_images "$repo/00-course-map/images" "$content/00-course-map/images" "$twins" "$repo/00-course-map/00-course-map.md"
h=$(copy_html "$repo/course_map/concept_map_3d.html" "$content/00-course-map/images/concept_map_3d.htm")
map="<iframe class=\"playground\" data-src=\"/00-course-map/images/concept_map_3d.htm\" title=\"3D concept map\" height=\"$(( ${h:-700} + 20 ))\" hidden></iframe><button type=\"button\" class=\"fig-toggle\" aria-pressed=\"false\">Open 3D concept map</button>"
fix_md "00-course-map/" < "$repo/00-course-map/00-course-map.md" | add_captions | embed_interactive "00-course-map/" "$twins" |
  awk -v map="$map" '/^## / && ++n == 2 { print map "\n\nInteractive 3D concept map: tap Open, then drag to rotate and scroll to zoom.\n" } { print }' > "$content/index.md"
mkdir -p "$content/tools" && cp "$repo/tools/plotly.min.js" "$content/tools/"
h1_to_frontmatter < "$repo/glossary.md" | fix_md "" > "$content/glossary.md"

# Glossary codes in the text open their definition (site/glossary_terms.py; GlossaryTerms.tsx toggles the box).
python3 "$repo/site/glossary_terms.py" "$repo" "$content"

# Our config and theme over Quartz's defaults
cp "$repo/site/quartz.config.ts" "$repo/site/quartz.layout.ts" "$quartz/"
cp "$repo/site/InteractiveFigures.tsx" "$repo/site/PdfLink.tsx" "$repo/site/GlossaryTerms.tsx" "$repo/site/BackPosition.tsx" \
   "$repo/site/CourseOrder.tsx" "$repo/course_map/course_order.json" "$quartz/quartz/components/"
cp "$repo/site/custom.scss" "$quartz/quartz/styles/custom.scss"
# Quartz scrolls the Explorer to the current Note with scrollIntoView, which also scrolls the page itself and
# pushes the title out of view on every Note. "nearest" scrolls only the Explorer list. No-op if the line changes.
sed -i 's/activeElement.scrollIntoView({ behavior: "smooth" })/activeElement.scrollIntoView({ behavior: "smooth", block: "nearest" })/' \
  "$quartz/quartz/components/scripts/explorer.inline.ts"

echo "content: $(find "$content" -name '*.md' | wc -l) pages, $(find "$content" -type f ! -name '*.md' ! -name '*.htm' | wc -l) images, $(find "$content" -name '*.htm' | wc -l) interactive pages"

# Site build trigger: edit this file to force a rebuild without changing a Note.
