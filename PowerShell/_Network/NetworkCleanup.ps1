# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: PowerShell
# ☆ File Name: NetworkCleanup.ps1
# ☆ Date: 2026-01-24
# ☆
# ☆ Description: Flushes DNS, resets Winsock, and clears IP caches.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

Write-Host "Starting Network Cache Cleanup..." -ForegroundColor Cyan

# Flush DNS Resolver Cache
ipconfig /flushdns

# Release and Renew IP Address
ipconfig /release
ipconfig /renew

# Reset Winsock Catalog and IP Stack
netsh winsock reset
netsh int ip reset

# Clear ARP Table
arp -d *

Write-Host "Cleanup complete. A system restart is recommended for changes to take effect." -ForegroundColor Green
