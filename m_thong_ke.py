from tkinter import messagebox
import ttkbootstrap as tb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from utils import clicked
from DB import cursor


def fetch_monthly_revenue(year):
    """
    Truy xuất tổng doanh thu hàng tháng trong một năm từ cơ sở dữ liệu.

    Args:
        year (int): Năm cần lấy dữ liệu.

    Returns:
        list: Danh sách tổng doanh thu hàng tháng.
    """
    total_amounts = []
    for month in range(1, 13):
        cursor.execute(
            "SELECT SUM(TotalAmt) FROM invoicedetailtbl "
            "WHERE YEAR(STR_TO_DATE(idDate, '%m/%d/%Y')) = %s "
            "AND MONTH(STR_TO_DATE(idDate, '%m/%d/%Y')) = %s",
            (year, month)
        )
        result = cursor.fetchone()
        total_amounts.append(result[0] if result[0] is not None else 0)
    return total_amounts


def update_graph(ax, canvas, year):
    """
    Cập nhật biểu đồ doanh thu hàng tháng.

    Args:
        ax: Trục của biểu đồ.
        canvas: Canvas hiển thị biểu đồ.
        year (int): Năm để hiển thị dữ liệu.
    """
    total_amounts = fetch_monthly_revenue(year)

    month_names = [
        "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6",
        "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"
    ]

    ax.clear()
    ax.set_facecolor('#F7F7F7')
    bars = ax.bar(range(1, 13), total_amounts, color='#FFC5C5')
    for bar, total in zip(bars, total_amounts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{total:.2f}", ha="center", va="bottom", fontsize=6)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names)
    ax.set_ylabel("Tổng doanh thu", fontsize=8)
    ax.set_title("Tổng doanh thu hàng tháng", fontsize=10)
    ax.tick_params(axis='x', labelsize=6)
    ax.tick_params(axis='y', labelsize=6)

    canvas.draw()


def show_thongKe(window, user_role, buttons, thongKe_btn):
    """
    Hiển thị giao diện thống kê.

    Args:
        window: Cửa sổ chính.
        user_role: Vai trò của người dùng.
        buttons: Danh sách các nút.
        thongKe_btn: Nút hiện tại đang được kích hoạt.
    """
    if user_role != 'admin':
        messagebox.showerror("Access Denied", "Bạn không có quyền truy cập vào tính năng này")
        return

    clicked(thongKe_btn, buttons)

    # Tạo frame chính
    thongKe_frame = tb.Labelframe(window, bootstyle="secondary", text="Quản lý thống kê")
    thongKe_frame.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")
    thongKe_frame.columnconfigure(0, weight=1)
    thongKe_frame.rowconfigure(0, weight=1)

    # Tạo frame cho nội dung
    content_frame = tb.Labelframe(thongKe_frame, bootstyle="secondary", text="Thống kê thu nhập theo năm")
    content_frame.grid(row=0, column=0, padx=5, pady=5, sticky="news")

    # Khởi tạo biểu đồ
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=content_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Dropdown chọn năm
    year_var = tb.StringVar()
    year_combobox = tb.Combobox(content_frame, textvariable=year_var)
    year_combobox['values'] = [year for year in range(2020, 2030)]
    year_combobox.current(4)
    year_combobox.pack(fill="x", padx=10, pady=10)

    # Nút cập nhật
    update_button = tb.Button(content_frame, text="Cập nhật", command=lambda: update_graph(ax, canvas, int(year_var.get())))
    update_button.pack(fill="x", padx=10, pady=10)

    # Hiển thị dữ liệu ban đầu
    update_graph(ax, canvas, int(year_combobox.get()))
