# ☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: concurrency.ex
# ☆ Date: 2025-10-18
# ☆

# Elixir's concurrency is based on the Actor Model. "Actors" are lightweight processes
# that are completely isolated from each other.

# We define the work we want to do concurrently as an anonymous function.

task = fn -> IO.puts("Hello from another process!") end


# `spawn` takes a function and runs it in a new, lightweight process.
# This happens immediately and does not block the main process.
# It returns a Process ID (PID), which is a reference to the new process.

spawn(task)


# The main script might finish before the spawned process gets a chance to run.
# So, we pause the main process for 100 milliseconds to give the other one time.

Process.sleep(100)

IO.puts("Hello from the main process!")
