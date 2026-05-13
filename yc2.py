import pandas as pd
import matplotlib.pyplot as plt
import os

# Đọc dữ liệu từ file Excel
file_path = 'DLYC2-1.xlsx'  # Giả định file Excel ở cùng thư mục
if not os.path.exists(file_path):
    print(f"File {file_path} không tồn tại. Vui lòng đặt file Excel vào thư mục BTL-N5.")
    exit()

df = pd.read_excel(file_path)

# Tên cột sử dụng trong dữ liệu
gia_column = 'Giá hiện tại (triệu/m²)'
quan_column = 'Quận/Huyện'
growth_column = 'Mức tăng trưởng dự báo (%)'

missing_columns = [col for col in [gia_column, quan_column, growth_column] if col not in df.columns]
if missing_columns:
    print(f"Thiếu cột dữ liệu: {missing_columns}. Các cột có sẵn: {list(df.columns)}")
    exit()

# Loại theo giá
loai_gia1 = df[df[gia_column] >= 70]
loai_gia2 = df[df[gia_column] < 70]

so_luong_gia1 = len(loai_gia1)
so_luong_gia2 = len(loai_gia2)
trung_binh_gia1 = loai_gia1[gia_column].mean() if so_luong_gia1 > 0 else 0
trung_binh_gia2 = loai_gia2[gia_column].mean() if so_luong_gia2 > 0 else 0

# Loại theo tiềm năng tăng trưởng
loai_tiemnang1 = df[df[growth_column] >= 15]
loai_tiemnang2 = df[df[growth_column] < 15]

so_luong_tiemnang1 = len(loai_tiemnang1)
so_luong_tiemnang2 = len(loai_tiemnang2)
trung_binh_tiemnang1 = loai_tiemnang1[growth_column].mean() if so_luong_tiemnang1 > 0 else 0
trung_binh_tiemnang2 = loai_tiemnang2[growth_column].mean() if so_luong_tiemnang2 > 0 else 0

# Danh sách quận/huyện của từng loại tiềm năng
tiemnang1_quan = sorted(loai_tiemnang1[quan_column].dropna().astype(str).unique())
tiemnang2_quan = sorted(loai_tiemnang2[quan_column].dropna().astype(str).unique())

# Vẽ biểu đồ giá
labels_gia = ['Loại 1: Giá cao (>=70)', 'Loại 2: Giá thấp (<70)']
sizes_gia = [so_luong_gia1, so_luong_gia2]
colors_gia = ['red', 'blue']

plt.figure(figsize=(8, 6))
plt.bar(labels_gia, sizes_gia, color=colors_gia)
plt.title('Phân loại theo giá hiện tại')
plt.ylabel('Số lượng mẫu')
plt.xlabel('Nhóm giá')
for i, v in enumerate(sizes_gia):
    plt.text(i, v + 0.5, str(v), ha='center', va='bottom')
plt.tight_layout()
plt.savefig('phan_loai_gia.png')
plt.close()

# Vẽ biểu đồ tiềm năng
labels_tiemnang = ['Loại 1: Tiềm năng cao (>=15%)', 'Loại 2: Tiềm năng thấp (<15%)']
sizes_tiemnang = [so_luong_tiemnang1, so_luong_tiemnang2]
colors_tiemnang = ['green', 'orange']

plt.figure(figsize=(8, 6))
plt.bar(labels_tiemnang, sizes_tiemnang, color=colors_tiemnang)
plt.title('Phân loại theo tiềm năng tăng trưởng dự báo')
plt.ylabel('Số lượng mẫu')
plt.xlabel('Nhóm tiềm năng')
for i, v in enumerate(sizes_tiemnang):
    plt.text(i, v + 0.5, str(v), ha='center', va='bottom')
plt.tight_layout()
plt.savefig('phan_loai_tiem_nang.png')
plt.close()

# Tạo bảng quận/huyện theo giá
max_len_gia = max(len(loai_gia1[quan_column].dropna().unique()), len(loai_gia2[quan_column].dropna().unique()))
quans_gia1 = sorted(loai_gia1[quan_column].dropna().astype(str).unique())
quans_gia2 = sorted(loai_gia2[quan_column].dropna().astype(str).unique())
quans_gia1 += [''] * (max_len_gia - len(quans_gia1))
quans_gia2 += [''] * (max_len_gia - len(quans_gia2))

bang_gia = 'Loại 1: Giá cao (>=70 triệu/m²) | Loại 2: Giá thấp (<70 triệu/m²)\n'
bang_gia += '--- | ---\n'
for q1, q2 in zip(quans_gia1, quans_gia2):
    bang_gia += f"{q1} | {q2}\n"

# Tạo bảng quận/huyện theo tiềm năng
max_len_tiemnang = max(len(tiemnang1_quan), len(tiemnang2_quan))
tiemnang1_quan += [''] * (max_len_tiemnang - len(tiemnang1_quan))
tiemnang2_quan += [''] * (max_len_tiemnang - len(tiemnang2_quan))

bang_tiemnang = 'Loại 1: Tiềm năng cao (>=15%) | Loại 2: Tiềm năng thấp (<15%)\n'
bang_tiemnang += '--- | ---\n'
for q1, q2 in zip(tiemnang1_quan, tiemnang2_quan):
    bang_tiemnang += f"{q1} | {q2}\n"

# Tạo báo cáo cho phân loại giá
report_price = f"""
=== BÁO CÁO PHÂN TÍCH GIÁ HIỆN TẠI ===

1. Tổng quan dữ liệu:
   - Tổng số mẫu: {len(df)}
   - Nguồn: File Excel {file_path}
   - Tiêu chí: Giá hiện tại >= 70 triệu/m² là Loại 1 (Giá cao), < 70 triệu/m² là Loại 2 (Giá thấp).

2. Kết quả phân loại:
   - Loại 1: Giá cao
     + Số lượng: {so_luong_gia1}
     + Trung bình giá: {trung_binh_gia1:.2f} triệu/m²
     + Tỷ lệ: {so_luong_gia1 / len(df) * 100:.2f}%
   - Loại 2: Giá thấp
     + Số lượng: {so_luong_gia2}
     + Trung bình giá: {trung_binh_gia2:.2f} triệu/m²
     + Tỷ lệ: {so_luong_gia2 / len(df) * 100:.2f}%

3. Danh sách quận/huyện theo giá:
{bang_gia}

4. Ghi chú:
   - Biểu đồ đã được lưu: phan_loai_gia.png
   - Kết quả giúp phân biệt khu vực giá cao và giá thấp.
"""

# Tạo báo cáo cho phân loại tiềm năng
growth_report = f"""
=== BÁO CÁO PHÂN TÍCH TIỀM NĂNG TĂNG TRƯỞNG ===

1. Tổng quan dữ liệu:
   - Tổng số mẫu: {len(df)}
   - Nguồn: File Excel {file_path}
   - Tiêu chí: Tăng trưởng dự báo >= 15% là Tiềm năng cao, < 15% là Tiềm năng thấp.

2. Kết quả phân loại:
   - Loại 1: Tiềm năng cao
     + Số lượng: {so_luong_tiemnang1}
     + Trung bình tăng trưởng: {trung_binh_tiemnang1:.2f}%
     + Tỷ lệ: {so_luong_tiemnang1 / len(df) * 100:.2f}%
   - Loại 2: Tiềm năng thấp
     + Số lượng: {so_luong_tiemnang2}
     + Trung bình tăng trưởng: {trung_binh_tiemnang2:.2f}%
     + Tỷ lệ: {so_luong_tiemnang2 / len(df) * 100:.2f}%

3. Danh sách quận/huyện theo tiềm năng:
{bang_tiemnang}

4. Ghi chú:
   - Biểu đồ đã được lưu: phan_loai_tiem_nang.png
   - Loại 1 tiềm năng cao là khu vực khách hàng nên mua.
   - Loại 2 tiềm năng thấp cần cân nhắc thêm.
"""

# Lưu hai báo cáo riêng
with open('bao_cao_gia.txt', 'w', encoding='utf-8') as f:
    f.write(report_price)

with open('bao_cao_tiem_nang.txt', 'w', encoding='utf-8') as f:
    f.write(growth_report)

print("Đã tạo 2 báo cáo riêng:")
print("- bao_cao_gia.txt")
print("- bao_cao_tiem_nang.txt")
print("Đã lưu biểu đồ:")
print("- phan_loai_gia.png")
print("- phan_loai_tiem_nang.png")