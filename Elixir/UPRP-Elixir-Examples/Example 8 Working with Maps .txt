# ☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: case_example.ex
# ☆
defmodule HttpHandler do

  def handle_response(response) do

    # The `case` statement will pattern match the `response` variable
    # against each clause from top to bottom.

    case response do

      # This clause matches a tuple where the first element is the atom `:ok`
      # and binds the second element to the variable `body`.

      {:ok, body} ->
        "Success! Body: #{body}"

      # This clause matches a tuple where the first two elements are `:error` and `404`.
      # The underscore `_` is a wildcard that matches anything, but we don't care
      # about its value, so we don't bind it.

      {:error, 404, _} ->
        "Error: Not Found"

      # This is a more general error clause that binds the code and message.

      {:error, code, message} ->
        "Generic Error #{code}: #{message}"

      # The underscore by itself is a "catch-all" clause, like a default case.
      # It will match any response that the clauses above did not.

      _ ->

        "Unknown response"

    end
  end
end

IO.puts(HttpHandler.handle_response({:ok, "Welcome!"}))
IO.puts(HttpHandler.handle_response({:error, 404, "Page missing"}))
