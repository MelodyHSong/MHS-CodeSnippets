# ☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: greeter.ex
# ☆

# All named functions in Elixir must belong to a module.
# We define a module using `defmodule`.

defmodule Greeter do

  # We define a public function using `def`. It takes one argument, `name`.

  def hello(name) do
    "Hello, #{name}!" # The last expression in a function is its return value.

  end

end

# To call a function, we use the syntax: Module.function(argument)

message = Greeter.hello("Melody")

IO.puts(message)
