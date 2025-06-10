import ctypes
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

import GIAODIEN_Window
import CHUCNANG_Method
import DANHSACH_DanhSachCacSach
from DOITUONG_Sach import Sach

# Chỉnh lại DPI hợp với độ phân giải hiện tại của màn hình Windows
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Hàm để khởi chạy cửa sổ đăng nhập
def moCuaSoDangNhap():
    global cuaSoDangNhap, usernameEntry, passwordEntry, roleVar
    cuaSoDangNhap = tk.Tk()
    cuaSoDangNhap.title("Đăng nhập")
    cuaSoDangNhap.resizable(False, False)
    cuaSoDangNhap.config(bg="#ADD8E6")

    theme = ttk.Style(cuaSoDangNhap)
    theme.theme_use('clam')

    theme.configure("MainFrame.TFrame", background="#ADD8E6")
    theme.configure("ImageFrame.TFrame", background="#ADD8E6") 

    theme.configure("RightContent.TFrame",
                            background="#FFFFFF", 
                            relief="solid",
                            borderwidth=2)

    theme.configure("LoginFormContent.TFrame", background="#FFFFFF")

    theme.configure("LoginHeading.TLabel",
                            background="#FFFFFF",
                            font=("Segoe UI", 22, "bold"),
                            foreground="#003366")

    theme.configure("LoginLabel.TLabel",
                            background="#FFFFFF",
                            font=("Segoe UI", 11),
                            foreground="#333333")

    theme.configure("LoginEntry.TEntry",
                            fieldbackground="#F5F5F5",
                            foreground="#333333",
                            insertcolor="#333333",
                            borderwidth=1,
                            relief="flat",
                            padding=(8, 8))
    theme.map("LoginEntry.TEntry",
                            fieldbackground=[('focus', '#E0F2F7')])

    theme.configure("LoginCombobox.TCombobox",
                            fieldbackground="#F5F5F5",
                            foreground="#333333",
                            selectbackground="#1976D2",
                            selectforeground="#FFFFFF",
                            font=("Segoe UI", 11),
                            padding=(8, 8))
    theme.map("LoginCombobox.TCombobox",
                            fieldbackground=[('readonly', '#F5F5F5'), ('focus', '#E0F2F7')])
    theme.configure('TCombobox.Listbox',
                            background='#F5F5F5',
                            foreground='#333333',
                            selectbackground='#1976D2',
                            selectforeground='#FFFFFF',
                            font=("Segoe UI", 11))

    theme.configure("LoginButton.TButton",
                            background="#1976D2",
                            foreground="#FFFFFF",
                            font=("Segoe UI", 12, "bold"),
                            borderwidth=0,
                            relief="flat",
                            padding=(20, 10))
    theme.map("LoginButton.TButton",
                            background=[('active', '#1565C0')])

    frameMain = ttk.Frame(cuaSoDangNhap, padding=20, style="MainFrame.TFrame")
    frameMain.pack(fill=tk.BOTH, expand=True)

    frameAnh = ttk.Frame(frameMain, style="ImageFrame.TFrame")
    frameAnh.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 0))

    image_width = 600
    image_height = 500

    try:
        image_path = "book_login.png" 
        anh = Image.open(image_path)
        anh = anh.resize((image_width, image_height), Image.LANCZOS)
        anhTk = ImageTk.PhotoImage(anh)
        anhLabel = ttk.Label(frameAnh, image=anhTk, background="#ADD8E6")
        anhLabel.image = anhTk
        anhLabel.pack(fill=tk.BOTH, expand=True)
    except FileNotFoundError:
        ttk.Label(frameAnh, text=f"Không tìm thấy ảnh: {image_path}", background="#ADD8E6", font=("Segoe UI", 12)).pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    except Exception as e:
        ttk.Label(frameAnh, text=f"Lỗi tải ảnh: {e}", background="#ADD8E6", font=("Segoe UI", 12)).pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    frameRightContent = ttk.Frame(frameMain, style="RightContent.TFrame")
    frameRightContent.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 0))

    frameRightContent.grid_rowconfigure(0, weight=1)
    frameRightContent.grid_rowconfigure(2, weight=1)
    frameRightContent.grid_columnconfigure(0, weight=1)

    ttk.Label(frameRightContent, text="ĐĂNG NHẬP", style="LoginHeading.TLabel").grid(row=0, column=0, pady=(30, 40), sticky="s")

    loginForm = ttk.Frame(frameRightContent, style="LoginFormContent.TFrame")
    loginForm.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)

    loginForm.grid_columnconfigure(0, weight=1)
    loginForm.grid_columnconfigure(1, weight=1)

    # Tên đăng nhập
    ttk.Label(loginForm, text="Tên đăng nhập:", style="LoginLabel.TLabel").grid(row=0, column=0, padx=10, pady=10, sticky='w')
    usernameEntry = ttk.Entry(loginForm, style="LoginEntry.TEntry")
    usernameEntry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    # Mật khẩu
    ttk.Label(loginForm, text="Mật khẩu:", style="LoginLabel.TLabel").grid(row=1, column=0, padx=10, pady=10, sticky='w')
    passwordEntry = ttk.Entry(loginForm, show="*", style="LoginEntry.TEntry")
    passwordEntry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

    # Chọn quyền
    ttk.Label(loginForm, text="Chọn quyền:", style="LoginLabel.TLabel").grid(row=2, column=0, padx=10, pady=10, sticky='w')
    roleVar = tk.StringVar()
    roleMenu = ttk.Combobox(loginForm, textvariable=roleVar, state="readonly", style="LoginCombobox.TCombobox")
    roleMenu["values"] = ("admin", "user")
    roleMenu.set("user")
    roleMenu.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

    # Nút Đăng nhập và Đăng ký
    frameButtonStyle = ttk.Style()
    frameButtonStyle.configure("LoginButtonFrame.TFrame", background = "White")
    frameButtons = ttk.Frame(loginForm, style="LoginButtonFrame.TFrame")
    frameButtons.grid(row=3, column=0, columnspan=2, pady=30, sticky="ew")
    frameButtons.columnconfigure(0, weight=1)
    frameButtons.columnconfigure(1, weight=1)

    ttk.Button(frameButtons, text="Đăng nhập", command=lambda: dangNhap(cuaSoDangNhap), style="LoginButton.TButton").grid(row=0, column=0, padx=10, sticky="ew")
    ttk.Button(frameButtons, text="Đăng ký", command=moCuaSoDangKy, style="LoginButton.TButton").grid(row=0, column=1, padx=10, sticky="ew")

    cuaSoDangNhap.update_idletasks()
    x = (cuaSoDangNhap.winfo_screenwidth() - cuaSoDangNhap.winfo_width()) // 2
    y = (cuaSoDangNhap.winfo_screenheight() - cuaSoDangNhap.winfo_height()) // 2
    cuaSoDangNhap.geometry(f"+{x}+{y}")

    cuaSoDangNhap.mainloop()

# Mở ứng dụng chính nếu đăng nhập thành công
def moGiaoDienChinh(role, dangnhap_window):
    dangnhap_window.destroy()  

    # Tạo window
    root = tk.Tk()
    
    # Hàm đăng xuất
    def dangXuat(event=None): 
        root.destroy() 
        moCuaSoDangNhap() 
   
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
        mainFrame,
        text="Đăng Xuất",
        font=("Segoe UI", 18, "underline", "bold"), 
        fg="#003366",
        bg="lightblue", 
        cursor="hand2" 
    )
    dangxuatLabel.place(relx=1.0, rely=0.0, anchor='ne', x=-60, y=20) 
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
            moGiaoDienChinh(role, cuaSoDangNhap) # Chuyển đến giao diện chính
        else:
            messagebox.showerror("Lỗi", "Quyền truy cập không hợp lệ cho tài khoản này!")
    else:
        messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

def moCuaSoDangKy():
    cuaSoDangKy = tk.Toplevel()
    cuaSoDangKy.title("Đăng ký")
    cuaSoDangKy.geometry("1200x700")
    cuaSoDangKy.resizable(False, False)
    cuaSoDangKy.config(bg="#ADD8E6")
    cuaSoDangKy.transient(cuaSoDangNhap)
    cuaSoDangKy.grab_set()
    cuaSoDangKy.focus_set()

    theme = ttk.Style(cuaSoDangKy)
    theme.configure("MainFrame.TFrame", background="#ADD8E6") 
    theme.configure("ImageFrame.TFrame", background="#ADD8E6") 

    theme.configure("RegisterRightContent.TFrame",
                            background="#FFFFFF", 
                            relief="solid",
                            borderwidth=2)

    theme.configure("RegisterFormContent.TFrame", background="#FFFFFF")

    theme.configure("RegisterHeading.TLabel",
                            background="#FFFFFF",
                            font=("Segoe UI", 22, "bold"),
                            foreground="#003366")

    theme.configure("RegisterLabel.TLabel",
                            background="#FFFFFF",
                            font=("Segoe UI", 11),
                            foreground="#333333")

    theme.configure("RegisterEntry.TEntry",
                            fieldbackground="#F5F5F5",
                            foreground="#333333",
                            insertcolor="#333333",
                            borderwidth=1,
                            relief="flat",
                            padding=(8, 8))
    theme.map("RegisterEntry.TEntry",
                            fieldbackground=[('focus', '#E0F2F7')])

    theme.configure("RegisterButton.TButton",
                            background="#1976D2",
                            foreground="#FFFFFF",
                            font=("Segoe UI", 12, "bold"),
                            borderwidth=0,
                            relief="flat",
                            padding=(20, 10))
    theme.map("RegisterButton.TButton",
                            background=[('active', '#1565C0')])

    frameMain = ttk.Frame(cuaSoDangKy, padding=20, style = "MainFrame.TFrame")
    frameMain.pack(fill=tk.BOTH, expand=True)

    frameAnh = ttk.Frame(frameMain, style="ImageFrame.TFrame")
    frameAnh.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 0))

    image_width = 600
    image_height = 500
    try:
        image_path = "book_login.png"
        anh = Image.open(image_path)
        anh = anh.resize((image_width, image_height), Image.LANCZOS)
        anhTk = ImageTk.PhotoImage(anh)
        anhLabel = ttk.Label(frameAnh, image=anhTk, background="#ADD8E6")
        anhLabel.image = anhTk
        anhLabel.pack(fill=tk.BOTH, expand=True)
    except FileNotFoundError:
        ttk.Label(frameAnh, text=f"Không tìm thấy ảnh: {image_path}", background="#ADD8E6", font=("Segoe UI", 12)).pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    except Exception as e:
        ttk.Label(frameAnh, text=f"Lỗi tải ảnh: {e}", background="#ADD8E6", font=("Segoe UI", 12)).pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    frameRightContent = ttk.Frame(frameMain, style="RegisterRightContent.TFrame")
    frameRightContent.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 0))

    frameRightContent.grid_rowconfigure(0, weight=1)
    frameRightContent.grid_rowconfigure(2, weight=1)
    frameRightContent.grid_columnconfigure(0, weight=1)

    ttk.Label(frameRightContent, text="ĐĂNG KÝ", style="RegisterHeading.TLabel").grid(row=0, column=0, pady=(30, 40), sticky="s")

    registerForm = ttk.Frame(frameRightContent, style="RegisterFormContent.TFrame")
    registerForm.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)

    registerForm.grid_columnconfigure(0, weight=1)
    registerForm.grid_columnconfigure(1, weight=1)

    # Tên đăng nhập
    ttk.Label(registerForm, text="Tên đăng nhập:", style="RegisterLabel.TLabel").grid(row=0, column=0, padx=10, pady=10, sticky='w')
    newUsernameEntry = ttk.Entry(registerForm, style="RegisterEntry.TEntry")
    newUsernameEntry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    # Mật khẩu
    ttk.Label(registerForm, text="Mật khẩu:", style="RegisterLabel.TLabel").grid(row=1, column=0, padx=10, pady=10, sticky='w')
    newPasswordEntry = ttk.Entry(registerForm, show="*", style="RegisterEntry.TEntry")
    newPasswordEntry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

    # Xác nhận Mật khẩu
    ttk.Label(registerForm, text="Xác nhận Mật khẩu:", style="RegisterLabel.TLabel").grid(row=2, column=0, padx=10, pady=10, sticky='w')
    confirmPasswordEntry = ttk.Entry(registerForm, show="*", style="RegisterEntry.TEntry")
    confirmPasswordEntry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

    newRoleVar = tk.StringVar(value="user")

    # Nút Đăng ký
    ttk.Button(registerForm, text="Đăng ký", command=lambda: xuLyDangKy(newUsernameEntry, newPasswordEntry, confirmPasswordEntry, newRoleVar, cuaSoDangKy), style="RegisterButton.TButton").grid(row=3, column=0, columnspan=2, pady=30, sticky="ew")

    cuaSoDangKy.update_idletasks()
    x = (cuaSoDangKy.winfo_screenwidth() - cuaSoDangKy.winfo_width()) // 2
    y = (cuaSoDangKy.winfo_screenheight() - cuaSoDangKy.winfo_height()) // 2
    cuaSoDangKy.geometry(f"+{x}+{y}")

    cuaSoDangKy.wait_window()

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
    moCuaSoDangNhap()