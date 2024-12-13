from tkinter import messagebox
import ttkbootstrap as tb
from DB import cursor, db
from utils import clicked


def show_nhaCungCap(window, user_role, buttons, nhaCungCap_btn):
    if user_role not in ['admin', 'cashier']:
        messagebox.showerror("Access Denied", "Bạn không có quyền truy cập vào tính năng này")
        return
    clicked(nhaCungCap_btn, buttons)
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
    nhaCungCap_frame = tb.Labelframe(window, bootstyle="secondary", text="Quản lý Nhà Cung Cấp")
    nhaCungCap_frame.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")
    nhaCungCap_frame.columnconfigure(0, weight=1)
    nhaCungCap_frame.rowconfigure(0, weight=1)
    nhaCungCap_frame.rowconfigure((1, 2, 3, 4, 5, 6), weight=15)

    header_frame = tb.Frame(nhaCungCap_frame, height=60)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="new")

    content_frame = tb.Frame(nhaCungCap_frame)
    content_frame.grid(row=0, column=0, columnspan=2, rowspan=7, sticky="news")
    content_frame.columnconfigure((0, 1), weight=50)
    content_frame.columnconfigure(3, weight=1)
    content_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

    tree_scroll = tb.Scrollbar(content_frame, orient="vertical", bootstyle="primary-round")
    tree_scroll.grid(row=0, rowspan=6, column=3, sticky="wnes", padx=5, pady=30)

    # Định nghĩa các cột cho bảng "supplier"
    columns = ("SupplierID", "SName", "SContact", "SAddress", "SEmail", "SNotes")
    table = tb.Treeview(content_frame, columns=columns, show='headings', yscrollcommand=tree_scroll.set,
                        style="Custom.Treeview")
    tree_scroll.config(command=table.yview)

    # Đặt tiêu đề cột
    table.heading("SupplierID", text="Supplier ID")
    table.heading("SName", text="Tên Nhà Cung Cấp")
    table.heading("SContact", text="Số Điện Thoại")
    table.heading("SAddress", text="Địa Chỉ")
    table.heading("SEmail", text="Email")
    table.heading("SNotes", text="Ghi Chú")

    # Đặt chiều rộng cột
    table.column("SupplierID", width=30, anchor="center")
    table.column("SName", width=150, anchor="center")
    table.column("SContact", width=100, anchor="center")
    table.column("SAddress", width=200, anchor="center")
    table.column("SEmail", width=150, anchor="center")
    table.column("SNotes", width=150, anchor="center")

    table.grid(row=0, column=0, padx=10, pady=10, rowspan=6, columnspan=2, sticky="news")

    funcbar = tb.Frame(content_frame, height=60)
    funcbar.grid(row=6, column=0, columnspan=3, sticky="news")
    funcbar.columnconfigure((0, 1, 2, 3, 5), weight=1)
    funcbar.columnconfigure(4, weight=30)

    def fetch_and_insert_data():
        # Câu lệnh SQL phù hợp với bảng "supplier"
        cursor.execute("SELECT SupplierID, SupplierName, SupplierContact, SupplierAddress, SupplierEmail, SupplierNotes FROM SupplierTbl")

        # Xóa dữ liệu cũ trong bảng
        for item in table.get_children():
            table.delete(item)

        # Lấy dữ liệu từ cơ sở dữ liệu
        data = cursor.fetchall()

        # Định dạng hiển thị
        table.tag_configure('evenrow', background='#f2f2f2')
        table.tag_configure('oddrow', background='#ffffff')
        for i, item in enumerate(data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            table.insert('', tb.END, values=(item[0], item[1], item[2], item[3], item[4], item[5]), tags=(tag,))

    fetch_and_insert_data()

    def themNhaCungCap():
        addwindow = tb.Toplevel(title="Thêm Nhà Cung Cấp", minsize=(380, 520))
        lf = tb.Labelframe(addwindow, bootstyle="secondary", text="")
        lf.pack(fill="both", padx=5, pady=5, expand=True, anchor="w")
        lf.columnconfigure((0, 1), weight=1)
        lf.columnconfigure(2, weight=30)
        lf.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Supplier ID
        id_lb = tb.Label(lf, bootstyle="secondary", text="Supplier ID")
        id_lb.grid(row=0, column=0, padx=10, pady=5, sticky="new")
        id_entry = tb.Entry(lf, width=16)
        id_entry.grid(row=0, column=2, padx=10, pady=5, sticky="new")
        cursor.execute("SELECT MAX(SupplierID) FROM SupplierTbl")
        result = cursor.fetchone()
        sID = result[0] + 1 if result and result[0] is not None else "No ID"
        id_entry.insert(0, sID)

        # Supplier Name
        name_lb = tb.Label(lf, bootstyle="secondary", text="Tên Nhà Cung Cấp")
        name_lb.grid(row=1, column=0, padx=10, pady=5, sticky="new")
        name_entry = tb.Entry(lf, width=16)
        name_entry.grid(row=1, column=2, padx=10, pady=5, sticky="new")

        # Contact
        contact_lb = tb.Label(lf, bootstyle="secondary", text="Liên Hệ")
        contact_lb.grid(row=2, column=0, padx=10, pady=5, sticky="new")
        contact_entry = tb.Entry(lf, width=16)
        contact_entry.grid(row=2, column=2, padx=10, pady=5, sticky="new")

        # Address
        address_lb = tb.Label(lf, bootstyle="secondary", text="Địa Chỉ")
        address_lb.grid(row=3, column=0, padx=10, pady=5, sticky="new")
        address_entry = tb.Entry(lf, width=16)
        address_entry.grid(row=3, column=2, padx=10, pady=5, sticky="new")

        # Email
        email_lb = tb.Label(lf, bootstyle="secondary", text="Email")
        email_lb.grid(row=4, column=0, padx=10, pady=5, sticky="new")
        email_entry = tb.Entry(lf, width=16)
        email_entry.grid(row=4, column=2, padx=10, pady=5, sticky="new")

        # Notes
        notes_lb = tb.Label(lf, bootstyle="secondary", text="Ghi Chú")
        notes_lb.grid(row=5, column=0, padx=10, pady=5, sticky="new")
        notes_entry = tb.Entry(lf, width=16)
        notes_entry.grid(row=5, column=2, padx=10, pady=5, sticky="new")

        def add_sql():
            supplier_id = id_entry.get()
            supplier_name = name_entry.get()
            supplier_contact = contact_entry.get()
            supplier_address = address_entry.get()
            supplier_email = email_entry.get()
            supplier_notes = notes_entry.get()

            if not supplier_id or not supplier_name or not supplier_contact or not supplier_address or not supplier_email:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin nhà cung cấp.")
                return

            try:
                cursor.execute(
                    "INSERT INTO SupplierTbl (SupplierID, SupplierName, SupplierContact, SupplierAddress, SupplierEmail, SupplierNotes) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (supplier_id, supplier_name, supplier_contact, supplier_address, supplier_email, supplier_notes)
                )
                db.commit()

                fetch_and_insert_data()

                messagebox.showinfo("Thành công", "Nhà cung cấp đã được thêm thành công!")
                addwindow.destroy()

            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ!")
            except db.Error as e:
                messagebox.showerror("Lỗi", f"Không thể thêm nhà cung cấp: {e}")

        them = tb.Button(addwindow, bootstyle="success", text="Thêm", command=add_sql)
        them.pack(side=tb.LEFT, fill="x", padx=10, pady=10, expand=True, anchor="w")

    def suaNhaCungCap():
        selected_item = table.focus()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhà cung cấp để sửa.")
            return

        ID = table.item(selected_item, 'values')[0]

        cursor.execute("SELECT * FROM SupplierTbl WHERE SupplierID=%s", (ID,))
        item_data = cursor.fetchone()

        editwindow = tb.Toplevel(title="Sửa Nhà Cung Cấp", minsize=(380, 520))
        lf = tb.Labelframe(editwindow, bootstyle="secondary", text="")
        lf.pack(fill="both", padx=5, pady=5, expand=True, anchor="w")
        lf.columnconfigure((0, 1), weight=1)
        lf.columnconfigure(2, weight=30)
        lf.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Các trường dữ liệu
        fields = [
            ("Supplier ID", item_data[0]),
            ("Tên Nhà Cung Cấp", item_data[1]),
            ("Liên Hệ", item_data[2]),
            ("Địa Chỉ", item_data[3]),
            ("Email", item_data[4]),
            ("Ghi Chú", item_data[5])
        ]
        entries = {}
        for i, (label_text, value) in enumerate(fields):
            label = tb.Label(lf, bootstyle="secondary", text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="new")
            entry = tb.Entry(lf, width=16)
            entry.grid(row=i, column=2, padx=10, pady=5, sticky="new")
            entry.insert(0, value)
            entries[label_text] = entry

        def update_sql():
            supplier_id = entries["Supplier ID"].get()
            supplier_name = entries["Tên Nhà Cung Cấp"].get()
            supplier_contact = entries["Liên Hệ"].get()
            supplier_address = entries["Địa Chỉ"].get()
            supplier_email = entries["Email"].get()
            supplier_notes = entries["Ghi Chú"].get()

            if not supplier_name or not supplier_contact or not supplier_address or not supplier_email:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin nhà cung cấp.")
                return

            try:
                cursor.execute(
                    "UPDATE SupplierTbl SET SupplierName=%s, SupplierContact=%s, SupplierAddress=%s, SupplierEmail=%s, SupplierNotes=%s WHERE SupplierID=%s",
                    (supplier_name, supplier_contact, supplier_address, supplier_email, supplier_notes, supplier_id)
                )
                db.commit()

                fetch_and_insert_data()
                messagebox.showinfo("Thành công", "Thông tin nhà cung cấp đã được cập nhật!")
                editwindow.destroy()
            except db.Error as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật nhà cung cấp: {e}")

        btn_update = tb.Button(editwindow, bootstyle="success", text="Sửa", command=update_sql)
        btn_update.pack(side=tb.LEFT, fill="x", padx=10, pady=10, expand=True, anchor="w")

    def xoaNhaCungCap():
        selected_item = table.focus()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhà cung cấp để xóa.")
            return

        ID = table.item(selected_item, 'values')[0]

        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa nhà cung cấp có ID {ID} không?")
        if confirm:
            try:
                cursor.execute("DELETE FROM SupplierTbl WHERE SupplierID=%s", (ID,))
                db.commit()

                fetch_and_insert_data()
                messagebox.showinfo("Thành công", "Nhà cung cấp đã được xóa!")
            except db.Error as e:
                messagebox.showerror("Lỗi", f"Không thể xóa nhà cung cấp: {e}")

    def timkiemNhaCungCap():
        keyword = search_entry.get()
        query = """
        SELECT SupplierID, SupplierName, SupplierContact, SupplierAddress, SupplierEmail, SupplierNotes 
        FROM SupplierTbl 
        WHERE SupplierID LIKE %s OR SupplierName LIKE %s OR SupplierContact LIKE %s OR SupplierAddress LIKE %s OR SupplierEmail LIKE %s
        """
        search_pattern = f'%{keyword}%'
        cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))

        # Xóa dữ liệu cũ trong bảng
        for item in table.get_children():
            table.delete(item)

        # Lấy dữ liệu và hiển thị
        data = cursor.fetchall()
        for item in data:
            table.insert('', tb.END, values=(item[0], item[1], item[2], item[3], item[4], item[5]))

    btn_them = tb.Button(funcbar, bootstyle="success-outline", text="Thêm", command=themNhaCungCap)
    btn_them.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    btn_sua = tb.Button(funcbar, bootstyle="success-outline", text="Sửa", command=suaNhaCungCap)
    btn_sua.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    btn_xoa = tb.Button(funcbar, bootstyle="danger-outline", text="Xóa", command=xoaNhaCungCap)
    btn_xoa.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    btn_refresh = tb.Button(funcbar, bootstyle="secondary-outline", text="Làm mới", command=fetch_and_insert_data)
    btn_refresh.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

    search_entry = tb.Entry(funcbar)
    search_entry.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

    btn_tim = tb.Button(funcbar, bootstyle="info-outline", text="Tìm", command=timkiemNhaCungCap)
    btn_tim.grid(row=0, column=5, padx=10, pady=10, sticky="ew")