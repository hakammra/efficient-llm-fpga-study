// One signed INT8 multiply-accumulate operation per accepted clock edge.
module mac_int8 (
    input  logic               clk,
    input  logic               rst_n,
    input  logic               clear,
    input  logic               valid_in,
    input  logic signed [7:0]  a,
    input  logic signed [7:0]  b,
    output logic signed [31:0] accumulator,
    output logic               valid_out
);
    logic signed [15:0] product;
    assign product = a * b;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            accumulator <= 32'sd0;
            valid_out <= 1'b0;
        end else if (clear) begin
            accumulator <= 32'sd0;
            valid_out <= 1'b0;
        end else begin
            valid_out <= valid_in;
            if (valid_in)
                accumulator <= accumulator + {{16{product[15]}}, product};
        end
    end
endmodule
