from tkinter import messagebox

import mysql
import ttkbootstrap as tb
from DB import cursor, db
from utils import clicked
from datetime import datetime, timedelta, date

def show_thuCung(window, user_role, buttons, thuCung_btn):
    """
    Hiển thị giao diện quản lý thú cưng.

    Args:
        window: Cửa sổ chính.
        user_role: Vai trò người dùng.
        buttons: Danh sách các nút.
        thuCung_btn: Nút hiện tại đang được kích hoạt.
    """
    if user_role not in ["admin", "cashier"]:
        messagebox.showerror("Access Denied", "Bạn không có quyền truy cập vào tính năng này.")
        return

    clicked(thuCung_btn, buttons)
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
    thuCung_frame = tb.Labelframe(window, bootstyle="secondary", text="Quản lý lưu trú")
    thuCung_frame.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")
    thuCung_frame.columnconfigure(0, weight=1)
    thuCung_frame.rowconfigure(0, weight=1)
    thuCung_frame.rowconfigure((1, 2, 3, 4, 5, 6), weight=15)

    content_frameT = tb.Frame(thuCung_frame)
    content_frameT.grid(row=0, column=0, columnspan=2, rowspan=7, sticky="news")
    content_frameT.columnconfigure((0, 1), weight=50)
    content_frameT.columnconfigure(3, weight=1)
    content_frameT.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

    tree_scrollT = tb.Scrollbar(content_frameT, orient="vertical", bootstyle="secondary-round")
    tree_scrollT.grid(row=0, rowspan=6, column=3, sticky="wnes", padx=5, pady=30)

    columns = ("tID", "tName", "tBreed", "tDOB", "pType", "tDate", "tRoom", "cID")
    table = tb.Treeview(content_frameT, columns=columns, show='headings', yscrollcommand=tree_scrollT.set,
                        style="Custom.Treeview")
    tree_scrollT.config(command=table.yview)

    table.heading("tID", text="Pet ID")
    table.heading("tName", text="Tên")
    table.heading("tBreed", text="Giống")
    table.heading("tDOB", text="Ngày sinh")
    table.heading("pType", text="Loài")
    table.heading("tDate", text="Ngày đăng ký")
    table.heading("tRoom", text="Phòng")
    table.heading("cID", text="ID Chủ")

    table.column("tID", width=20, anchor="center")
    table.column("tName", width=50, anchor="center")
    table.column("tBreed", width=70, anchor="center")
    table.column("tDOB", width=40, anchor="center")
    table.column("pType", width=30, anchor="center")
    table.column("tDate", width=30, anchor="center")
    table.column("tRoom", width=30, anchor="center")
    table.column("cID", width=30, anchor="center")
    table.grid(row=0, column=0, padx=10, pady=10, rowspan=6, columnspan=2, sticky="news")

    funcbar = tb.Frame(content_frameT, height=60)
    funcbar.grid(row=6, column=0, columnspan=3, sticky="news")
    funcbar.columnconfigure((0, 1, 2, 3, 5), weight=1)
    funcbar.columnconfigure(4, weight=30)

    def fetch_and_insert_data():
        cursor.execute(
            "SELECT PetCareID, PetName, PetBreed, PetDOB, PetType, StartDate, PetRoomID, CustID  FROM petcaretbl")
        for item in table.get_children():
            table.delete(item)
        data = cursor.fetchall()

        table.tag_configure('evenrow', background='#f2f2f2')
        table.tag_configure('oddrow', background='#ffffff')
        for i, item in enumerate(data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            table.insert('', tb.END, values=(
                f"P{item[0]}", item[1], item[2], item[3], item[4], item[5], f"PR{item[6]}", f"KH{item[7]}"), tags=(tag,))


    fetch_and_insert_data()

    def themPet():
        addwindow = tb.Toplevel(title="Thêm lưu trú", minsize=(380, 800))
        lf = tb.Labelframe(addwindow, bootstyle="secondary", text="")
        lf.pack(fill="both", padx=5, pady=5, expand=True, anchor="w")
        lf.columnconfigure((0, 1), weight=1)
        lf.columnconfigure(2, weight=30)
        lf.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        id_lb = tb.Label(lf, bootstyle="secondary", text="ID")
        id_lb.grid(row=0, column=0, padx=10, pady=5, sticky="new")
        id_entry = tb.Entry(lf, width=16)
        id_entry.grid(row=0, column=2, padx=10, pady=5, sticky="new")
        cursor.execute("Select MAX(PetCareID) FROM petcaretbl")
        result = cursor.fetchone()
        kID = result[0] + 1 if result and result[0] is not None else "No ID"
        id_entry.insert(0, kID)

        pname_lb = tb.Label(lf, bootstyle="secondary", text="Tên")
        pname_lb.grid(row=1, column=0, padx=10, pady=5, sticky="new")
        pname_entry = tb.Entry(lf, width=16)
        pname_entry.grid(row=1, column=2, padx=10, pady=5, sticky="new")

        breed_lb = tb.Label(lf, bootstyle="secondary", text="Giống")
        breed_lb.grid(row=2, column=0, padx=10, pady=5, sticky="new")
        breed_entry = tb.Entry(lf, width=16)
        breed_entry.grid(row=2, column=2, padx=10, pady=5, sticky="new")

        dob_lb = tb.Label(lf, bootstyle="secondary", text="Ngày sinh")
        dob_lb.grid(row=3, column=0, padx=10, pady=5, sticky="new")
        dob_entry = tb.DateEntry(lf, width=16)
        dob_entry.grid(row=3, column=2, padx=10, pady=5, sticky="new")

        ptype = ["Thú", "Chim", "Cá", "Khác"]
        type_lb = tb.Label(lf, bootstyle="secondary", text="Loài")
        type_lb.grid(row=4, column=0, padx=10, pady=5, sticky="new")
        type_entry = tb.Combobox(lf, width=16, values=ptype)
        type_entry.grid(row=4, column=2, padx=10, pady=5, sticky="new")

        date_lb = tb.Label(lf, bootstyle="secondary", text="Ngày đăng ký")
        date_lb.grid(row=5, column=0, padx=10, pady=5, sticky="new")
        date_entry = tb.DateEntry(lf, width=16)
        date_entry.grid(row=5, column=2, padx=10, pady=5, sticky="new")

        def getRoom(event):
            loai = type_entry.get()
            cursor.execute(
                "SELECT PetRoomID FROM petroomtbl WHERE RStatus = 'Trống' AND RType = %s",
                (loai,))
            rooms_data = cursor.fetchall()
            rooms = [f"PR{str(row[0])}" for row in rooms_data]
            room_entry['values'] = rooms

        type_entry.bind("<<ComboboxSelected>>", getRoom)

        room_lb = tb.Label(lf, bootstyle="secondary", text="Phòng")
        room_lb.grid(row=6, column=0, padx=10, pady=5, sticky="new")
        room_entry = tb.Combobox(lf, width=16)
        room_entry.grid(row=6, column=2, padx=10, pady=5, sticky="new")

        cursor.execute("SELECT CustID FROM customertbl")
        customer_data = cursor.fetchall()
        customer = [f"KH{str(row[0])}" for row in customer_data]

        cus_lb = tb.Label(lf, bootstyle="secondary", text="Khách hàng")
        cus_lb.grid(row=7, column=0, padx=10, pady=5, sticky="new")
        cus_entry = tb.Combobox(lf, width=16, values=customer)
        cus_entry.grid(row=7, column=2, padx=10, pady=5, sticky="new")

        def getcName(event):
            khach = cus_entry.get().strip("KH")
            cursor.execute(
                "SELECT CustName FROM customertbl WHERE CustID = %s",
                (khach,))
            cName = cursor.fetchone()
            if cName:  # Check if cName is not None
                cus_name_entry.delete(0, 'end')
                cus_name_entry.insert(0, cName[0])  # Insert only the name

        cus_entry.bind("<<ComboboxSelected>>", getcName)

        cus_name_lb = tb.Label(lf, bootstyle="secondary", text="Tên khách hàng")
        cus_name_lb.grid(row=8, column=0, padx=10, pady=5, sticky="new")
        cus_name_entry = tb.Entry(lf, width=16)
        cus_name_entry.grid(row=8, column=2, padx=10, pady=5, sticky="new")

        def add_sql():
            pid = id_entry.get()
            pname = pname_entry.get()
            breed = breed_entry.get()
            dob = dob_entry.entry.get()
            ptype = type_entry.get()
            date = date_entry.entry.get()
            room = room_entry.get()
            customerID = cus_entry.get().strip("KH")

            if not pid or not pname or not breed or not dob or not ptype or not date or not room or not customerID:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!.")
                return
            try:
                cursor.execute(
                    "INSERT INTO petcaretbl (PetCareID, PetName, PetBreed, PetDOB, PetType, StartDate, PetRoomID, CustID) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (pid, pname, breed, dob, ptype, date, room, customerID)
                )
                cursor.execute("UPDATE petroomtbl SET RStatus = 'Đủ' WHERE PetRoomID = %s", (room,))
                db.commit()

                fetch_and_insert_data()

                messagebox.showinfo("Thành công", "Thông tin lưu trú đã được thêm thành công!")
                addwindow.destroy()

            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ!")
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Không thể đăng ký lưu trú: {e}")

        them = tb.Button(addwindow, bootstyle="success", text="Thêm", command=add_sql)
        them.pack(side=tb.LEFT, fill="x", padx=10, pady=10, expand=True, anchor="w")

    def suaPet():
        selected_item = table.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Vui lòng chọn một thú cưng để sửa.")
            return

        item = table.item(selected_item)
        pet_data = item['values']

        editwindow = tb.Toplevel()
        editwindow.title("Sửa lưu trú")
        editwindow.minsize(380, 800)

        lf = tb.Labelframe(editwindow, text="")
        lf.pack(fill="both", padx=5, pady=5, expand=True, anchor="w")
        lf.columnconfigure((0, 1), weight=1)
        lf.columnconfigure(2, weight=30)
        lf.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        id_lb = tb.Label(lf, text="ID", bootstyle="secondary")
        id_lb.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        id_entry = tb.Entry(lf, width=16)
        id_entry.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        id_entry.insert(0, pet_data[0])
        id_entry.config(state='disabled')

        pname_lb = tb.Label(lf, text="Tên", bootstyle="secondary")
        pname_lb.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        pname_entry = tb.Entry(lf, width=16)
        pname_entry.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        pname_entry.insert(0, pet_data[1])

        breed_lb = tb.Label(lf, text="Giống", bootstyle="secondary")
        breed_lb.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        breed_entry = tb.Entry(lf, width=16)
        breed_entry.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        breed_entry.insert(0, pet_data[2])

        # Convert string dates to datetime objects
        dob_date = datetime.strptime(pet_data[3], "%m/%d/%Y")
        reg_date = datetime.strptime(pet_data[5], "%m/%d/%Y")

        dob_lb = tb.Label(lf, text="Ngày sinh", bootstyle="secondary")
        dob_lb.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        dob_entry = tb.DateEntry(lf, width=16)
        dob_entry.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        dob_entry["startdate"] = dob_date

        ptype = ["Thú", "Chim", "Cá", "Khác"]
        type_lb = tb.Label(lf, text="Loài", bootstyle="secondary")
        type_lb.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        type_entry = tb.Combobox(lf, width=16, values=ptype)
        type_entry.grid(row=4, column=2, padx=10, pady=5, sticky="w")
        type_entry.set(pet_data[4])

        date_lb = tb.Label(lf, text="Ngày đăng ký", bootstyle="secondary")
        date_lb.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        date_entry = tb.DateEntry(lf, width=16)
        date_entry.grid(row=5, column=2, padx=10, pady=5, sticky="w")
        date_entry["startdate"] = reg_date

        room_lb = tb.Label(lf, text="Phòng", bootstyle="secondary")
        room_lb.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        room_entry = tb.Combobox(lf, width=16)
        room_entry.grid(row=6, column=2, padx=10, pady=5, sticky="w")
        room_entry.set(pet_data[6])

        cus_lb = tb.Label(lf, text="Khách hàng", bootstyle="secondary")
        cus_lb.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        cus_entry = tb.Combobox(lf, width=16)
        cus_entry.grid(row=7, column=2, padx=10, pady=5, sticky="w")
        cus_entry.set(pet_data[7])

        def save_changes():
            pid = id_entry.get().strip("P")
            pname = pname_entry.get()
            breed = breed_entry.get()
            dob = dob_entry.entry.get()
            ptype = type_entry.get()
            date = date_entry.entry.get()
            room = room_entry.get().strip("PR")
            customerID = cus_entry.get().strip("KH")

            if not pid or not pname or not breed or not dob or not ptype or not date or not room or not customerID:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return
            try:
                cursor.execute(
                    "UPDATE petcaretbl SET PetName=%s, PetBreed=%s, PetDOB=%s, PetType=%s, StartDate=%s, PetRoomID=%s, CustID=%s WHERE PetCareID=%s",
                    (pname, breed, dob, ptype, date, room, customerID, pid)
                )
                db.commit()

                fetch_and_insert_data()

                messagebox.showinfo("Thành công", "Thông tin lưu trú đã được cập nhật thành công!")
                editwindow.destroy()

            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ!")
            except db.Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật lưu trú: {e}")

        save_btn = tb.Button(editwindow, bootstyle="success", text="Lưu", command=save_changes)
        save_btn.pack(side=tb.LEFT, fill="x", padx=10, pady=10, expand=True, anchor="w")

    def traPet():
        selected_item = table.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Vui lòng chọn một thú cưng để trả.")
            return
        item = table.item(selected_item)
        pet_data = item['values']
        pid = pet_data[0].strip("P")
        rid = pet_data[6].strip("PR")

        confirm = messagebox.askyesno("Xác nhận trả", f"Trả phòng: Pet ID: {pid}, Room ID: {rid}?")
        if confirm:
            try:
                cursor.execute("DELETE FROM petcaretbl WHERE PetCareID =%s", (pid,))
                cursor.execute("UPDATE petroomtbl SET RStatus = 'Trống' WHERE PetRoomID =%s", (rid,))
                db.commit()

                fetch_and_insert_data()

                messagebox.showinfo("Thành công", f"Thú cưng ID {pid} đã được trả thành công!")

            except db.Error as e:
                messagebox.showerror("Lỗi", f"Xảy ra lỗi khi trả thú: {e}")

    def timPet():
        keyword = e.get().strip()

        # Clear previous table data
        for item in table.get_children():
            table.delete(item)

        if not keyword:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa để tìm kiếm.")
            return

        try:
            # Attempt to parse the keyword as an integer to search by PetCareID, PetRoomID, or CustID
            search_id = int(keyword)
            cursor.execute(
                "SELECT PetCareID, PetName, PetBreed, PetDOB, PetType, StartDate, PetRoomID, CustID "
                "FROM petcaretbl WHERE PetCareID = %s OR PetName LIKE %s",
                (search_id, '%' + keyword + '%',)
            )
        except ValueError:
            # If keyword is not an integer, search by PetName
            cursor.execute(
                "SELECT PetCareID, PetName, PetBreed, PetDOB, PetType, StartDate, PetRoomID, CustID "
                "FROM petcaretbl WHERE PetName LIKE %s",
                ('%' + keyword + '%',)
            )

        data = cursor.fetchall()

        if not data:
            messagebox.showinfo("Thông báo", f"Không tìm thấy kết quả nào cho từ khóa '{keyword}'.")
            return

        for item in data:
            table.insert('', 'end', values=(
                f"P{item[0]}", item[1], item[2], item[3], item[4], item[5], f"PR{item[6]}", f"KH{item[7]}"
            ))

        # Clear search entry after displaying results
        e.delete(0, 'end')

    add = tb.Button(funcbar, bootstyle="success-outline", text="Thêm", width=14, command=themPet)
    add.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    sua = tb.Button(funcbar, bootstyle="success-outline", text="Sửa", width=14, command=suaPet)
    sua.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    xoa = tb.Button(funcbar, bootstyle="danger-outline", text="Trả phòng", width=14, command=traPet)
    xoa.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    e = tb.Entry(funcbar, bootstyle="secondary", textvariable="Tìm kiếm")
    e.grid(row=0, column=6, padx=5, pady=10, sticky="we")
    tim = tb.Button(funcbar, bootstyle="success-outline", text="Tìm kiếm", width=14, command=timPet)
    tim.grid(row=0, column=7, padx=5, pady=10, sticky="e")
