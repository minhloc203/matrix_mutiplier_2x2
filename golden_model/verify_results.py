# ============================================================
# verify_results.py
# ------------------------------------------------------------
# Buoc 3 trong flow thay yeu cau:
#   Doc input_vectors.txt (A, B) + modelsim_output.txt (C tu Verilog)
#   Tu tinh lai C_expected = A @ B bang numpy (golden model)
#   So sanh voi C tu Verilog -> in PASS / FAIL cho tung test case
# ============================================================
import numpy as np
import sys


def read_inputs(path):
    cases = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            vals = list(map(int, line.split()))
            if len(vals) != 8:
                print(f"CANH BAO: dong khong hop le trong {path}: {line}")
                continue
            A = np.array(vals[0:4]).reshape(2, 2)
            B = np.array(vals[4:8]).reshape(2, 2)
            cases.append((A, B))
    return cases


def read_outputs(path):
    outs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            vals = list(map(int, line.split()))
            if len(vals) != 4:
                print(f"CANH BAO: dong khong hop le trong {path}: {line}")
                continue
            C = np.array(vals).reshape(2, 2)
            outs.append(C)
    return outs


def read_names(path):
    try:
        with open(path) as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return None


def main():
    inputs = read_inputs("input_vectors.txt")
    outputs = read_outputs("modelsim_output.txt")
    names = read_names("test_case_names.txt")

    if len(inputs) != len(outputs):
        print(f"CANH BAO: so luong test khong khop! "
              f"input={len(inputs)} dong, output={len(outputs)} dong")

    n_pass, n_fail = 0, 0
    fail_list = []

    for idx, ((A, B), C_hw) in enumerate(zip(inputs, outputs)):
        C_expected = A @ B          # golden model - dung phep nhan numpy co san
        match = np.array_equal(C_hw, C_expected)
        name = names[idx] if names and idx < len(names) else f"Test_{idx+1}"
        status = "PASS" if match else "FAIL"

        if match:
            n_pass += 1
        else:
            n_fail += 1
            fail_list.append(name)

        print(f"[{status}] {name}")
        print(f"    A = {A.tolist()}   B = {B.tolist()}")
        print(f"    Verilog C = {C_hw.tolist()}")
        print(f"    Expected  = {C_expected.tolist()}")
        if not match:
            diff = C_hw - C_expected
            print(f"    >>> SAI LECH (Verilog - Expected) = {diff.tolist()}")
        print()

    print("=" * 55)
    print(f"TONG KET: {n_pass} PASS / {n_fail} FAIL / {len(inputs)} test")
    if fail_list:
        print("Cac test FAIL:", ", ".join(fail_list))
    print("=" * 55)

    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()
