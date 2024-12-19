from datetime import timedelta, datetime
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.widgets import DateEntry
from utils import clicked
from DB import cursor
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

plt.style.use('seaborn-v0_8-pastel')


def format_vnd(amount):
    return f"{amount:,.0f}".replace(',', '.') + " VND"


def fetch_revenue_and_customers_7_days():
    """
    Lấy dữ liệu doanh thu và số lượng khách hàng trong 7 ngày gần nhất.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)  # 7 ngày gần nhất
    cursor.execute(
        """
        SELECT it.InvoiceDate, 
               SUM(idt.TotalAmt) AS revenue, 
               COUNT(DISTINCT it.CustID) AS customers
        FROM invoicetbl AS it
        LEFT JOIN invoicedetailtbl AS idt ON it.InvoiceID = idt.InvoiceID
        WHERE it.InvoiceDate BETWEEN %s AND %s
        GROUP BY it.InvoiceDate
        ORDER BY it.InvoiceDate ASC
        """,
        (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    )
    results = cursor.fetchall()

    # Chuyển dữ liệu thành định dạng danh sách ngày, doanh thu và khách hàng
    days = []
    revenues = []
    customers = []
    for i in range(7):
        current_day = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        match = next((row for row in results if row[0] == current_day), None)
        days.append(current_day)
        revenues.append(match[1] if match else 0)
        customers.append(match[2] if match else 0)

    return days, revenues, customers


def update_weekly_graph(ax_revenue, ax_customers, canvas, start_date=None):
    """
    Cập nhật biểu đồ thống kê theo 7 ngày gần nhất.
    """
    days, revenues, customers = fetch_revenue_and_customers_7_days()

    # Biểu đồ doanh thu
    ax_revenue.clear()
    ax_revenue.set_facecolor('#F7F7F7')
    bars_revenue = ax_revenue.bar(days, revenues, color='#FFC5C5')
    ax_revenue.set_title('Doanh thu 7 ngày gần nhất', fontsize=10)
    ax_revenue.set_ylabel('Doanh thu (VND)', fontsize=8)
    ax_revenue.tick_params(axis='x', labelrotation=45, labelsize=8)
    for bar, revenue in zip(bars_revenue, revenues):
        ax_revenue.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                        format_vnd(revenue), ha="center", va="bottom", fontsize=6)

    # Biểu đồ số lượng khách hàng
    ax_customers.clear()
    ax_customers.set_facecolor('#F7F7F7')
    bars_customers = ax_customers.bar(days, customers, color='#85C1E9')
    ax_customers.set_title('Số lượng khách hàng 7 ngày gần nhất', fontsize=10)
    ax_customers.set_ylabel('Số khách hàng', fontsize=8)
    ax_customers.tick_params(axis='x', labelrotation=45, labelsize=8)
    for bar, customer_count in zip(bars_customers, customers):
        ax_customers.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                          customer_count, ha="center", va="bottom", fontsize=6)

    canvas.draw()


def fetch_daily_revenue(date):
    cursor.execute(
        "SELECT SUM(idt.TotalAmt) "
        "FROM invoicedetailtbl AS idt "
        "JOIN invoicetbl AS it ON idt.InvoiceID = it.InvoiceID "
        "WHERE it.InvoiceDate = %s",
        (date,)
    )
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0


def fetch_daily_customers(date):
    cursor.execute(
        "SELECT COUNT(DISTINCT it.CustID) "
        "FROM invoicetbl AS it "
        "WHERE it.InvoiceDate = %s",  # So sánh trực tiếp ngày dạng text
        (date,)
    )
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0


def fetch_daily_services(date):
    cursor.execute(
        "SELECT SUM(idt.SQuantity) "
        "FROM invoicedetailtbl AS idt "
        "JOIN invoicetbl AS it ON idt.InvoiceID = it.InvoiceID "
        "WHERE it.InvoiceDate = %s",  # So sánh trực tiếp ngày dạng text
        (date,)
    )
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0


def fetch_daily_hot_services(date):
    cursor.execute(
        """
        SELECT idt.ServiceID, SUM(idt.SQuantity) AS TotalQuantity 
        FROM invoicedetailtbl AS idt
        JOIN invoicetbl AS it ON idt.InvoiceID = it.InvoiceID
        WHERE it.InvoiceDate = %s
        GROUP BY idt.ServiceID
        ORDER BY TotalQuantity DESC
        LIMIT 1
        """,
        (date,)
    )
    result = cursor.fetchone()
    return result[0] if result else None


def fetch_daily_hot_services_counter(date):
    cursor.execute(
        """
        SELECT idt.ServiceID, SUM(idt.SQuantity) AS TotalQuantity 
        FROM invoicedetailtbl AS idt
        JOIN invoicetbl AS it ON idt.InvoiceID = it.InvoiceID
        WHERE it.InvoiceDate = %s
        GROUP BY idt.ServiceID
        ORDER BY TotalQuantity DESC
        LIMIT 1
        """,
        (date,)
    )
    result = cursor.fetchone()
    return result[1] if result else 0


def fetch_hSevriceName(service_id):
    cursor.execute(
        "SELECT SName FROM servicetbl WHERE ServiceID = %s",
        (service_id,)
    )
    result = cursor.fetchone()
    return result[0] if result else None


def update_daily_stats(date_var, revenue_label, customers_label, services_label):
    date = date_var.entry.get()  # Lấy giá trị ngày từ entry

    revenue = fetch_daily_revenue(date)
    customers = fetch_daily_customers(date)
    services = fetch_daily_services(date)

    revenue_label.config(text=f"Tổng doanh thu: {format_vnd(revenue)}")
    customers_label.config(text=f"Tổng số khách hàng: {customers}")
    services_label.config(text=f"Số dịch vụ đã tiêu thụ: {services}")


def fetch_monthly_revenue(year):
    total_amounts = []
    for month in range(1, 13):
        cursor.execute(
            r"SELECT SUM(idt.TotalAmt) "
            r"FROM invoicedetailtbl AS idt "
            r"JOIN invoicetbl AS it ON idt.InvoiceID = it.InvoiceID "
            r"WHERE YEAR(STR_TO_DATE(it.InvoiceDate, '%%m/%%d/%%Y')) = %s "
            r"AND MONTH(STR_TO_DATE(it.InvoiceDate, '%%m/%%d/%%Y')) = %s",
            (year, month)
        )
        result = cursor.fetchone()
        total_amounts.append(result[0] if result[0] is not None else 0)
    return total_amounts


def fetch_monthly_service_usage(year):
    count_usage = []
    for month in range(1, 13):
        cursor.execute(
            r"SELECT SUM(idt.TotalAmt) "
            r"FROM invoicedetailtbl AS idt "
            r"JOIN invoicetbl AS it ON idt.InvoiceID = it.InvoiceID "
            r"WHERE YEAR(STR_TO_DATE(it.InvoiceDate, '%%m/%%d/%%Y')) = %s "
            r"AND MONTH(STR_TO_DATE(it.InvoiceDate, '%%m/%%d/%%Y')) = %s",
            (year, month)
        )
        result = cursor.fetchone()
        count_usage.append(result[0] if result[0] is not None else 0)
    return count_usage

def update_monthly_service_usage_graph(ax, canvas, year):
    count_usage = fetch_monthly_service_usage(year)

    month_names = [
        "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6",
        "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"
    ]

    ax.clear()
    ax.set_facecolor('#F7F7F7')
    bars = ax.bar(range(1, 13), count_usage, color='#FFC5C5')
    for bar, total in zip(bars, count_usage):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), format_vnd(total), ha="center", va="bottom",
                fontsize=6)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names)
    ax.set_ylabel("Tổng số lượt sử dụng", fontsize=8)
    ax.set_title("Tổng nhu cầu hàng tháng", fontsize=10)
    ax.tick_params(axis='x', labelsize=6)
    ax.tick_params(axis='y', labelsize=6)

    canvas.draw()


def update_monthly_graph(ax, canvas, year):
    total_amounts = fetch_monthly_revenue(year)

    month_names = [
        "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6",
        "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"
    ]

    ax.clear()
    ax.set_facecolor('#F7F7F7')
    bars = ax.bar(range(1, 13), total_amounts, color='#FFC5C5')
    for bar, total in zip(bars, total_amounts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), format_vnd(total), ha="center", va="bottom",
                fontsize=6)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names)
    ax.set_ylabel("Tổng doanh thu", fontsize=8)
    ax.set_title("Tổng doanh thu hàng tháng", fontsize=10)
    ax.tick_params(axis='x', labelsize=6)
    ax.tick_params(axis='y', labelsize=6)

    canvas.draw()


def show_thongKe(window, user_role, buttons, thongKe_btn):
    if user_role != 'admin':
        messagebox.showerror("Access Denied", "Bạn không có quyền truy cập vào tính năng này")
        return

    clicked(thongKe_btn, buttons)

    thongKe_frame = tb.Labelframe(window, bootstyle="secondary", text="Quản lý thống kê")
    thongKe_frame.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")
    thongKe_frame.columnconfigure(0, weight=1)
    thongKe_frame.rowconfigure(0, weight=1)

    notebook = tb.Notebook(thongKe_frame, bootstyle="secondary")
    notebook.pack(fill="both", expand=True, padx=5, pady=5)

    # ======== Tab Thống kê theo ngày ========
    daily_tab = tb.Frame(notebook)
    notebook.add(daily_tab, text="Thống kê theo ngày")

    # Date entry
    date_var = tb.StringVar()
    date_entry = tb.DateEntry(daily_tab, bootstyle="info", dateformat="%m/%d/%Y")
    date_entry.pack(fill="x", padx=10, pady=10)

    # Labels for displaying statistics
    revenue_label = tb.Label(daily_tab, text="Tổng doanh thu: ", bootstyle="info")
    revenue_label.pack(fill="x", padx=10, pady=5)

    customers_label = tb.Label(daily_tab, text="Tổng số khách hàng: ", bootstyle="info")
    customers_label.pack(fill="x", padx=10, pady=5)

    services_label = tb.Label(daily_tab, text="Số dịch vụ đã tiêu thụ: ", bootstyle="info")
    services_label.pack(fill="x", padx=10, pady=5)

    hot_services_label = tb.Label(daily_tab, text="Dịch vụ bán chạy nhất: ", bootstyle="info")
    hot_services_label.pack(fill="x", padx=10, pady=5)

    # Create Matplotlib figure and canvas
    fig_daily = Figure(figsize=(6, 4), dpi=100)
    ax_daily = fig_daily.add_subplot(111)
    canvas_daily = FigureCanvasTkAgg(fig_daily, master=daily_tab)
    canvas_daily.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def update_daily_graph(date):
        """
        Cập nhật biểu đồ theo dữ liệu doanh thu ngày.
        """
        revenue = fetch_daily_revenue(date)
        customers = fetch_daily_customers(date)
        services = fetch_daily_services(date)
        hot_services = fetch_daily_hot_services(date)
        hot_service_name = fetch_hSevriceName(hot_services)

        # Cập nhật nhãn
        revenue_label.config(text=f"Tổng doanh thu: {format_vnd(revenue)}")
        customers_label.config(text=f"Tổng số khách hàng: {customers}")
        services_label.config(text=f"Số dịch vụ đã tiêu thụ: {services}")
        hot_services_label.config(text=f"Dịch vụ bán chạy nhất trong ngày: {hot_service_name} ({hot_services})")

        # Cập nhật biểu đồ
        ax_daily.clear()
        categories = ['Doanh thu', 'Khách hàng', 'Dịch vụ']
        values = [revenue, customers, services]
        colors = ['#FFC5C5', '#85C1E9', '#82E0AA']

        bars = ax_daily.bar(categories, values, color=colors)
        for bar, value in zip(bars, values):
            ax_daily.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                          str(value), ha="center", va="bottom", fontsize=10)

        ax_daily.set_title(f"Thống kê ngày: {date}", fontsize=12)
        ax_daily.set_ylabel("Giá trị")
        canvas_daily.draw()

    # Button to update daily stats and graph
    daily_update_button = tb.Button(
        daily_tab, text="Cập nhật",
        command=lambda: update_daily_graph(date_entry.entry.get())
    )
    daily_update_button.pack(fill="x", padx=10, pady=10)

    # ======== Tab Thống kê theo tháng ========
    monthly_tab = tb.Frame(notebook)
    notebook.add(monthly_tab, text="Thống kê theo tháng")

    current_year = datetime.now().year
    year_var = tb.StringVar()
    year_combobox = tb.Combobox(monthly_tab, textvariable=year_var)
    year_combobox['values'] = [year for year in range(current_year - 5, current_year + 5)]
    year_combobox.current(4)
    year_combobox.pack(fill="x", padx=10, pady=10)

    fig_monthly = Figure(figsize=(6, 4), dpi=100)
    ax_monthly = fig_monthly.add_subplot(111)
    canvas_monthly = FigureCanvasTkAgg(fig_monthly, master=monthly_tab)
    canvas_monthly.get_tk_widget().pack(fill="both", expand=True)

    monthly_update_button = tb.Button(
        monthly_tab, text="Cập nhật",
        command=lambda: update_monthly_graph(ax_monthly, canvas_monthly, int(year_var.get()))
    )
    monthly_update_button.pack(fill="x", padx=10, pady=10)

    update_monthly_graph(ax_monthly, canvas_monthly, int(year_combobox.get()))


    # # ======== Tab Thống kê theo dịch vụ ========
    # monthly_tab = tb.Frame(notebook)
    # notebook.add(monthly_tab, text="Thống kê theo dịch vụ")
    #
    # current_year = datetime.now().year
    # year_var = tb.StringVar()
    # year_combobox = tb.Combobox(monthly_tab, textvariable=year_var)
    # year_combobox['values'] = [year for year in range(current_year - 5, current_year + 5)]
    # year_combobox.current(4)
    # year_combobox.pack(fill="x", padx=10, pady=10)
    #
    # fig_monthly = Figure(figsize=(6, 4), dpi=100)
    # ax_monthly = fig_monthly.add_subplot(111)
    # canvas_monthly = FigureCanvasTkAgg(fig_monthly, master=monthly_tab)
    # canvas_monthly.get_tk_widget().pack(fill="both", expand=True)
    #
    # monthly_update_button = tb.Button(
    #     monthly_tab, text="Cập nhật",
    #     command=lambda: update_monthly_graph(ax_monthly, canvas_monthly, int(year_var.get()))
    # )
    # monthly_update_button.pack(fill="x", padx=10, pady=10)
    #
    # update_monthly_graph(ax_monthly, canvas_monthly, int(year_combobox.get()))


    # ======== Tab Thống kê theo từng dịch vụ ========
    monthly_service_tab = tb.Frame(notebook)
    notebook.add(monthly_service_tab, text="Thống kê theo từng dịch vụ")

    current_year = datetime.now().year
    year_var = tb.StringVar()
    year_combobox = tb.Combobox(monthly_service_tab, textvariable=year_var)
    year_combobox['values'] = [year for year in range(current_year - 5, current_year + 5)]
    year_combobox.current(4)
    year_combobox.pack(fill="x", padx=10, pady=10)


    def get_service_name():
        cursor.execute(
            "SELECT SName FROM servicetbl"
        )
        results = cursor.fetchall()
        service_names = []

        for row in results:
            service_names.append(row[0])

        return service_names

    service_var = tb.StringVar()
    sercice_combobox = tb.Combobox(monthly_service_tab, textvariable=service_var)
    sercice_combobox['values'] = get_service_name()
    sercice_combobox.current(4)
    sercice_combobox.pack(fill="x", padx=10, pady=10)

    fig_monthly_service_usage = Figure(figsize=(6, 4), dpi=100)
    ax_monthly = fig_monthly.add_subplot(111)
    canvas_monthly = FigureCanvasTkAgg(fig_monthly_service_usage, master=monthly_service_tab)
    canvas_monthly.get_tk_widget().pack(fill="both", expand=True)

    monthly_update_button = tb.Button(
        monthly_service_tab, text="Cập nhật",
        command=lambda: update_monthly_service_usage_graph(ax_monthly, canvas_monthly, int(year_var.get()))
    )
    monthly_update_button.pack(fill="x", padx=10, pady=10)

    update_monthly_service_usage_graph(ax_monthly, canvas_monthly, int(year_combobox.get()))
