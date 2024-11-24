def clicked(indicator, buttons):
    """
    Đổi màu nút được chọn và đặt các nút khác về trạng thái mặc định.

    Args:
        indicator: Nút được nhấn.
        buttons: Danh sách tất cả các nút cần điều chỉnh.
    """
    for button in buttons:
        button.configure(foreground="#2b2b2b")  # Màu mặc định
    indicator.configure(foreground="white")  # Màu của nút được chọn
