from datetime import timedelta, datetime
from tkinter import messagebox
import ttkbootstrap as tb
from utils import clicked
from DB import cursor
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-pastel')

def format_vnd(amount):
    return f"{amount:,.0f}".replace(',', '.') + " VND"


#Thống kê 7 ngày gần nhẩt
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

#Thống kê daily
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

#Thống kê số lượng dịch vụ sử dụng từng tháng trong năm
def fetch_monthly_service_usage(year, service_id):
    count_usage = []
    for month in range(1, 13):
        cursor.execute(
            r"SELECT SUM(idt.SQuantity) "
            r"FROM invoicedetailtbl AS idt "
            r"JOIN invoicetbl AS it ON idt.InvoiceID = it.InvoiceID "
            r"WHERE YEAR(STR_TO_DATE(it.InvoiceDate, '%%d/%%m/%%Y')) = %s "
            r"AND MONTH(STR_TO_DATE(it.InvoiceDate, '%%d/%%m/%%Y')) = %s "
            r"AND idt.ServiceID = %s",
            (year, month, service_id)
        )
        result = cursor.fetchone()
        count_usage.append(result[0] if result[0] is not None else 0)
    return count_usage



def update_monthly_service_usage_graph(ax, canvas, year, service_id):
    count_usage = fetch_monthly_service_usage(year, service_id)

    month_names = [
        "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6",
        "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"
    ]

    ax.clear()
    ax.set_facecolor('#F7F7F7')
    bars = ax.bar(range(1, 13), count_usage, color='#FFC5C5')
    for bar, total in zip(bars, count_usage):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), total, ha="center", va="bottom",
                fontsize=6)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names)
    ax.set_ylabel("Tổng số lượt sử dụng", fontsize=8)
    ax.set_title(f"Tổng nhu cầu hàng tháng cho dịch vụ: {service_id}", fontsize=10)
    ax.tick_params(axis='x', labelsize=6)
    ax.tick_params(axis='y', labelsize=6)

    canvas.draw()


#Thống kê doanh thu từng tháng trong năm
def fetch_monthly_revenue(year):
    # Thực hiện truy vấn SQL
    cursor.execute(
        """
        SELECT 
            MONTH(STR_TO_DATE(it.InvoiceDate, '%%d/%%m/%%Y')) AS month,
            SUM(idt.TotalAmt) AS total_revenue
        FROM 
            invoicedetailtbl AS idt
        JOIN 
            invoicetbl AS it 
            ON idt.InvoiceID = it.InvoiceID
        WHERE 
            YEAR(STR_TO_DATE(it.InvoiceDate, '%%d/%%m/%%Y')) = %s
        GROUP BY 
            MONTH(STR_TO_DATE(it.InvoiceDate, '%%d/%%m/%%Y'))
        ORDER BY 
            month;
        """,
        (year,)
    )
    results = cursor.fetchall()

    # Khởi tạo danh sách doanh thu mặc định (0 cho các tháng không có dữ liệu)
    total_amounts = [0] * 12
    for month, total_revenue in results:
        total_amounts[month - 1] = total_revenue if total_revenue is not None else 0

    return total_amounts


def update_monthly_graph(ax, canvas, year):
    # Lấy doanh thu từng tháng
    total_amounts = fetch_monthly_revenue(year)

    # Tên các tháng
    month_names = [
        "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6",
        "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"
    ]

    # Xóa dữ liệu cũ trên biểu đồ
    ax.clear()
    ax.set_facecolor('#F7F7F7')

    # Vẽ biểu đồ cột với doanh thu từng tháng
    bars = ax.bar(range(1, 13), total_amounts, color='#FFC5C5')

    # Hiển thị giá trị doanh thu trên từng cột
    for bar, total in zip(bars, total_amounts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # Vị trí giữa cột
            bar.get_height(),                  # Đỉnh cột
            format_vnd(total),                 # Định dạng tiền tệ
            ha="center", va="bottom", fontsize=6
        )

    # Thiết lập tên các tháng trên trục X
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names)

    # Tùy chỉnh kích thước nhãn trục
    ax.tick_params(axis='x', labelsize=6)
    ax.tick_params(axis='y', labelsize=6)

    # Cập nhật biểu đồ
    canvas.draw()


def fetch_monthly_expenses(year):
    """
    Lấy tổng chi theo từng tháng trong năm từ bảng stockintbl.

    :param year: Năm cần thống kê (dạng số nguyên, ví dụ: 2024).
    :return: Danh sách tổng chi (12 phần tử, mỗi phần tử tương ứng với một tháng).
    """
    # Thực hiện truy vấn SQL
    cursor.execute(
        """
        SELECT 
            SUBSTR(StockInDate, 6, 2) AS month,  -- Lấy tháng từ vị trí 6-7
            SUM(TotalAmt) AS total_expense      -- Tính tổng chi tiêu
        FROM 
            stockintbl
        WHERE 
            SUBSTR(StockInDate, 1, 4) = %s      -- Lọc theo năm (4 ký tự đầu tiên)
        GROUP BY 
            SUBSTR(StockInDate, 6, 2)           -- Nhóm theo tháng
        ORDER BY 
            month;                              -- Sắp xếp theo tháng
        """,
        (str(year),)
    )
    results = cursor.fetchall()

    # Khởi tạo danh sách chi tiêu mặc định (0 cho các tháng không có dữ liệu)
    total_expenses = [0] * 12
    for month, total_expense in results:
        month = int(month)  # Chuyển đổi tháng từ chuỗi sang số nguyên
        total_expenses[month - 1] = total_expense if total_expense is not None else 0

    return total_expenses

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
    notebook.add(daily_tab, text="Doanh thu ngày")

    # Date entry
    date_var = tb.StringVar()
    date_entry = tb.DateEntry(daily_tab, bootstyle="info", dateformat="%d/%m/%Y")
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

    # ======== Tab Thống kê doanh thu theo tháng trong 1 năm ========
    monthly_tab = tb.Frame(notebook)
    notebook.add(monthly_tab, text="Doanh thu theo tháng")

    current_year = datetime.now().year
    year_var_monthly = tb.StringVar()
    year_combobox_monthly = tb.Combobox(monthly_tab, textvariable=year_var_monthly)
    year_combobox_monthly['values'] = [year for year in range(current_year - 5, current_year + 5)]
    year_combobox_monthly.current(4)
    year_combobox_monthly.pack(fill="x", padx=10, pady=10)

    fig_monthly = Figure(figsize=(6, 4), dpi=100)
    ax_monthly = fig_monthly.add_subplot(111)
    canvas_monthly = FigureCanvasTkAgg(fig_monthly, master=monthly_tab)
    canvas_monthly.get_tk_widget().pack(fill="both", expand=True)

    monthly_update_button = tb.Button(
        monthly_tab, text="Cập nhật",
        command=lambda: update_monthly_graph(ax_monthly, canvas_monthly, int(year_var_monthly.get()))
    )
    monthly_update_button.pack(fill="x", padx=10, pady=10)

    update_monthly_graph(ax_monthly, canvas_monthly, int(year_combobox_monthly.get()))

    # ======== Tab Thống kê số dịch vụ được sử dụng trong các tháng của năm ========
    monthly_service_tab = tb.Frame(notebook)
    notebook.add(monthly_service_tab, text="Dịch vụ bán được trong các tháng")
    current_year = datetime.now().year
    year_var_service = tb.StringVar()
    year_combobox_service = tb.Combobox(monthly_service_tab, textvariable=year_var_service)
    year_combobox_service['values'] = [year for year in range(current_year - 5, current_year + 5)]
    year_combobox_service.current(4)
    year_combobox_service.pack(fill="x", padx=10, pady=10)

    def get_service_name():
        cursor.execute("SELECT ServiceID, SName FROM servicetbl")
        results = cursor.fetchall()
        service_map = {str(row[0]): row[1] for row in results}  # ServiceID làm key
        return service_map

    def get_service_id_by_name(service_name):
        for service_id, name in service_map.items():
            if name == service_name:
                return int(service_id)
        return None

    service_var = tb.StringVar()
    service_combobox = tb.Combobox(monthly_service_tab, textvariable=service_var)
    service_map = get_service_name()
    service_combobox['values'] = list(service_map.values())
    service_combobox.current(4)
    service_combobox.pack(fill="x", padx=10, pady=10)


    fig_monthly_service = Figure(figsize=(6, 4), dpi=100)
    ax_monthly_service = fig_monthly_service.add_subplot(111)
    canvas_monthly_service = FigureCanvasTkAgg(fig_monthly_service, master=monthly_service_tab)
    canvas_monthly_service.get_tk_widget().pack(fill="both", expand=True)

    monthly_update_button_service = tb.Button(
        monthly_service_tab, text="Cập nhật",
        command=lambda: update_monthly_service_usage_graph(
            ax_monthly_service,
            canvas_monthly_service,
            int(year_var_service.get()),
            get_service_id_by_name(service_var.get())  # Lấy ServiceID từ tên dịch vụ
        )
    )

    monthly_update_button_service.pack(fill="x", padx=10, pady=10)

    update_monthly_service_usage_graph(
        ax_monthly_service,
        canvas_monthly_service,
        int(year_combobox_service.get()),
        service_combobox.get()
    )

    # ======== Tab Thống kê tổng chi theo tháng trong 1 năm ========
    monthly_expense_tab = tb.Frame(notebook)
    notebook.add(monthly_expense_tab, text="Tổng chi theo tháng")

    # Tạo combobox để chọn năm
    current_year = datetime.now().year
    year_var_monthly_expense = tb.StringVar()
    year_combobox_monthly_expense = tb.Combobox(monthly_expense_tab, textvariable=year_var_monthly_expense)
    year_combobox_monthly_expense['values'] = [year for year in range(current_year - 5, current_year + 5)]
    year_combobox_monthly_expense.current(5)  # Mặc định chọn năm hiện tại
    year_combobox_monthly_expense.pack(fill="x", padx=10, pady=10)

    # Tạo biểu đồ matplotlib
    fig_monthly_expense = Figure(figsize=(6, 4), dpi=100)
    ax_monthly_expense = fig_monthly_expense.add_subplot(111)
    canvas_monthly_expense = FigureCanvasTkAgg(fig_monthly_expense, master=monthly_expense_tab)
    canvas_monthly_expense.get_tk_widget().pack(fill="both", expand=True)

    # Nút cập nhật
    monthly_update_button_expense = tb.Button(
        monthly_expense_tab,
        text="Cập nhật",
        command=lambda: update_monthly_expense_graph(ax_monthly_expense, canvas_monthly_expense,
                                                     int(year_var_monthly_expense.get()))
    )
    monthly_update_button_expense.pack(fill="x", padx=10, pady=10)

    # Hàm cập nhật biểu đồ
    def update_monthly_expense_graph(ax, canvas, year):
        """
        Cập nhật biểu đồ thống kê tổng chi theo tháng trong năm.

        :param ax: Đối tượng Axes của Matplotlib.
        :param canvas: Đối tượng Canvas của Matplotlib.
        :param year: Năm cần thống kê (dạng số nguyên, ví dụ: 2024).
        """
        # Lấy dữ liệu tổng chi từng tháng
        total_expenses = fetch_monthly_expenses(year)

        # Tên các tháng
        month_names = [
            "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6",
            "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"
        ]

        # Xóa dữ liệu cũ trên biểu đồ
        ax.clear()
        ax.set_facecolor('#F7F7F7')

        # Vẽ biểu đồ cột với tổng chi từng tháng
        bars = ax.bar(range(1, 13), total_expenses, color='#82E0AA')

        # Hiển thị giá trị tổng chi trên từng cột
        for bar, total in zip(bars, total_expenses):
            ax.text(
                bar.get_x() + bar.get_width() / 2,  # Vị trí giữa cột
                bar.get_height(),  # Đỉnh cột
                format_vnd(total),  # Định dạng tiền tệ
                ha="center", va="bottom", fontsize=6
            )

        # Thiết lập tên các tháng trên trục X
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(month_names)

        # Tùy chỉnh kích thước nhãn trục
        ax.tick_params(axis='x', labelsize=6)
        ax.tick_params(axis='y', labelsize=6)

        # Thiết lập tiêu đề và nhãn trục
        ax.set_title(f"Tổng chi theo tháng trong năm {year}", fontsize=10)
        ax.set_ylabel("Tổng chi (VND)", fontsize=8)
        ax.set_xlabel("Tháng", fontsize=8)

        # Cập nhật biểu đồ
        canvas.draw()

    # Lần đầu khởi chạy: cập nhật biểu đồ với năm mặc định
    update_monthly_expense_graph(ax_monthly_expense, canvas_monthly_expense, int(year_combobox_monthly_expense.get()))


