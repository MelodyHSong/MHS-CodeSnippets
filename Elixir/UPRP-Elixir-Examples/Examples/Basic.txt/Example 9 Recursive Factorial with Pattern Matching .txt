# ☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: factorial.ex
# ☆

defmodule Math do

  # We can define multiple function clauses with the same name.
  # Elixir uses pattern matching to decide which one to run.

  # This is the "base case" for the recursion. It only matches when the argument is 0.

  def factorial(0), do: 1

  # This clause has a "guard clause" (`when n > 0`). It will only match if
  # the argument `n` is greater than 0.
  # This is the "recursive step".

  def factorial(n) when n > 0 do

    n * factorial(n - 1)

  end
end

IO.puts(Math.factorial(5)) # 120
