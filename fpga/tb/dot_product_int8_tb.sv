`timescale 1ns/1ps

module dot_product_int8_tb;
    logic clk = 1'b0;
    logic rst_n = 1'b0;
    logic valid_in = 1'b0;
    logic signed [7:0] a0 = 0, a1 = 0, a2 = 0, a3 = 0;
    logic signed [7:0] w0 = 0, w1 = 0, w2 = 0, w3 = 0;
    logic signed [17:0] result;
    logic valid_out;
    integer signed expected = 0;
    integer checked = 0;
    integer signed rng = 32'h2468ace1;
    integer signed vectors [0:7];
    integer index;
    integer lane;

    dot_product_int8 dut (.*);
    always #5 clk = ~clk;

    task automatic apply_case(
        input integer signed x0, x1, x2, x3,
        input integer signed y0, y1, y2, y3,
        input logic next_valid
    );
        begin
            @(negedge clk);
            a0 = x0; a1 = x1; a2 = x2; a3 = x3;
            w0 = y0; w1 = y1; w2 = y2; w3 = y3;
            valid_in = next_valid;
            if (next_valid)
                expected = x0*y0 + x1*y1 + x2*y2 + x3*y3;
            @(posedge clk);
            #1;
            checked = checked + 1;
            if (result !== expected || valid_out !== next_valid)
                $fatal(1, "Case %0d: result=%0d expected=%0d valid_out=%0b expected_valid=%0b",
                       checked, result, expected, valid_out, next_valid);
        end
    endtask

    initial begin
        $dumpfile("fpga/waveforms/dot_product_int8.vcd");
        $dumpvars(0, dot_product_int8_tb);
        repeat (2) @(posedge clk);
        #1;
        if (result !== 0 || valid_out !== 0)
            $fatal(1, "Reset failed");
        @(negedge clk);
        rst_n = 1'b1;

        apply_case(1, 2, 3, 4, 5, 6, 7, 8, 1);              // 70
        apply_case(-1, 2, -3, 4, 5, -6, 7, -8, 1);          // mixed signs
        apply_case(0, 0, 0, 0, -128, 127, -1, 1, 1);        // zero
        apply_case(-128, -128, -128, -128, -128, -128, -128, -128, 1);
        apply_case(-128, -128, -128, -128, 127, 127, 127, 127, 1);
        apply_case(127, 127, 127, 127, 127, 127, 127, 127, 1);
        apply_case(9, 9, 9, 9, 9, 9, 9, 9, 0);              // hold result

        // Independent integer reference over a repeatable pseudo-random sequence.
        for (index = 0; index < 500; index = index + 1) begin
            for (lane = 0; lane < 8; lane = lane + 1) begin
                rng = rng * 32'sd1664525 + 32'sd1013904223;
                vectors[lane] = ((rng >> 16) & 255) - 128;
            end
            apply_case(vectors[0], vectors[1], vectors[2], vectors[3],
                       vectors[4], vectors[5], vectors[6], vectors[7], 1);
        end

        @(negedge clk);
        rst_n = 1'b0;
        #1;
        if (result !== 0 || valid_out !== 0)
            $fatal(1, "Asynchronous reset failed");
        $display("PASS: %0d dot-product cases plus reset checks", checked);
        $finish;
    end
endmodule
