import pandas as pd
import os

file_path = 'DLYC2-1.xlsx'
output_html = 'report.html'

if not os.path.exists(file_path):
    raise FileNotFoundError(f"Không tìm thấy file dữ liệu '{file_path}'. Vui lòng đặt file vào thư mục BTL-N5.")

# Đọc dữ liệu
df = pd.read_excel(file_path)

# Tên cột dữ liệu
price_col = 'Giá hiện tại (triệu/m²)'
district_col = 'Quận/Huyện'
growth_col = 'Mức tăng trưởng dự báo (%)'

missing = [c for c in [district_col, price_col, growth_col] if c not in df.columns]
if missing:
    raise ValueError(f"Thiếu cột dữ liệu: {missing}. Các cột có sẵn: {list(df.columns)}")

# Chuẩn hóa dữ liệu
records = df[[district_col, price_col, growth_col]].copy()
records[district_col] = records[district_col].astype(str).str.strip()
records[price_col] = pd.to_numeric(records[price_col], errors='coerce')
records[growth_col] = pd.to_numeric(records[growth_col], errors='coerce')

# Nhóm theo giá và tiềm năng
records['Nhóm giá'] = records[price_col].apply(lambda x: 'Giá cao (>=70)' if x >= 70 else 'Giá trung bình/thấp (<70)')
records['Tiềm năng'] = records[growth_col].apply(lambda x: 'Tiềm năng cao (>=15%)' if x >= 15 else 'Tiềm năng thấp (<15%)')
records['Khuyến nghị'] = records.apply(
    lambda row: 'Nên mua' if row[growth_col] >= 15 and row[price_col] < 70 else (
        'Cân nhắc' if row[growth_col] < 15 or row[price_col] >= 70 else 'Cân nhắc'
    ),
    axis=1
)

# Các thống kê chung
summary = {
    'Tổng số mẫu': len(records),
    'Loại giá cao': len(records[records['Nhóm giá'] == 'Giá cao (>=70)']),
    'Loại giá thấp': len(records[records['Nhóm giá'] == 'Giá trung bình/thấp (<70)']),
    'Giá trung bình Loại 1': records.loc[records['Nhóm giá'] == 'Giá cao (>=70)', price_col].mean(),
    'Giá trung bình Loại 2': records.loc[records['Nhóm giá'] == 'Giá trung bình/thấp (<70)', price_col].mean(),
    'Tiềm năng cao': len(records[records['Tiềm năng'] == 'Tiềm năng cao (>=15%)']),
    'Tiềm năng thấp': len(records[records['Tiềm năng'] == 'Tiềm năng thấp (<15%)']),
    'Tăng trưởng trung bình tiềm năng cao': records.loc[records['Tiềm năng'] == 'Tiềm năng cao (>=15%)', growth_col].mean(),
    'Tăng trưởng trung bình tiềm năng thấp': records.loc[records['Tiềm năng'] == 'Tiềm năng thấp (<15%)', growth_col].mean(),
}

# Tạo bảng HTML
price_table_rows = []
growth_table_rows = []
combined_rows = []
for _, row in records.iterrows():
    district = row[district_col]
    price = '' if pd.isna(row[price_col]) else f"{row[price_col]:.2f}"
    growth = '' if pd.isna(row[growth_col]) else f"{row[growth_col]:.2f}%"
    price_group = row['Nhóm giá']
    growth_group = row['Tiềm năng']
    recommend = row['Khuyến nghị']

    price_table_rows.append(f"<tr><td>{district}</td><td>{price}</td><td>{price_group}</td></tr>")
    growth_table_rows.append(f"<tr><td>{district}</td><td>{growth}</td><td>{growth_group}</td></tr>")
    combined_rows.append(
        f"<tr><td>{district}</td><td>{price}</td><td>{price_group}</td><td>{growth}</td><td>{growth_group}</td><td>{recommend}</td></tr>"
    )

html_content = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Báo cáo đầu tư bất động sản</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f5f7fb; color: #222; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}
    header {{ text-align: center; margin-bottom: 24px; }}
    h1 {{ margin: 0; font-size: 2.4rem; color: #0b3d91; }}
    p.subtitle {{ margin: 8px 0 0; color: #555; }}
    .card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin: 24px 0; }}
    .card {{ background: white; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.08); padding: 18px; }}
    .card h2 {{ margin: 0 0 12px; font-size: 1.1rem; color: #0b3d91; }}
    .card p {{ margin: 0; font-size: 1.25rem; font-weight: 600; }}
    .search-box {{ margin: 24px 0; display: flex; justify-content: center; }}
    .search-box input {{ width: 100%; max-width: 480px; padding: 14px 16px; border-radius: 12px; border: 1px solid #ccc; font-size: 1rem; }}
    .table-section {{ margin-bottom: 32px; }}
    table {{ width: 100%; border-collapse: collapse; background: white; box-shadow: 0 8px 24px rgba(0,0,0,0.08); border-radius: 12px; overflow: hidden; }}
    th, td {{ padding: 14px 16px; text-align: left; border-bottom: 1px solid #eceff4; }}
    th {{ background: #0b3d91; color: white; position: sticky; top: 0; }}
    tbody tr:hover {{ background: #f1f6ff; }}
    .note {{ background: #ffffff; padding: 18px 20px; border-left: 4px solid #0b3d91; margin-bottom: 24px; }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Báo cáo đầu tư bất động sản</h1>
      <p class="subtitle">Tổng hợp thông tin giá và tiềm năng tăng trưởng để hỗ trợ quyết định đầu tư.</p>
    </header>

    <div class="card-grid">
      <div class="card"><h2>Tổng số mẫu</h2><p>{summary['Tổng số mẫu']}</p></div>
      <div class="card"><h2>Giá cao</h2><p>{summary['Loại giá cao']}</p></div>
      <div class="card"><h2>Giá thấp</h2><p>{summary['Loại giá thấp']}</p></div>
      <div class="card"><h2>Tiềm năng cao</h2><p>{summary['Tiềm năng cao']}</p></div>
      <div class="card"><h2>Tiềm năng thấp</h2><p>{summary['Tiềm năng thấp']}</p></div>
    </div>

    <div class="search-box">
      <input id="searchInput" type="search" placeholder="Tìm quận/huyện..." oninput="filterTables()" />
    </div>

    <div class="note">
      <strong>Hướng dẫn:</strong> Nhập quận/huyện để tìm nhanh thông tin giá và tiềm năng. Khách hàng nên mua khi tiềm năng cao và giá không quá cao; cân nhắc khi tiềm năng thấp.
    </div>

    <section class="table-section">
      <h2>Phân loại theo giá</h2>
      <table id="priceTable">
        <thead>
          <tr><th>Quận/Huyện</th><th>Giá hiện tại (triệu/m²)</th><th>Nhóm giá</th></tr>
        </thead>
        <tbody>
          {''.join(price_table_rows)}
        </tbody>
      </table>
    </section>

    <section class="table-section">
      <h2>Phân loại theo tiềm năng</h2>
      <table id="growthTable">
        <thead>
          <tr><th>Quận/Huyện</th><th>Tăng trưởng dự báo (%)</th><th>Tiềm năng</th></tr>
        </thead>
        <tbody>
          {''.join(growth_table_rows)}
        </tbody>
      </table>
    </section>

    <section class="table-section">
      <h2>Thông tin tổng hợp</h2>
      <table id="combinedTable">
        <thead>
          <tr><th>Quận/Huyện</th><th>Giá hiện tại</th><th>Nhóm giá</th><th>Tăng trưởng</th><th>Tiềm năng</th><th>Khuyến nghị</th></tr>
        </thead>
        <tbody>
          {''.join(combined_rows)}
        </tbody>
      </table>
    </section>
  </div>

  <script>
    function filterTables() {{
      const filter = document.getElementById('searchInput').value.toLowerCase();
      const tables = ['priceTable', 'growthTable', 'combinedTable'];
      tables.forEach(id => {{
        const tbody = document.querySelector('#' + id + ' tbody');
        tbody.querySelectorAll('tr').forEach(row => {{
          const text = row.textContent.toLowerCase();
          row.style.display = text.includes(filter) ? '' : 'none';
        }});
      }});
    }}
  </script>
</body>
</html>
"""

with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Đã tạo trang web báo cáo: {output_html}")
