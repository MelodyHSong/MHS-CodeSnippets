# ☆ Network Cleanup (PowerShell) ☆

> "Because sometimes your internet just needs to forget its ex-connections."

A robust PowerShell script designed to perform a deep-clean of the Windows network stack. This tool is perfect for resolving stubborn "No Internet" errors, DNS resolution failures, and stale routing tables by resetting the Sockets API and TCP/IP stack.

## ☆ Installation & Prerequisites

This script requires Administrative privileges to modify system-level network settings.

### Quick Install

1. Copy the code into a text editor (like Notepad or VS Code).
2. Save the file as `NetworkCleanup.ps1`.
3. Ensure your PowerShell Execution Policy allows scripts by running `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` in a PowerShell terminal.

## ☆ Usage

Right-click the script and select **Run with PowerShell**. You will be prompted by User Account Control (UAC) for Administrator permissions.

###	Example Usage

```powershell
.\NetworkCleanup.ps1
```
## ☆ License

This project is licensed under the MIT License. You are free to use, modify, and distribute this code in your own projects—just keep the headers intact!

---

*Turning it off and on again, but with more flair— MelodyHSong*
