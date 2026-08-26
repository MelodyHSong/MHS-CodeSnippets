# ☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: matching.ex
# ☆

# Here, the match operator (=) binds the value 10 to the variable `x`.

x = 10

# We use string interpolation to print the value inside the string.

IO.puts("The value of x is #{x}")


# In Elixir, data is immutable. We aren't changing the original 10.
# Instead, we are "rebinding" the variable `x` to a new value, 20.

x = 20

IO.puts("The new value of x is #{x}")


# Pattern matching is powerful for destructuring data.
# Here, we match a tuple. `:ok` is an atom, a common way to show status.
# The variable `status` is bound to `:ok` and `message` is bound to "Success".

{status, message} = {:ok, "Success"}

IO.puts("Status is #{status}, message is '#{message}'")
