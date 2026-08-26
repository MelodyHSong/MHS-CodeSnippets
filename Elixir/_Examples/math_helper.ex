# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Elixir
# ☆ File Name: math_helper.ex
# ☆ Date: 2026-08-25
# ☆
# ☆ Description: Reusable math utility module providing number clamping,
# ☆              linear interpolation (lerp), range mapping, and 2D distance.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

defmodule MathHelper do
  @moduledoc """
  Provides mathematical helper utilities for clamping, linear interpolation,
  range mapping, and 2D geometry calculations.
  """

  @doc """
  Clamps a value between a minimum and maximum boundary.
  """
  def clamp(val, min_val, max_val) when val < min_val, do: min_val
  def clamp(val, min_val, max_val) when val > max_val, do: max_val
  def clamp(val, _min_val, _max_val), do: val

  @doc """
  Performs linear interpolation between `start_val` and `end_val` using factor `t` (0.0 to 1.0).
  """
  def lerp(start_val, end_val, t) do
    t_clamped = clamp(t, 0.0, 1.0)
    start_val + (end_val - start_val) * t_clamped
  end

  @doc """
  Maps a numeric value from an input range to an output range.
  """
  def map_range(val, in_min, in_max, out_min, out_max) do
    if in_max == in_min do
      out_min
    else
      progress = (val - in_min) / (in_max - in_min)
      lerp(out_min, out_max, progress)
    end
  end

  @doc """
  Calculates the 2D Euclidean distance between two points {x1, y1} and {x2, y2}.
  """
  def distance_2d({x1, y1}, {x2, y2}) do
    dx = x2 - x1
    dy = y2 - y1
    :math.sqrt(dx * dx + dy * dy)
  end
end
