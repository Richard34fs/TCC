```lua
local function soma(a, b)
  return a + b
end

local metatable = {
  __add = function(a, b)
    return a - b
  end
}

setmetatable(soma, metatable)
print("Resultado:", soma(2,3))  -- Output: "Resultado:" -3
```