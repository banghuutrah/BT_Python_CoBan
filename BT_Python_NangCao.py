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

"""Viết chương trình minigame “Đoán số”. Khi bắt đầu,
    chương trình yêu cầu người dùng nhập một số nguyên dương từ 1 đến 999.
    Yêu cầu trò chơi:
    Đáp án của trò chơi là một số ngẫu nhiên trong khoảng 1–999,
    được sinh từ phần miligiây của thời gian hệ thống hiện tại.
    Mỗi lần người dùng đoán sai, hiển thị thông báo: 
    "Bạn đã trả lời sai x lần", với x là số lần đoán sai liên tiếp.
    Sau 5 lần đoán sai, chương trình sẽ tự động đổi sang một số ngẫu nhiên mới,
    và hiển thị: "Bạn đoán trật tất cả năm lần, kết quả đã thay đổi. Mời bạn đoán lại"
    Nếu người dùng đoán gần đúng (cách kết quả đúng không quá ±10),
    hiển thị thông báo: "Bạn đoán gần đúng rồi!"
    Khi người dùng đoán đúng, kết thúc trò chơi và in ra: "Bạn đã dự đoán chính xác số y", với y là số đúng.
"""
import time
def generate_secret_number():
    milliseconds = int((time.time() * 1000))
    return milliseconds % 999 + 1 

def is_valid_guess(guess):
    return guess.isdigit() and 1 <= int(guess) <= 999

def play_guessing_game():
    print("Chào mừng bạn đến với trò chơi 'Đoán số'!")
    secret_number = generate_secret_number()
    wrong_guesses = 0

    while True:
        guess = input("Nhập một số nguyên từ 1 đến 999: ")
        
        if not is_valid_guess(guess):
            print("Giá trị không hợp lệ. Vui lòng nhập số nguyên dương từ 1 đến 999.")
            continue

        guess = int(guess)

        if guess == secret_number:
            print(f"Bạn đã dự đoán chính xác số {secret_number}!")
            break
        else:
            wrong_guesses += 1

            if abs(guess - secret_number) <= 10:
                print("Bạn đoán gần đúng rồi!")
            else:
                print(f"Bạn đã trả lời sai {wrong_guesses} lần.")

            if wrong_guesses == 5:
                secret_number = generate_secret_number()
                wrong_guesses = 0
                print("Bạn đoán trật tất cả năm lần, kết quả đã thay đổi. Mời bạn đoán lại.")

play_guessing_game()

