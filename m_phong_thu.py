from tkinter import messagebox

import mysql
import ttkbootstrap as tb
from DB import cursor, db
from utils import clicked

def fetch_room_data(table, search_query=None, search_column=None):
    """
    Truy xuất dữ liệu phòng thú cưng từ database và hiển thị trong bảng.

    Args:
        table: Bảng Treeview để hiển thị dữ liệu.
        search_query (str): Từ khóa tìm kiếm.
        search_column (str): Thuộc tính tìm kiếm.
    """
    query = "SELECT PetRoomID, RName, RStatus, RType, RPrice FROM PetRoomTbl"
    params = ()

    if search_query and search_column:
        column_map = {
            "ID": "PetRoomID",
            "Tên phòng": "RName",
            "Trạng thái": "RStatus",
            "Loại phòng": "RType",
            "Giá": "RPrice"
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
        def format_vnd(amount):
            return f"{amount:,.0f}".replace(',', '.') + " VND"

        table.tag_configure('evenrow', background='#f2f2f2')
        table.tag_configure('oddrow', background='#ffffff')
        for i, item in enumerate(data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            formatted_total = format_vnd(item[4])
            table.insert('', tb.END, values=(item[0], item[1], item[2], item[3], formatted_total), tags=(tag,))


    except mysql.connector.Error as e:
        messagebox.showerror("Lỗi", f"Không thể lấy dữ liệu phòng: {e}")
    finally:
        try:
            cursor.fetchall()  # Xử lý kết quả chưa đọc (nếu có)
        except mysql.connector.Error:
            pass



def add_room(fetch_function):
    """
    Hiển thị giao diện thêm phòng thú cưng.
    """
    add_window = tb.Toplevel(title="Thêm phòng thú cưng", minsize=(380, 520))
    lf = tb.Labelframe(add_window, bootstyle="secondary", text="Thêm phòng")
    lf.pack(fill="both", padx=5, pady=5, expand=True)

    lf.columnconfigure((0, 1), weight=1)
    lf.columnconfigure(2, weight=30)
    lf.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

    # ID
    tb.Label(lf, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    id_entry = tb.Entry(lf)
    id_entry.grid(row=0, column=2, padx=10, pady=5, sticky="e")
    cursor.execute("SELECT MAX(PetRoomID) FROM PetRoomTbl")
    result = cursor.fetchone()
    new_id = result[0] + 1 if result and result[0] else 1
    id_entry.insert(0, new_id)
    id_entry.configure(state="readonly")

    # Các trường khác
    fields = [
        ("Tên phòng", "name"),
        ("Trạng thái", "status"),
        ("Loại phòng", "type"),
        ("Giá", "price")
    ]
    entries = {}

    for i, (label, key) in enumerate(fields, start=1):
        tb.Label(lf, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        if key == "status":
            entry = tb.Combobox(lf, values=["Trống", "Đủ"], width=16)
        else:
            entry = tb.Entry(lf, width=16)
        entry.grid(row=i, column=2, padx=10, pady=5, sticky="e")
        entries[key] = entry

    def save_new_room():
        """
        Lưu phòng mới vào database.
        """
        values = {key: entry.get() for key, entry in entries.items()}
        if any(not value for value in values.values()):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            cursor.execute(
                "INSERT INTO PetRoomTbl (PetRoomID, RName, RStatus, RType, RPrice) VALUES (%s, %s, %s, %s, %s)",
                (new_id, values["name"], values["status"], values["type"], values["price"])
            )
            db.commit()
            fetch_function()
            messagebox.showinfo("Thành công", "Phòng đã được thêm.")
            add_window.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Không thể thêm phòng: {e}")

    tb.Button(add_window, text="Thêm", bootstyle="success", command=save_new_room).pack(fill="x", padx=10, pady=10)



def edit_room(table, fetch_function):
    """
    Hiển thị giao diện sửa thông tin phòng thú cưng.
    """
    selected_item = table.focus()
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn phòng để sửa.")
        return

    room_data = table.item(selected_item, "values")
    room_id = room_data[0]

    edit_window = tb.Toplevel(title="Sửa phòng thú cưng", minsize=(380, 520))
    lf = tb.Labelframe(edit_window, bootstyle="secondary", text="Sửa phòng")
    lf.pack(fill="both", padx=5, pady=5, expand=True)

    fields = ["Tên phòng", "Trạng thái", "Loại phòng", "Giá"]
    entries = {}

    for i, field in enumerate(fields, start=1):
        tb.Label(lf, text=field).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tb.Entry(lf, width=16) if field != "Trạng thái" else tb.Combobox(lf, values=["Trống", "Đủ"])
        entry.grid(row=i, column=2, padx=10, pady=5, sticky="e")
        entry.insert(0, room_data[i])
        entries[field] = entry

    def save_changes():
        """
        Lưu thông tin thay đổi của phòng vào database.
        """
        values = {field: entry.get() for field, entry in entries.items()}
        if any(not value for value in values.values()):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            cursor.execute(
                "UPDATE PetRoomTbl SET RName=%s, RStatus=%s, RType=%s, RPrice=%s WHERE PetRoomID=%s",
                (values["Tên phòng"], values["Trạng thái"], values["Loại phòng"], values["Giá"], room_id)
            )
            db.commit()
            fetch_function()
            messagebox.showinfo("Thành công", "Phòng đã được cập nhật.")
            edit_window.destroy()
        except mysql.connector.Error as e:  # Sử dụng đúng ngoại lệ
            messagebox.showerror("Lỗi", f"Không thể sửa phòng: {e}")
        finally:
            try:
                cursor.fetchall()  # Xử lý kết quả chưa đọc (nếu có)
            except mysql.connector.Error:
                pass

    tb.Button(edit_window, text="Lưu", bootstyle="success", command=save_changes).pack(fill="x", padx=10, pady=10)


def delete_room(table, fetch_function):
    """
    Xóa phòng thú cưng được chọn.
    """
    selected_item = table.focus()
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn phòng để xóa.")
        return

    room_id = table.item(selected_item, "values")[0]

    confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa phòng ID {room_id}?")
    if confirm:
        try:
            cursor.execute("DELETE FROM PetRoomTbl WHERE PetRoomID=%s", (room_id,))
            db.commit()
            fetch_function()
            messagebox.showinfo("Thành công", f"Phòng {room_id} đã được xóa.")
        except mysql.connector.Error as e:  # Sử dụng đúng ngoại lệ
            messagebox.showerror("Lỗi", f"Không thể xóa phòng: {e}")
        finally:
            try:
                cursor.fetchall()  # Xử lý kết quả chưa đọc (nếu có)
            except mysql.connector.Error:
                pass

def search_room(table, search_query, search_column):
    """
    Tìm kiếm phòng trong cơ sở dữ liệu và hiển thị kết quả trong bảng.
    """
    columns = ["PetRoomID", "RName", "RStatus", "RType", "RPrice"]
    table_name = "PetRoomTbl"

    # Gọi hàm tìm kiếm và lấy kết quả
    results = search_in_database(search_query, search_column, table_name, columns)

    # Nếu có kết quả, thêm vào bảng
    if results:
        for item in table.get_children():
            table.delete(item)
        for result in results:
            table.insert('', tb.END, values=result)


def show_thuCungRoom(window, user_role, buttons, thuCungRoom_btn):
    """
    Hiển thị giao diện quản lý phòng thú cưng.
    """
    if user_role not in ["admin", "cashier"]:
        messagebox.showerror("Access Denied", "Bạn không có quyền truy cập vào tính năng này.")
        return

    clicked(thuCungRoom_btn, buttons)
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
    thuCungRoom_frame = tb.Labelframe(window, bootstyle="secondary", text="Quản lý phòng thú cưng")
    thuCungRoom_frame.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")
    thuCungRoom_frame.columnconfigure(0, weight=1)
    thuCungRoom_frame.rowconfigure(0, weight=1)
    thuCungRoom_frame.rowconfigure((1, 2, 3, 4, 5, 6), weight=15)

    header_frame = tb.Frame(thuCungRoom_frame, height=60)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="new")

    content_frame = tb.Frame(thuCungRoom_frame)
    content_frame.grid(row=0, column=0, columnspan=2, rowspan=7, sticky="news")
    content_frame.columnconfigure((0, 1), weight=50)
    content_frame.columnconfigure(3, weight=1)
    content_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

    tree_scroll = tb.Scrollbar(content_frame, orient="vertical", bootstyle="primary-round")
    tree_scroll.grid(row=0, rowspan=6, column=3, sticky="wnes", padx=5, pady=30)

    columns = ("cID", "cName", "cStatus", "cType", "cPrice")
    table = tb.Treeview(content_frame, columns=columns, show='headings', yscrollcommand=tree_scroll.set,
                        style="Custom.Treeview")
    tree_scroll.config(command=table.yview)

    table.heading("cID", text="ID")
    table.heading("cName", text="Tên phòng")
    table.heading("cStatus", text="Trạng thái")
    table.heading("cType", text="Loại phòng")
    table.heading("cPrice", text="Giá")

    table.column("cID", width=30, anchor="center")
    table.column("cName", width=150, anchor="center")
    table.column("cStatus", width=80, anchor="center")
    table.column("cType", width=70, anchor="center")
    table.column("cPrice", width=50, anchor="center")

    table.grid(row=0, column=0, padx=10, pady=10, rowspan=6, columnspan=2, sticky="news")

    funcbar = tb.Frame(content_frame, height=60)
    funcbar.grid(row=6, column=0, columnspan=3, sticky="news")
    funcbar.columnconfigure((0, 1, 2, 3, 5), weight=1)
    funcbar.columnconfigure(4, weight=30)

    fetch_room_data(table)

    # Thanh chức năng
    funcbar = tb.Frame(thuCungRoom_frame)
    funcbar.grid(row=7, column=0, sticky="nsew")

    tb.Button(funcbar, text="Thêm", bootstyle="success-outline",
              command=lambda: add_room(lambda: fetch_room_data(table))).grid(row=0, column=0, padx=10, pady=10)
    tb.Button(funcbar, text="Sửa", bootstyle="success-outline",
              command=lambda: edit_room(table, lambda: fetch_room_data(table))).grid(row=0, column=1, padx=10, pady=10)
    tb.Button(funcbar, text="Xóa", bootstyle="danger-outline",
              command=lambda: delete_room(table, lambda: fetch_room_data(table))).grid(row=0, column=2, padx=10, pady=10)

    # Dropdown để chọn thuộc tính tìm kiếm
    columns_map = {
        "ID": "PetRoomID",
        "Tên phòng": "RName",
        "Trạng thái": "RStatus",
        "Loại phòng": "RType",
        "Giá": "RPrice"
    }
    search_column = tb.StringVar()
    search_dropdown = tb.Combobox(funcbar, textvariable=search_column, values=list(columns_map.keys()), width=14)
    search_dropdown.grid(row=0, column=3, padx=10, pady=10)
    search_dropdown.set("Tên phòng")  # Mặc định tìm theo "Tên phòng"

    # Thanh tìm kiếm
    search_entry = tb.Entry(funcbar, width=20)
    search_entry.grid(row=0, column=4, padx=10, pady=10)

    # Nút tìm kiếm
    tb.Button(funcbar, text="Tìm kiếm", bootstyle="primary-outline",
              command=lambda: fetch_room_data(
                  table,
                  search_query=search_entry.get(),
                  search_column=search_dropdown.get()
              )
              ).grid(row=0, column=5, padx=10, pady=10)

