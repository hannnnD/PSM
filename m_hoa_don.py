import subprocess
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb

from DB import cursor, db
from utils import clicked
from datetime import datetime, timedelta, date
import os

import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def show_hoaDon(window, user_role, buttons, hoaDon_btn, emp_id):
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
    style = tb.Style()
    style.configure("Custom.Treeview",
                    borderwidth=1,
                    relief="solid",  # Tạo viền quanh bảng
                    rowheight=25,  # Điều chỉnh chiều cao hàng
                    background="#fdfdfd",  # Màu nền
                    foreground="#000")  # Màu chữ
    style.configure("Custom.Treeview.Heading",
                    background="#76EEC6",  # Màu nền tiêu đề
                    foreground="#000",  # Màu chữ tiêu đề
                    borderwidth=1,
                    relief="solid")  # Tạo viền cho tiêu đề
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
    # Áp dụng kiểu tùy chỉnh cho Treeview
    table = tb.Treeview(content_frame, columns=columns, show='headings', yscrollcommand=tree_scroll.set,
                        style="Custom.Treeview")


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
                   SUM(COALESCE(InvoiceDetailTbl.TotalAmt, 0)) as TotalAmt
            FROM InvoiceTbl
            LEFT JOIN CustomerTbl ON InvoiceTbl.CustID = CustomerTbl.CustID
            LEFT JOIN EmployeeTbl ON InvoiceTbl.EmpID = EmployeeTbl.EmpID
            LEFT JOIN InvoiceDetailTbl ON InvoiceTbl.InvoiceID = InvoiceDetailTbl.InvoiceID
            GROUP BY InvoiceTbl.InvoiceID, InvoiceTbl.InvoiceDate, CustomerTbl.CustName, 
                     EmployeeTbl.EmpName
            """

        cursor.execute(query)
        for item in table.get_children():
            table.delete(item)
        data = cursor.fetchall()

        def format_vnd(amount):
            return f"{amount:,.0f}".replace(',', '.') + " VND"

        table.tag_configure('evenrow', background='#f2f2f2')
        table.tag_configure('oddrow', background='#ffffff')
        for i, item in enumerate(data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            formatted_total = format_vnd(item[4])
            table.insert('', tb.END, values=(item[0], item[1], item[2], item[3], formatted_total), tags=(tag,))

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

        total_prices = []  # Khởi tạo một danh sách để lưu total_price cho mỗi dịch vụ

        def add_to_bill():
            try:
                service_id = service_id_entry.get()
                service_name = service_name_entry.get()
                service_price = float(service_price_entry.get())
                service_qty = int(service_qty_entry.get())

                if not service_qty or service_qty <= 0:
                    raise ValueError("Invalid quantity")

                # Tính toán tổng tiền
                total_price = service_price * service_qty

                # Thêm vào hóa đơn
                bill_tree.insert("", "end", values=(service_id, service_name, service_qty, total_price))

                # Lưu total_price vào danh sách
                total_prices.append(total_price)

                # Cập nhật tổng hóa đơn
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
                # Lấy các thông tin từ giao diện
                invoice_id_val = invoice_id.get()
                invoice_date_val = invoice_date.entry.get()
                cust_id_val = cust_id_entry.get()

                # Lưu thông tin vào bảng hóa đơn chính (InvoiceTbl)
                cursor.execute(
                    "INSERT INTO InvoiceTbl (InvoiceID, InvoiceDate, CustID, EmpID) VALUES (%s, %s, %s, %s)",
                    (invoice_id_val, invoice_date_val, cust_id_val, emp_id)
                )

                # Lặp qua từng dịch vụ trong hóa đơn từ giao diện
                for idx, item in enumerate(bill_tree.get_children()):
                    values = bill_tree.item(item, "values")
                    service_id_val = values[0]  # Lấy ServiceID
                    service_name_val = values[1]  # Lấy tên dịch vụ
                    service_qty_val = int(values[2])  # Lấy số lượng (SQuantity)
                    total_service_amount = float(values[3])  # Lấy tổng tiền (TotalAmt)

                    # Lấy giá dịch vụ (SPrice) từ cơ sở dữ liệu để đảm bảo tính chính xác
                    cursor.execute("SELECT SPrice FROM ServiceTbl WHERE ServiceID = %s", (service_id_val,))
                    service_price_val = cursor.fetchone()[0]

                    # Kiểm tra tồn kho trước khi cập nhật
                    cursor.execute("SELECT SQuantity FROM ServiceTbl WHERE ServiceID = %s", (service_id_val,))
                    available_qty = cursor.fetchone()[0]
                    if available_qty < service_qty_val:
                        raise ValueError(f"Không đủ số lượng dịch vụ {service_name_val}. Số còn lại: {available_qty}")

                    # Lưu chi tiết hóa đơn vào bảng InvoiceDetailTbl
                    cursor.execute(
                        """
                        INSERT INTO InvoiceDetailTbl (InvoiceID, ServiceID, SQuantity, SPrice, TotalAmt, idDate) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (invoice_id_val, service_id_val, service_qty_val, service_price_val, total_service_amount,
                         invoice_date_val)
                    )

                    # Cập nhật số lượng tồn kho trong bảng ServiceTbl
                    cursor.execute(
                        "UPDATE ServiceTbl SET SQuantity = SQuantity - %s WHERE ServiceID = %s",
                        (service_qty_val, service_id_val)
                    )

                # Xác nhận lưu tất cả thay đổi vào cơ sở dữ liệu
                db.commit()

                # Thông báo khi lưu thành công
                messagebox.showinfo("Success", "Invoice saved successfully")

            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
                db.rollback()
            except Exception as e:
                # Xử lý lỗi và rollback khi gặp lỗi
                messagebox.showerror("Error", str(e))
                db.rollback()

        pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))

        def print_invoice():
            try:
                # Định dạng số tiền
                def format_currency(amount):
                    return f"{amount:,.0f}".replace(',', '.') + " VND"

                # Tạo file PDF tạm thời
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                pdf_file_path = temp_file.name
                temp_file.close()

                # Tạo PDF
                c = canvas.Canvas(pdf_file_path, pagesize=letter)
                c.setFont("DejaVuSans", 16)
                c.drawCentredString(300, 750, "HÓA ĐƠN DỊCH VỤ")  # Tiêu đề trung tâm

                # Thông tin hóa đơn
                c.setFont("DejaVuSans", 12)
                c.drawString(50, 700, f"Nhân viên: {emp_id}")
                c.drawString(50, 680, f"Mã hóa đơn: {invoice_id.get()}")
                c.drawString(400, 680, f"Ngày: {invoice_date.entry.get()}")

                # Header bảng dịch vụ
                y = 640
                table_data = [["STT", "Tên dịch vụ", "SL", "Đơn giá", "Thành tiền"]]
                total_amount = 0

                # Thêm dữ liệu từ TreeView
                for index, item in enumerate(bill_tree.get_children(), start=1):
                    values = bill_tree.item(item, "values")
                    service_name = values[1]
                    quantity = int(values[2])
                    price = float(values[3])
                    total = price
                    total_amount += total

                    table_data.append([
                        str(index),
                        service_name,
                        str(quantity),
                        format_currency(price),
                        format_currency(total),
                    ])

                # Tổng hóa đơn
                formatted_total_amount = format_currency(total_amount)
                table_data.append(["", "", "", "Tổng cộng:", formatted_total_amount])

                # Tạo bảng
                table = Table(table_data, colWidths=[50, 200, 50, 100, 100])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Nền header
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Kẻ ô
                ]))
                table.wrapOn(c, 50, y)
                table.drawOn(c, 50, y - len(table_data) * 20)

                # Lời cảm ơn
                c.setFont("DejaVuSans", 12)
                c.drawCentredString(300, y - len(table_data) * 20 - 40,
                                    "Cảm ơn quý khách đã sử dụng dịch vụ của chúng tôi!")

                c.save()

                try:
                    os.startfile(pdf_file_path, "print")  # Mở với ứng dụng mặc định để in
                except OSError:
                    # Nếu không có ứng dụng mặc định, dùng subprocess
                    try:
                        subprocess.run(["AcroRd32.exe", "/p", "/h", pdf_file_path], check=True)
                    except FileNotFoundError:
                        messagebox.showerror("Error",
                                             "Không tìm thấy ứng dụng để in PDF. Vui lòng cài đặt Adobe Acrobat Reader.")
                    except Exception as subprocess_error:
                        messagebox.showerror("Error", f"Lỗi khi in hóa đơn qua subprocess: {subprocess_error}")

            except Exception as e:
                messagebox.showerror("Error", f"Lỗi khi in hóa đơn: {e}")

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
        customer_tree = tb.Treeview(customer_list_frame,
                                    columns=customer_columns,
                                    show="headings",
                                    style="Custom.Treeview")

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

        add_to_bill_btn = tb.Button(service_frame, text="Thêm vào hóa đơn", bootstyle="success-outline",
                                    command=add_to_bill)
        add_to_bill_btn.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        remove_from_bill_btn = tb.Button(service_frame, text="Xóa khỏi hóa đơn", bootstyle="danger-outline",
                                         command=remove_from_bill)
        remove_from_bill_btn.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Service List
        service_list_frame = tb.Labelframe(lf, bootstyle="secondary", text="Danh sách dịch vụ")
        service_list_frame.grid(row=1, column=1, padx=10, pady=10, sticky="news")

        service_columns = ("service_id", "service_name", "category", "quantity", "price")
        service_tree = tb.Treeview(service_list_frame,
                                   columns=service_columns,
                                   show="headings",
                                   style="Custom.Treeview")


        for col in service_columns:
            service_tree.heading(col, text=col.replace("_", " ").title())
            service_tree.column(col, width=85)
        service_tree.grid(row=0, column=0, sticky="nsew")

        service_tree.heading("service_id", text="Id")
        service_tree.heading("service_name", text="Dịch vụ")
        service_tree.heading("category", text="Danh mục")
        service_tree.heading("quantity", text="Số lượng")
        service_tree.heading("price", text="Giá")
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

        tb.Label(bill_info_frame, text="Ngày xuất hóa đơn").grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # DateEntry của ttkbootstrap
        invoice_date = tb.DateEntry(bill_info_frame)
        invoice_date.grid(row=1, column=1, padx=10, pady=5)

        # Thay đổi giá trị ban đầu thành định dạng d/m/y
        current_date = datetime.strptime(invoice_date.entry.get(), "%m/%d/%Y").strftime("%d/%m/%Y")
        invoice_date.entry.delete(0, "end")
        invoice_date.entry.insert(0, current_date)
        invoice_date.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Bill Frame
        bill_frame = tb.Labelframe(lf, bootstyle="secondary", text="Hóa đơn")
        bill_frame.grid(row=1, column=2, padx=10, pady=10, sticky="news")

        bill_columns = ("service_id_to_bill", "service_name_to_bill", "quantity_to_bill", "price_to_bill")
        bill_tree = tb.Treeview(bill_frame,
                                columns=bill_columns,
                                show="headings",
                                style="Custom.Treeview")

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

        # Tiêu đề "Tổng hóa đơn" được nâng cấp với font và màu sắc
        tk.Label(
            total_frame,
            text="Tổng hóa đơn:",
            font=("Arial", 10, "bold"),
            fg="#333",  # Màu chữ xám đậm
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Giá trị tổng hóa đơn được làm nổi bật với màu chữ xanh lá
        total_var = tk.StringVar(value="0")
        total_label = tk.Label(
            total_frame,
            textvariable=total_var,
            font=("Arial", 10, "bold"),
            fg="green",  # Màu chữ xanh lá để làm nổi bật giá trị
        )
        total_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Print Invoice Button
        print_invoice_btn = tb.Button(lf, text="In hóa đơn", bootstyle="success-outline",
                                      command=lambda: [save_invoice(emp_id), print_invoice()])
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

    def search_invoice():
        keyword = search_entry.get().strip()  # Lấy từ khóa tìm kiếm từ entry

        # Xóa dữ liệu cũ trong bảng
        for item in table.get_children():
            table.delete(item)

        if not keyword:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa để tìm kiếm.")
            return

        try:
            # Sử dụng truy vấn của bạn và áp dụng tìm kiếm dựa trên từ khóa
            cursor.execute(f"""
                SELECT InvoiceTbl.InvoiceID, InvoiceTbl.InvoiceDate, CustomerTbl.CustName, 
                       EmployeeTbl.EmpName, 
                       SUM(COALESCE(InvoiceDetailTbl.TotalAmt, 0)) as TotalAmt
                FROM InvoiceTbl
                LEFT JOIN CustomerTbl ON InvoiceTbl.CustID = CustomerTbl.CustID
                LEFT JOIN EmployeeTbl ON InvoiceTbl.EmpID = EmployeeTbl.EmpID
                LEFT JOIN InvoiceDetailTbl ON InvoiceTbl.InvoiceID = InvoiceDetailTbl.InvoiceID
                WHERE InvoiceTbl.InvoiceID LIKE %s
                   OR CustomerTbl.CustName LIKE %s
                   OR EmployeeTbl.EmpName LIKE %s
                   OR InvoiceTbl.InvoiceDate LIKE %s
                GROUP BY InvoiceTbl.InvoiceID, InvoiceTbl.InvoiceDate, CustomerTbl.CustName, 
                         EmployeeTbl.EmpName
            """, (
                f"%{keyword}%",  # Tìm kiếm theo InvoiceID
                f"%{keyword}%",  # Tìm kiếm theo CustName
                f"%{keyword}%",  # Tìm kiếm theo EmpName
                f"%{keyword}%"  # Tìm kiếm theo InvoiceDate
            ))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi tìm kiếm: {e}")
            return

        data = cursor.fetchall()

        if not data:
            messagebox.showinfo("Thông báo", f"Không tìm thấy kết quả nào cho từ khóa '{keyword}'.")
            return

        # Hiển thị dữ liệu trong bảng
        for item in data:
            table.insert('', 'end', values=item)

        # Xóa ô tìm kiếm sau khi hiển thị kết quả
        search_entry.delete(0, 'end')

    add_btn = tb.Button(funcbar, text="Thêm Hóa Đơn", command=add_invoice, bootstyle="success-outline")
    add_btn.grid(row=0, column=0, padx=5, pady=5)

    update_btn = tb.Button(funcbar, text="Sửa Hóa Đơn", command=update_invoice, bootstyle="success-outline")
    update_btn.grid(row=0, column=1, padx=5, pady=5)

    delete_btn = tb.Button(funcbar, text="Xóa Hóa Đơn", command=delete_invoice, bootstyle="danger-outline")
    delete_btn.grid(row=0, column=2, padx=5, pady=5)

    refresh_btn = tb.Button(funcbar, text="Làm Mới", command=fetch_and_insert_data, bootstyle="secondary-outline")
    refresh_btn.grid(row=0, column=3, padx=5, pady=5)

    search_entry = tb.Entry(funcbar, bootstyle="secondary", width=20)
    search_entry.grid(row=0, column=6, padx=5, pady=10, sticky="we")

    search_btn = tb.Button(funcbar, bootstyle="success-outline", text="Tìm kiếm", width=14, command=search_invoice)
    search_btn.grid(row=0, column=7, padx=5, pady=10, sticky="e")

