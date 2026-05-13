import math


def calculate_factorial(n):
    """Tính giai thừa của n."""
    return math.factorial(n)


def calculate_average(values):
    """Tính giá trị trung bình của danh sách giá trị."""
    if not values:
        return 0
    return sum(values) / len(values)


def calculate_compound_interest(principal, monthly_rate, months):
    """Tính số tiền cuối cùng và lợi nhuận với lãi kép hàng tháng."""
    balance = principal
    monthly_balances = []
    for month in range(1, months + 1):
        balance *= 1 + monthly_rate
        monthly_balances.append((month, balance))
    return balance, balance - principal, monthly_balances


def build_report():
    # Phần 1: Phân tích tổ hợp
    n = 7
    factorial_n = calculate_factorial(n)
    part_1_lines = [
        '=== PHẦN 1: PHÂN TÍCH TỔ HỢP (TÍNH GIAI THỪA) ===',
        f'1. Dữ liệu: số lượng nhân sự n = {n}',
        '2. Yêu cầu: Tính số cách sắp xếp thứ tự đứng của các thành viên theo một hàng ngang.',
        f'3. Công thức: n! = 1 * 2 * 3 * ... * n',
        f'4. Kết quả: {n}! = {factorial_n}',
        '',
    ]

    # Phần 2: Kiểm soát chất lượng sản xuất
    defects = [12, 15, 8, 20, 14, 11, 10]
    count_defects = len(defects)
    average_defects = calculate_average(defects)
    part_2_lines = [
        '=== PHẦN 2: KIỂM SOÁT CHẤT LƯỢNG SẢN XUẤT (TÍNH GIÁ TRỊ TRUNG BÌNH) ===',
        '1. Dữ liệu: số lượng sản phẩm lỗi theo ngày trong tuần.',
        f'   Dãy số: {defects}',
        f'   Số lượng phần tử: {count_defects}',
        f'2. Tổng số sản phẩm lỗi trong tuần: {sum(defects)}',
        f'3. Công thức trung bình: trung bình = tổng / số lượng',
        f'4. Kết quả: giá trị trung bình số sản phẩm lỗi mỗi ngày = {average_defects:.2f}',
        '',
    ]

    # Phần 3: Dự báo tăng trưởng tài chính
    principal = 500_000_000
    monthly_rate = 0.008
    months = 12
    final_balance, profit, monthly_balances = calculate_compound_interest(principal, monthly_rate, months)
    part_3_lines = [
        '=== PHẦN 3: DỰ BÁO TĂNG TRƯỞNG TÀI CHÍNH (LÃI KÉP HÀNG THÁNG) ===',
        f'1. Dữ liệu: số tiền gửi ban đầu P = {principal:,} VNĐ',
        f'   Lãi suất cố định hàng tháng r = {monthly_rate * 100:.2f}%',
        f'   Thời gian gửi t = {months} tháng',
        '2. Công thức lãi kép: A = P * (1 + r)^t',
        f'3. Kết quả sau tháng thứ {months}:',
        f'   Tổng số tiền cuối cùng (gốc + lãi) = {final_balance:,.0f} VNĐ',
        f'   Số tiền lợi nhuận lãi ròng = {profit:,.0f} VNĐ',
        '4. Chi tiết số dư theo từng tháng:',
    ]
    for month, balance in monthly_balances:
        part_3_lines.append(f'   - Tháng {month:02d}: {balance:,.0f} VNĐ')
    part_3_lines.append('')

    result_lines = [
        'BÁO CÁO KẾT QUẢ CHI TIẾT CÁC BƯỚC THỰC HIỆN',
        '==================================================',
        '',
    ]
    result_lines.extend(part_1_lines)
    result_lines.extend(part_2_lines)
    result_lines.extend(part_3_lines)

    return '\n'.join(result_lines)


def save_report(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    report_path = 'ket_qua_yc3.txt'
    report_content = build_report()
    save_report(report_path, report_content)
    print(f'Hoàn thành: đã tạo file báo cáo chi tiết {report_path}')
