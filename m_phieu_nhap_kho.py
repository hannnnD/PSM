from datetime import datetime
from tkinter import messagebox
import ttkbootstrap as tb
from DB import cursor, db
from utils import clicked


def show_phieuNhap(window, user_role, buttons, phieuNhap_btn):
    if user_role not in ['admin', 'cashier']:
        messagebox.showerror("Access Denied", "Bạn không có quyền truy cập vào tính năng này")
        return

    clicked(phieuNhap_btn, buttons)

    # Style cho bảng
    style = tb.Style()
    style.configure("Custom.Treeview",
                    borderwidth=1,
                    relief="solid",
                    rowheight=25,
                    background="#fdfdfd",
                    foreground="#000")
    style.configure("Custom.Treeview.Heading",
                    background="#76EEC6",
                    foreground="#000",
                    borderwidth=1,
                    relief="solid")

    # Frame chính
    phieuNhap_frame = tb.Labelframe(window, bootstyle="secondary", text="Quản lý Phiếu Nhập Kho")
    phieuNhap_frame.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")
    phieuNhap_frame.columnconfigure(0, weight=1)
    phieuNhap_frame.rowconfigure(0, weight=1)
    phieuNhap_frame.rowconfigure((1, 2, 3, 4, 5, 6), weight=15)

    # Header frame
    header_frame = tb.Frame(phieuNhap_frame, height=60)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="new")

    # Content frame
    content_frame = tb.Frame(phieuNhap_frame)
    content_frame.grid(row=0, column=0, columnspan=2, rowspan=7, sticky="news")
    content_frame.columnconfigure((0, 1), weight=50)
    content_frame.columnconfigure(3, weight=1)
    content_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

    # Scrollbar cho bảng
    tree_scroll = tb.Scrollbar(content_frame, orient="vertical", bootstyle="primary-round")
    tree_scroll.grid(row=0, rowspan=6, column=3, sticky="wnes", padx=5, pady=30)

    # Định nghĩa các cột cho bảng "stockin"
    columns = (
    "StockinID", "Nhà Cung Cấp", "Dịch Vụ", "Số Lượng", "Giá", "Giá Chiết Khấu", "Tổng Tiền", "Ngày Nhập Kho",
    "Ghi Chú")
    table = tb.Treeview(content_frame, columns=columns, show='headings', yscrollcommand=tree_scroll.set,
                        style="Custom.Treeview")
    tree_scroll.config(command=table.yview)

    # Đặt tiêu đề cột
    table.heading("StockinID", text="Stockin ID")
    table.heading("Nhà Cung Cấp", text="Nhà Cung Cấp")
    table.heading("Dịch Vụ", text="Dịch Vụ")
    table.heading("Số Lượng", text="Số Lượng")
    table.heading("Giá", text="Giá")
    table.heading("Giá Chiết Khấu", text="Giá Chiết Khấu")
    table.heading("Tổng Tiền", text="Tổng Tiền")
    table.heading("Ngày Nhập Kho", text="Ngày Nhập Kho")
    table.heading("Ghi Chú", text="Ghi Chú")

    # Đặt chiều rộng cột
    table.column("StockinID", width=30, anchor="center")
    table.column("Nhà Cung Cấp", width=150, anchor="center")
    table.column("Dịch Vụ", width=150, anchor="center")
    table.column("Số Lượng", width=100, anchor="center")
    table.column("Giá", width=100, anchor="center")
    table.column("Giá Chiết Khấu", width=120, anchor="center")
    table.column("Tổng Tiền", width=120, anchor="center")
    table.column("Ngày Nhập Kho", width=120, anchor="center")
    table.column("Ghi Chú", width=150, anchor="center")

    table.grid(row=0, column=0, padx=10, pady=10, rowspan=6, columnspan=2, sticky="news")

    # Thanh công cụ chức năng
    funcbar = tb.Frame(content_frame, height=60)
    funcbar.grid(row=6, column=0, columnspan=3, sticky="news")
    funcbar.columnconfigure((0, 1, 2, 3, 5), weight=1)
    funcbar.columnconfigure(4, weight=30)

    def fetch_and_insert_data():
        # Câu lệnh SQL lấy dữ liệu từ bảng "stockin"
        query = """
        SELECT 
            StockinTbl.StockinID, 
            SupplierTbl.SupplierName, 
            ServiceTbl.SName, 
            StockinTbl.Quantity, 
            StockinTbl.Price, 
            StockinTbl.DiscountedPrice, 
            StockinTbl.TotalAmt, 
            StockinTbl.StockinDate, 
            StockinTbl.Notes 
        FROM StockinTbl 
        JOIN SupplierTbl ON StockinTbl.SupplierID = SupplierTbl.SupplierID 
        JOIN ServiceTbl ON StockinTbl.ServiceID = ServiceTbl.ServiceID
        """
        cursor.execute(query)

        # Xóa dữ liệu cũ trong bảng
        for item in table.get_children():
            table.delete(item)

        # Lấy dữ liệu từ cơ sở dữ liệu
        data = cursor.fetchall()

        def format_vnd(amount):
            if amount is None:
                return "0 VND"  # Hoặc giá trị mặc định bạn muốn hiển thị
            return f"{amount:,.0f}".replace(',', '.') + " VND"

        # Định dạng hiển thị
        table.tag_configure('evenrow', background='#f2f2f2')
        table.tag_configure('oddrow', background='#ffffff')
        for i, item in enumerate(data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            formatted_item = (
                item[0],
                item[1],
                item[2],
                item[3],
                format_vnd(item[4]),
                format_vnd(item[5]),
                format_vnd(item[6]),
                item[7],
                item[8]
            )
            table.insert('', tb.END, values=formatted_item, tags=(tag,))

    fetch_and_insert_data()

    def themPhieuNhap():
        addwindow = tb.Toplevel(title="Thêm Phiếu Nhập", minsize=(400, 600))
        lf = tb.Labelframe(addwindow, bootstyle="secondary", text="Thông Tin Phiếu Nhập")
        lf.pack(fill="both", padx=5, pady=5, expand=True, anchor="w")
        lf.columnconfigure((0, 1), weight=1)
        lf.columnconfigure(2, weight=30)
        lf.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        # Stockin ID
        id_lb = tb.Label(lf, bootstyle="secondary", text="Stockin ID")
        id_lb.grid(row=0, column=0, padx=10, pady=5, sticky="new")
        id_entry = tb.Entry(lf, width=16)
        id_entry.grid(row=0, column=2, padx=10, pady=5, sticky="new")
        cursor.execute("SELECT MAX(StockinID) FROM StockinTbl")
        result = cursor.fetchone()
        sID = result[0] + 1 if result and result[0] is not None else 1
        id_entry.insert(0, sID)

        # Supplier Name (Dropdown)
        supplier_lb = tb.Label(lf, bootstyle="secondary", text="Nhà Cung Cấp")
        supplier_lb.grid(row=1, column=0, padx=10, pady=5, sticky="new")
        supplier_cb = tb.Combobox(lf, width=16, state="readonly")
        supplier_cb.grid(row=1, column=2, padx=10, pady=5, sticky="new")
        cursor.execute("SELECT SupplierID, SupplierName FROM SupplierTbl")
        suppliers = cursor.fetchall()
        supplier_dict = {supplier[1]: supplier[0] for supplier in suppliers}
        supplier_cb['values'] = list(supplier_dict.keys())

        # Service Name (Dropdown)
        service_lb = tb.Label(lf, bootstyle="secondary", text="Dịch Vụ")
        service_lb.grid(row=2, column=0, padx=10, pady=5, sticky="new")
        service_cb = tb.Combobox(lf, width=16, state="readonly")
        service_cb.grid(row=2, column=2, padx=10, pady=5, sticky="new")
        cursor.execute("SELECT ServiceID, SName FROM ServiceTbl")
        services = cursor.fetchall()
        service_dict = {service[1]: service[0] for service in services}
        service_cb['values'] = list(service_dict.keys())

        # Quantity
        quantity_lb = tb.Label(lf, bootstyle="secondary", text="Số Lượng")
        quantity_lb.grid(row=3, column=0, padx=10, pady=5, sticky="new")
        quantity_entry = tb.Entry(lf, width=16)
        quantity_entry.grid(row=3, column=2, padx=10, pady=5, sticky="new")

        # Price
        price_lb = tb.Label(lf, bootstyle="secondary", text="Giá")
        price_lb.grid(row=4, column=0, padx=10, pady=5, sticky="new")
        price_entry = tb.Entry(lf, width=16)
        price_entry.grid(row=4, column=2, padx=10, pady=5, sticky="new")

        # Discounted Price
        discount_lb = tb.Label(lf, bootstyle="secondary", text="Giá Chiết Khấu")
        discount_lb.grid(row=5, column=0, padx=10, pady=5, sticky="new")
        discount_entry = tb.Entry(lf, width=16)
        discount_entry.grid(row=5, column=2, padx=10, pady=5, sticky="new")

        # Stockin Date
        date_lb = tb.Label(lf, bootstyle="secondary", text="Ngày Nhập Kho")
        date_lb.grid(row=6, column=0, padx=10, pady=5, sticky="new")
        date_entry = tb.Entry(lf, width=16)
        date_entry.grid(row=6, column=2, padx=10, pady=5, sticky="new")
        current_date = datetime.now().strftime("%Y-%m-%d")
        date_entry.insert(0, current_date)
        # Notes
        notes_lb = tb.Label(lf, bootstyle="secondary", text="Ghi Chú")
        notes_lb.grid(row=7, column=0, padx=10, pady=5, sticky="new")
        notes_entry = tb.Entry(lf, width=16)
        notes_entry.grid(row=7, column=2, padx=10, pady=5, sticky="new")

        def add_sql():
            stockin_id = id_entry.get()
            supplier_name = supplier_cb.get()
            service_name = service_cb.get()
            quantity = quantity_entry.get()
            price = price_entry.get()
            discounted_price = discount_entry.get()
            stockin_date = date_entry.get()
            notes = notes_entry.get()

            # Validate inputs
            if not stockin_id or not supplier_name or not service_name or not quantity or not price or not stockin_date:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
                return

            try:
                quantity = int(quantity)
                price = float(price)
                discounted_price = float(discounted_price) if discounted_price else 0
                totalamt = (quantity * price) - discounted_price

                supplier_id = supplier_dict[supplier_name]
                service_id = service_dict[service_name]

                # Update stockin table
                cursor.execute(
                    "INSERT INTO StockinTbl (StockinID, SupplierID, ServiceID, Quantity, Price, DiscountedPrice, TotalAmt, StockinDate, Notes) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (stockin_id, supplier_id, service_id, quantity, price, discounted_price, totalamt, stockin_date,
                     notes)
                )

                # Update quantity in ServiceTbl
                cursor.execute(
                    "UPDATE ServiceTbl SET SQuantity = SQuantity + %s WHERE ServiceID = %s",
                    (quantity, service_id)
                )

                db.commit()

                fetch_and_insert_data()

                messagebox.showinfo("Thành công", "Phiếu nhập đã được thêm thành công!")
                addwindow.destroy()

            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ!")
            except db.Error as e:
                messagebox.showerror("Lỗi", f"Không thể thêm phiếu nhập: {e}")

        them = tb.Button(addwindow, bootstyle="success", text="Thêm", command=add_sql)
        them.pack(side=tb.LEFT, fill="x", padx=10, pady=10, expand=True, anchor="w")

    def suaPhieuNhap():
        selected_item = table.focus()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn phiếu nhập để sửa.")
            return

        stockin_id = table.item(selected_item, 'values')[0]

        # Lấy dữ liệu hiện tại của phiếu nhập
        cursor.execute("SELECT * FROM StockinTbl WHERE StockinID=%s", (stockin_id,))
        stockin_data = cursor.fetchone()

        # Tạo cửa sổ sửa phiếu nhập
        editwindow = tb.Toplevel(title="Sửa Phiếu Nhập", minsize=(400, 600))
        lf = tb.Labelframe(editwindow, bootstyle="secondary", text="Sửa Phiếu Nhập")
        lf.pack(fill="both", padx=5, pady=5, expand=True, anchor="w")
        lf.columnconfigure((0, 1), weight=1)
        lf.columnconfigure(2, weight=30)
        lf.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        # Lấy danh sách nhà cung cấp và dịch vụ
        cursor.execute("SELECT SupplierID, SupplierName FROM SupplierTbl")
        supplier_data = cursor.fetchall()
        supplier_dict = {supplier[1]: supplier[0] for supplier in supplier_data}  # Ánh xạ tên -> ID
        supplier_names = [supplier[1] for supplier in supplier_data]

        cursor.execute("SELECT ServiceID, SName FROM ServiceTbl")
        service_data = cursor.fetchall()
        service_dict = {service[1]: service[0] for service in service_data}  # Ánh xạ tên -> ID
        service_names = [service[1] for service in service_data]

        # Các trường nhập liệu
        supplier_label = tb.Label(lf, bootstyle="secondary", text="Nhà Cung Cấp")
        supplier_label.grid(row=0, column=0, padx=10, pady=5, sticky="new")
        supplier_combobox = tb.Combobox(lf, values=supplier_names, state="readonly")
        supplier_combobox.grid(row=0, column=2, padx=10, pady=5, sticky="new")

        # Gán giá trị mặc định
        supplier_combobox.set(next((name for name, id_ in supplier_dict.items() if id_ == stockin_data[1]), ""))

        service_label = tb.Label(lf, bootstyle="secondary", text="Dịch Vụ")
        service_label.grid(row=1, column=0, padx=10, pady=5, sticky="new")
        service_combobox = tb.Combobox(lf, values=service_names, state="readonly")
        service_combobox.grid(row=1, column=2, padx=10, pady=5, sticky="new")

        # Gán giá trị mặc định
        service_combobox.set(next((name for name, id_ in service_dict.items() if id_ == stockin_data[2]), ""))

        fields = [
            ("Số Lượng", stockin_data[3]),
            ("Giá", stockin_data[4]),
            ("Giá Chiết Khấu", stockin_data[5]),
            ("Ngày Nhập Kho", stockin_data[7]),
            ("Ghi Chú", stockin_data[8]),
        ]
        entries = {}
        for i, (label_text, value) in enumerate(fields, start=2):
            label = tb.Label(lf, bootstyle="secondary", text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="new")
            entry = tb.Entry(lf, width=16)
            entry.grid(row=i, column=2, padx=10, pady=5, sticky="new")
            entry.insert(0, value)
            entries[label_text] = entry

        def update_sql():
            # Lấy dữ liệu từ các trường nhập
            new_supplier_name = supplier_combobox.get()
            new_service_name = service_combobox.get()
            new_quantity = int(entries["Số Lượng"].get())
            new_price = float(entries["Giá"].get())
            new_discounted_price = float(entries["Giá Chiết Khấu"].get() or 0)
            new_date = entries["Ngày Nhập Kho"].get()
            new_notes = entries["Ghi Chú"].get()

            # Kiểm tra nhà cung cấp và dịch vụ có hợp lệ không
            if new_supplier_name not in supplier_dict or new_service_name not in service_dict:
                messagebox.showerror("Lỗi", "Vui lòng chọn nhà cung cấp và dịch vụ hợp lệ.")
                return

            new_supplier_id = supplier_dict[new_supplier_name]
            new_service_id = service_dict[new_service_name]

            # Lấy dữ liệu hiện tại
            current_quantity = stockin_data[3]
            service_id = stockin_data[2]

            # Tính toán UCQuantity và UpdateSQuantity
            uc_quantity = new_quantity - current_quantity
            cursor.execute("SELECT SQuantity FROM ServiceTbl WHERE ServiceID=%s", (service_id,))
            current_squantity = cursor.fetchone()[0]
            update_squantity = current_squantity - uc_quantity

            # Cập nhật bảng StockinTbl và ServiceTbl
            try:
                total_amt = (new_quantity * new_price) - new_discounted_price

                # Cập nhật StockinTbl
                cursor.execute(
                    "UPDATE StockinTbl SET SupplierID=%s, ServiceID=%s, Quantity=%s, Price=%s, DiscountedPrice=%s, TotalAmt=%s, StockinDate=%s, Notes=%s WHERE StockinID=%s",
                    (
                    new_supplier_id, new_service_id, new_quantity, new_price, new_discounted_price, total_amt, new_date,
                    new_notes, stockin_id)
                )

                # Cập nhật SQuantity trong ServiceTbl
                cursor.execute(
                    "UPDATE ServiceTbl SET SQuantity=%s WHERE ServiceID=%s",
                    (update_squantity, service_id)
                )

                db.commit()

                fetch_and_insert_data()
                messagebox.showinfo("Thành công", "Phiếu nhập đã được sửa thành công!")
                editwindow.destroy()

            except db.Error as e:
                messagebox.showerror("Lỗi", f"Không thể sửa phiếu nhập: {e}")

        # Nút cập nhật
        btn_update = tb.Button(editwindow, bootstyle="success", text="Sửa", command=update_sql)
        btn_update.pack(side=tb.LEFT, fill="x", padx=10, pady=10, expand=True, anchor="w")

    def xoaPhieuNhap():
        selected_item = table.focus()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn phiếu nhập để xóa.")
            return

        stockin_id = table.item(selected_item, 'values')[0]

        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa phiếu nhập có ID {stockin_id} không?")
        if confirm:
            try:
                # Lấy số lượng và service_id từ phiếu nhập
                cursor.execute("SELECT ServiceID, Quantity FROM StockinTbl WHERE StockinID=%s", (stockin_id,))
                service_id, quantity = cursor.fetchone()

                # Cập nhật lại số lượng trong ServiceTbl
                cursor.execute("UPDATE ServiceTbl SET SQuantity = SQuantity - %s WHERE ServiceID = %s",
                               (quantity, service_id))

                # Xóa phiếu nhập
                cursor.execute("DELETE FROM StockinTbl WHERE StockinID=%s", (stockin_id,))
                db.commit()

                fetch_and_insert_data()
                messagebox.showinfo("Thành công", "Phiếu nhập đã được xóa!")
            except db.Error as e:
                messagebox.showerror("Lỗi", f"Không thể xóa phiếu nhập: {e}")

    def timkiemPhieuNhap():
        keyword = search_entry.get()
        query = """
        SELECT StockinID, SupplierID, ServiceID, Quantity, Price, DiscountedPrice, TotalAmt, StockinDate, Notes
        FROM StockinTbl 
        WHERE StockinID LIKE %s OR SupplierID LIKE %s OR ServiceID LIKE %s OR StockinDate LIKE %s
        """
        search_pattern = f'%{keyword}%'
        cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))

        # Xóa dữ liệu cũ trong bảng
        for item in table.get_children():
            table.delete(item)

        # Hiển thị dữ liệu mới
        data = cursor.fetchall()
        for row in data:
            table.insert('', tb.END, values=row)

    btn_them = tb.Button(funcbar, bootstyle="success-outline", text="Thêm", command=themPhieuNhap)
    btn_them.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    btn_sua = tb.Button(funcbar, bootstyle="success-outline", text="Sửa", command=suaPhieuNhap)
    btn_sua.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    btn_xoa = tb.Button(funcbar, bootstyle="danger-outline", text="Xóa", command=xoaPhieuNhap)
    btn_xoa.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    btn_refresh = tb.Button(funcbar, bootstyle="secondary-outline", text="Làm mới", command=fetch_and_insert_data)
    btn_refresh.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

    search_entry = tb.Entry(funcbar)
    search_entry.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

    btn_tim = tb.Button(funcbar, bootstyle="info-outline", text="Tìm", command=timkiemPhieuNhap)
    btn_tim.grid(row=0, column=5, padx=10, pady=10, sticky="ew")