@echo off
:: ☆ Author: ☆ MelodyHSong ☆
:: ☆ Language: Batch
:: ☆ File Name: NetworkCleanup.bat

echo Flushing Network Caches...

ipconfig /flushdns
ipconfig /registerdns
ipconfig /release
ipconfig /renew
netsh winsock reset
netsh int ip reset
arp -d *
nbtstat -R
nbtstat -RR

echo Done! Please restart your computer.
pause