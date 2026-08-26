-- ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
-- ☆ Author: ☆ MelodyHSong ☆
-- ☆ Language: Lua
-- ☆ File Name: 01_basics.lua
-- ☆ Date: 2026-08-25
-- ☆
-- ☆ Description: Demonstrates Lua syntax basics including variables, control flow,
-- ☆              string manipulation, functions, and 1-based array indexing.
-- ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

print("==========================================")
print("  ☆ Welcome to Lua Basics ☆")
print("==========================================")

-- 1. Variables & Types
local greeting = "Hello, Lua!"
local version = _VERSION
local isAwesome = true
local price = 19.99

print(string.format("Status: %s (Running on %s)", greeting, version))
print(string.format("Types: isAwesome=%s (%s), price=%.2f (%s)", 
    tostring(isAwesome), type(isAwesome), price, type(price)))

-- 2. Functions & Control Flow
local function evaluateScore(score)
    if score >= 90 then
        return "Rank: S - Outstanding!"
    elseif score >= 75 then
        return "Rank: A - Great job!"
    elseif score >= 50 then
        return "Rank: B - Passing."
    else
        return "Rank: F - Try again!"
    end
end

print("\n--- Control Flow Evaluation ---")
local testScores = { 95, 82, 60, 45 }
for _, score in ipairs(testScores) do
    print(string.format("Score: %d -> %s", score, evaluateScore(score)))
end

-- 3. 1-Based Indexing Demonstration
print("\n--- 1-Based Array Indexing ---")
local inventory = { "Health Potion", "Mana Elixir", "Iron Sword", "Magic Ring" }

print("First item (index 1): " .. inventory[1])
print("Total items (#inventory): " .. #inventory)

print("Inventory List:")
for index, item in ipairs(inventory) do
    print(string.format("  [%d] %s", index, item))
end

print("\nBasics example executed successfully!")
