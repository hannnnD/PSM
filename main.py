import tkinter as tk
import ttkbootstrap as tb

from m_dich_vu import show_dichVu
from m_hoa_don import show_hoaDon
from m_khach_hang import show_khachHang
from m_nhan_vien import show_nhanVien
from m_phong_thu import show_thuCungRoom
from m_thong_ke import show_thongKe
from m_thu_cung import show_thuCung


def main(user_role, emp_id):
    # Tạo cửa sổ chính
    window = tb.Window(title="Quản lý dịch vụ thú cưng", themename="minty", minsize=(1280, 800))
    window.columnconfigure(0, weight=1)
    window.columnconfigure((1, 2, 3, 4, 5), weight=15)
    window.rowconfigure(0, weight=1)

    # Tạo menu frame
    menu_frame = tb.Frame(window, width=40, bootstyle="primary")
    menu_frame.grid(row=0, column=0, sticky="wnse")
    menu_frame.columnconfigure(0, weight=1)
    menu_frame.columnconfigure(1, weight=10)
    menu_frame.rowconfigure((1, 2, 3, 4, 5, 6, 7), weight=1)
    menu_frame.rowconfigure(0, weight=2)
    menu_frame.rowconfigure(7, weight=3)

    # Hàm tiện ích để tạo nút
    def create_button(frame, image_path, text, command, row, column):
        icon = tk.PhotoImage(file=image_path)
        button = tk.Button(
            frame,
            image=icon,
            text=text,
            compound=tk.LEFT,
            padx=20,
            pady=20,
            width=130,
            height=30,
            anchor=tk.W,
            command=command
        )
        button.image = icon  # Giữ tham chiếu tới hình ảnh
        button.grid(row=row, column=column, padx=10, pady=10)
        return button

    # Danh sách các nút
    buttons = []
    buttons.append(create_button(menu_frame, "img/stats_light.png", "Thống kê",
                                 lambda: show_thongKe(window, user_role, buttons, buttons[0]), 1, 0))
    buttons.append(create_button(menu_frame, "img/customer_light.png", "Khách hàng",
                                 lambda: show_khachHang(window, user_role, buttons, buttons[1]), 2, 0))
    buttons.append(create_button(menu_frame, "img/animal-shelter.png", "Phòng thú",
                                 lambda: show_thuCungRoom(window, user_role, buttons, buttons[2]), 3, 0))
    buttons.append(create_button(menu_frame, "img/pet_light.png", "Thú",
                                 lambda: show_thuCung(window, user_role, buttons, buttons[3]), 4, 0))
    buttons.append(create_button(menu_frame, "img/supply-chain_light.png", "Dịch vụ",
                                 lambda: show_dichVu(window, user_role, buttons, buttons[4]), 5, 0))
    buttons.append(create_button(menu_frame, "img/recipt_light.png", "Hóa đơn",
                                 lambda: show_hoaDon(window, user_role, buttons, buttons[5]), 6, 0))
    buttons.append(create_button(menu_frame, "img/work_light.png", "Nhân viên",
                                 lambda: show_nhanVien(window, user_role, buttons, buttons[6]), 7, 0))


    # Chạy giao diện chính
    window.mainloop()

if __name__ == "__main__":
    main(user_role='admin', emp_id='1')