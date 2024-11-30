from tkinter import messagebox

import mysql
import ttkbootstrap as tb
from DB import cursor, db
from utils import clicked


def fetch_customer_data(table, search_query=None, search_column=None):
    """
    Truy xuất dữ liệu khách hàng từ database và hiển thị trong bảng.

    Args:
        table: Bảng Treeview để hiển thị dữ liệu.
        search_query (str): Từ khóa tìm kiếm.
        search_column (str): Thuộc tính tìm kiếm.
    """
    query = "SELECT CustID, CustName, CustNumber, CustAddress, CustRegisDate, CustNotes FROM customertbl"
    params = ()

    if search_query and search_column:
        column_map = {
            "ID": "CustID",
            "Họ tên": "CustName",
            "Liên hệ": "CustNumber",
            "Địa chỉ": "CustAddress",
            "Ngày đăng ký": "CustRegisDate",
            "Ghi chú": "CustNotes"
        }
        column = column_map.get(search_column)
        if column:
            query += f" WHERE {column} LIKE %s"
            params = (f"%{search_query}%",)

    try:
        cursor.execute(query, params)
        data = cursor.fetchall()

        # Xóa dữ liệu cũ trong bảng
        for item in table.get_children():
            table.delete(item)

        # Thêm dữ liệu mới vào bảng
        table.tag_configure('evenrow', background='#f2f2f2')
        table.tag_configure('oddrow', background='#ffffff')
        for i, item in enumerate(data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            table.insert('', tb.END, values=(f"KH{item[0]}", item[1], item[2], item[3], item[4], item[5]), tags=(tag,))



    except mysql.connector.Error as e:  # Sử dụng ngoại lệ đúng
        messagebox.showerror("Lỗi", f"Không thể lấy dữ liệu khách hàng: {e}")
    finally:
        cursor.fetchall()  # Đảm bảo không còn kết quả chưa đọc


def add_customer(fetch_function):
    """
    Hiển thị giao diện thêm khách hàng.
    """
    add_window = tb.Toplevel(title="Thêm khách hàng", minsize=(380, 520))
    lf = tb.Labelframe(add_window, bootstyle="secondary", text="")
    lf.pack(fill="both", padx=5, pady=5, expand=True)

    lf.columnconfigure((0, 1), weight=1)
    lf.columnconfigure(2, weight=30)
    lf.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

    # ID
    tb.Label(lf, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    id_entry = tb.Entry(lf)
    id_entry.grid(row=0, column=2, padx=10, pady=5, sticky="e")
    cursor.execute("SELECT MAX(CustID) FROM customertbl")
    result = cursor.fetchone()
    new_id = result[0] + 1 if result and result[0] is not None else 1
    id_entry.insert(0, new_id)
    id_entry.configure(state="readonly")

    # Các trường khác
    fields = [("Họ tên", "name"), ("Số điện thoại", "number"), ("Địa chỉ", "address"), ("Ngày đăng ký", "date"), ("Ghi chú", "note")]
    entries = {}

    for i, (label, key) in enumerate(fields, start=1):
        tb.Label(lf, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        if key == "date":
            entry = tb.DateEntry(lf, width=16)
        else:
            entry = tb.Entry(lf, width=16)
        entry.grid(row=i, column=2, padx=10, pady=5, sticky="e")
        entries[key] = entry

    # Nút thêm
    def save_new_customer():
        id = id_entry.get()
        values = {
            field: (entry.entry.get() if isinstance(entry, tb.DateEntry) else entry.get())
            for field, entry in entries.items()
        }

        if any(not value for value in values.values()):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin khách hàng.")
            return

        try:
            cursor.execute(
                "INSERT INTO customertbl (CustID, CustName, CustNumber, CustAddress, CustRegisDate, CustNotes) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (id, values['name'], values['number'], values['address'], values['date'], values['note'])
            )
            db.commit()
            fetch_function()
            messagebox.showinfo("Thành công", "Khách hàng đã được thêm thành công!")
            add_window.destroy()

        except db.Error as e:
            messagebox.showerror("Lỗi", f"Không thể thêm khách hàng: {e}")

    tb.Button(add_window, text="Thêm", bootstyle="success", command=save_new_customer).pack(fill="x", padx=10, pady=10)

def delete_customer(table, fetch_function):
    """
    Xóa khách hàng đã chọn.
    """
    selected_item = table.focus()
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn khách hàng để xóa.")
        return

    customer_id = table.item(selected_item, 'values')[0].strip('KH')
    confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa khách hàng ID: KH{customer_id}?")
    if confirm:
        try:
            cursor.execute("DELETE FROM customertbl WHERE CustID = %s", (customer_id,))
            db.commit()
            fetch_function()
            messagebox.showinfo("Thành công", f"Khách hàng KH{customer_id} đã được xóa.")
        except db.Error as e:
            messagebox.showerror("Lỗi", f"Không thể xóa khách hàng: {e}")


def edit_customer(table, fetch_function):
    """
    Hiển thị giao diện sửa khách hàng đã chọn.
    """
    selected_item = table.focus()
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn khách hàng để sửa.")
        return

    customer_data = table.item(selected_item, 'values')
    customer_id = customer_data[0].strip('KH')

    edit_window = tb.Toplevel(title="Sửa khách hàng", minsize=(380, 520))
    lf = tb.Labelframe(edit_window, bootstyle="secondary", text="Sửa thông tin khách hàng")
    lf.pack(fill="both", padx=5, pady=5, expand=True)

    lf.columnconfigure((0, 1), weight=1)
    lf.columnconfigure(2, weight=30)
    lf.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

    # Các trường nhập
    fields = ["Họ tên", "Số điện thoại", "Địa chỉ", "Ngày đăng ký", "Ghi chú"]
    entries = {}

    for i, field in enumerate(fields):
        tb.Label(lf, text=field).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        if field == "Ngày đăng ký":
            entry = tb.DateEntry(lf, width=16)
            entry.entry.delete(0, "end")  # Xóa nội dung cũ
            entry.entry.insert(0, customer_data[i + 1])  # Đặt ngày từ dữ liệu
        else:
            entry = tb.Entry(lf, width=16)
            entry.insert(0, customer_data[i + 1])
        entry.grid(row=i, column=2, padx=10, pady=5, sticky="e")
        entries[field] = entry

    # Lưu thay đổi
    def save_changes():
        values = {
            field: (entry.entry.get() if isinstance(entry, tb.DateEntry) else entry.get())
            for field, entry in entries.items()
        }

        if any(not value for value in values.values()):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            cursor.execute(
                "UPDATE customertbl SET CustName=%s, CustNumber=%s, CustAddress=%s, CustRegisDate=%s, CustNotes=%s WHERE CustID=%s",
                (values["Họ tên"], values["Số điện thoại"], values["Địa chỉ"], values["Ngày đăng ký"], values["Ghi chú"], customer_id)
            )
            db.commit()
            fetch_function()
            messagebox.showinfo("Thành công", "Thông tin khách hàng đã được cập nhật.")
            edit_window.destroy()
        except db.Error as e:
            messagebox.showerror("Lỗi", f"Không thể sửa khách hàng: {e}")

    tb.Button(edit_window, text="Lưu", bootstyle="success", command=save_changes).pack(fill="x", padx=10, pady=10)


def search_customer(table, fetch_function, search_entry, search_column):
    """
    Tìm kiếm khách hàng theo cột được chọn.

    Args:
        table: Bảng Treeview hiển thị dữ liệu.
        fetch_function: Hàm để tải lại dữ liệu.
        search_entry: Entry chứa từ khóa tìm kiếm.
        search_column: Cột được chọn từ dropdown để tìm kiếm.
    """
    query = search_entry.get().strip()
    column = search_column.get()

    if not query:
        messagebox.showerror("Lỗi", "Vui lòng nhập từ khóa tìm kiếm.")
        return

    if not column:
        messagebox.showerror("Lỗi", "Vui lòng chọn thuộc tính để tìm kiếm.")
        return

    # Gọi hàm fetch_function với từ khóa tìm kiếm và cột
    fetch_function(table, search_query=query, search_column=column)

def show_khachHang(window, user_role, buttons, khachHang_btn):
    """
    Hiển thị giao diện quản lý khách hàng.

    Args:
        window: Cửa sổ chính.
        user_role: Vai trò người dùng.
        buttons: Danh sách các nút.
        khachHang_btn: Nút hiện tại đang được kích hoạt.
    """
    if user_role not in ['admin', 'cashier']:
        messagebox.showerror("Access Denied", "Bạn không có quyền truy cập vào tính năng này.")
        return

    clicked(khachHang_btn, buttons)
    style = tb.Style()
    style.configure("Custom.Treeview",
                    borderwidth=1,
                    relief="solid",  # Tạo viền quanh bảng
                    rowheight=25,  # Điều chỉnh chiều cao hàng
                    background="#fdfdfd",  # Màu nền
                    foreground="#000")  # Màu chữ
    style.configure("Custom.Treeview.Heading",
                    background="#e1e1e1",  # Màu nền tiêu đề
                    foreground="#000",  # Màu chữ tiêu đề
                    borderwidth=1,
                    relief="solid")  # Tạo viền cho tiêu đề
    # Tạo frame chính
    khachHang_frame = tb.Labelframe(window, bootstyle="secondary", text="Quản lý khách hàng")
    khachHang_frame.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")
    khachHang_frame.columnconfigure(0, weight=1)
    khachHang_frame.rowconfigure(0, weight=1)

    # Tạo bảng hiển thị dữ liệu khách hàng
    content_frame = tb.Frame(khachHang_frame)
    content_frame.grid(row=0, column=0, columnspan=2, rowspan=7, sticky="news")
    content_frame.columnconfigure((0, 1), weight=50)
    content_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

    # Bảng và cuộn
    columns = ("cID", "cName", "cNumber", "cAddress", "cRegDate", "cNote")
    table = tb.Treeview(content_frame, columns=columns, show='headings')
    for col in columns:
        table.heading(col, text=col)
    table.grid(row=0, column=0, padx=10, pady=10, rowspan=6, columnspan=2, sticky="news")
    tree_scroll = tb.Scrollbar(content_frame, orient="vertical", bootstyle="primary-round")
    tree_scroll.grid(row=0, rowspan=6, column=3, sticky="wnes", padx=5, pady=30)

    columns = ("cID", "cName", "cNumber", "cAddress", "cRegDate", "cNote")
    table = tb.Treeview(content_frame, columns=columns, show='headings', yscrollcommand=tree_scroll.set,
                        style="Custom.Treeview")
    tree_scroll.config(command=table.yview)

    table.heading("cID", text="ID")
    table.heading("cName", text="Họ tên")
    table.heading("cNumber", text="Liên hệ")
    table.heading("cAddress", text="Địa chỉ")
    table.heading("cRegDate", text="Ngày đăng ký")
    table.heading("cNote", text="Ghi chú")

    table.column("cID", width=30, anchor="center")
    table.column("cName", width=150, anchor="center")
    table.column("cNumber", width=80, anchor="center")
    table.column("cAddress", width=70, anchor="center")
    table.column("cRegDate", width=50, anchor="center")
    table.column("cNote", width=50, anchor="center")

    table.grid(row=0, column=0, padx=10, pady=10, rowspan=6, columnspan=2, sticky="news")

    funcbar = tb.Frame(content_frame, height=60)
    funcbar.grid(row=6, column=0, columnspan=3, sticky="news")
    funcbar.columnconfigure((0, 1, 2, 3, 5), weight=1)
    funcbar.columnconfigure(4, weight=30)
    # Tải dữ liệu
    fetch_customer_data(table)

    # Thanh chức năng
    funcbar = tb.Frame(khachHang_frame)
    funcbar.grid(row=6, column=0, sticky="nsew")

    tb.Button(funcbar, text="Thêm", bootstyle="success-outline",
              command=lambda: add_customer(lambda: fetch_customer_data(table))).grid(row=0, column=0, padx=10, pady=10)
    tb.Button(funcbar, text="Sửa", bootstyle="success-outline",
              command=lambda: edit_customer(table, lambda: fetch_customer_data(table))).grid(row=0, column=1, padx=10, pady=10)
    tb.Button(funcbar, text="Xóa", bootstyle="danger-outline",
              command=lambda: delete_customer(table, lambda: fetch_customer_data(table))).grid(row=0, column=2, padx=10, pady=10)

    # Dropdown và tìm kiếm
    columns = ["ID", "Họ tên", "Liên hệ", "Địa chỉ", "Ngày đăng ký", "Ghi chú"]
    search_column = tb.StringVar()
    search_dropdown = tb.Combobox(funcbar, textvariable=search_column, values=columns, width=14)
    search_dropdown.grid(row=0, column=3, padx=10, pady=10)
    search_dropdown.set("ID")  # Thuộc tính mặc định

    search_entry = tb.Entry(funcbar, width=20)
    search_entry.grid(row=0, column=4, padx=10, pady=10, sticky="e")

    tb.Button(
        funcbar, text="Tìm kiếm", bootstyle="primary-outline",
        command=lambda: search_customer(table, fetch_customer_data, search_entry, search_dropdown)
    ).grid(row=0, column=5, padx=10, pady=10)


