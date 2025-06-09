import ctypes
import tkinter as tk
from tkinter import ttk, messagebox

import GIAODIEN_Window
import CHUCNANG_Method
import DANHSACH_DanhSachCacSach

# Chỉnh lại DPI hợp với độ phân giải hiện tại
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Hàm để khởi chạy cửa sổ đăng nhập
def mocuasodangnhap():
    global cuaSoDangNhap, usernameEntry, passwordEntry, roleVar
    cuaSoDangNhap = tk.Tk()
    cuaSoDangNhap.title("Đăng nhập")
    cuaSoDangNhap.geometry("560x320")
    cuaSoDangNhap.config(bg="lightblue")
    theme = ttk.Style(cuaSoDangNhap)
    theme.theme_use('clam')

    # Style cửa sổ đăng nhập
    dangNhapStyle = ttk.Style()
    dangNhapStyle.configure("frameDangNhap.TFrame",
                            background="lightblue",      # Nền xanh biển
                            foreground="#000000",       # Chữ trắng
                            font=("Segoe UI", 10, "bold"),  # In đậm
                            borderwidth=1)

    dangNhapStyle.configure("dangNhapButton.TButton",
                            background="#1976D2",      # Nền xanh biển
                            foreground="#FFFFFF",       # Chữ trắng
                            font=("Segoe UI", 10, "bold"),  # In đậm
                            borderwidth=1)

    # **Tạo Frame chứa các thành phần theo chiều ngang**
    frameMain = ttk.Frame(cuaSoDangNhap, padding=10, style="frameDangNhap.TFrame")
    frameMain.pack()

    # **Tên đăng nhập**
    ttk.Label(frameMain, text="Tên đăng nhập:", background="lightblue").grid(row=0, column=0, padx=5, sticky='w')
    usernameEntry = ttk.Entry(frameMain)
    usernameEntry.grid(row=0, column=1, padx=5)

    # **Mật khẩu**
    ttk.Label(frameMain, text="Mật khẩu:", background="lightblue").grid(row=1, column=0, padx=5, sticky='w')
    passwordEntry = ttk.Entry(frameMain, show="*")
    passwordEntry.grid(row=1, column=1, padx=5)

    # **Chọn quyền**
    ttk.Label(frameMain, text="Chọn quyền:", background="lightblue").grid(row=2, column=0, padx=5)
    roleVar = tk.StringVar()
    roleMenu = ttk.Combobox(frameMain, textvariable=roleVar, state="readonly", width=10)
    roleMenu["values"] = ("admin", "user")
    roleMenu.grid(row=2, column=1, padx=10)

    # **Nút Đăng nhập và Đăng ký**
    frameButtons = ttk.Frame(cuaSoDangNhap, padding=5, style="frameDangNhap.TFrame")
    frameButtons.pack()

    ttk.Button(frameButtons, text="Đăng nhập", command=lambda: dangNhap(cuaSoDangNhap), style="dangNhapButton.TButton").grid(row=0, column=0, padx=10)
    ttk.Button(frameButtons, text="Đăng ký", command=moCuaSoDangKy, style="dangNhapButton.TButton").grid(row=0, column=1, padx=10)
    
    cuaSoDangNhap.mainloop()


# Mở ứng dụng chính nếu đăng nhập thành công
def moGiaoDienChinh(role, dangnhap_window):
    dangnhap_window.destroy()  

    # Tạo window
    root = tk.Tk()
    
    # Hàm đăng xuất
    def dangXuat(event=None): 
        root.destroy() 
        mocuasodangnhap() 

   
    # Thông tin mặc định của giao diện chính 
    rootWidth = root.winfo_screenwidth()
    rootHeight= root.winfo_screenheight()
    
    theme = ttk.Style(root)
    theme.theme_use('clam')
    title = "Quản lý sách cá nhân"
    resolution = f"{rootWidth-100}x{rootHeight-260}+{int(rootWidth * 0.05)}+{int(rootHeight * 0.05)}"

    root.title(title)
    root.geometry(resolution)
    root.resizable(True, True)

    # Thanh cuộn
    container = ttk.Frame(root)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, background="lightblue")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Khung chính của phần mềm 
    # Style frame chính
    styleMainframe = ttk.Style()
    styleMainframe.configure("MainFrame.TFrame", background="lightblue")

    mainFrame = ttk.Frame(canvas, padding=60, borderwidth=5, style="MainFrame.TFrame")

    canvas_window = canvas.create_window((0, 0), window=mainFrame, anchor="nw")
    root.columnconfigure(0, weight=1)

    def on_mainFrame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    mainFrame.bind("<Configure>", on_mainFrame_configure)

    # (Không bắt buộc) Thêm scroll chuột
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def resize_canvas(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", resize_canvas)

    # Tiêu đề
    tieuDeLabel = tk.Label(
        mainFrame, 
        text="Kho Sách Cá Nhân", 
        font=("Segoe UI", 23, "bold"), 
        bg ="lightblue", 
        fg = "#003366")
    tieuDeLabel.pack(anchor='n', pady = (0,10))
    mainFrame.columnconfigure(0, weight=1)

    # Đăng xuất
    dangxuatLabel = tk.Label(
        root,
        text="Đăng Xuất",
        font=("Segoe UI", 15, "underline", "bold"), 
        fg="#003366",
        bg="lightblue", 
        cursor="hand2" 
    )
    dangxuatLabel.place(relx=1.0, rely=0.0, anchor='ne', x=-60, y=70) 
    dangxuatLabel.bind("<Button-1>", dangXuat)


    # Các frame con trong mainFrame
    # Style frame con
    frameConStyle = ttk.Style()
    frameConStyle.configure("frameCon.TFrame", background="#E3F2FD")

    # Khung tìm kiếm
    noiDungTimKiem = tk.StringVar()

    searchFrame = ttk.LabelFrame(mainFrame, text="Tìm kiếm", style="frameCon.TFrame")
    searchFrame.pack(fill="x", pady=30, ipady=10)

    ttk.Entry(searchFrame, textvariable=noiDungTimKiem).grid(row=0, column=0, padx=10)
    ttk.Button(searchFrame, text= "Tìm", command=lambda: CHUCNANG_Method.timSach(noiDungTimKiem, tree)).grid(row=0, column=1, padx=15, ipadx=13, ipady=6)
    ttk.Button(searchFrame, text="Tìm sách online", command=lambda: GIAODIEN_Window.timSachOnlineWindow(mainFrame, tree)).grid(row=0, column=2, padx=15, ipadx=13, ipady=6)    

    # Khung danh sách các sách
    # Style cho danh sách
    treeViewStyle = ttk.Style()
    treeViewStyle.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=50,
        background="#FFFFFF",        # Nền trắng
        foreground="#212121",        # Chữ xám đậm
        fieldbackground="#FFFFFF"    # Nền trắng cho vùng trống
    )
    treeViewStyle.configure(
        "Treeview.Heading",
        font=("Segoe UI", 11, "bold"),
        background="#1976D2",        # Xanh đậm
        foreground="#FFFFFF"         # Chữ trắng
    )
    treeViewStyle.map(
        "Treeview",
        background=[('selected', '#1976D2')],
        foreground=[('selected', '#FFFFFF')]
    )

    treeViewFrame = ttk.Frame(mainFrame, style="frameCon.TFrame")
    treeViewFrame.pack(fill="both")
    treeViewFrame.columnconfigure(1, weight=1)
    
    tree = ttk.Treeview(treeViewFrame, columns=("ID", "Tiêu đề", "Tác giả", "Năm xuất bản"), show="headings", height=12)

    # Ghi tiêu đề cột
    tree.heading("ID", text="ID")
    tree.heading("Tiêu đề", text="Tiêu đề")
    tree.heading("Tác giả", text="Tác giả")
    tree.heading("Năm xuất bản", text="Năm xuất bản")

    # Căn chỉnh các dòng mỗi cột
    tree.column("ID", width=10, anchor="center")
    tree.column("Tiêu đề", width=100, anchor="center")
    tree.column("Tác giả", width=100, anchor="center")
    tree.column("Năm xuất bản", width=10, anchor="center")

    tree.grid(row=2, column=0, columnspan=10, padx=10, pady=30, sticky="ew")
    tree.bind("<<TreeviewSelect>>", CHUCNANG_Method.chonTuCay)
    DANHSACH_DanhSachCacSach.DsSachObject = DANHSACH_DanhSachCacSach.docFileJson()
    CHUCNANG_Method.taiSachLenTreeView(tree)
    
    # Thanh cuộn
    thanhCuon = ttk.Scrollbar(treeViewFrame, orient=tk.VERTICAL, command=tree.yview)
    thanhCuon.grid(row=2, column=2, sticky="nsw", pady=30)
    tree.configure(yscrollcommand=thanhCuon.set)

    # Khung nút chức năng
    # Style các nút
    nutStyle = ttk.Style()
    nutStyle.theme_use("clam")
    nutStyle.configure(
        "TButton",
        background="#FFFFFF",      # Nền trắng
        foreground="#1976D2",      # Chữ xanh đậm
        font=("Segoe UI", 10, "bold"),
        borderwidth=1
    )

    framNutStyle = ttk.Style()
    framNutStyle.configure("frameNutStyle.TFrame", 
                           background = "lightblue")

    nutFrame = ttk.Frame(mainFrame, style="frameNutStyle.TFrame")
    nutFrame.pack(expand=False, ipady=20, pady=20)

    # Thông số của button
    buttonWidth = 17
    buttonHeight = 15

    ttk.Button(nutFrame, text="Xem thông tin sách", command=lambda: GIAODIEN_Window.xemThongTinSachWindow(mainFrame, tree), width=buttonWidth).grid(row=0, column=0, padx=10, ipady=buttonHeight)
    
    if role == "admin": 
        ttk.Button(nutFrame, text="Thêm sách", width=buttonWidth, command=lambda: GIAODIEN_Window.themSachWindow(mainFrame, tree)).grid(row=0, column=1, padx=50, ipady=buttonHeight)
        ttk.Button(nutFrame, text="Xoá sách", width=buttonWidth, command=lambda: GIAODIEN_Window.xoaSachWindow(tree)).grid(row=0, column=2, padx=50, ipady=buttonHeight)
        ttk.Button(nutFrame, text="Cập nhật sách", width=buttonWidth, command=lambda: GIAODIEN_Window.capNhatSachWindow(mainFrame, tree)).grid(row=0, column=3, padx=50, ipady=buttonHeight)

    ttk.Button(nutFrame, text="Đọc sách", width=buttonWidth, command=lambda: CHUCNANG_Method.docSach(tree)).grid(row=0, column=4, padx=50, ipady=buttonHeight)

    root.mainloop()

# Đăng nhập/ Đăng ký
def dangNhap(cuaSoDangNhap):
    username = usernameEntry.get()
    password = passwordEntry.get()
    role = roleVar.get()

    role_from_db = DANHSACH_DanhSachCacSach.xacThucUser(username, password)
    if role_from_db:
        if role == role_from_db:
            messagebox.showinfo("Thành công", f"Chào mừng {username}!\nQuyền: {role}")
            moGiaoDienChinh(role, cuaSoDangNhap) 
        else:
            messagebox.showerror("Lỗi", "Quyền truy cập không hợp lệ!")
    else:
        messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

def moCuaSoDangKy():
    cuaSoDangKy = tk.Toplevel()
    cuaSoDangKy.title("Đăng ký")
    cuaSoDangKy.geometry("400x250") 
    cuaSoDangKy.config(bg="lightblue")
    # Style cửa sổ đăng nhập
    dangKyStyle = ttk.Style()
    dangKyStyle.configure("frameDangKy.TFrame",
                    background="lightblue",      # Nền xanh biển
                    foreground="#000000",      # Chữ trắng
                    font=("Segoe UI", 10, "bold"),  # In đậm
                    borderwidth=1)

    dangKyStyle.configure("dangKyButton.TButton",
                    background="#1976D2",      # Nền xanh biển
                    foreground="#FFFFFF",      # Chữ trắng
                    font=("Segoe UI", 10, "bold"),  # In đậm
                    borderwidth=1)
    # **Tạo Frame chứa các phần tử đăng ký**
    frameMain = ttk.Frame(cuaSoDangKy, padding=10, style = "frameDangKy.TFrame")
    frameMain.pack()

    # **Tên đăng nhập**
    ttk.Label(frameMain, text="Tên đăng nhập:", background="lightblue").grid(row=0, column=0, padx=5, sticky='w')
    newUsernameEntry = ttk.Entry(frameMain, width=15)
    newUsernameEntry.grid(row=0, column=1, padx=5)

    # **Mật khẩu**
    ttk.Label(frameMain, text="Mật khẩu:", background="lightblue").grid(row=1, column=0, padx=5, sticky='w')
    newPasswordEntry = ttk.Entry(frameMain, show="*", width=15)
    newPasswordEntry.grid(row=1, column=1, padx=5)

    # **Xác nhận Mật khẩu**
    ttk.Label(frameMain, text="Xác nhận Mật khẩu:", background="lightblue").grid(row=2, column=0, padx=5, sticky='w')
    confirmPasswordEntry = ttk.Entry(frameMain, show="*", width=20)
    confirmPasswordEntry.grid(row=2, column=1, padx=5)

    # **Chọn quyền**
    newRoleVar = tk.StringVar(value="user") # giá trị mặc định là "user"

    # **Nút Đăng ký**
    ttk.Button(frameMain, text="Đăng ký", command=lambda: xuLyDangKy(newUsernameEntry, newPasswordEntry, confirmPasswordEntry, newRoleVar, cuaSoDangKy), style="dangKyButton.TButton").grid(row=3, column=1, padx=10)

def xuLyDangKy(usernameEntry, passwordEntry, confirmPasswordEntry, roleVar, register_window):
    username = usernameEntry.get()
    password = passwordEntry.get()
    confirm_password = confirmPasswordEntry.get()
    role = roleVar.get()

    if not username or not password or not confirm_password:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
        return

    if password != confirm_password:
        messagebox.showerror("Lỗi", "Mật khẩu và xác nhận mật khẩu không khớp!")
        return
    
    success, message = DANHSACH_DanhSachCacSach.themUser(username, password, role) 

    if success:
        messagebox.showinfo("Thành công", message + "\nVui lòng đăng nhập.")
        register_window.destroy()
    else:
        messagebox.showerror("Lỗi", message)

if __name__ == "__main__":
    mocuasodangnhap()