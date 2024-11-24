from tkinter import messagebox
import ttkbootstrap as tb
from DB import cursor, db
from utils import clicked


def fetch_service_data(table, keyword=None):
    """
    Truy xuất dữ liệu dịch vụ từ database và hiển thị trong bảng.

    Args:
        table: Bảng Treeview để hiển thị dữ liệu.
        keyword: Từ khóa tìm kiếm.
    """
    query = "SELECT ServiceID, SName, SCategories, SQuantity, SPrice, SNotes FROM ServiceTbl"
    params = ()
    if keyword:
        query += " WHERE ServiceID LIKE %s OR SName LIKE %s"
        params = (f"%{keyword}%", f"%{keyword}%")

    try:
        cursor.execute(query, params)
        data = cursor.fetchall()

        # Xóa dữ liệu cũ trong bảng
        for item in table.get_children():
            table.delete(item)

        # Thêm dữ liệu mới vào bảng
        for item in data:
            table.insert("", tb.END, values=item)
    except db.Error as e:
        messagebox.showerror("Lỗi", f"Không thể lấy dữ liệu dịch vụ: {e}")


def add_service(table):
    """
    Hiển thị giao diện thêm dịch vụ.
    """
    add_window = tb.Toplevel(title="Thêm dịch vụ", minsize=(380, 520))
    lf = tb.Labelframe(add_window, bootstyle="secondary", text="Thông tin dịch vụ")
    lf.pack(fill="both", padx=5, pady=5, expand=True)

    lf.columnconfigure((0, 1), weight=1)
    lf.columnconfigure(2, weight=30)
    lf.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

    # ID tự động
    tb.Label(lf, text="Service ID").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    id_entry = tb.Entry(lf, width=16)
    id_entry.grid(row=0, column=2, padx=10, pady=5, sticky="e")
    cursor.execute("SELECT MAX(ServiceID) FROM ServiceTbl")
    result = cursor.fetchone()
    new_id = result[0] + 1 if result and result[0] is not None else 1
    id_entry.insert(0, new_id)
    id_entry.configure(state="readonly")

    # Các trường khác
    fields = ["Tên dịch vụ", "Danh mục", "Số lượng", "Giá", "Ghi chú"]
    entries = {}
    for i, field in enumerate(fields, start=1):
        tb.Label(lf, text=field).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tb.Entry(lf, width=16)
        entry.grid(row=i, column=2, padx=10, pady=5, sticky="e")
        entries[field] = entry

    # Nút lưu
    def save_new_service():
        values = {field: entry.get() for field, entry in entries.items()}
        if any(not value for value in values.values()):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin dịch vụ.")
            return

        try:
            cursor.execute(
                "INSERT INTO ServiceTbl (ServiceID, SName, SCategories, SQuantity, SPrice, SNotes) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (new_id, values["Tên dịch vụ"], values["Danh mục"], values["Số lượng"], values["Giá"], values["Ghi chú"]),
            )
            db.commit()
            fetch_service_data(table)
            messagebox.showinfo("Thành công", "Dịch vụ đã được thêm thành công!")
            add_window.destroy()
        except db.Error as e:
            messagebox.showerror("Lỗi", f"Không thể thêm dịch vụ: {e}")

    tb.Button(add_window, text="Thêm", bootstyle="success", command=save_new_service).pack(
        fill="x", padx=10, pady=10
    )


def edit_service(table):
    """
    Hiển thị giao diện sửa dịch vụ đã chọn.
    """
    selected_item = table.focus()
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn dịch vụ để sửa.")
        return

    service_data = table.item(selected_item, "values")
    edit_window = tb.Toplevel(title="Sửa dịch vụ", minsize=(380, 520))
    lf = tb.Labelframe(edit_window, bootstyle="secondary", text="Thông tin dịch vụ")
    lf.pack(fill="both", padx=5, pady=5, expand=True)

    lf.columnconfigure((0, 1), weight=1)
    lf.columnconfigure(2, weight=30)
    lf.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

    # ID không sửa
    tb.Label(lf, text="Service ID").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    id_entry = tb.Entry(lf, width=16)
    id_entry.grid(row=0, column=2, padx=10, pady=5, sticky="e")
    id_entry.insert(0, service_data[0])
    id_entry.configure(state="readonly")

    # Các trường khác
    fields = ["Tên dịch vụ", "Danh mục", "Số lượng", "Giá", "Ghi chú"]
    entries = {}
    for i, field in enumerate(fields, start=1):
        tb.Label(lf, text=field).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tb.Entry(lf, width=16)
        entry.insert(0, service_data[i])
        entry.grid(row=i, column=2, padx=10, pady=5, sticky="e")
        entries[field] = entry

    # Nút lưu
    def save_changes():
        values = {field: entry.get() for field, entry in entries.items()}
        if any(not value for value in values.values()):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            cursor.execute(
                "UPDATE ServiceTbl SET SName=%s, SCategories=%s, SQuantity=%s, SPrice=%s, SNotes=%s WHERE ServiceID=%s",
                (values["Tên dịch vụ"], values["Danh mục"], values["Số lượng"], values["Giá"], values["Ghi chú"], service_data[0]),
            )
            db.commit()
            fetch_service_data(table)
            messagebox.showinfo("Thành công", "Dịch vụ đã được cập nhật!")
            edit_window.destroy()
        except db.Error as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật dịch vụ: {e}")

    tb.Button(edit_window, text="Lưu", bootstyle="success", command=save_changes).pack(
        fill="x", padx=10, pady=10
    )


def delete_service(table):
    """
    Xóa dịch vụ đã chọn.
    """
    selected_item = table.focus()
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn dịch vụ để xóa.")
        return

    service_id = table.item(selected_item, "values")[0]
    confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa dịch vụ ID {service_id}?")
    if confirm:
        try:
            cursor.execute("DELETE FROM ServiceTbl WHERE ServiceID=%s", (service_id,))
            db.commit()
            fetch_service_data(table)
            messagebox.showinfo("Thành công", "Dịch vụ đã được xóa.")
        except db.Error as e:
            messagebox.showerror("Lỗi", f"Không thể xóa dịch vụ: {e}")


def show_dichVu(window, user_role, buttons, dichVu_btn):
    """
    Hiển thị giao diện quản lý dịch vụ.
    """
    if user_role not in ["admin", "cashier"]:
        messagebox.showerror("Access Denied", "Bạn không có quyền truy cập vào tính năng này.")
        return

    clicked(dichVu_btn, buttons)

    # Tạo frame chính
    dichVu_frame = tb.Labelframe(window, bootstyle="secondary", text="Quản lý dịch vụ")
    dichVu_frame.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")

    # Tạo bảng hiển thị
    columns = ("ServiceID", "SName", "SCategories", "SQuantity", "SPrice", "SNotes")
    table = tb.Treeview(dichVu_frame, columns=columns, show="headings")
    for col in columns:
        table.heading(col, text=col)
    table.grid(row=0, column=0, padx=10, pady=10, sticky="news")
    fetch_service_data(table)

    # Thanh chức năng
    funcbar = tb.Frame(dichVu_frame, height=60)
    funcbar.grid(row=1, column=0, sticky="new")

    tb.Button(funcbar, text="Thêm", command=lambda: add_service(table)).pack(side="left", padx=5)
    tb.Button(funcbar, text="Sửa", command=lambda: edit_service(table)).pack(side="left", padx=5)
    tb.Button(funcbar, text="Xóa", command=lambda: delete_service(table)).pack(side="left", padx=5)

    search_entry = tb.Entry(funcbar)
    search_entry.pack(side="left", padx=5)
    tb.Button(funcbar, text="Tìm kiếm", command=lambda: fetch_service_data(table, search_entry.get())).pack(side="left", padx=5)
