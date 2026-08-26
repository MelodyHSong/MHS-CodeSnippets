# ☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: arithmetic.ex
# ☆

a = 10
b = 5

IO.puts("Addition: #{a + b}")
IO.puts("Subtraction: #{a - b}")
IO.puts("Multiplication: #{a * b}")

# Standard division in Elixir always returns a float.

IO.puts("Division: #{a / b}") # Result: 2.0

# For integer division, you must use the `div` function.

IO.puts("Integer Division: #{div(a, b)}") # Result: 2

# To get the remainder of a division, use the `rem` function.

IO.puts("Remainder: #{rem(a, b)}") # Result: 0

