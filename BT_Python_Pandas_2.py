import pandas as pd
import numpy as np
"""Tạo bảng Nhân viên có 6 dòng với các cột:
- ID: [101, 102, 103, 104, 105, 106]
- Name: ['An', 'Bình', 'Cường', 'Dương', NaN, 'Hạnh']
- Age: [25, NaN, 30, 22, 28, 35]
- Department: ['HR', 'IT', 'IT', 'Finance', 'HR', NaN]
- Salary: [700, 800, 750, NaN, 710, 770]
Tạo bảng Phòng ban gồm 4 dòng với các cột:
- Department: ['HR', 'IT', 'Finance', 'Marketing']
- Manager: ['Trang', 'Khoa', 'Minh', 'Lan']
Yêu cầu
- Kiểm tra các ô dữ liệu bị thiếu trong bảng Nhân viên.
- Xoá các dòng trong bảng Nhân viên nếu dòng đó có hơn 2 giá trị bị thiếu.
- Điền giá trị cho các ô bị thiếu:
- Name: thay bằng "Chưa rõ".
- Age: thay bằng giá trị trung bình của cột Age.
- Salary: thay bằng giá trị nằm trước đó của ô bị thiếu của cột Salary.
- Department: thay bằng "Unknown".
- Chuyển kiểu dữ liệu của Age và Salary sang int.
- Tạo cột mới Salary_after_tax: giá trị sẽ là cột Salary -10% thuế
- Lọc ra các nhân viên thuộc phòng IT và có tuổi lớn hơn 25.
- Sắp xếp bảng nhân viên theo Salary_after_tax giảm dần.
- Nhóm nhân viên theo Department và tính mức lương trung bình cho từng phòng ban.
- Dùng merge() để nối bảng nhân viên với bảng quản lý phòng ban 
  theo cột Department để biết ai là Manager của từng nhân viên.
- Tạo bảng Nhân viên Mới gồm 2 nhân viên mới và dùng concat() để thêm họ vào bảng Nhân viên.
"""
NhanVien = {
    'ID': [101, 102, 103, 104, 105, 106],
    'Name': ['An', 'Bình', 'Cường', 'Dương', np.nan, 'Hạnh'],
    'Age': [25, np.nan, 30, 22, 28, 35],
    'Department': ['HR', 'IT', 'IT', 'Finance', 'HR', np.nan],
    'Salary': [700, 800, 750, np.nan, 710, 770]
}
df_NhanVien = pd.DataFrame(NhanVien)

PhongBan = {
    'Department': ['HR', 'IT', 'Finance', 'Marketing'],
    'Manager': ['Trang', 'Khoa', 'Minh', 'Lan']
}
df_PhongBan = pd.DataFrame(PhongBan)

# print(NhanVien.isnull())
print("\nTổng số ô bị thiếu theo cột:")
print(df_NhanVien.isnull().sum())

#
df_NhanVien = df_NhanVien.dropna(thresh=2)
print("\nBảng Nhân viên sau khi xoá các dòng có hơn 2 giá trị bị thiếu:")
print(df_NhanVien)

#
df_NhanVien.fillna({'Name': "Chưa rõ"}, inplace=True)
df_NhanVien.fillna({'Age': df_NhanVien['Age'].mean()}, inplace=True)
df_NhanVien.fillna({'Salary': df_NhanVien['Salary'].ffill()}, inplace=True)
df_NhanVien.fillna({'Department': "Unknown"}, inplace=True)
print("\nBảng Nhân viên sau khi điền giá trị là:")
print(df_NhanVien)

#
df_NhanVien['Age'] = df_NhanVien['Age'].astype(int)
df_NhanVien['Salary'] = df_NhanVien['Salary'].astype(int)
print(df_NhanVien.dtypes)

#
df_NhanVien['Salary_after_tax'] = df_NhanVien['Salary'] * 0.9
print(df_NhanVien)

#
df_filtered = df_NhanVien[(df_NhanVien['Department'] == 'IT') & (df_NhanVien['Age'] > 25)]
print(df_filtered)

#
df_Sorted = df_NhanVien.sort_values(by ='Salary_after_tax', ascending=False)
print(df_NhanVien)

#
df_GroupDep =df_NhanVien.groupby('Department')['Salary'].mean().reset_index()
print(df_GroupDep)

#
df_merged = pd.merge(df_NhanVien, df_PhongBan, on='Department', how='left')
print(df_merged)

#
New_NhanVien = {
    'ID': [107, 108],
    'Name': ['Kiên', 'Loan'],
    'Age': [26, 29],
    'Department': ['Marketing', 'Finance'],
    'Salary': [720, 810]
}
df_New_NhanVien = pd.DataFrame(New_NhanVien)

df_New_NhanVien = df_New_NhanVien.astype({'Age': int, 'Salary': int})
df_NhanVien = pd.concat([df_NhanVien, df_New_NhanVien], ignore_index=True)
print(df_NhanVien)