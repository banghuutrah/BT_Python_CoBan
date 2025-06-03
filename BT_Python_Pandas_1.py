import pandas as pd
"""Tạo một DataFrame tên là df_students chứa thông tin của 10 sinh viên:
- Name: tên sinh viên
- Age: tuổi
- Gender: giới tính
- Score: điểm tổng kết
Yêu cầu:
Hiển thị:
- Toàn bộ dữ liệu của bảng
- 3 dòng đầu tiên
- Theo index=2 và cột Name
- Theo index=10 và cột Age
- Các cột Name và Score
- Thêm một cột tên Pass với giá trị True nếu giá trị cột Score >= 5, ngược lại là False.
- Sắp xếp danh sách sinh viên theo điểm Score giảm dần."""
data = {
    'Name': ['Huu', 'Bình', 'Hoai', 'Quoc', 'Huong', 'Luu', 'Lan', 'Thanh', 'Quang', 'Tuyet'],
    'Age': [20, 21, 22, 20, 23, 21, 22, 20, 21, 23],
    'Gender': ['Nam', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nữ', 'Nam', 'Nữ'],
    'Score': [6.5, 7.0, 8.2, 4.5, 5.0, 9.1, 3.2, 6.8, 7.5, 4.0]
}

df_students = pd.DataFrame(data)

#
print("1.Toàn bộ dữ liệu của bảng là: ")
print(df_students)

#
print("\n2.Ba dòng đầu tiên của bảng là:")
print(df_students.head(3))

#
print("\n3.Theo index = 2 và cột Name là:")
print(df_students.loc[2, "Name"])

#
print("\n4.Theo index = 10 và cột Age là:")
try:    
    print(df_students.loc[10, "Age"])
except KeyError:
    print("Không tồn tại index = 10 trong DataFrame")

#
print("\n5.Các cột Name và Score là:")
print(df_students[['Name', 'Score']])

#
print("\n6.Dữ liệu của cột Pass là:")
df_students['Pass'] = df_students['Score'] >= 5
print(df_students[['Name', 'Pass']])

#
print("\n7.Danh sách sắp xếp theo điểm Score giảm dần là:")
df_sorted = df_students.sort_values(by='Score', ascending=False)
print(df_sorted[['Name', 'Score']])