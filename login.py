import tkinter
from tkinter import messagebox
import mysql.connector
from DB import cursor, db
import customtkinter
from main import main

# Thiết lập giao diện
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

window = customtkinter.CTk()
window.geometry("600x500")
window.title("Quản lý dịch vụ thú cưng")

frame = customtkinter.CTkFrame(window, width=350, height=400, corner_radius=20)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

label_title = customtkinter.CTkLabel(frame, text="Đăng nhập", font=("Monsterat", 28), bg_color="transparent")
label_title.place(x=60, y=50)


# Đóng cửa sổ
def destroy_window():
    try:
        cursor.close()
        db.close()
    except mysql.connector.Error:
        pass
    window.destroy()

# Kiểm tra thông tin đăng nhập
def check_credentials():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu.")
        return

    try:
        # Kiểm tra kết nối cơ sở dữ liệu
        if not db.is_connected():
            db.reconnect()

        query = "SELECT * FROM usertbl WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            user_role = result[3]
            emp_id = result[4]
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            destroy_window()
            main(user_role, emp_id)
        else:
            messagebox.showerror("Thất bại", "Tên đăng nhập hoặc mật khẩu không đúng.")
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {err}")
    except Exception as ex:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi không mong muốn: {ex}")

# Các trường nhập liệu
username_entry = customtkinter.CTkEntry(frame, width=230, placeholder_text="Tên đăng nhập")
password_entry = customtkinter.CTkEntry(frame, width=230, placeholder_text="Mật khẩu", show="*")

username_entry.place(x=60, y=150)
password_entry.place(x=60, y=200)

# Nút đăng nhập
login_button = customtkinter.CTkButton(frame, width=100, text="Đăng nhập", corner_radius=6, command=check_credentials)
login_button.place(x=130, y=310)

# Chạy ứng dụng
window.protocol("WM_DELETE_WINDOW", destroy_window)  # Đảm bảo đóng kết nối khi thoát
window.mainloop()
