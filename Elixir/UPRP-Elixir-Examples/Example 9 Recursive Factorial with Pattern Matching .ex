# ☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: pipe_example.ex
# ☆

# The pipe operator `|>` makes chains of data transformations highly readable.
# The result of each line is passed as the first argument to the next line's function.

# 1. Start with a Range of numbers from 1 to 10.

1..10

# 2. Pipe the range into `map`. Square each number.
#    `&(&1 * &1)` is a shorthand for `fn x -> x * x end`.

|> Enum.map(&(&1 * &1))

# 3. Pipe the list of squares into `filter`. Keep only the odd numbers.

|> Enum.filter(&(rem(&1, 2) != 0))

# 4. Pipe the list of odd squares into `sum` to get the total.

|> Enum.sum()

# 5. Pipe the sum into another shorthand function to create a string.

|> (&("The final result is #{&1}")).()

# 6. Pipe the final string into `IO.puts` to print it.

|> IO.puts()
