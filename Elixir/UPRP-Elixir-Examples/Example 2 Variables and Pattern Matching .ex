# ☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: cond_example.ex
# ☆

age = 25

# `cond` is used for checking multiple conditions, like an if/else-if/else chain.
# It evaluates each expression until it finds one that is not `nil` or `false`.

status =
  cond do

    age < 13 -> "Child"

    age >= 13 and age < 20 -> "Teenager"

    age >= 20 -> "Adult"

    # `true` is used as the final clause to act as an `else`, since it will always match.

    true -> "Default case"

  end

IO.puts(status)
