import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk  # Để hiển thị logo
import mysql.connector
import customtkinter
from main import main
from DB import cursor, db

# Thiết lập giao diện
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Cửa sổ chính
window = customtkinter.CTk()
window.geometry("600x500")
window.title("Quản lý dịch vụ thú cưng")

# Frame chính
frame = customtkinter.CTkFrame(window, width=350, height=450, corner_radius=20)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Thêm logo
logo_image = Image.open("img/pets.png")
logo_image = logo_image.resize((80, 80), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = customtkinter.CTkLabel(frame, image=logo_photo, text="")
logo_label.place(x=135, y=20)

# Tiêu đề
label_title = customtkinter.CTkLabel(frame, text="Đăng nhập", font=("Monsterat", 24, "bold"))
label_title.place(x=110, y=120)

# Đóng cửa sổ
def destroy_window():
    window.destroy()

# Kiểm tra thông tin đăng nhập
def check_credentials():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        error_label.configure(text="Vui lòng nhập tên đăng nhập và mật khẩu.")
        return

    try:
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
            error_label.configure(text="Tên đăng nhập hoặc mật khẩu không đúng.")
    except mysql.connector.Error as err:
        error_label.configure(text=f"Lỗi cơ sở dữ liệu: {err}")
    except Exception as ex:
        error_label.configure(text=f"Lỗi không mong muốn: {ex}")
        print(ex)

# Các trường nhập liệu
username_entry = customtkinter.CTkEntry(frame, width=250, placeholder_text="Tên đăng nhập")
password_entry = customtkinter.CTkEntry(frame, width=250, placeholder_text="Mật khẩu", show="*")

username_entry.place(x=50, y=180)
password_entry.place(x=50, y=230)


# Nút đăng nhập
login_button = customtkinter.CTkButton(frame, width=250, text="Đăng nhập", corner_radius=6, command=check_credentials)
login_button.place(x=50, y=280)

# Nhãn hiển thị lỗi
error_label = customtkinter.CTkLabel(frame, text="", text_color="red", font=("Monsterat", 12))
error_label.place(x=50, y=320)

# Chạy ứng dụng
window.protocol("WM_DELETE_WINDOW", destroy_window)
window.mainloop()
