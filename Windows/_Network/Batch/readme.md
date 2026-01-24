# ☆ Network Cleanup (Batch) ☆

> "Refreshing your network like a cold glass of water on a humid Puerto Rican afternoon."

A lightweight, "double-click and done" Batch script for clearing network caches. It targets the DNS resolver, NetBIOS cache, and ARP table to ensure your PC isn't holding onto outdated or corrupt routing information.

## ☆ Installation & Prerequisites

No installation is required. This script runs natively on any Windows machine using the Command Prompt (CMD) interface.

### Quick Install

1. Copy the Batch code into Notepad.
2. Save the file with the extension `.bat` (e.g., `NetFix.bat`).

## ☆ Usage

To ensure the `netsh` and `arp` commands execute correctly, you must **Right-click the file and select "Run as Administrator."**

###	Example Usage

Double-click the file to run. The command window will remain open after completion so you can review the results before pressing any key to exit.

## ☆ License

This project is licensed under the MIT License. You are free to use, modify, and distribute this code in your own projects—just keep the headers intact!

---

*I'd tell you a DNS joke, but it might take 24 hours to propagate, by MelodyHSong*