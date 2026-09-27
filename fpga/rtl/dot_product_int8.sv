// Four signed INT8 products are formed in parallel and summed in one cycle.
module dot_product_int8 (
    input  logic               clk,
    input  logic               rst_n,
    input  logic               valid_in,
    input  logic signed [7:0]  a0,
    input  logic signed [7:0]  a1,
    input  logic signed [7:0]  a2,
    input  logic signed [7:0]  a3,
    input  logic signed [7:0]  w0,
    input  logic signed [7:0]  w1,
    input  logic signed [7:0]  w2,
    input  logic signed [7:0]  w3,
    output logic signed [17:0] result,
    output logic               valid_out
);
    logic signed [15:0] p0, p1, p2, p3;
    logic signed [16:0] pair01, pair23;
    logic signed [17:0] sum;

    assign p0 = a0 * w0;
    assign p1 = a1 * w1;
    assign p2 = a2 * w2;
    assign p3 = a3 * w3;
    assign pair01 = {p0[15], p0} + {p1[15], p1};
    assign pair23 = {p2[15], p2} + {p3[15], p3};
    assign sum = {pair01[16], pair01} + {pair23[16], pair23};

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            result <= 18'sd0;
            valid_out <= 1'b0;
        end else begin
            valid_out <= valid_in;
            if (valid_in)
                result <= sum;
        end
    end
endmodule
