# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: 04_modules.exs
# ☆ Date: 2026-08-25
# ☆
# ☆ Description: Demonstrates loading and invoking functions from an external
# ☆              Elixir module file (math_helper.ex).
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

# Load and compile the math_helper.ex module relative to this file
Code.require_file("math_helper.ex", __DIR__)

IO.puts("==========================================")
IO.puts("  ☆ Elixir Module Import & Usage ☆")
IO.puts("==========================================")

# 1. Clamp Test
raw_val = 145
clamped_val = MathHelper.clamp(raw_val, 0, 100)
IO.puts("Clamp(#{raw_val}, 0, 100) => #{clamped_val}")

# 2. Lerp Step Progression Test
start_val = 10.0
end_val = 50.0

IO.puts("\n--- Lerp Step Progression ---")
for step <- 0..4 do
  factor = step / 4.0
  current = MathHelper.lerp(start_val, end_val, factor)
  IO.puts("  Factor #{Float.round(factor, 2)} : Lerp(#{start_val}, #{end_val}) => #{Float.round(current, 2)}")
end

# 3. Range Mapping Test (mapping CPU load 0-100% to fan speed 1000-4000 RPM)
cpu_load = 72.5
fan_rpm = MathHelper.map_range(cpu_load, 0.0, 100.0, 1000.0, 4000.0)
IO.puts("\nCPU Load (#{cpu_load}%) -> Target Fan Speed: #{Float.round(fan_rpm, 0)} RPM")

# 4. 2D Distance Test
p1 = {0.0, 0.0}
p2 = {3.0, 4.0}
dist = MathHelper.distance_2d(p1, p2)
IO.puts("\nDistance between #{inspect(p1)} and #{inspect(p2)} => #{Float.round(dist, 2)}")

IO.puts("\nModule example executed successfully!")
