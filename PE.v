// ============================================================
// PE.v - Processing Element (Multiply-Accumulate unit)
// Dung cho Systolic Array 2x2 - FAP201
// ------------------------------------------------------------
// Moi chu ky clock:
//   - Nhan a_in * b_in (2 so 8-bit co dau)
//   - Cong don ket qua vao sum_out (17-bit co dau, chong tran)
//   - Day a_in ra a_out, b_in ra b_out cho PE ben canh (o chu ky sau)
// clear_acc = 1 : xoa sum_out ve 0 (dung truoc khi bat dau 1 phep
//                 nhan ma tran moi)
// ============================================================
module PE (
    input  wire              clk,
    input  wire              rst,
    input  wire              clear_acc,
    input  wire signed [7:0] a_in,
    input  wire signed [7:0] b_in,
    output reg  signed [7:0] a_out,
    output reg  signed [7:0] b_out,
    output reg  signed [16:0] sum_out
);

    // 8-bit x 8-bit (co dau) = 16-bit (co dau)
    wire signed [15:0] mult_result;
    assign mult_result = a_in * b_in;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            a_out   <= 8'sd0;
            b_out   <= 8'sd0;
            sum_out <= 17'sd0;
        end else begin
            // Day du lieu sang PE ke tiep (systolic flow)
            a_out <= a_in;
            b_out <= b_in;

            // Cong don (mo rong dau 16-bit -> 17-bit truoc khi cong)
            if (clear_acc)
                sum_out <= 17'sd0;
            else
                sum_out <= sum_out + {mult_result[15], mult_result};
        end
    end

endmodule
