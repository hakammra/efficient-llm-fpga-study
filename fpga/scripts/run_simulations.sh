#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p fpga/build fpga/waveforms

iverilog -g2012 -Wall -s mac_int8_tb -o fpga/build/mac_int8.vvp \
  fpga/rtl/mac_int8.sv fpga/tb/mac_int8_tb.sv
vvp fpga/build/mac_int8.vvp | tee fpga/build/mac_simulation.log

iverilog -g2012 -Wall -s dot_product_int8_tb -o fpga/build/dot_product_int8.vvp \
  fpga/rtl/dot_product_int8.sv fpga/tb/dot_product_int8_tb.sv
vvp fpga/build/dot_product_int8.vvp | tee fpga/build/dot_product_simulation.log
