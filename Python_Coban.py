# cau1: Viết chương trình đổi các từ ở đầu câu sang chữ hoa và những từ không phải đầu câu sang chữ thường.
def ChuyenDoi(n):
    w_list = n.split()
    for i in range(len(w_list)):
        if i == 0:
            w_list[i] = w_list[i].capitalize()
        else:
            w_list[i] = w_list[i].lower()
    return ' '.join(w_list)

# input = "toi đAnG HọC laP Trình"
# output = ChuyenDoi(input)
# print(output)
# cau2: Viết chương trình đảo ngược thứ tự các từ có trong chuỗi.
def DaoNguoc(n):
    w_list = n.split()
    w_list.reverse()
    return ' '.join(w_list)
# input = " lap trinh bang ngon ngu python "
# output = DaoNguoc(input)
# print(output)
# cau3: Viết chương trình tìm kiếm ký tự xuất hiện nhiều nhất trong chuỗi.
def KyTuMax(n):
    count = {}
    for ky_tu in n:
        if ky_tu in count:
            count[ky_tu] += 1
        else:
            count[ky_tu] = 1
    x = None
    y = 0
    for ky_tu, so_lan  in count.items():
        if so_lan > y:
            y = so_lan
            x = ky_tu
    return x, y
# input = " bbaaabbkkcxkkaaoi"
# output = KyTuMax(input)
# print(f"{output[0]} xuat hien {output[1]} la nhieu nhat")
#cau4: Viết chương trình nhập một chuỗi bất kỳ, liệt kê số lần xuất hiện của mỗi ký tự.
def SoLanXuatHien(n):
    count = {}
    for ky_tu in n:
        if ky_tu in count:
            count[ky_tu] += 1
        else:
            count[ky_tu] = 1
    return count
# Chuoi = input("Nhap chuoi bat ky: ")
# output = SoLanXuatHien(Chuoi)
# for ky_tu, so_lan in output.items():
#     print(f"{ky_tu} : {so_lan} lần")

#cau5: Viết hàm kiểm tra xem trong chuỗi có ký tự số hay không. Nếu có, tách các số đó ra thành một mảng riêng.
def KT_KyTuSo(n):
    danh_sach = []
    for ky_tu in n:
        if ky_tu.isdigit():
            danh_sach.append(ky_tu)
    return danh_sach
# Nhap_Chuoi = input("Nhap chuoi bat ky:")
# output = KT_KyTuSo(Nhap_Chuoi)
# if output:
#     print("Trong chuoi co ky tu so la:" , output)
# else:
#     print("Trong chuoi khong co ky tu so!")
#cau6: Viết hàm cắt chuỗi họ tên thành chuỗi họ lót và chuỗi tên.
def TachChuoiHoTen(hoten):
    danh_sach = hoten.strip().split()
    if len(danh_sach) == 0:
        return "", ""
    ten = danh_sach[-1]
    ho_lot= " ".join(danh_sach[:-1])
    return ho_lot, ten
# Ho_Ten = input("Nhap ho ten: ")
# output = TachChuoiHoTen(Ho_Ten)
# print(f"Ho lot: {output[0]}")
# print(f"Ten: {output[1]}")
#cau7: Viết chương trình chuyển ký tự đầu tiên của mỗi từ trong chuỗi thành chữ in hoa.
input_str = "toi dang hoc lap trinh bang ngon ngu python"
output_str = input_str.title()
#print(output_str)
#cau8: Viết chương trình đổi chữ xen kẽ: một chữ hoa và một chữ thường.
def ChuyenDoiXenKe(n):
    kq = []
    for i, ky_tu in enumerate(n):
        if i % 2 == 0:
            kq.append(ky_tu.upper())
        else:
            kq.append(ky_tu.lower())
    return ''.join(kq)
Chuoi = "ABCDEfgh"
output = ChuyenDoiXenKe(Chuoi)
print(output)
#cau9:Viết chương trình nhập vào một chuỗi ký tự, kiểm tra xem chuỗi đó có đối xứng không.
#Chuỗi đối xứng là chuỗi mà khi viết ngược lại vẫn giống như ban đầu.
def KT_ChuoiDoiXung(n):
    n = n.strip().lower()
    return n == n[::-1]
nhap_chuoi = input("Nhap 1 chuoi bat ky: ")
if KT_ChuoiDoiXung(nhap_chuoi):
    print("la chuoi doi xung")
else:
    print("khong phải chuoi doi xung")
#cau10:  Viết chương trình nhập vào một số có 3 chữ số, xuất ra dòng chữ mô tả giá trị con số đó.
