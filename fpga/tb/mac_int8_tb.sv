`timescale 1ns/1ps

module mac_int8_tb;
    logic clk = 1'b0;
    logic rst_n = 1'b0;
    logic clear = 1'b0;
    logic valid_in = 1'b0;
    logic signed [7:0] a = 8'sd0;
    logic signed [7:0] b = 8'sd0;
    logic signed [31:0] accumulator;
    logic valid_out;
    integer signed expected = 0;
    integer checked = 0;
    integer signed rng = 32'h13579bdf;
    integer signed random_a;
    integer signed random_b;
    integer index;

    mac_int8 dut (.*);
    always #5 clk = ~clk;

    task automatic apply_case(
        input integer signed next_a,
        input integer signed next_b,
        input logic next_valid,
        input logic next_clear
    );
        begin
            @(negedge clk);
            a = next_a;
            b = next_b;
            valid_in = next_valid;
            clear = next_clear;
            if (next_clear)
                expected = 0;
            else if (next_valid)
                expected = expected + next_a * next_b;
            @(posedge clk);
            #1;
            checked = checked + 1;
            if (accumulator !== expected || valid_out !== (next_valid && !next_clear))
                $fatal(1, "Case %0d: a=%0d b=%0d valid=%0b clear=%0b: acc=%0d expected=%0d valid_out=%0b",
                       checked, next_a, next_b, next_valid, next_clear,
                       accumulator, expected, valid_out);
        end
    endtask

    initial begin
        $dumpfile("fpga/waveforms/mac_int8.vcd");
        $dumpvars(0, mac_int8_tb);
        repeat (2) @(posedge clk);
        #1;
        if (accumulator !== 0 || valid_out !== 0)
            $fatal(1, "Reset failed");
        @(negedge clk);
        rst_n = 1'b1;

        apply_case(3, 4, 1, 0);           // positive product
        apply_case(-5, 7, 1, 0);          // negative product and accumulation
        apply_case(-6, -8, 1, 0);         // two negative operands
        apply_case(0, -128, 1, 0);        // zero
        apply_case(-128, -128, 1, 0);     // largest positive INT8 product
        apply_case(-128, 127, 1, 0);      // most negative INT8 product
        apply_case(127, 127, 1, 0);       // positive boundary
        apply_case(19, -23, 0, 0);        // invalid input must hold the sum
        apply_case(9, 9, 1, 1);           // clear has priority over valid
        apply_case(-1, 1, 1, 0);

        // A fixed linear congruential sequence makes the vectors reproducible.
        for (index = 0; index < 500; index = index + 1) begin
            rng = rng * 32'sd1664525 + 32'sd1013904223;
            random_a = ((rng >> 16) & 255) - 128;
            rng = rng * 32'sd1664525 + 32'sd1013904223;
            random_b = ((rng >> 16) & 255) - 128;
            apply_case(random_a, random_b, 1, 0);
        end

        @(negedge clk);
        rst_n = 1'b0;
        #1;
        if (accumulator !== 0 || valid_out !== 0)
            $fatal(1, "Asynchronous reset failed");
        $display("PASS: %0d MAC cases plus reset checks", checked);
        $finish;
    end
endmodule
