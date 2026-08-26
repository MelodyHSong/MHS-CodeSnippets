-- ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
-- ☆ Author: ☆ MelodyHSong ☆
-- ☆ Language: Lua
-- ☆ File Name: math_helper.lua
-- ☆ Date: 2026-08-25
-- ☆
-- ☆ Description: Reusable math utility module for clamping, interpolation (lerp),
-- ☆              range mapping, and 2D vector operations.
-- ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

local MathHelper = {}

--- Clamps a number between a minimum and maximum value.
--- @param val number
--- @param min number
--- @param max number
--- @return number
function MathHelper.clamp(val, min, max)
    if val < min then return min end
    if val > max then return max end
    return val
end

--- Performs linear interpolation between two values.
--- @param a number Start value
--- @param b number End value
--- @param t number Interpolation factor (0.0 to 1.0)
--- @return number
function MathHelper.lerp(a, b, t)
    return a + (b - a) * MathHelper.clamp(t, 0.0, 1.0)
end

--- Maps a value from one numeric range to another.
--- @param val number
--- @param inMin number
--- @param inMax number
--- @param outMin number
--- @param outMax number
--- @return number
function MathHelper.mapRange(val, inMin, inMax, outMin, outMax)
    if inMax == inMin then return outMin end
    local progress = (val - inMin) / (inMax - inMin)
    return MathHelper.lerp(outMin, outMax, progress)
end

--- Calculates the 2D Euclidean distance between two points.
--- @param x1 number
--- @param y1 number
--- @param x2 number
--- @param y2 number
--- @return number
function MathHelper.distance2D(x1, y1, x2, y2)
    local dx = x2 - x1
    local dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)
end

return MathHelper
