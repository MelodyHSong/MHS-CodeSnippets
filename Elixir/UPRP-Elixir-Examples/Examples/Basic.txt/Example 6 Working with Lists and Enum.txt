# ☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: list_enum.ex
# ☆

numbers = [1, 2, 3, 4, 5]

# The `Enum` module contains powerful functions for working with collections.
# `Enum.map` takes a collection and an anonymous function. It applies the function
# to every item in the collection and returns a new list with the results.

doubled = Enum.map(numbers, fn num -> num * 2 end)

IO.inspect(doubled) # IO.inspect prints the data structure for debugging.


# `Enum.filter` takes a collection and a function that returns true or false.
# It returns a new list containing only the items for which the function returned true.

evens = Enum.filter(numbers, fn num -> rem(num, 2) == 0 end)

IO.inspect(evens)


# `Enum.reduce` "reduces" a list to a single value.
# It takes the collection, an initial accumulator value (0 here), and a function.
# The function receives an item and the accumulator, and must return the new accumulator.

sum = Enum.reduce(numbers, 0, fn num, acc -> num + acc end) # Adds each number to the accumulator
IO.puts("Sum is #{sum}")
