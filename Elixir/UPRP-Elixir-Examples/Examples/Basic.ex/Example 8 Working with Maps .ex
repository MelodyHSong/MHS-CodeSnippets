# ☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: map_example.ex
# ☆

# A map is a key-value store. Here we use atoms as keys, which is common and efficient.

user = %{name: "Melody", language: "C#", level: 10}


# You can access map values using the dot notation if the key is an atom.

IO.puts(user.name)

# The bracket notation works for any type of key.

IO.puts(user[:language])


# To "update" a map, you use this special syntax.
# Because data is immutable, this creates a NEW map with the specified changes.

updated_user = %{user | language: "Elixir"}


# The new map has the new value.

IO.puts(updated_user.language) # Prints "Elixir"

# The original map is completely unchanged.

IO.puts(user.language) # Prints "C#", the original is unchanged

