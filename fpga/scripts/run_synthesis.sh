#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p fpga/build

for top in mac_int8 dot_product_int8; do
  yosys -Q -T -l "fpga/build/${top}_synthesis.log" -p \
    "read_verilog -sv fpga/rtl/${top}.sv; hierarchy -check -top ${top}; proc; opt; stat; synth -top ${top}; stat" \
    > /dev/null
  echo "Generic synthesis completed: ${top}"
  tail -n 23 "fpga/build/${top}_synthesis.log"
done
