-- ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
-- ☆ Author: ☆ MelodyHSong ☆
-- ☆ Language: Lua
-- ☆ File Name: 02_tables_and_oop.lua
-- ☆ Date: 2026-08-25
-- ☆
-- ☆ Description: Demonstrates Lua table manipulation, iteration methods,
-- ☆              table library functions, and OOP classes using Metatables.
-- ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

print("==========================================")
print("  ☆ Lua Tables & Object-Oriented Logic ☆")
print("==========================================")

-- 1. Dictionaries (Key-Value Tables)
local playerStats = {
    username = "MelodyHSong",
    level = 42,
    class = "Mage",
    gold = 1250,
    isOnline = true
}

print("\n--- Player Stats (Dictionary via pairs) ---")
for key, value in pairs(playerStats) do
    print(string.format("  %-10s : %s", key, tostring(value)))
end

-- 2. Table Library Utilities (Insert, Sort, Concat)
local scores = { 450, 120, 890, 310, 670 }
table.insert(scores, 990) -- Add high score

print("\n--- Unsorted Scores ---")
print("Scores string: " .. table.concat(scores, ", "))

table.sort(scores, function(a, b) return a > b end) -- Descending order

print("--- Sorted High Scores (Descending) ---")
for place, score in ipairs(scores) do
    print(string.format("  #%d Place: %d pts", place, score))
end

-- 3. Simple OOP Pattern using Metatables
local Character = {}
Character.__index = Character

function Character.new(name, maxHp, attackPower)
    local self = setmetatable({}, Character)
    self.name = name
    self.hp = maxHp
    self.maxHp = maxHp
    self.attackPower = attackPower
    return self
end

function Character:takeDamage(amount)
    self.hp = math.max(0, self.hp - amount)
    print(string.format("[%s] took %d damage! (HP: %d/%d)", self.name, amount, self.hp, self.maxHp))
end

function Character:heal(amount)
    self.hp = math.min(self.maxHp, self.hp + amount)
    print(string.format("[%s] healed %d HP! (HP: %d/%d)", self.name, amount, self.hp, self.maxHp))
end

function Character:isAlive()
    return self.hp > 0
end

print("\n--- OOP Metatable Demonstration ---")
local hero = Character.new("Astra", 100, 25)
hero:takeDamage(35)
hero:takeDamage(50)
hero:heal(20)
print(string.format("Hero Alive Status: %s", tostring(hero:isAlive())))

print("\nTables and OOP example executed successfully!")
