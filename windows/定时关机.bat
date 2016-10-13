@echo off
set /p time=倒数关机秒数:
Shutdown -s -t %time%
pause
exit