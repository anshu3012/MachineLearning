#!/usr/bin/env bash
# Fill a Quartz checkout with the Notes and apply our config.
# Usage: site/build-content.sh <quartz-dir>
# Only copies: *.md plus images/*.{png,gif,svg,jpg}. Copies are edited; repo files are never touched.
set -euo pipefail
repo=$(cd "$(dirname "$0")/.." && pwd)
quartz=$(cd "$1" && pwd)
content="$quartz/content"
rm -rf "$content" && mkdir -p "$content"

# Edits applied to every copied Markdown file ($1 = root-absolute image dir, with trailing slash, or empty):
#  1. drop pandoc size attributes after image links: ](x.png){height=40%}
#  2. Note links -> bare file name; Quartz resolves them by unique file name (markdownLinkResolution: shortest)
#  3. course map -> site root, glossary -> bare name
#  4. images -> root-absolute path, because "shortest" treats unknown relative paths as root-relative
#  5. our blockquote openers -> Quartz callouts: "> **Key point:** text" becomes "> [!tip] Key point" + "> text";
#     later "> ..." lines of the same blockquote stay inside the callout. "Where this fits" starts collapsed.
fix_md() {
  sed -E \
    -e 's/\)\{(width|height)=[^}]*\}/)/g' \
    -e 's#\]\(([^)]*/)?([A-Z]{2}-[0-9]{3}-[^/)]+)\.md\)#](\2)#g' \
    -e 's#\]\(([^)]*/)?00-course-map\.md\)#](/)#g' \
    -e 's#\]\(([^)]*/)?glossary\.md\)#](glossary)#g' \
    -e "s#\]\(images/#](/$1images/#g" \
    -e 's/^> \*\*Key point:\*\* ?(.*)$/> [!tip] Key point\n> \1/' \
    -e 's/^> \*\*Extra:\*\* ?(.*)$/> [!note] Extra\n> \1/' \
    -e 's/^> \*\*Another way to see it:\*\* ?(.*)$/> [!example] Another way to see it\n> \1/' \
    -e 's/^> \*\*Where this fits:\*\* ?(.*)$/> [!info]- Where this fits\n> \1/'
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

# Files without front matter: turn the first-line "# Title" into front matter so Quartz shows the right title.
h1_to_frontmatter() {
  awk 'NR==1 && /^# / { printf "---\ntitle: \"%s\"\n---\n", substr($0, 3); next } { print }'
}

copy_images() {  # $1 = source images dir, $2 = destination dir
  [ -d "$1" ] || return 0
  mkdir -p "$2"
  find "$1" -maxdepth 1 -type f \( -name '*.png' -o -name '*.gif' -o -name '*.svg' -o -name '*.jpg' \) -exec cp -t "$2" {} +
}

# Notes: XX/NN-chapter/XX-NNN-slug/XX-NNN-slug.md -> XX/NN-chapter/XX-NNN-slug.md (flat, so the Explorer shows
# Subject > Chapter > Note); images stay in XX/NN-chapter/XX-NNN-slug/images/.
for note in "$repo"/{MA,ML,DL}/*/[A-Z][A-Z]-[0-9][0-9][0-9]-*/; do
  note=${note%/}
  name=$(basename "$note")
  rel=${note#"$repo"/}
  chapter=$(dirname "$rel")
  mkdir -p "$content/$chapter"
  fix_md "$rel/" < "$note/$name.md" | add_captions > "$content/$chapter/$name.md"
  copy_images "$note/images" "$content/$rel/images"
done

# Chapter index Notes: XX/NN-chapter/NN-chapter.md -> XX/NN-chapter/index.md (Quartz's folder page).
# Only the title and the intro line are kept; Quartz's own folder listing is the list of Notes.
for idx in "$repo"/{MA,ML,DL}/*/[0-9][0-9]-*.md; do
  chapter=${idx#"$repo"/}
  chapter=${chapter%/*}
  h1_to_frontmatter < "$idx" | awk '/^- /{skip=1} !skip' | fix_md "" > "$content/$chapter/index.md"
done

# Course map -> home page; glossary at root
fix_md "" < "$repo/00-course-map/00-course-map.md" > "$content/index.md"
copy_images "$repo/00-course-map/images" "$content/images"
h1_to_frontmatter < "$repo/glossary.md" | fix_md "" > "$content/glossary.md"

# Our config and theme over Quartz's defaults
cp "$repo/site/quartz.config.ts" "$repo/site/quartz.layout.ts" "$quartz/"
cp "$repo/site/custom.scss" "$quartz/quartz/styles/custom.scss"
# Quartz scrolls the Explorer to the current Note with scrollIntoView, which also scrolls the page itself and
# pushes the title out of view on every Note. "nearest" scrolls only the Explorer list. No-op if the line changes.
sed -i 's/activeElement.scrollIntoView({ behavior: "smooth" })/activeElement.scrollIntoView({ behavior: "smooth", block: "nearest" })/' \
  "$quartz/quartz/components/scripts/explorer.inline.ts"

echo "content: $(find "$content" -name '*.md' | wc -l) pages, $(find "$content" -type f ! -name '*.md' | wc -l) images"

# Site build trigger: edit this file to force a rebuild without changing a Note.
