import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from DB import cursor, db
from utils import clicked
from datetime import datetime, timedelta, date

def show_hoaDon(window, user_role, buttons, hoaDon_btn):
    """
    Hiển thị giao diện quản lý hóa đơn.

    Args:
        window: Cửa sổ chính.
        user_role: Vai trò người dùng.
        buttons: Danh sách các nút.
        hoaDon_btn: Nút hiện tại đang được kích hoạt.
    """
    if user_role not in ["admin", "cashier"]:
        messagebox.showerror("Access Denied", "Bạn không có quyền truy cập vào tính năng này.")
        return

    clicked(hoaDon_btn, buttons)

    invoice_frame = tb.Labelframe(window, bootstyle="secondary", text="Quản lý Hóa đơn")
    invoice_frame.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")
    invoice_frame.columnconfigure(0, weight=1)
    invoice_frame.rowconfigure(0, weight=1)
    invoice_frame.rowconfigure((1, 2, 3, 4, 5, 6), weight=15)

    header_frame = tb.Frame(invoice_frame, height=60)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="new")

    content_frame = tb.Frame(invoice_frame)
    content_frame.grid(row=0, column=0, columnspan=2, rowspan=7, sticky="news")
    content_frame.columnconfigure((0, 1), weight=50)
    content_frame.columnconfigure(3, weight=1)
    content_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

    tree_scroll = tb.Scrollbar(content_frame, orient="vertical", bootstyle="primary-round")
    tree_scroll.grid(row=0, rowspan=6, column=3, sticky="wnes", padx=5, pady=30)

    columns = ("InvoiceID", "InvoiceDate", "CustName", "EmpName", "TotalAmt")
    table = tb.Treeview(content_frame, columns=columns, show='headings', yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=table.yview)

    table.heading("InvoiceID", text="Mã Hóa Đơn")
    table.heading("InvoiceDate", text="Ngày Hóa Đơn")
    table.heading("CustName", text="Tên Khách Hàng")
    table.heading("EmpName", text="Tên Nhân Viên")
    table.heading("TotalAmt", text="Tổng Tiền")

    table.column("InvoiceID", width=30, anchor="center")
    table.column("InvoiceDate", width=150, anchor="center")
    table.column("CustName", width=80, anchor="center")
    table.column("EmpName", width=70, anchor="center")
    table.column("TotalAmt", width=150, anchor="center")

    table.grid(row=0, column=0, padx=10, pady=10, rowspan=6, columnspan=2, sticky="news")

    funcbar = tb.Frame(content_frame, height=60)
    funcbar.grid(row=6, column=0, columnspan=3, sticky="news")
    funcbar.columnconfigure((0, 1, 2, 3, 5), weight=1)
    funcbar.columnconfigure(4, weight=30)

    def fetch_and_insert_data():
        query = """
                SELECT InvoiceTbl.InvoiceID, InvoiceTbl.InvoiceDate, CustomerTbl.CustName, 
                       EmployeeTbl.EmpName, 
                       SUM(COALESCE(InvoiceDetailTbl.TotalAmt, 0) + COALESCE(PetCareInvoiceDetailTbl.TotalAmt, 0)) as TotalAmt
                FROM InvoiceTbl
                LEFT JOIN CustomerTbl ON InvoiceTbl.CustID = CustomerTbl.CustID
                LEFT JOIN EmployeeTbl ON InvoiceTbl.EmpID = EmployeeTbl.EmpID
                LEFT JOIN InvoiceDetailTbl ON InvoiceTbl.InvoiceID = InvoiceDetailTbl.InvoiceID
                LEFT JOIN PetCareInvoiceDetailTbl ON InvoiceTbl.InvoiceID = PetCareInvoiceDetailTbl.InvoiceID
                GROUP BY InvoiceTbl.InvoiceID, InvoiceTbl.InvoiceDate, CustomerTbl.CustName, 
                         EmployeeTbl.EmpName
                """
        cursor.execute(query)
        for item in table.get_children():
            table.delete(item)
        data = cursor.fetchall()
        for item in data:
            table.insert('', tb.END, values=(item[0], item[1], item[2], item[3], item[4]))

    fetch_and_insert_data()

    def add_invoice():
        def load_customer_data():
            cursor.execute("SELECT CustID, CustName, CustNumber, CustAddress FROM CustomerTbl")
            customers = cursor.fetchall()

            for customer in customers:
                customer_tree.insert("", "end", values=customer)

        def on_customer_select(event):
            selected_item = customer_tree.selection()[0]
            values = customer_tree.item(selected_item, "values")
            cust_id_entry.config(state="normal")
            cust_name_entry.config(state="normal")
            cust_contact_entry.config(state="normal")
            cust_address_entry.config(state="normal")
            cust_id_entry.delete(0, tk.END)
            cust_id_entry.insert(0, values[0])
            cust_name_entry.delete(0, tk.END)
            cust_name_entry.insert(0, values[1])
            cust_contact_entry.delete(0, tk.END)
            cust_contact_entry.insert(0, values[2])
            cust_address_entry.delete(0, tk.END)
            cust_address_entry.insert(0, values[3])
            cust_id_entry.config(state="readonly")
            cust_name_entry.config(state="readonly")
            cust_contact_entry.config(state="readonly")
            cust_address_entry.config(state="readonly")

        def load_service_data():
            cursor.execute("SELECT ServiceID, SName, SCategories, SQuantity, SPrice FROM ServiceTbl")
            services = cursor.fetchall()

            for service in services:
                service_tree.insert("", "end", values=service)

        def on_service_select(event):
            selected_item = service_tree.selection()[0]
            values = service_tree.item(selected_item, "values")
            service_id_entry.config(state="normal")
            service_name_entry.config(state="normal")
            service_price_entry.config(state="normal")
            service_id_entry.delete(0, tk.END)
            service_id_entry.insert(0, values[0])
            service_name_entry.delete(0, tk.END)
            service_name_entry.insert(0, values[1])
            service_price_entry.delete(0, tk.END)
            service_price_entry.insert(0, values[4])
            service_id_entry.config(state="readonly")
            service_name_entry.config(state="readonly")
            service_price_entry.config(state="readonly")

        def add_to_bill():
            try:
                service_id = service_id_entry.get()
                service_name = service_name_entry.get()
                service_price = float(service_price_entry.get())
                service_qty = int(service_qty_entry.get())

                if not service_qty or service_qty <= 0:
                    raise ValueError("Invalid quantity")

                total_price = service_qty * service_price

                # Add to bill tree
                bill_tree.insert("", "end", values=(service_id, service_name, service_qty, total_price))

                # Update total bill
                current_total = float(total_var.get())
                new_total = current_total + total_price
                total_var.set(str(new_total))

            except ValueError as ve:
                messagebox.showerror("Invalid Input", str(ve))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def remove_from_bill():
            selected_item = bill_tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "No item selected")
                return

            for item in selected_item:
                values = bill_tree.item(item, "values")
                bill_tree.delete(item)

                total_price = float(values[2])
                current_total = float(total_var.get())
                new_total = current_total - total_price
                total_var.set(str(new_total))

        def save_invoice(emp_id):
            try:
                invoice_id_val = invoice_id.get()
                invoice_date_val = invoice_date.entry.get()
                cust_id_val = cust_id_entry.get()
                total_amount = total_var.get()

                cursor.execute(
                    "INSERT INTO InvoiceTbl (InvoiceID, InvoiceDate, CustID, EmpID) VALUES (%s, %s, %s, %s)",
                    (invoice_id_val, invoice_date_val, cust_id_val, emp_id)
                )

                for item in bill_tree.get_children():
                    values = bill_tree.item(item, "values")
                    service_id_val = values[0]
                    service_qty_val = values[2]
                    service_price_val = values[3]

                    cursor.execute(
                        "INSERT INTO InvoiceDetailTbl (InvoiceID, ServiceID, SQuantity, SPrice, TotalAmt, idDate) VALUES (%s, %s, %s, %s, %s, %s)",
                        (invoice_id_val, service_id_val, service_qty_val, service_price_val, total_amount,
                         invoice_date_val)
                    )

                    cursor.execute(
                        "UPDATE ServiceTbl SET SQuantity = SQuantity - %s WHERE ServiceID = %s",
                        (service_qty_val, service_id_val)
                    )

                db.commit()
                messagebox.showinfo("Success", "Invoice saved successfully")

            except Exception as e:
                messagebox.showerror("Error", str(e))
                db.rollback()

        def show_invoice_preview():
            # Hàm để định dạng số tiền
            def format_currency(amount):
                return "{:,.0f} ₫".format(amount).replace(",", ".")

            # Tạo cửa sổ mới để hiển thị thông tin hóa đơn
            preview_window = tb.Toplevel(title="Xem trước hóa đơn", minsize=(600, 800))
            preview_window.geometry("600x800")

            # Frame chính chứa toàn bộ nội dung hóa đơn
            main_frame = tb.Frame(preview_window, bootstyle="secondary")
            main_frame.pack(fill="both", padx=10, pady=10, expand=True)

            # Tiêu đề hóa đơn
            invoice_title_frame = tb.Frame(main_frame)
            invoice_title_frame.pack(fill="x", pady=10)
            tb.Label(invoice_title_frame, text="INVOICE", font=("Arial", 24, "bold")).pack()

            # Thông tin nhân viên và mã hóa đơn
            emp_invoice_info_frame = tb.Frame(main_frame)
            emp_invoice_info_frame.pack(fill="x", pady=10)

            tb.Label(emp_invoice_info_frame, text="NHÂN VIÊN:", font=("Arial", 12)).grid(row=0, column=0,
                                                                                         sticky="w")
            tb.Label(emp_invoice_info_frame, text=emp_id, font=("Arial", 12, "bold")).grid(row=0, column=1,
                                                                                           sticky="w", padx=10)
            tb.Label(emp_invoice_info_frame, text="MÃ HÓA ĐƠN:", font=("Arial", 12)).grid(row=0, column=2,
                                                                                          sticky="e", padx=(20, 0))
            tb.Label(emp_invoice_info_frame, text=invoice_id.get(), font=("Arial", 12, "bold")).grid(row=0,
                                                                                                     column=3,
                                                                                                     sticky="e",
                                                                                                     padx=10)
            tb.Label(emp_invoice_info_frame, text="DATE:", font=("Arial", 12)).grid(row=1, column=2, sticky="e",
                                                                                    padx=(20, 0), pady=5)
            tb.Label(emp_invoice_info_frame, text=invoice_date.entry.get(), font=("Arial", 12, "bold")).grid(row=1,
                                                                                                             column=3,
                                                                                                             sticky="e",
                                                                                                             padx=10,
                                                                                                             pady=5)

            # Danh sách dịch vụ
            service_frame = tb.Frame(main_frame)
            service_frame.pack(fill="both", pady=10, expand=True)

            service_columns = ("sl", "service_name", "price", "quantity", "total")
            service_tree_preview = tb.Treeview(service_frame, columns=service_columns, show="headings")

            # Setting headings and column properties explicitly
            service_tree_preview.heading("sl", text="SL.")
            service_tree_preview.heading("service_name", text="TÊN DỊCH VỤ")
            service_tree_preview.heading("price", text="PRICE")
            service_tree_preview.heading("quantity", text="QTY.")
            service_tree_preview.heading("total", text="TOTAL")

            service_tree_preview.column("sl", width=50, anchor="center")
            service_tree_preview.column("service_name", width=250, anchor="center")
            service_tree_preview.column("price", width=100, anchor="center")
            service_tree_preview.column("quantity", width=50, anchor="center")
            service_tree_preview.column("total", width=100, anchor="center")

            service_tree_preview.pack(fill="both", expand=True)

            # Thêm dữ liệu từ bill_tree vào service_tree_preview
            total_amount = 0
            for index, item in enumerate(bill_tree.get_children(), start=1):
                values = bill_tree.item(item, "values")
                service_name = values[1]
                quantity = int(float(values[2]))  # Chuyển đổi thành số nguyên nếu cần
                price = float(values[3])
                total = quantity * price
                total_amount += total
                formatted_price = format_currency(price)
                formatted_total = format_currency(total)
                service_tree_preview.insert("", "end", values=(
                    index, service_name, formatted_price, quantity, formatted_total))

            # Tổng hóa đơn
            total_frame = tb.Frame(main_frame)
            total_frame.pack(fill="x", pady=10)

            formatted_total_amount = format_currency(total_amount)
            tb.Label(total_frame, text="TỔNG HÓA ĐƠN:", font=("Arial", 12, "bold")).grid(row=0, column=2,
                                                                                         sticky="e", padx=10)
            tb.Label(total_frame, text=formatted_total_amount, font=("Arial", 12, "bold")).grid(row=0, column=3,
                                                                                                sticky="e", padx=10)

            # Lời cảm ơn
            thanks_frame = tb.Frame(main_frame)
            thanks_frame.pack(fill="x", pady=10)
            tb.Label(thanks_frame, text="Thank you for believing in us", font=("Arial", 12, "italic")).pack()

        add_window = tb.Toplevel(title="Thêm hóa đơn", minsize=(1280, 800))
        add_window.geometry("1280x800")

        lf = tb.Labelframe(add_window, bootstyle="secondary", text="")
        lf.pack(fill="both", padx=5, pady=5, expand=True, anchor="w")
        lf.columnconfigure((0, 1, 2), weight=1)
        lf.rowconfigure((0, 1, 2, 3), weight=1)

        customer_frame = tb.Labelframe(lf, bootstyle="secondary", text="Khách hàng")
        customer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="news")

        tk.Label(customer_frame, text="Mã khách hàng").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        cust_id_entry = tk.Entry(customer_frame, state="readonly")
        cust_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(customer_frame, text="Tên khách hàng").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        cust_name_entry = tk.Entry(customer_frame, state="readonly")
        cust_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(customer_frame, text="Liên hệ").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        cust_contact_entry = tk.Entry(customer_frame, state="readonly")
        cust_contact_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(customer_frame, text="Địa chỉ").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        cust_address_entry = tk.Entry(customer_frame, state="readonly")
        cust_address_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Customer List
        customer_list_frame = tb.Labelframe(lf, bootstyle="secondary", text="Danh sách khách hàng")
        customer_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="news")

        customer_columns = ("cust_id", "cust_name", "contact", "address")
        customer_tree = tb.Treeview(customer_list_frame, columns=customer_columns, show="headings")

        # Setting headings and column properties explicitly
        customer_tree.heading("cust_id", text="Id")
        customer_tree.heading("cust_name", text="Tên khách")
        customer_tree.heading("contact", text="SDT")
        customer_tree.heading("address", text="Địa chỉ")

        customer_tree.column("cust_id", width=30, anchor="center")
        customer_tree.column("cust_name", width=80, anchor="center")
        customer_tree.column("contact", width=80, anchor="center")
        customer_tree.column("address", width=80, anchor="center")

        customer_tree.grid(row=0, column=0, sticky="nsew")

        customer_list_frame.grid_rowconfigure(0, weight=1)
        customer_list_frame.grid_columnconfigure(0, weight=1)

        customer_tree.bind("<<TreeviewSelect>>", on_customer_select)

        # Load customer data
        load_customer_data()

        # Service Section
        service_frame = tb.Labelframe(lf, bootstyle="secondary", text="Dịch vụ")
        service_frame.grid(row=0, column=1, padx=10, pady=10, sticky="news")

        tk.Label(service_frame, text="Mã dịch vụ").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        service_id_entry = tk.Entry(service_frame, state="readonly")
        service_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(service_frame, text="Tên dịch vụ").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        service_name_entry = tk.Entry(service_frame, state="readonly")
        service_name_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        tk.Label(service_frame, text="Giá").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        service_price_entry = tk.Entry(service_frame, state="readonly")
        service_price_entry.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        tk.Label(service_frame, text="Số lượng").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        service_qty_entry = tk.Entry(service_frame)
        service_qty_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        add_to_bill_btn = tb.Button(service_frame, text="Thêm vào hóa đơn", bootstyle="primary",
                                    command=add_to_bill)
        add_to_bill_btn.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        remove_from_bill_btn = tb.Button(service_frame, text="Xóa khỏi hóa đơn", bootstyle="danger",
                                         command=remove_from_bill)
        remove_from_bill_btn.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Service List
        service_list_frame = tb.Labelframe(lf, bootstyle="secondary", text="Danh sách dịch vụ")
        service_list_frame.grid(row=1, column=1, padx=10, pady=10, sticky="news")

        service_columns = ("service_id", "service_name", "category", "quantity", "price")
        service_tree = tb.Treeview(service_list_frame, columns=service_columns, show="headings")
        for col in service_columns:
            service_tree.heading(col, text=col.replace("_", " ").title())
            service_tree.column(col, width=85)
        service_tree.grid(row=0, column=0, sticky="nsew")

        service_list_frame.grid_rowconfigure(0, weight=1)
        service_list_frame.grid_columnconfigure(0, weight=1)

        service_tree.bind("<<TreeviewSelect>>", on_service_select)

        # Load service data
        load_service_data()

        bill_info_frame = tb.Labelframe(lf, bootstyle="secondary", text="Chi tiết hóa đơn")
        bill_info_frame.grid(row=0, column=2, padx=10, pady=10, sticky="news")

        tk.Label(bill_info_frame, text="Mã hóa đơn").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        invoice_id = tk.Entry(bill_info_frame)
        invoice_id.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        cursor.execute("Select MAX(InvoiceID) FROM invoicetbl")
        result = cursor.fetchone()
        kID = result[0] + 1 if result and result[0] is not None else "No ID"
        invoice_id.insert(0, kID)

        tk.Label(bill_info_frame, text="Ngày xuất hóa đơn").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        invoice_date = tb.DateEntry(bill_info_frame)
        invoice_date.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Bill Frame
        bill_frame = tb.Labelframe(lf, bootstyle="secondary", text="Hóa đơn")
        bill_frame.grid(row=1, column=2, padx=10, pady=10, sticky="news")

        bill_columns = ("service_id_to_bill", "service_name_to_bill", "quantity_to_bill", "price_to_bill")
        bill_tree = tb.Treeview(bill_frame, columns=bill_columns, show="headings")

        # Setting headings and column properties explicitly
        bill_tree.heading("service_id_to_bill", text="Id Dịch Vụ")
        bill_tree.heading("service_name_to_bill", text="Tên Dịch Vụ")
        bill_tree.heading("quantity_to_bill", text="Số Lượng")
        bill_tree.heading("price_to_bill", text="Giá")

        bill_tree.column("service_id_to_bill", width=95, anchor="center")
        bill_tree.column("service_name_to_bill", width=95, anchor="center")
        bill_tree.column("quantity_to_bill", width=95, anchor="center")
        bill_tree.column("price_to_bill", width=95, anchor="center")

        bill_tree.grid(row=0, column=0, sticky="nsew")

        bill_frame.grid_rowconfigure(0, weight=1)
        bill_frame.grid_columnconfigure(0, weight=1)

        # Total Bill Section
        total_frame = tb.Frame(lf, bootstyle="secondary")
        total_frame.grid(row=2, column=2, padx=10, pady=10, sticky="new")

        tk.Label(total_frame, text="Tổng hóa đơn").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        total_var = tk.StringVar(value="0")
        total_label = tk.Label(total_frame, textvariable=total_var)
        total_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Print Invoice Button
        print_invoice_btn = tb.Button(lf, text="In hóa đơn", bootstyle="success",
                                      command=lambda: [save_invoice(emp_id), show_invoice_preview()])
        print_invoice_btn.grid(row=4, column=2, padx=10, pady=10, sticky="new")

    def update_invoice():
        try:
            selected_item = table.selection()[0]
            values = table.item(selected_item, "values")
            invoice_id = values[0]

            cursor.execute("""
                        SELECT ServiceTbl.SName, InvoiceDetailTbl.ServiceID, InvoiceDetailTbl.SQuantity, InvoiceDetailTbl.SPrice, InvoiceDetailTbl.TotalAmt
                        FROM InvoiceDetailTbl
                        JOIN ServiceTbl ON InvoiceDetailTbl.ServiceID = ServiceTbl.ServiceID
                        WHERE InvoiceID = %s
                    """, (invoice_id,))
            invoice_details = cursor.fetchall()

            update_window = tb.Toplevel(title="Cập nhật hóa đơn", minsize=(300, 400))

            lf = tb.Labelframe(update_window, text="Cập nhật hóa đơn")
            lf.pack(fill="both", padx=5, pady=5, expand=True)
            lf.columnconfigure((0, 1, 2, 3), weight=1)
            lf.rowconfigure(tuple(range(20)), weight=1)

            entries = []
            total_var = tk.StringVar(value=str(sum(item[4] for item in invoice_details)))

            tk.Label(lf, text="Dịch vụ").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            tk.Label(lf, text="Số lượng").grid(row=0, column=1, padx=10, pady=5, sticky="w")
            tk.Label(lf, text="Giá cả").grid(row=0, column=2, padx=10, pady=5, sticky="w")
            tk.Label(lf, text="Tổng cộng").grid(row=0, column=3, padx=10, pady=5, sticky="w")

            for index, (service_name, service_id, s_quantity, s_price, total_amt) in enumerate(invoice_details,
                                                                                               start=1):
                service_entry = tk.Entry(lf)
                service_entry.insert(0, service_name)
                service_entry.grid(row=index, column=0, padx=10, pady=5, sticky="w")
                service_entry.config(state='readonly')

                qty_entry = tk.Entry(lf)
                qty_entry.insert(0, str(s_quantity))
                qty_entry.grid(row=index, column=1, padx=10, pady=5, sticky="w")

                price_entry = tk.Entry(lf)
                price_entry.insert(0, str(s_price))
                price_entry.grid(row=index, column=2, padx=10, pady=5, sticky="w")
                price_entry.config(state='readonly')

                total_entry = tk.Entry(lf)
                total_entry.insert(0, str(total_amt))
                total_entry.grid(row=index, column=3, padx=10, pady=5, sticky="w")
                total_entry.config(state='readonly')

                entries.append((service_id, qty_entry, s_price, total_entry))

            tk.Label(lf, text="Tổng hóa đơn").grid(row=len(invoice_details) + 1, column=0, padx=10, pady=5,
                                                   sticky="w")
            total_invoice_label = tk.Label(lf, textvariable=total_var)
            total_invoice_label.grid(row=len(invoice_details) + 1, column=1, padx=10, pady=5, sticky="w")

            def recalculate_total():
                total = 0
                for service_id, qty_entry, s_price, total_entry in entries:
                    try:
                        qty = int(qty_entry.get())
                        total_amt = qty * s_price
                        total += total_amt
                        total_entry.config(state='normal')
                        total_entry.delete(0, tk.END)
                        total_entry.insert(0, str(total_amt))
                        total_entry.config(state='readonly')
                    except ValueError:
                        messagebox.showerror("Lỗi", f"Số lượng cho dịch vụ {service_id} không hợp lệ")
                        return
                total_var.set(str(total))

            def save_updates():
                try:
                    for service_id, qty_entry, s_price, _ in entries:
                        s_quantity = int(qty_entry.get())
                        total_amt = s_quantity * s_price

                        # Update invoice details
                        cursor.execute("""
                                    UPDATE InvoiceDetailTbl
                                    SET SQuantity = %s, TotalAmt = %s
                                    WHERE InvoiceID = %s AND ServiceID = %s
                                """, (s_quantity, total_amt, invoice_id, service_id))

                    # Commit changes
                    db.commit()
                    fetch_and_insert_data()
                    messagebox.showinfo("Thành công", "Cập nhật hóa đơn thành công")
                    update_window.destroy()

                except Exception as e:
                    db.rollback()
                    messagebox.showerror("Lỗi", str(e))

            for _, qty_entry, _, _ in entries:
                qty_entry.bind("<KeyRelease>", lambda event: recalculate_total())

            save_btn = tk.Button(lf, text="Lưu cập nhật", command=save_updates)
            save_btn.grid(row=len(invoice_details) + 2, column=1, padx=10, pady=5, sticky="w")

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_invoice():
        try:
            selected_item = table.selection()[0]
            values = table.item(selected_item, "values")
            invoice_id = values[0]

            cursor.execute("DELETE FROM InvoiceDetailTbl WHERE InvoiceID = %s", (invoice_id,))
            db.commit()

            cursor.execute("DELETE FROM InvoiceTbl WHERE InvoiceID = %s", (invoice_id,))
            db.commit()

            table.delete(selected_item)
            messagebox.showinfo("Success", "Invoice deleted successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            db.rollback()

    add_btn = tb.Button(funcbar, text="Thêm Hóa Đơn", command=add_invoice, bootstyle="success")
    add_btn.grid(row=0, column=0, padx=5, pady=5)

    update_btn = tb.Button(funcbar, text="Sửa Hóa Đơn", command=update_invoice, bootstyle="info")
    update_btn.grid(row=0, column=1, padx=5, pady=5)

    delete_btn = tb.Button(funcbar, text="Xóa Hóa Đơn", command=delete_invoice, bootstyle="danger")
    delete_btn.grid(row=0, column=2, padx=5, pady=5)

    refresh_btn = tb.Button(funcbar, text="Làm Mới", command=fetch_and_insert_data, bootstyle="secondary")
    refresh_btn.grid(row=0, column=3, padx=5, pady=5)