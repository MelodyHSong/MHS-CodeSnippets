# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: 03_pattern_matching_control.exs
# ☆ Date: 2026-08-25
# ☆
# ☆ Description: Demonstrates pattern matching in control flow: function clauses,
# ☆              case statements, cond expressions, and happy-path 'with' chains.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

defmodule PatternDemo do
  # 1. Multiple Function Clauses (Pattern Matching in Function Signatures)
  def greet(%{name: name, role: :admin}) do
    "Welcome Administrator #{name}! [Full Access Granted]"
  end

  def greet(%{name: name}) do
    "Hello #{name}! [Standard User Access]"
  end

  def greet(_) do
    "Welcome Guest!"
  end

  # 2. Function with Guard Clauses (when)
  def classify_age(age) when is_integer(age) and age >= 18, do: :adult
  def classify_age(age) when is_integer(age) and age >= 0, do: :minor
  def classify_age(_), do: :invalid

  # 3. Tuple Result Processor using case
  def handle_response(response) do
    case response do
      {:ok, data} -> "SUCCESS: Payload received -> #{inspect(data)}"
      {:error, :not_found} -> "ERROR 404: Resource missing."
      {:error, reason} -> "ERROR: Failed due to #{inspect(reason)}"
      _ -> "UNKNOWN: Unrecognized response format."
    end
  end

  # 4. Happy-path chaining using 'with'
  def authenticate_and_fetch(user_db, user_id) do
    with {:ok, user} <- Map.fetch(user_db, user_id),
         {:ok, true} <- {:ok, user.active?},
         {:ok, token} <- {:ok, "TOKEN_#{user.name}_99"} do
      {:ok, token}
    else
      :error -> {:error, :user_not_found}
      {:ok, false} -> {:error, :account_disabled}
    end
  end
end

IO.puts("==========================================")
IO.puts("  ☆ Elixir Pattern Matching Control Flow ☆")
IO.puts("==========================================")

# Testing Function Clauses
admin_user = %{name: "Melody", role: :admin}
normal_user = %{name: "Alex", role: :member}

IO.puts(PatternDemo.greet(admin_user))
IO.puts(PatternDemo.greet(normal_user))
IO.puts(PatternDemo.greet(%{}))

# Testing Guard Clauses
IO.puts("\n--- Guard Clauses ---")
IO.puts("Age 21 Category: #{inspect(PatternDemo.classify_age(21))}")
IO.puts("Age 14 Category: #{inspect(PatternDemo.classify_age(14))}")

# Testing Case Expression
IO.puts("\n--- Case Statement ---")
IO.puts(PatternDemo.handle_response({:ok, "User Data Payload"}))
IO.puts(PatternDemo.handle_response({:error, :not_found}))
IO.puts(PatternDemo.handle_response({:error, :timeout}))

# Testing 'with' Chain
db = %{
  1 => %{name: "Melody", active?: true},
  2 => %{name: "Bob", active?: false}
}

IO.puts("\n--- 'with' Pipeline ---")
IO.puts("User 1 Auth: #{inspect(PatternDemo.authenticate_and_fetch(db, 1))}")
IO.puts("User 2 Auth: #{inspect(PatternDemo.authenticate_and_fetch(db, 2))}")
IO.puts("User 3 Auth: #{inspect(PatternDemo.authenticate_and_fetch(db, 3))}")

IO.puts("\nPattern matching control flow example executed successfully!")
