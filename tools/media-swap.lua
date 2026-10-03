-- PDF build only.
-- Images: GIF -> its key-frames PNG; PNG -> a vector PDF of the same name if one exists.
-- Block quotes starting with **Key point:**, **Extra:** or **Python:** become coloured boxes.
local function exists(p) local f = io.open(p, "r"); if f then f:close() return true end return false end

function Image(img)
  local src = img.src
  if src:match("%.gif$") then
    img.src = src:gsub("%.gif$", "_frames.png")
  elseif src:match("%.png$") then
    local pdf = src:gsub("%.png$", ".pdf")
    if exists(pdf) then img.src = pdf end
  end
  -- Fit inside the text width and a third of the page height (keeping the shape), so figures rarely
  -- jump pages. A figure can ask for more with {height=88%} (e.g. full-page Concept maps).
  local h = (img.attributes.height or "35%"):gsub("%%", "")
  return pandoc.RawInline("latex", "\\includegraphics[width=\\linewidth,height=" .. tonumber(h) / 100
    .. "\\textheight,keepaspectratio]{" .. img.src .. "}")
end

local boxes = { ["Key point:"] = "keypoint", ["Extra:"] = "extra", ["Python:"] = "pythonbox" }

function BlockQuote(bq)
  local first = bq.content[1]
  if first and first.t == "Para" and first.content[1] and first.content[1].t == "Strong" then
    local env = boxes[pandoc.utils.stringify(first.content[1])]
    if env then
      local out = { pandoc.RawBlock("latex", "\\begin{" .. env .. "}") }
      for _, b in ipairs(bq.content) do table.insert(out, b) end
      table.insert(out, pandoc.RawBlock("latex", "\\end{" .. env .. "}"))
      return out
    end
  end
end

-- The Summary starts on a fresh page, so it can be revised on its own.
function Header(h)
  if h.level == 2 and pandoc.utils.stringify(h):match("Summary$") then
    return { pandoc.RawBlock("latex", "\\newpage"), h }
  end
end
