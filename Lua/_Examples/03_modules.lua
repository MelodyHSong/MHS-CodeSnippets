-- ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
-- ☆ Author: ☆ MelodyHSong ☆
-- ☆ Language: Lua
-- ☆ File Name: 03_modules.lua
-- ☆ Date: 2026-08-25
-- ☆
-- ☆ Description: Demonstrates loading external Lua modules using `require()`
-- ☆              and using imported helper functions.
-- ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

-- Determine script directory so require works regardless of current working directory
local scriptPath = debug.getinfo(1, "S").source:sub(2):match("(.*[/\\])") or ""
package.path = scriptPath .. "?.lua;" .. package.path

local MathHelper = require("math_helper")

print("==========================================")
print("  ☆ Lua Module Import Example ☆")
print("==========================================")

-- 1. Clamp Test
local rawVal = 150
local clampedVal = MathHelper.clamp(rawVal, 0, 100)
print(string.format("Clamp(%d, 0, 100) => %d", rawVal, clampedVal))

-- 2. Lerp (Linear Interpolation) Test
local startVal, endVal = 10, 50
print("\n--- Lerp Step Progression ---")
for step = 0, 10, 2.5 do
    local factor = step / 10.0
    local current = MathHelper.lerp(startVal, endVal, factor)
    print(string.format("  Factor %.2f : Lerp(%d, %d) => %.2f", factor, startVal, endVal, current))
end

-- 3. Range Mapping Test (e.g. mapping health 0-250 to health bar width 0-100%)
local hp = 175
local healthPercent = MathHelper.mapRange(hp, 0, 250, 0, 100)
print(string.format("\nMap HP (%d / 250) to percentage => %.1f%%", hp, healthPercent))

-- 4. Distance 2D Test
local p1x, p1y = 0, 0
local p2x, p2y = 3, 4
local dist = MathHelper.distance2D(p1x, p1y, p2x, p2y)
print(string.format("Distance between (0,0) and (3,4) => %.2f", dist))

print("\nModule example executed successfully!")
