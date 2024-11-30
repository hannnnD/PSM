from tkinter import messagebox
import ttkbootstrap as tb
from DB import cursor, db
from utils import clicked


def show_dichVu(window, user_role, buttons, dichVu_btn):
    if user_role not in ['admin', 'cashier']:
        messagebox.showerror("Access Denied", "Bạn không có quyền truy cập vào tính năng này")
        return
    clicked(dichVu_btn, buttons)
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
    dichVu_frame = tb.Labelframe(window, bootstyle="secondary", text="Quản lý Dịch vụ")
    dichVu_frame.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")
    dichVu_frame.columnconfigure(0, weight=1)
    dichVu_frame.rowconfigure(0, weight=1)
    dichVu_frame.rowconfigure((1, 2, 3, 4, 5, 6), weight=15)

    header_frame = tb.Frame(dichVu_frame, height=60)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="new")

    content_frame = tb.Frame(dichVu_frame)
    content_frame.grid(row=0, column=0, columnspan=2, rowspan=7, sticky="news")
    content_frame.columnconfigure((0, 1), weight=50)
    content_frame.columnconfigure(3, weight=1)
    content_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

    tree_scroll = tb.Scrollbar(content_frame, orient="vertical", bootstyle="primary-round")
    tree_scroll.grid(row=0, rowspan=6, column=3, sticky="wnes", padx=5, pady=30)

    columns = ("ServiceID", "SName", "SCategories", "SQuantity", "SPrice", "SNotes")
    table = tb.Treeview(content_frame, columns=columns, show='headings', yscrollcommand=tree_scroll.set,
                        style="Custom.Treeview")
    tree_scroll.config(command=table.yview)

    table.heading("ServiceID", text="Service ID")
    table.heading("SName", text="Tên dịch vụ")
    table.heading("SCategories", text="Danh mục")
    table.heading("SQuantity", text="Số lượng")
    table.heading("SPrice", text="Giá")
    table.heading("SNotes", text="Ghi chú")

    table.column("ServiceID", width=30, anchor="center")
    table.column("SName", width=150, anchor="center")
    table.column("SCategories", width=80, anchor="center")
    table.column("SQuantity", width=70, anchor="center")
    table.column("SPrice", width=50, anchor="center")
    table.column("SNotes", width=150, anchor="center")

    table.grid(row=0, column=0, padx=10, pady=10, rowspan=6, columnspan=2, sticky="news")

    funcbar = tb.Frame(content_frame, height=60)
    funcbar.grid(row=6, column=0, columnspan=3, sticky="news")
    funcbar.columnconfigure((0, 1, 2, 3, 5), weight=1)
    funcbar.columnconfigure(4, weight=30)

    def fetch_and_insert_data():
        cursor.execute("SELECT ServiceID, SName, SCategories, SQuantity, SPrice, SNotes FROM ServiceTbl")
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
            table.insert('', tb.END, values=(item[0], item[1], item[2], item[3], formatted_total, item[5]), tags=(tag,))

    fetch_and_insert_data()

    def themDichVu():
        addwindow = tb.Toplevel(title="Thêm dịch vụ", minsize=(380, 520))
        lf = tb.Labelframe(addwindow, bootstyle="secondary", text="")
        lf.pack(fill="both", padx=5, pady=5, expand=True, anchor="w")
        lf.columnconfigure((0, 1), weight=1)
        lf.columnconfigure(2, weight=30)
        lf.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        id_lb = tb.Label(lf, bootstyle="secondary", text="Service ID")
        id_lb.grid(row=0, column=0, padx=10, pady=5, sticky="new")
        id_entry = tb.Entry(lf, width=16)
        id_entry.grid(row=0, column=2, padx=10, pady=5, sticky="new")
        cursor.execute("Select MAX(ServiceID) FROM ServiceTbl")
        result = cursor.fetchone()
        sID = result[0] + 1 if result and result[0] is not None else "No ID"
        id_entry.insert(0, sID)

        name_lb = tb.Label(lf, bootstyle="secondary", text="Tên dịch vụ")
        name_lb.grid(row=1, column=0, padx=10, pady=5, sticky="new")
        name_entry = tb.Entry(lf, width=16)
        name_entry.grid(row=1, column=2, padx=10, pady=5, sticky="new")

        categories_lb = tb.Label(lf, bootstyle="secondary", text="Danh mục")
        categories_lb.grid(row=2, column=0, padx=10, pady=5, sticky="new")
        categories_entry = tb.Entry(lf, width=16)
        categories_entry.grid(row=2, column=2, padx=10, pady=5, sticky="new")

        quantity_lb = tb.Label(lf, bootstyle="secondary", text="Số lượng")
        quantity_lb.grid(row=3, column=0, padx=10, pady=5, sticky="new")
        quantity_entry = tb.Entry(lf, width=16)
        quantity_entry.grid(row=3, column=2, padx=10, pady=5, sticky="new")

        price_lb = tb.Label(lf, bootstyle="secondary", text="Giá")
        price_lb.grid(row=4, column=0, padx=10, pady=5, sticky="new")
        price_entry = tb.Entry(lf, width=16)
        price_entry.grid(row=4, column=2, padx=10, pady=5, sticky="new")

        notes_lb = tb.Label(lf, bootstyle="secondary", text="Ghi chú")
        notes_lb.grid(row=5, column=0, padx=10, pady=5, sticky="new")
        notes_entry = tb.Entry(lf, width=16)
        notes_entry.grid(row=5, column=2, padx=10, pady=5, sticky="new")

        def add_sql():
            id = id_entry.get()
            name = name_entry.get()
            categories = categories_entry.get()
            quantity = quantity_entry.get()
            price = price_entry.get()
            notes = notes_entry.get()

            if not id or not name or not categories or not quantity or not price:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin dịch vụ.")
                return
            try:
                cursor.execute(
                    "INSERT INTO ServiceTbl (ServiceID, SName, SCategories, SQuantity, SPrice, SNotes) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id, name, categories, quantity, price, notes)
                )
                db.commit()

                fetch_and_insert_data()

                messagebox.showinfo("Thành công", "Thông tin đã được thêm thành công!")
                addwindow.destroy()

            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ!")
            except db.Error as e:
                messagebox.showerror("Lỗi", f"Không thể thêm dịch vụ: {e}")

        them = tb.Button(addwindow, bootstyle="success", text="Thêm", command=add_sql)
        them.pack(side=tb.LEFT, fill="x", padx=10, pady=10, expand=True, anchor="w")

    def suaDichVu():
        selected_item = table.focus()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn dịch vụ để sửa.")
            return

        ID = table.item(selected_item, 'values')[0]

        cursor.execute("SELECT * FROM ServiceTbl WHERE ServiceID=%s", (ID,))
        item_data = cursor.fetchone()

        editwindow = tb.Toplevel(title="Sửa dịch vụ", minsize=(380, 520))
        lf = tb.Labelframe(editwindow, bootstyle="secondary", text="")
        lf.pack(fill="both", padx=5, pady=5, expand=True, anchor="w")
        lf.columnconfigure((0, 1), weight=1)
        lf.columnconfigure(2, weight=30)
        lf.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        id_lb = tb.Label(lf, bootstyle="secondary", text="Service ID")
        id_lb.grid(row=0, column=0, padx=10, pady=5, sticky="new")
        id_entry = tb.Entry(lf, width=16)
        id_entry.grid(row=0, column=2, padx=10, pady=5, sticky="new")

        name_lb = tb.Label(lf, bootstyle="secondary", text="Tên dịch vụ")
        name_lb.grid(row=1, column=0, padx=10, pady=5, sticky="new")
        name_entry = tb.Entry(lf, width=16)
        name_entry.grid(row=1, column=2, padx=10, pady=5, sticky="new")

        categories_lb = tb.Label(lf, bootstyle="secondary", text="Danh mục")
        categories_lb.grid(row=2, column=0, padx=10, pady=5, sticky="new")
        categories_entry = tb.Entry(lf, width=16)
        categories_entry.grid(row=2, column=2, padx=10, pady=5, sticky="new")

        quantity_lb = tb.Label(lf, bootstyle="secondary", text="Số lượng")
        quantity_lb.grid(row=3, column=0, padx=10, pady=5, sticky="new")
        quantity_entry = tb.Entry(lf, width=16)
        quantity_entry.grid(row=3, column=2, padx=10, pady=5, sticky="new")

        price_lb = tb.Label(lf, bootstyle="secondary", text="Giá")
        price_lb.grid(row=4, column=0, padx=10, pady=5, sticky="new")
        price_entry = tb.Entry(lf, width=16)
        price_entry.grid(row=4, column=2, padx=10, pady=5, sticky="new")

        notes_lb = tb.Label(lf, bootstyle="secondary", text="Ghi chú")
        notes_lb.grid(row=5, column=0, padx=10, pady=5, sticky="new")
        notes_entry = tb.Entry(lf, width=16)
        notes_entry.grid(row=5, column=2, padx=10, pady=5, sticky="new")

        id_entry.insert(0, item_data[0])
        name_entry.insert(0, item_data[1])
        categories_entry.insert(0, item_data[2])
        quantity_entry.insert(0, item_data[3])
        price_entry.insert(0, item_data[4])
        notes_entry.insert(0, item_data[5])

        def update_sql():
            id = id_entry.get()
            name = name_entry.get()
            categories = categories_entry.get()
            quantity = quantity_entry.get()
            price = price_entry.get()
            notes = notes_entry.get()

            if not id or not name or not categories or not quantity or not price:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin dịch vụ.")
                return
            try:
                cursor.execute(
                    "UPDATE ServiceTbl SET SName=%s, SCategories=%s, SQuantity=%s, SPrice=%s, SNotes=%s WHERE ServiceID=%s",
                    (name, categories, quantity, price, notes, id)
                )
                db.commit()

                fetch_and_insert_data()

                messagebox.showinfo("Thành công", "Thông tin đã được cập nhật thành công!")
                editwindow.destroy()

            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ!")
            except db.Error as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật dịch vụ: {e}")

        sua = tb.Button(editwindow, bootstyle="success", text="Sửa", command=update_sql)
        sua.pack(side=tb.LEFT, fill="x", padx=10, pady=10, expand=True, anchor="w")

    def xoaDichVu():
        selected_item = table.focus()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn dịch vụ để xóa.")
            return

        ID = table.item(selected_item, 'values')[0]

        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa dịch vụ có ID {ID} không?")
        if confirm:
            try:
                cursor.execute("DELETE FROM ServiceTbl WHERE ServiceID=%s", (ID,))
                db.commit()

                fetch_and_insert_data()

                messagebox.showinfo("Thành công", "Dịch vụ đã được xóa thành công!")
            except db.Error as e:
                messagebox.showerror("Lỗi", f"Không thể xóa dịch vụ: {e}")

    btn_them = tb.Button(funcbar, bootstyle="success-outline", text="Thêm", command=themDichVu)
    btn_them.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    btn_sua = tb.Button(funcbar, bootstyle="success-outline", text="Sửa", command=suaDichVu)
    btn_sua.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    btn_xoa = tb.Button(funcbar, bootstyle="danger-outline", text="Xóa", command=xoaDichVu)
    btn_xoa.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    btn_refresh = tb.Button(funcbar, bootstyle="secondary-outline", text="Làm mới", command=fetch_and_insert_data)
    btn_refresh.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

    search_entry = tb.Entry(funcbar)
    search_entry.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

    def timkiemDichVu():
        keyword = search_entry.get()
        cursor.execute(
            "SELECT ServiceID, SName, SCategories, SQuantity, SPrice, SNotes FROM ServiceTbl WHERE ServiceID LIKE %s OR SName LIKE %s",
            (f'%{keyword}%', f'%{keyword}%')
        )
        for item in table.get_children():
            table.delete(item)
        data = cursor.fetchall()
        for item in data:
            table.insert('', tb.END, values=(item[0], item[1], item[2], item[3], item[4], item[5]))

    btn_tim = tb.Button(funcbar, bootstyle="info-outline", text="Tìm", command=timkiemDichVu)
    btn_tim.grid(row=0, column=5, padx=10, pady=10, sticky="ew")