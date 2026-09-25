@echo off
setlocal
cd /d "%~dp0..\.."
where iverilog >nul 2>nul
if errorlevel 1 (
    echo Icarus Verilog is not on PATH. See fpga\README.md for setup.
    exit /b 1
)
where vvp >nul 2>nul
if errorlevel 1 (
    echo vvp is not on PATH. See fpga\README.md for setup.
    exit /b 1
)
if not exist "fpga\build" mkdir "fpga\build"
iverilog -g2012 -Wall -s mac_int8_tb -o "fpga\build\mac_int8.vvp" "fpga\rtl\mac_int8.sv" "fpga\tb\mac_int8_tb.sv"
if errorlevel 1 exit /b 1
vvp "fpga\build\mac_int8.vvp"
if errorlevel 1 exit /b 1
echo Waveform: fpga\waveforms\mac_int8.vcd
