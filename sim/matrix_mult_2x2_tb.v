// ============================================================
// matrix_mult_2x2_tb.v
// ------------------------------------------------------------
// Flow dung theo yeu cau cua thay (post-processing verification):
//   1) Python tao input_vectors.txt (chi chua A, B - KHONG co dap an)
//   2) Testbench nay doc file, dua A,B vao SystolicArray2x2 theo
//      dung lich "do lech" (skewing) t0..t3, ghi ket qua C ra
//      modelsim_output.txt
//   3) Python doc modelsim_output.txt, tu tinh lai A*B, so sanh
// ============================================================
`timescale 1ns/1ps

module matrix_mult_2x2_tb;

    reg clk;
    reg rst;
    reg clear_acc;
    reg signed [7:0] a_in0, a_in1, b_in0, b_in1;
    wire signed [16:0] C00, C01, C10, C11;

    integer infile, outfile;
    integer scan_ok;
    integer A00,A01,A10,A11,B00,B01,B10,B11;
    integer test_num;

    SystolicArray2x2 dut (
        .clk(clk), .rst(rst), .clear_acc(clear_acc),
        .a_in0(a_in0), .a_in1(a_in1), .b_in0(b_in0), .b_in1(b_in1),
        .C00(C00), .C01(C01), .C10(C10), .C11(C11)
    );

    // Clock 10ns / chu ky
    always #5 clk = ~clk;

    // Chay 1 phep nhan hoan chinh cho 1 cap ma tran A,B
    task run_one_matrix;
        input signed [7:0] a00,a01,a10,a11;
        input signed [7:0] b00,b01,b10,b11;
        begin
            // --- Reset + xoa accumulator truoc khi bat dau ---
            rst = 1; clear_acc = 1;
            a_in0 = 0; a_in1 = 0; b_in0 = 0; b_in1 = 0;
            @(posedge clk);
            rst = 0;
            @(posedge clk);
            clear_acc = 0;

            // --- t0: bom A00, B00 ---
            a_in0 = a00; a_in1 = 0;
            b_in0 = b00; b_in1 = 0;
            @(posedge clk);

            // --- t1: bom A01,A10 va B10,B01 (dung cheo) ---
            a_in0 = a01; a_in1 = a10;
            b_in0 = b10; b_in1 = b01;
            @(posedge clk);

            // --- t2: bom A11, B11 ---
            a_in0 = 0;   a_in1 = a11;
            b_in0 = 0;   b_in1 = b11;
            @(posedge clk);

            // --- t3: khong bom them, cho du lieu cuoi lan het luoi ---
            a_in0 = 0; a_in1 = 0;
            b_in0 = 0; b_in1 = 0;
            @(posedge clk);

            // 1 canh du phong de dam bao gia tri da on dinh
            @(posedge clk);
        end
    endtask

    initial begin
        clk = 0;
        test_num = 0;

        infile  = $fopen("input_vectors.txt", "r");
        outfile = $fopen("modelsim_output.txt", "w");

        if (infile == 0) begin
            $display("LOI: khong mo duoc input_vectors.txt");
            $finish;
        end

        while (!$feof(infile)) begin
            scan_ok = $fscanf(infile, "%d %d %d %d %d %d %d %d\n",
                               A00, A01, A10, A11, B00, B01, B10, B11);
            if (scan_ok == 8) begin
                test_num = test_num + 1;
                run_one_matrix(A00[7:0], A01[7:0], A10[7:0], A11[7:0],
                                B00[7:0], B01[7:0], B10[7:0], B11[7:0]);

                $fwrite(outfile, "%0d %0d %0d %0d\n", C00, C01, C10, C11);

                $display("TEST %0d | A=[%0d,%0d;%0d,%0d] B=[%0d,%0d;%0d,%0d] => C=[%0d,%0d;%0d,%0d]",
                          test_num, A00,A01,A10,A11, B00,B01,B10,B11, C00,C01,C10,C11);
            end
        end

        $fclose(infile);
        $fclose(outfile);
        $display("=================================================");
        $display("Mo phong xong. Da xu ly %0d test case.", test_num);
        $display("Ket qua da ghi vao modelsim_output.txt");
        $display("=================================================");
        $finish;
    end

endmodule
