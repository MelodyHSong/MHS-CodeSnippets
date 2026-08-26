# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: 02_pipe_and_enum.exs
# ☆ Date: 2026-08-25
# ☆
# ☆ Description: Demonstrates functional pipelines with the pipe operator (|>)
# ☆              and standard collection operations using the Enum module.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

IO.puts("==========================================")
IO.puts("  ☆ Elixir Pipe Operator & Enum Module ☆")
IO.puts("==========================================")

# 1. Functional Data Pipeline using |>
scores = [45, 88, 92, 60, 75, 100, 32]

processed_scores =
  scores
  |> Enum.filter(fn score -> score >= 60 end)
  |> Enum.map(fn score -> score + 5 end)
  |> Enum.sort(:desc)

IO.puts("Original Scores:  #{inspect(scores)}")
IO.puts("Processed Scores: #{inspect(processed_scores)} (Filtered >=60, +5 bonus, sorted desc)")

# 2. Aggregations with Enum.reduce
total_sum = Enum.reduce(processed_scores, 0, fn score, acc -> acc + score end)
average = total_sum / length(processed_scores)

IO.puts("\n--- Score Statistics ---")
IO.puts("Total Sum: #{total_sum}")
IO.puts("Average:   #{Float.round(average, 2)}")

# 3. String Processing Pipeline
raw_input = "   elixir, functional, concurrent, fault-tolerant   "

tags =
  raw_input
  |> String.trim()
  |> String.split(",")
  |> Enum.map(&String.trim/1)
  |> Enum.map(&String.capitalize/1)

IO.puts("\n--- Tag Processing Pipeline ---")
IO.puts("Raw String: \"#{raw_input}\"")
IO.puts("Parsed Tags: #{inspect(tags)}")

IO.puts("\nPipe and Enum example executed successfully!")
