#☆
#☆ Author: ✩ MelodyHSong ✩
#☆ Language: Elixir
#☆ File Name: resilient_counter.exs
#☆ Date: 2025-10-30
#☆ "Oh how I HATE coding Elixir." - Melody H. Song
#☆

# --- 1. THE WORKER (The component designed to perform division and crash) ---
defmodule DivisionWorker do
  # Agent is used to simply hold the state of the divisor (the number we divide by).
  use Agent

  @initial_divisor -10 # START: We now start the divisor at -10
  @crash_point 0       # The divisor that causes the crash

  # Starts the Worker process with an initial divisor
  def start_link(init_arg \\ @initial_divisor) do
    # Prints when the process starts (or restarts)
    IO.puts("--- Worker Started/Restarted. Divisor set to #{init_arg}")
    # The initial state function is called here to set the Agent's state.
    Agent.start_link(fn -> init_arg end, name: __MODULE__)
  end

  # Public API to reset the worker's internal state (used after a crash)
  def reset_state(new_divisor) do
    # Agent.update is used to safely change the worker's state.
    Agent.update(__MODULE__, fn _ -> new_divisor end)
    IO.puts("Client: Worker state manually reset to #{new_divisor} for sequence continuation.")
  end

  # Public API to perform division
  def divide(numerator) do
    # Agent.get_and_update is used to safely read and update the process state.
    Agent.get_and_update(__MODULE__, fn divisor ->

      # Use an 'if' block to check for the intentional crash condition.
      if divisor == @crash_point do
        # Prints before the crash happens
        IO.puts("--- CRASH EVENT: Division by Zero! (Divisor was #{@crash_point})")
        # This causes the Worker process to CRASH.
        raise "CRASHING: Attempted division by zero!"
      else
        # Success: Calculate the result, and set the NEW divisor for the next run.
        result = numerator / divisor

        # The return value is {value_to_return_to_client, new_state_for_agent}
        # NEW LOGIC: The new state is divisor + 1 to count upwards.
        {result, divisor + 1}
      end
    end)
  end
end


# --- 2. THE SUPERVISOR (The component that ensures recovery) ---
defmodule AppSupervisor do
  use Supervisor

  @initial_divisor -10 # Re-declare for clean module access

  def start_link(init_arg) do
    Supervisor.start_link(__MODULE__, init_arg, name: __MODULE__)
  end

  @impl true
  def init(_init_arg) do
    children = [
      %{
        id: DivisionWorker,
        # Access @initial_divisor correctly in the start specification
        start: {DivisionWorker, :start_link, [@initial_divisor]}
      }
    ]

    # The strategy :one_for_one ensures only the failed process is replaced.
    Supervisor.init(children, strategy: :one_for_one)
  end
end


# --- 3. EXECUTION SIMULATION (Client Code) ---

# Start the supervisor, which initializes the DivisionWorker with divisor -10
AppSupervisor.start_link(:ok)

# CRITICAL: Sleep briefly to allow the Supervisor and Agent to fully initialize.
Process.sleep(100)

numerator = 100.0 # Use float to match Elixir's division output

IO.puts("\n--- Simulation: Crash & Recovery (-10 to 0, then 1 to 10) ---")
IO.puts("Target: Crash at 0, Restart at 1, Continue to 10.")

# We need 23 iterations to cover the full run from -10 to 0 (11 steps) and the subsequent run
# from 1 to 10 (10 steps) with some safety margin for the crash/restart.
Enum.each(1..23, fn i ->

  # We call the crashing function DIRECTLY, isolating it in a try/catch block.
  try do
    result = DivisionWorker.divide(numerator)
    # The current divisor is the iteration number minus 10 (approximate).
    IO.puts("Iteration #{i}: Result = #{result}")
  catch
    # This block handles the exit signal from the crashing worker.
    :exit, _ ->
      IO.puts("Client: Crash signal received and suppressed. Supervisor handled restart.")
      # The supervisor restarts the worker back to -10, but we immediately fix the state.
      Process.sleep(100)

      # *** CRITICAL RECOVERY STEP ***
      # We call the new function to reset the state to 1, effectively skipping the negative numbers.
      DivisionWorker.reset_state(1)
  end
end)
