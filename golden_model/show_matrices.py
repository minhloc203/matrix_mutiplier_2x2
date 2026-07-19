# ============================================================
# show_matrices.py
# ------------------------------------------------------------
# Doc input_vectors.txt + modelsim_output.txt + test_case_names.txt
# roi in ra man hinh duoi dang ma tran 2x2 de nhin cho de,
# thay vi 1 dong so dai ngoang.
#
# Vi du hien thi cho 1 test case:
#
#   TEST 4: Ca hai ma tran deu toan so am
#   ---------------------------------------
#     A =            B =
#     [ -1  -2 ]     [ -5  -6 ]
#     [ -3  -4 ]     [ -7  -8 ]
#
#     C (ket qua tu Verilog) =
#     [ 19  22 ]
#     [ 43  50 ]
# ============================================================
import os


def read_lines(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def fmt_matrix_2x2(vals, width=6):
    """vals: list 4 phan tu -> tra ve list 2 dong dang '[ a  b ]'."""
    m00, m01, m10, m11 = vals
    row0 = f"[ {m00:>{width}} {m01:>{width}} ]"
    row1 = f"[ {m10:>{width}} {m11:>{width}} ]"
    return row0, row1


def print_side_by_side(title_a, rows_a, title_b, rows_b, gap=4):
    width_a = max(len(title_a), len(rows_a[0]), len(rows_a[1]))
    print(f"  {title_a.ljust(width_a)}{' ' * gap}{title_b}")
    print(f"  {rows_a[0].ljust(width_a)}{' ' * gap}{rows_b[0]}")
    print(f"  {rows_a[1].ljust(width_a)}{' ' * gap}{rows_b[1]}")


def main():
    in_lines = read_lines("input_vectors.txt")
    out_lines = read_lines("modelsim_output.txt")
    name_lines = read_lines("test_case_names.txt")

    if in_lines is None:
        print("Khong tim thay input_vectors.txt. Hay chay gen_test_vectors.py truoc.")
        return

    n = len(in_lines)
    has_output = out_lines is not None and len(out_lines) == n
    if out_lines is not None and len(out_lines) != n:
        print(f"CANH BAO: so dong modelsim_output.txt ({len(out_lines)}) "
              f"khac input_vectors.txt ({n}) -> bo qua hien thi ket qua C.\n")

    for i in range(n):
        vals = list(map(int, in_lines[i].split()))
        A = vals[0:4]
        B = vals[4:8]
        name = name_lines[i] if name_lines and i < len(name_lines) else f"Test {i+1}"

        print("=" * 60)
        print(f"TEST {i+1}: {name}")
        print("-" * 60)

        rows_a = fmt_matrix_2x2(A)
        rows_b = fmt_matrix_2x2(B)
        print_side_by_side("A =", rows_a, "B =", rows_b)

        if has_output:
            C = list(map(int, out_lines[i].split()))
            rows_c = fmt_matrix_2x2(C, width=8)
            print()
            print("  C (ket qua tu Verilog, C = A x B) =")
            print(f"  {rows_c[0]}")
            print(f"  {rows_c[1]}")
        print()

    print("=" * 60)
    print(f"Tong cong: {n} test case")
    if not has_output:
        print("(Chua co modelsim_output.txt -> chi hien thi input A, B."
              " Chay ModelSim xong roi chay lai script nay de xem ca C.)")


if __name__ == "__main__":
    main()
