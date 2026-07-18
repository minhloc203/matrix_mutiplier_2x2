# ============================================================
# gen_test_vectors.py
# ------------------------------------------------------------
# Sinh cac cap ma tran A, B (2x2, so nguyen co dau 8-bit: -128..127)
# ghi ra input_vectors.txt cho testbench Verilog doc.
# File CHI chua input (A, B) - KHONG chua dap an, dung yeu cau
# flow "post-processing verification" cua thay.
#
# Cac truong hop quan trong duoc bao phu (theo de cuong hinh gui):
#   - So am
#   - So 0
#   - Gia tri lon nhat (127)
#   - Gia tri nho nhat (-128)
#   - Ma tran don vi (identity)
#   - Ma tran toan so am
#   - Ket qua bang 0
#   - Truong hop gan overflow
#   - Truong hop doi dau
#   - Cac test random tong quat
# ============================================================
import random

random.seed(42)   # co dinh seed de ket qua tai hien duoc (reproducible)

INT8_MIN, INT8_MAX = -128, 127

test_cases = []   # list of (A: list4, B: list4)
test_names = []   # ten/mo ta tuong ung, cung thu tu voi test_cases


def add_case(name, A, B):
    test_cases.append((A, B))
    test_names.append(name)


# ---- 1. Ma tran toan so 0 ----
add_case("Ma tran A va B deu bang 0", [0, 0, 0, 0], [0, 0, 0, 0])

# ---- 2. Ma tran don vi (Identity) ----
I = [1, 0, 0, 1]
R = [5, -3, 2, 7]
add_case("Ma tran don vi nhan ma tran bat ky (I x B = B)", I, R)
add_case("Ma tran bat ky nhan ma tran don vi (A x I = A)", R, I)

# ---- 3. Ma tran toan so am ----
add_case("Ca hai ma tran deu toan so am", [-1, -2, -3, -4], [-5, -6, -7, -8])

# ---- 4. Gia tri lon nhat (127) - kiem tra bien tren ----
add_case("Gia tri lon nhat 127", [127, 127, 127, 127], [127, 127, 127, 127])

# ---- 5. Gia tri nho nhat (-128) - truong hop GAN OVERFLOW nhat ----
#   (-128)*(-128) = 16384, cong don 2 lan = 32768 -> vua du 17-bit signed
add_case("Gia tri nho nhat -128 (gan tran so - overflow)",
         [-128, -128, -128, -128], [-128, -128, -128, -128])

# ---- 5b. Mot bien the near-overflow khac: max duong nhan min am ----
add_case("Gan overflow - pha tron cuc tri 127 va -128",
         [127, -128, 127, -128], [-128, 127, -128, 127])

# ---- 6. Truong hop doi dau (sign change) trong qua trinh cong don ----
#   VD: A00*B00 duong nhung A01*B10 am, tong co the doi dau
add_case("Doi dau trong qua trinh cong don",
         [-5, 10, -15, 20], [3, -4, 5, -6])

# ---- 7. Ket qua bang 0 (cac so hang trieu tieu nhau) ----
add_case("Ket qua C bang 0", [1, -1, 1, -1], [1, 1, 1, 1])

# ---- 8. So 0 xen ke voi so am/duong ----
add_case("So 0 xen ke voi so am va duong", [0, -7, 8, 0], [0, 4, -6, 0])

# ---- 9. Random cases (bao phu toan dai gia tri -128..127) ----
N_RANDOM = 20
for i in range(N_RANDOM):
    A = [random.randint(INT8_MIN, INT8_MAX) for _ in range(4)]
    B = [random.randint(INT8_MIN, INT8_MAX) for _ in range(4)]
    add_case(f"Test ngau nhien so {i+1}", A, B)


# ---- Ghi ra file ----
with open("input_vectors.txt", "w") as f_in, \
     open("test_case_names.txt", "w") as f_name:
    for (A, B), name in zip(test_cases, test_names):
        f_in.write(f"{A[0]} {A[1]} {A[2]} {A[3]} "
                    f"{B[0]} {B[1]} {B[2]} {B[3]}\n")
        f_name.write(name + "\n")

print(f"Da tao {len(test_cases)} test case:")
for name in test_names:
    print(f"  - {name}")
print("\nDa ghi: input_vectors.txt, test_case_names.txt")
