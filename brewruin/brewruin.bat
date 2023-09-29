@echo off
echo Brew Ruin / build 1.00
echo ----------------------
echo Installing libraries...
echo Installing Requests Library & py -m pip install -qq requests
echo Installing Websockets Library & py -m pip install -qq websockets
echo Installing Asyncio Library & py -m pip install -qq asyncio
echo ----------------------
echo Running BrewRuin
timeout 2
py bin/src.py