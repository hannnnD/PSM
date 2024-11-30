import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from DB import cursor, db
from utils import clicked
from datetime import datetime, timedelta, date


def show_nhanVien(window, user_role, buttons, nhanVien_btn):
    if user_role not in ["admin", "cashier"]:
        messagebox.showerror("Access Denied", "Bạn không có quyền truy cập vào tính năng này.")
        return

    clicked(nhanVien_btn, buttons)
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


    nhanVien_frame = tb.Labelframe(window, bootstyle="secondary", text="Quản lý nhân viên")
    nhanVien_frame.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")
    nhanVien_frame.columnconfigure(0, weight=1)
    nhanVien_frame.rowconfigure(0, weight=1)
    nhanVien_frame.rowconfigure((1, 2, 3, 4, 5, 6), weight=15)

    header_frame = tb.Frame(nhanVien_frame, height=60)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="new")

    content_frame = tb.Frame(nhanVien_frame)
    content_frame.grid(row=0, column=0, columnspan=2, rowspan=7, sticky="news")
    content_frame.columnconfigure((0, 1), weight=50)
    content_frame.columnconfigure(3, weight=1)
    content_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

    tree_scroll = tb.Scrollbar(content_frame, orient="vertical", bootstyle="primary-round")
    tree_scroll.grid(row=0, rowspan=6, column=3, sticky="wnes", padx=5, pady=30)

    columns = (
        "eID", "eName", "eDOB", "eGender", "eNumber", "eAddress", "eStartDate", "eSalary", "eWorkShift", "eStatus",
        "eNotes", "eRole")
    # Áp dụng kiểu tùy chỉnh cho Treeview
    table = tb.Treeview(content_frame, columns=columns, show='headings', yscrollcommand=tree_scroll.set,
                        style="Custom.Treeview")


    tree_scroll.config(command=table.yview)

    table.heading("eID", text="ID")
    table.heading("eName", text="Họ tên")
    table.heading("eDOB", text="Ngày sinh")
    table.heading("eGender", text="Giới tính")
    table.heading("eNumber", text="Liên hệ")
    table.heading("eAddress", text="Địa chỉ")
    table.heading("eStartDate", text="Ngày bắt đầu")
    table.heading("eSalary", text="Lương")
    table.heading("eWorkShift", text="Ca làm việc")
    table.heading("eStatus", text="Trạng thái")
    table.heading("eNotes", text="Ghi chú")
    table.heading("eRole", text="Vị trí")

    table.column("eID", width=30, anchor="center")
    table.column("eName", width=150, anchor="center")
    table.column("eDOB", width=80, anchor="center")
    table.column("eGender", width=70, anchor="center")
    table.column("eNumber", width=70, anchor="center")
    table.column("eAddress", width=70, anchor="center")
    table.column("eStartDate", width=50, anchor="center")
    table.column("eSalary", width=50, anchor="center")
    table.column("eWorkShift", width=70, anchor="center")
    table.column("eStatus", width=50, anchor="center")
    table.column("eNotes", width=70, anchor="center")
    table.column("eRole", width=50, anchor="center")

    table.grid(row=0, column=0, padx=10, pady=10, rowspan=6, columnspan=2, sticky="news")

    funcbar = tb.Frame(content_frame, height=60)
    funcbar.grid(row=6, column=0, columnspan=3, sticky="news")
    funcbar.columnconfigure((0, 1, 2, 3, 5), weight=1)
    funcbar.columnconfigure(4, weight=30)

    def fetch_and_insert_data():
        cursor.execute(
            "SELECT EmpID, EmpName, EmpDOB, EmpGender, EmpNumber, EmpAddress, EmpStartDate, EmpSalary, EmpWorkShift, EmpStatus, EmpNotes, EmpRole FROM employeetbl")
        for item in table.get_children():
            table.delete(item)
        data = cursor.fetchall()
        def format_vnd(amount):
            return f"{amount:,.0f}".replace(',', '.') + " VND"

        table.tag_configure('evenrow', background='#f2f2f2')
        table.tag_configure('oddrow', background='#ffffff')
        for i, item in enumerate(data):
            formatted_total = format_vnd(item[7])
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            table.insert('', tb.END, values=(
                f"NV{item[0]}", item[1], item[2], item[3], item[4], item[5], item[6], formatted_total, item[8], item[9],
                item[10], item[11]), tags=(tag,))

    fetch_and_insert_data()

    def themNV():
        addwindow = tb.Toplevel(title="Thêm nhân viên", minsize=(380, 600))
        lf = tb.Labelframe(addwindow, bootstyle="secondary", text="")
        lf.pack(fill="both", padx=5, pady=5, expand=True, anchor="w")
        lf.columnconfigure((0, 1), weight=1)
        lf.columnconfigure(2, weight=30)
        lf.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14), weight=1)

        id_lb = tb.Label(lf, bootstyle="secondary", text="ID")
        id_lb.grid(row=0, column=0, padx=10, pady=5, sticky="new")
        id_entry = tb.Entry(lf, width=16)
        id_entry.grid(row=0, column=2, padx=10, pady=5, sticky="new")
        cursor.execute("Select MAX(EmpID) FROM employeetbl")
        result = cursor.fetchone()
        eID = result[0] + 1 if result and result[0] is not None else 1
        id_entry.insert(0, eID)

        name_lb = tb.Label(lf, bootstyle="secondary", text="Họ tên")
        name_lb.grid(row=1, column=0, padx=10, pady=5, sticky="new")
        name_entry = tb.Entry(lf, width=16)
        name_entry.grid(row=1, column=2, padx=10, pady=5, sticky="new")

        dob_lb = tb.Label(lf, bootstyle="secondary", text="Ngày sinh")
        dob_lb.grid(row=2, column=0, padx=10, pady=5, sticky="new")
        dob_entry = tb.DateEntry(lf, width=16)
        dob_entry.grid(row=2, column=2, padx=10, pady=5, sticky="new")

        gender_lb = tb.Label(lf, bootstyle="secondary", text="Giới tính")
        gender_lb.grid(row=3, column=0, padx=10, pady=5, sticky="new")
        gender_entry = tb.Entry(lf, width=16)
        gender_entry.grid(row=3, column=2, padx=10, pady=5, sticky="new")

        number_lb = tb.Label(lf, bootstyle="secondary", text="Số điện thoại")
        number_lb.grid(row=4, column=0, padx=10, pady=5, sticky="new")
        number_entry = tb.Entry(lf, width=16)
        number_entry.grid(row=4, column=2, padx=10, pady=5, sticky="new")

        address_lb = tb.Label(lf, bootstyle="secondary", text="Địa chỉ")
        address_lb.grid(row=5, column=0, padx=10, pady=5, sticky="new")
        address_entry = tb.Entry(lf, width=16)
        address_entry.grid(row=5, column=2, padx=10, pady=5, sticky="new")

        startdate_lb = tb.Label(lf, bootstyle="secondary", text="Ngày bắt đầu")
        startdate_lb.grid(row=6, column=0, padx=10, pady=5, sticky="new")
        startdate_entry = tb.DateEntry(lf, width=16)
        startdate_entry.grid(row=6, column=2, padx=10, pady=5, sticky="new")

        salary_lb = tb.Label(lf, bootstyle="secondary", text="Lương")
        salary_lb.grid(row=7, column=0, padx=10, pady=5, sticky="new")
        salary_entry = tb.Entry(lf, width=16)
        salary_entry.grid(row=7, column=2, padx=10, pady=5, sticky="new")

        workshift_lb = tb.Label(lf, bootstyle="secondary", text="Ca làm việc")
        workshift_lb.grid(row=8, column=0, padx=10, pady=5, sticky="new")
        workshift_entry = tb.Entry(lf, width=16)
        workshift_entry.grid(row=8, column=2, padx=10, pady=5, sticky="new")

        status_lb = tb.Label(lf, bootstyle="secondary", text="Trạng thái")
        status_lb.grid(row=9, column=0, padx=10, pady=5, sticky="new")
        status_entry = tb.Entry(lf, width=16)
        status_entry.grid(row=9, column=2, padx=10, pady=5, sticky="new")

        notes_lb = tb.Label(lf, bootstyle="secondary", text="Ghi chú")
        notes_lb.grid(row=10, column=0, padx=10, pady=5, sticky="new")
        notes_entry = tb.Entry(lf, width=16)
        notes_entry.grid(row=10, column=2, padx=10, pady=5, sticky="new")

        emprole_lb = tb.Label(lf, bootstyle="secondary", text="Vị trí (Nhân viên)")
        emprole_lb.grid(row=11, column=0, padx=10, pady=5, sticky="new")
        emprole_entry = tb.Entry(lf, width=16)
        emprole_entry.grid(row=11, column=2, padx=10, pady=5, sticky="new")

        userrole_lb = tb.Label(lf, bootstyle="secondary", text="Vị trí (Người dùng)")
        userrole_lb.grid(row=12, column=0, padx=10, pady=5, sticky="new")
        userrole_entry = tb.Entry(lf, width=16)
        userrole_entry.grid(row=12, column=2, padx=10, pady=5, sticky="new")

        username_lb = tb.Label(lf, bootstyle="secondary", text="Tên người dùng")
        username_lb.grid(row=13, column=0, padx=10, pady=5, sticky="new")
        username_entry = tb.Entry(lf, width=16)
        username_entry.grid(row=13, column=2, padx=10, pady=5, sticky="new")

        password_lb = tb.Label(lf, bootstyle="secondary", text="Mật khẩu")
        password_lb.grid(row=14, column=0, padx=10, pady=5, sticky="new")
        password_entry = tb.Entry(lf, width=16, show='*')
        password_entry.grid(row=14, column=2, padx=10, pady=5, sticky="new")

        def save_data():
            eID = id_entry.get()
            name = name_entry.get()
            dob = dob_entry.entry.get()
            gender = gender_entry.get()
            number = number_entry.get()
            address = address_entry.get()
            startdate = startdate_entry.entry.get()
            salary = salary_entry.get()
            workshift = workshift_entry.get()
            status = status_entry.get()
            notes = notes_entry.get()
            emprole = emprole_entry.get()
            userrole = userrole_entry.get()
            username = username_entry.get()
            password = password_entry.get()

            if eID and name and username and password:
                cursor.execute(
                    "INSERT INTO employeetbl (EmpID, EmpName, EmpDOB, EmpGender, EmpNumber, EmpAddress, EmpStartDate, EmpSalary, EmpWorkShift, EmpStatus, EmpNotes, EmpRole) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (eID, name, dob, gender, number, address, startdate, salary, workshift, status, notes, emprole))
                cursor.execute("INSERT INTO usertbl (EmpID, username, password, role) VALUES (%s, %s, %s, %s)",
                               (eID, username, password, userrole))
                db.commit()
                fetch_and_insert_data()
                addwindow.destroy()
            else:
                messagebox.showerror("Invalid Data", "Hãy nhập đầy đủ thông tin")

        save_btn = tb.Button(lf, text="Lưu", command=save_data)
        save_btn.grid(row=15, column=0, columnspan=3, pady=10)

    add_btn = tb.Button(funcbar, text="Thêm", command=themNV, bootstyle="success-outline")
    add_btn.grid(row=0, column=0, padx=10, pady=10)

    def suaNV():
        selected_item = table.focus()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên để sửa.")
            return

        ID = table.item(selected_item, 'values')[0].strip('NV')

        cursor.execute("SELECT * FROM employeetbl WHERE EmpID=%s", (ID,))
        item_data = cursor.fetchone()

        editwindow = tb.Toplevel(title="Sửa thông tin nhân viên", minsize=(380, 600))
        lf = tb.Labelframe(editwindow, bootstyle="secondary", text="")
        lf.pack(fill="both", padx=5, pady=5, expand=True, anchor="w")
        lf.columnconfigure((0, 1), weight=1)
        lf.columnconfigure(2, weight=30)
        lf.rowconfigure(list(range(15)), weight=1)

        id_lb = tb.Label(lf, bootstyle="secondary", text="ID")
        id_lb.grid(row=0, column=0, padx=10, pady=5, sticky="new")
        id_entry = tb.Entry(lf, width=16)
        id_entry.grid(row=0, column=2, padx=10, pady=5, sticky="new")

        name_lb = tb.Label(lf, bootstyle="secondary", text="Họ tên")
        name_lb.grid(row=1, column=0, padx=10, pady=5, sticky="new")
        name_entry = tb.Entry(lf, width=16)
        name_entry.grid(row=1, column=2, padx=10, pady=5, sticky="new")

        dob_lb = tb.Label(lf, bootstyle="secondary", text="Ngày sinh")
        dob_lb.grid(row=2, column=0, padx=10, pady=5, sticky="new")
        dob_entry = tb.Entry(lf, width=16)
        dob_entry.grid(row=2, column=2, padx=10, pady=5, sticky="new")

        gender_lb = tb.Label(lf, bootstyle="secondary", text="Giới tính")
        gender_lb.grid(row=3, column=0, padx=10, pady=5, sticky="new")
        gender_entry = tb.Entry(lf, width=16)
        gender_entry.grid(row=3, column=2, padx=10, pady=5, sticky="new")

        number_lb = tb.Label(lf, bootstyle="secondary", text="Số điện thoại")
        number_lb.grid(row=4, column=0, padx=10, pady=5, sticky="new")
        number_entry = tb.Entry(lf, width=16)
        number_entry.grid(row=4, column=2, padx=10, pady=5, sticky="new")

        address_lb = tb.Label(lf, bootstyle="secondary", text="Địa chỉ")
        address_lb.grid(row=5, column=0, padx=10, pady=5, sticky="new")
        address_entry = tb.Entry(lf, width=16)
        address_entry.grid(row=5, column=2, padx=10, pady=5, sticky="new")

        startdate_lb = tb.Label(lf, bootstyle="secondary", text="Ngày bắt đầu")
        startdate_lb.grid(row=6, column=0, padx=10, pady=5, sticky="new")
        startdate_entry = tb.Entry(lf, width=16)
        startdate_entry.grid(row=6, column=2, padx=10, pady=5, sticky="new")

        salary_lb = tb.Label(lf, bootstyle="secondary", text="Lương")
        salary_lb.grid(row=7, column=0, padx=10, pady=5, sticky="new")
        salary_entry = tb.Entry(lf, width=16)
        salary_entry.grid(row=7, column=2, padx=10, pady=5, sticky="new")

        workshift_lb = tb.Label(lf, bootstyle="secondary", text="Ca làm việc")
        workshift_lb.grid(row=8, column=0, padx=10, pady=5, sticky="new")
        workshift_entry = tb.Entry(lf, width=16)
        workshift_entry.grid(row=8, column=2, padx=10, pady=5, sticky="new")

        status_lb = tb.Label(lf, bootstyle="secondary", text="Trạng thái")
        status_lb.grid(row=9, column=0, padx=10, pady=5, sticky="new")
        status_entry = tb.Entry(lf, width=16)
        status_entry.grid(row=9, column=2, padx=10, pady=5, sticky="new")

        notes_lb = tb.Label(lf, bootstyle="secondary", text="Ghi chú")
        notes_lb.grid(row=10, column=0, padx=10, pady=5, sticky="new")
        notes_entry = tb.Entry(lf, width=16)
        notes_entry.grid(row=10, column=2, padx=10, pady=5, sticky="new")

        role_lb = tb.Label(lf, bootstyle="secondary", text="Vị trí (Nhân viên)")
        role_lb.grid(row=11, column=0, padx=10, pady=5, sticky="new")
        role_entry = tb.Entry(lf, width=16)
        role_entry.grid(row=11, column=2, padx=10, pady=5, sticky="new")

        userrole_lb = tb.Label(lf, bootstyle="secondary", text="Vị trí (Người dùng)")
        userrole_lb.grid(row=12, column=0, padx=10, pady=5, sticky="new")
        userrole_entry = tb.Entry(lf, width=16)
        userrole_entry.grid(row=12, column=2, padx=10, pady=5, sticky="new")

        username_lb = tb.Label(lf, bootstyle="secondary", text="Tên người dùng")
        username_lb.grid(row=13, column=0, padx=10, pady=5, sticky="new")
        username_entry = tb.Entry(lf, width=16)
        username_entry.grid(row=13, column=2, padx=10, pady=5, sticky="new")

        password_lb = tb.Label(lf, bootstyle="secondary", text="Mật khẩu")
        password_lb.grid(row=14, column=0, padx=10, pady=5, sticky="new")
        password_entry = tb.Entry(lf, width=16, show='*')
        password_entry.grid(row=14, column=2, padx=10, pady=5, sticky="new")

        id_entry.insert(0, item_data[0])
        name_entry.insert(0, item_data[1])
        dob_entry.insert(0, (item_data[2]))
        gender_entry.insert(0, item_data[3])
        number_entry.insert(0, item_data[4])
        address_entry.insert(0, item_data[5])
        startdate_entry.insert(0, item_data[6])
        salary_entry.insert(0, item_data[7])
        workshift_entry.insert(0, item_data[8])
        status_entry.insert(0, item_data[9])
        notes_entry.insert(0, item_data[10])
        role_entry.insert(0, item_data[11])

        cursor.execute("SELECT username, password, role FROM usertbl WHERE EmpID=%s", (ID,))
        user_data = cursor.fetchone()
        if user_data:
            username_entry.insert(0, user_data[0])
            password_entry.insert(0, user_data[1])
            userrole_entry.insert(0, user_data[2])

        def save_changes():
            id = id_entry.get()
            name = name_entry.get()
            dob = dob_entry.get()
            gender = gender_entry.get()
            number = number_entry.get()
            address = address_entry.get()
            startdate = startdate_entry.get()
            salary = salary_entry.get()
            workshift = workshift_entry.get()
            status = status_entry.get()
            notes = notes_entry.get()
            role = role_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            userrole = userrole_entry.get()

            if not id or not name or not dob or not gender or not number or not address or not startdate or not salary or not workshift or not status or not notes or not role or not username or not password or not userrole:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin nhân viên.")
                return

            try:
                cursor.execute(
                    "UPDATE employeetbl SET EmpName=%s, EmpDOB=%s, EmpGender=%s, EmpNumber=%s, EmpAddress=%s, EmpStartDate=%s, EmpSalary=%s, EmpWorkShift=%s, EmpStatus=%s, EmpNotes=%s, EmpRole=%s WHERE EmpID=%s",
                    (name, dob, gender, number, address, startdate, salary, workshift, status, notes, role, ID)
                )
                cursor.execute(
                    "UPDATE usertbl SET username=%s, password=%s, role=%s WHERE EmpID=%s",
                    (username, password, userrole, ID)
                )
                db.commit()

                fetch_and_insert_data()

                messagebox.showinfo("Thành công", "Thông tin nhân viên đã được cập nhật thành công!")
                editwindow.destroy()

            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ.")

        save_btn = tb.Button(lf, bootstyle="success", text="Lưu", command=save_changes)
        save_btn.grid(row=15, column=0, columnspan=3, pady=10)

    edit_btn = tb.Button(funcbar, text="Sửa", command=suaNV, bootstyle="warning-outline")
    edit_btn.grid(row=0, column=1, padx=10, pady=10)

    def xoaNV():
        selected_item = table.focus()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên để xóa.")
            return

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa nhân viên này?")
        if confirm:
            ID = table.item(selected_item, 'values')[0].strip('NV')

            try:
                cursor.execute("DELETE FROM usertbl WHERE EmpID=%s", (ID,))
                cursor.execute("DELETE FROM employeetbl WHERE EmpID=%s", (ID,))
                db.commit()
                fetch_and_insert_data()
                messagebox.showinfo("Thành công", "Đã xóa nhân viên thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi xóa nhân viên: {str(e)}")

    delete_btn = tb.Button(funcbar, text="Xóa", command=xoaNV, bootstyle="danger-outline")
    delete_btn.grid(row=0, column=2, padx=10, pady=10)