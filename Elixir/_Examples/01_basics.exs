# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: 01_basics.exs
# ☆ Date: 2026-08-25
# ☆
# ☆ Description: Demonstrates Elixir basics including pattern matching,
# ☆              immutable data structures, atoms, lists, and maps.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

IO.puts("==========================================")
IO.puts("  ☆ Welcome to Elixir Basics ☆")
IO.puts("==========================================")

# 1. Atoms, Variables & Immutability
status = :ok
message = "Hello, Elixir!"
version = System.version()

IO.puts("Status Atom: #{inspect(status)}")
IO.puts("Message: #{message} (Elixir v#{version})")

# 2. Pattern Matching with Tuples & Destructuring
{:ok, result_val} = {:ok, 42}
IO.puts("Pattern Matched Tuple Value: #{result_val}")

# Destructuring lists into Head and Tail
[head | tail] = [10, 20, 30, 40]
IO.puts("List Head: #{head}")
IO.puts("List Tail: #{inspect(tail)}")

# 3. Maps & Map Access
player = %{
  username: "MelodyHSong",
  level: 50,
  class: :archmage,
  active?: true
}

IO.puts("\n--- Map Data Access ---")
IO.puts("Username: #{player.username}")
IO.puts("Class: #{inspect(player.class)}")
IO.puts("Level: #{player.level}")

# Updating a map (creates a new map immutably)
updated_player = %{player | level: 51}
IO.puts("Updated Level (Immutable): #{updated_player.level}")
IO.puts("Original Level Unchanged: #{player.level}")

# 4. Anonymous Functions
double = fn x -> x * 2 end
add = &(&1 + &2) # Capture operator shorthand syntax

IO.puts("\n--- Anonymous Functions ---")
IO.puts("double(21) => #{double.(21)}")
IO.puts("add.(15, 25) => #{add.(15, 25)}")

IO.puts("\nBasics example executed successfully!")
