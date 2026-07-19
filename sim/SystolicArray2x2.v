// ============================================================
// SystolicArray2x2.v - Top module: luoi 4 PE cho phep nhan
// ma tran 2x2 (C = A x B)
// ------------------------------------------------------------
//        b_in0        b_in1
//           |            |
// a_in0--[PE00]------[PE01]
//           |            |
// a_in1--[PE10]------[PE11]
//
// - a_in0, a_in1 : bien vao cho hang 0 va hang 1 cua A
// - b_in0, b_in1 : bien vao cho cot 0 va cot 1 cua B
// - Testbench chiu trach nhiem "lam le" (skew) du lieu theo
//   dung 4 chu ky t0..t3 da phan tich (xem test bench ben duoi)
// ============================================================
module SystolicArray2x2 (
    input  wire              clk,
    input  wire              rst,
    input  wire              clear_acc,
    input  wire signed [7:0] a_in0,
    input  wire signed [7:0] a_in1,
    input  wire signed [7:0] b_in0,
    input  wire signed [7:0] b_in1,
    output wire signed [16:0] C00,
    output wire signed [16:0] C01,
    output wire signed [16:0] C10,
    output wire signed [16:0] C11
);

    wire signed [7:0] pe00_a_out, pe00_b_out;
    wire signed [7:0] pe01_b_out;
    wire signed [7:0] pe10_a_out;

    // PE00: nhan truc tiep tu bien (a_in0, b_in0)
    PE pe00 (
        .clk(clk), .rst(rst), .clear_acc(clear_acc),
        .a_in(a_in0), .b_in(b_in0),
        .a_out(pe00_a_out), .b_out(pe00_b_out),
        .sum_out(C00)
    );

    // PE01: a lay tu PE00 (chay ngang), b lay tu bien cot 1
    PE pe01 (
        .clk(clk), .rst(rst), .clear_acc(clear_acc),
        .a_in(pe00_a_out), .b_in(b_in1),
        .a_out(), .b_out(pe01_b_out),
        .sum_out(C01)
    );

    // PE10: a lay tu bien hang 1, b lay tu PE00 (chay doc)
    PE pe10 (
        .clk(clk), .rst(rst), .clear_acc(clear_acc),
        .a_in(a_in1), .b_in(pe00_b_out),
        .a_out(pe10_a_out), .b_out(),
        .sum_out(C10)
    );

    // PE11: a lay tu PE10, b lay tu PE01 (xa bien nhat -> xong tre nhat)
    PE pe11 (
        .clk(clk), .rst(rst), .clear_acc(clear_acc),
        .a_in(pe10_a_out), .b_in(pe01_b_out),
        .a_out(), .b_out(),
        .sum_out(C11)
    );

endmodule
