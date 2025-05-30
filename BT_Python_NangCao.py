import math
def Is_Valid_Integer(chuoi):
    """Viết chương trình tìm tất cả các số chia hết cho 3 nhưng không phải là số chính phương,
        nằm trong đoạn từ a đến b (với a và b là hai số nguyên do người dùng nhập vào).
        Yêu cầu:
        Kiểm tra định dạng dữ liệu người dùng nhập vào (phải là số, a < b, và là số nguyên).
        Kết quả là chuỗi các số thoả mãn điều kiện, in ra trên một dòng, cách nhau bằng dấu phẩy.
        Ví dụ: nhập a = 1, b = 30 → xuất: 3,6,12,15,18,21,24,27,30 
        (trừ các số chính phương như 9, 16, 25 nếu chia hết cho 3)."""
    try:
        int(chuoi)
        return True
    except ValueError:
        return False
def Is_Perfect_Square(n):
    return int(math.sqrt(n)) ** 2 == n
def Find_Numbers(a, b):
    result = []
    for i in range(a, b + 1):
        if i % 3 == 0 and not Is_Perfect_Square(i):
            result.append(str(i))
    return ', '.join(result)
#
a_input = input("Nhap so nguyen a: ")
b_input = input("Nhap so nguyen b: ")

if Is_Valid_Integer(a_input) and Is_Valid_Integer(b_input):
    a = int(a_input)
    b = int(b_input)

    if a < b:
        output = Find_Numbers(a, b)
        print(f"Ket qua: {output}")
    else:
        print("a phai be hon b!")
else:
    print("Khong dung dinh dang so nguyen!")

