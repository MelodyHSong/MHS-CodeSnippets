# ☆ Lua Code Snippets ☆

> "Lightweight, fast, and ready to embed!"

Welcome to the **Lua Code Snippets** directory! This collection contains reusable Lua scripts, algorithms, and modular logic patterns designed for game development, desktop scripting, and embedded environment integrations.

## ☆ Installation & Prerequisites

To run or test these scripts, ensure you have a Lua environment installed or a compatible host application/engine.

### Quick Install

- **Standalone Interpreter**: Download and install Lua (Lua 5.1+, LuaJIT, or Lua 5.4) from [lua.org](https://www.lua.org/).
  ```bash
  # Windows (via Scoop or Chocolatey)
  scoop install lua
  # or
  choco install lua
  ```
- **Supported Environments & Editors**:
  - **Visual Studio Code** (with *Lua* by sumneko / Lua Language Server)
  - **Roblox Studio** / **LÖVE 2D** / **Solar2D** (for game scripting)
  - **Neovim** / **Visual Studio 2022**

## ☆ Folder Structure

* **_Examples**: Introductory Lua scripts demonstrating syntax basics, table operations, OOP metatables, and modular `require()` logic.

## ☆ Usage

Browse the subdirectories to find specific implementations and helper utilities. Most modules are structured to be easily included or required in your custom projects.

### Example Usage

Running a standalone Lua script:
```bash
lua script_name.lua
```

Importing a module within your own code:
```lua
local Utility = require("utility_module")
Utility.doSomething()
```

## ☆ License

This project is licensed under the MIT License. You are free to use, modify, and distribute this code in your own projects— just keep the headers intact!

---

*Remember: arrays start at 1! — MelodyHSong*
