-- PDF build only: GIF -> its key-frames PNG; PNG -> a vector PDF of the same name if one exists.
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
