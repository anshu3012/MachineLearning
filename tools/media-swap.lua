-- PDF build only.
-- Images: GIF -> its key-frames PNG; PNG -> a vector PDF of the same name if one exists.
-- Block quotes starting with **Key point:** or **Extra:** become coloured boxes.
local function exists(p) local f = io.open(p, "r"); if f then f:close() return true end return false end

function Image(img)
  local src = img.src
  if src:match("%.gif$") then
    img.src = src:gsub("%.gif$", "_frames.png")
  elseif src:match("%.png$") then
    local pdf = src:gsub("%.png$", ".pdf")
    if exists(pdf) then img.src = pdf end
  end
  return img
end

local boxes = { ["Key point:"] = "keypoint", ["Extra:"] = "extra" }

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
