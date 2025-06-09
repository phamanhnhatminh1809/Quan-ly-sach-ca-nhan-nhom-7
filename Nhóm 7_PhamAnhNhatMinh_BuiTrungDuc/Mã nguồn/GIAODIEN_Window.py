import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk

import DANHSACH_DanhSachCacSach
import CHUCNANG_Method 
from DOITUONG_Sach import Sach

def xemThongTinSachWindow(frame, tree):
    try:
        luaChon = tree.selection()
        if not luaChon:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cuốn sách để xem thông tin")
            return

        # Độ phân giải của frame chính
        mainFrameWidth = frame.winfo_screenwidth()
        mainFrameHeight = frame.winfo_screenheight()
        
        # Window xem thông tin
        xemWindow = tk.Toplevel(frame)
        xemWindow.title("Xem thông tin sách")
        xemWindow.config(bg="#f4f4f4")
        xemWindow.transient(frame)
        xemWindow.focus_set()  
        xemWindow.grab_set() 

       

        
         
        # Style
        style = ttk.Style()
        # Background, font cho frame và label
        style.configure("frameXemThongTin.TFrame", background="lightblue")
        style.configure("frameXemThongTin.TLabel", background="lightblue", font=("Segoe UI", 15))
        style.configure("frameXemThongTin.Title.TLabel", font=("Segoe UI", 23, "bold"), foreground="#0056b3", background = "#f4f4f4")
        style.configure("frameXemThongTin.Bold.TLabel", font=("Segoe UI", 15, "bold"), foreground="#333333", background = "lightblue")

        def cachDong(labelText, valueText):
            textLenght = len(valueText)
            insertIndex = 39
            
            while textLenght > 40:
                valueText = valueText[:insertIndex] + '\n' + valueText[insertIndex:]
                textLenght  -= 40
                insertIndex += 40
                labelText += '\n'
            return labelText, valueText
        
        def taoDongChu(frame, labelText, valueText):
            try:
                labelText, valueText = cachDong(labelText, valueText)
            except:
                pass
            rowFrame = ttk.Frame(frame)
            rowFrame.pack(fill="x", pady=30)
            label = ttk.Label(rowFrame, text=labelText, style="frameXemThongTin.Bold.TLabel")
            label.pack(side="left", anchor="w", ipadx=10)
            value = ttk.Label(rowFrame, text=valueText, style="frameXemThongTin.TLabel")
            value.pack(side="left", anchor="w", expand=True, fill="x")
            
        # Id cuốn sách được chọn
        idSach = int(tree.item(luaChon)["values"][0])

        # Tiêu đề
        for sach in DANHSACH_DanhSachCacSach.DsSachObject:
            if sach.id == idSach:
                title_label = ttk.Label(xemWindow, text=sach.ten, style="frameXemThongTin.Title.TLabel", anchor="center")
                title_label.pack()
            
        # Frame để chứa thông tin và ảnh
        xemThongTinFrame = ttk.Frame(xemWindow, style="frameXemThongTin.TFrame")
        xemThongTinFrame.pack(expand=True)
        xemThongTinFrame.columnconfigure(0,weight=1)

        for sach in DANHSACH_DanhSachCacSach.DsSachObject:
            if sach.id == idSach:
                # Frame thông tin chi tiết 
                thong_tin_frame = ttk.Frame(xemThongTinFrame, style="frameXemThongTin.TFrame")
                thong_tin_frame.grid(row=1, column=1, sticky="nw", pady=(10,15), padx=(40, 10))
                
                if CHUCNANG_Method.kiemTraSachCoLayTuAPI(sach.duongDan):
                    duongDanFile = sach.duongDan
                else:
                    duongDanFile = os.path.abspath(sach.duongDan)

                taoDongChu(thong_tin_frame, "ID:", str(sach.id))
                taoDongChu(thong_tin_frame, "Tác giả:", sach.tacGia)
                taoDongChu(thong_tin_frame, "Năm xuất bản:", sach.namXB)
                taoDongChu(thong_tin_frame, "Đường dẫn:",  duongDanFile)

                # Frame ảnh bìa 
                anhBiaFrame = ttk.Frame(xemThongTinFrame, style="frameXemThongTin.TFrame")
                anhBiaFrame.grid(row=1, column=0, sticky="e", padx=(10,0), pady=(0,15))

                if CHUCNANG_Method.kiemTraSachCoLayTuAPI(sach.duongDan) == False:
                    anhBia = CHUCNANG_Method.layAnhBiaTuFile(sach.duongDan)
                    
                    anhBiaLabel = ttk.Label(anhBiaFrame, image=anhBia, style="frameXemThongTin.TLabel")
                    anhBiaLabel.image = anhBia
                    anhBiaLabel.grid(row=0, column=0, sticky="w")
                else:
                    anhBia = ImageTk.PhotoImage(CHUCNANG_Method.layAnhBiaTuAPI(sach.duongDan))
                    
                    anhBiaLabel = ttk.Label(anhBiaFrame, image=anhBia, style="frameXemThongTin.TLabel")
                    anhBiaLabel.image = anhBia
                    anhBiaLabel.grid(row=0, column=0, sticky="w")
                break

        # Gán geometry chỉ với vị trí, không thay đổi kích thước
        xemWindow.update_idletasks()

        # Thông tin của frame xem thông tin
        xemWindowWidth = xemWindow.winfo_reqwidth()
        xemWindowHeight = xemWindow.winfo_reqheight()
        viTriX = int(mainFrameWidth / 2 - xemWindowWidth / 2)
        viTriY = int(mainFrameHeight / 2 - xemWindowHeight / 2)

        xemWindow.geometry(f"{xemWindowWidth}x{xemWindowHeight}+{viTriX}+{viTriY}")
    except:
        return

def themSachWindow(frame, tree): 
    # Độ phân giải của frame chính
    mainFrameWidth = frame.winfo_screenwidth()
    mainFrameHeight = frame.winfo_screenheight()

    # Thông tin của frame xem thông tin
    themWindowWidth = int(mainFrameWidth * 0.47)
    themWindowHeight = int(mainFrameHeight * 0.39)
    viTriX = int(mainFrameWidth / 2 - themWindowWidth / 2)
    viTriY = int(mainFrameHeight / 2 - themWindowHeight / 2)

    # Window thêm sách
    themWindow = tk.Toplevel(frame)
    themWindow.title("Thêm sách mới")
    themWindow.geometry(f"{themWindowWidth}x{themWindowHeight}+{viTriX}+{viTriY}") 
    themWindow.resizable(False, False)
    themWindow.config(bg="#f4f4f4")
    themWindow.transient(frame)           
    themWindow.grab_set()                
    themWindow.focus_set()  

    # Style
    style = ttk.Style()

    # Font chung cho các Label và Entry
    style.configure("themWindow.TLabel", font=("Segoe UI", 15, "bold"), padding=5, background = "lightblue")
    style.configure("themWindow.TEntry", font=("Segoe UI", 16), padding=5, background = "lightblue")
    style.configure("themWindow.TButton", background="#FFFFFF", foreground="#1976D2", font=("Segoe UI", 10, "bold"), borderwidth=1)

    # Background cho các frame
    style.configure("themWindow.Form.TFrame", background="lightblue", borderwidth=1, relief="groove") 
    style.configure("themWindow.Button.TFrame", background = "#f4f4f4") 

    # Font cho tiêu đề form
    style.configure("themWindow.FormTitle.TLabel", font=("Segoe UI", 18, "bold"), foreground="#0056b3", background = "#f4f4f4")

    # Căn giữa nội dung form
    themWindow.grid_rowconfigure(0, weight=1) # Row cho tiêu đề (nếu có)
    themWindow.grid_rowconfigure(1, weight=1) # Row cho form chính
    themWindow.grid_rowconfigure(2, weight=1) # Row cho nút
    themWindow.grid_columnconfigure(0, weight=1)

    # Title
    title_label = ttk.Label(themWindow, text="THÊM SÁCH MỚI", style="themWindow.FormTitle.TLabel")
    title_label.grid(row=0, column=0, pady=(20, 10), sticky="n")

    # Frame chứa các entry để người dùng nhập vào
    nhapFrame = ttk.Frame(themWindow, style="themWindow.Form.TFrame", padding=(20, 20, 20, 20))
    nhapFrame.grid(row=1, column=0, padx=50, pady=10, sticky="nsew")

    # Cấu hình các cột trong nhapFrame
    nhapFrame.grid_columnconfigure(0, weight=1) # Cột cho Labels
    nhapFrame.grid_columnconfigure(1, weight=3) # Cột cho Entries
    nhapFrame.grid_columnconfigure(2, weight=1) # Cột cho nút Browse

    # Tiêu Đề
    ttk.Label(nhapFrame, text="Tiêu Đề:", style="themWindow.TLabel").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    tenEntry = ttk.Entry(nhapFrame, style="themWindow.TEntry") 
    tenEntry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=5) 

    # Tác Giả
    ttk.Label(nhapFrame, text="Tác Giả:", style="themWindow.TLabel").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    tacGiaEntry = ttk.Entry(nhapFrame, style="themWindow.TEntry")
    tacGiaEntry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

    # Năm Xuất Bản
    ttk.Label(nhapFrame, text="Năm Xuất Bản:", style="themWindow.TLabel").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    namXBEntry = ttk.Entry(nhapFrame, style="themWindow.TEntry")
    namXBEntry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

    # Đường Dẫn PDF
    ttk.Label(nhapFrame, text="Đường Dẫn PDF:", style="themWindow.TLabel").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    duongDanEntry = ttk.Entry(nhapFrame, style="themWindow.TEntry")
    duongDanEntry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

    # Nút Duyệt File
    nutBrowse = ttk.Button(nhapFrame, text="Browse...", command=lambda: CHUCNANG_Method.chonFilePdf(duongDanEntry, themWindow), style="themWindow.TButton")
    nutBrowse.grid(row=3, column=2, sticky="e", padx=(0, 5), pady=5)

    def luuSach():
        ten = tenEntry.get()
        tacGia = tacGiaEntry.get()
        namXB = namXBEntry.get()
        duongDanTuyetDoi = duongDanEntry.get()
    
        if not ten:
            messagebox.showerror("Lỗi", "Vui lòng nhập tiêu đề sách!")
            return
        if duongDanTuyetDoi and not os.path.exists(duongDanTuyetDoi):
            messagebox.showerror("Lỗi", "File PDF không tồn tại!")
            return
        
        # Chuyển đường dẫn tuyệt đối sang đường dẫn tương đối
        duongDanTuongDoi = os.path.relpath(duongDanTuyetDoi, start=os.curdir)
        
        # Tạo id mới
        idMoi = max([sach.id for sach in DANHSACH_DanhSachCacSach.DsSachObject], default=0) + 1

        # Thêm sách mới
        sachMoi = Sach(id=idMoi, ten=ten, tacGia=tacGia, namXB=namXB, duongDan=duongDanTuongDoi)
        DANHSACH_DanhSachCacSach.DsSachObject.append(sachMoi)
        DANHSACH_DanhSachCacSach.luuVaoFileJson()
        CHUCNANG_Method.taiSachLenTreeView(tree)
        themWindow.destroy()
        messagebox.showinfo("Thành công", "Thêm sách thành công!")

    # Frame nút Thêm và Hủy 
    nutFrame = ttk.Frame(themWindow, style="themWindow.Button.TFrame") 
    nutFrame.grid(row=2, column=0, pady=(5, 50), sticky="s")

    # Cấu hình các cột trong nút frame
    nutFrame.grid_columnconfigure(0, weight=1)
    nutFrame.grid_columnconfigure(1, weight=1)
    
    # Nút Thêm
    themSachButton = ttk.Button(nutFrame, text="Thêm Sách", command=luuSach, style="themWindow.TButton")
    themSachButton.grid(row=0, column=0, padx=30, pady=5)

    # Nút Hủy
    huyButton = ttk.Button(nutFrame, text="Hủy Bỏ", command=themWindow.destroy, style="themWindow.TButton")
    huyButton.grid(row=0, column=1, padx=30, pady=5)

    themWindow.wait_window()

def xoaSachWindow(tree):
    luaChon = tree.selection()
    if not luaChon:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cuốn sách để xoá!")
        return 
    if messagebox.askyesno("Xác nhận", "Bạn có muốn xoá cuốn sách này?"):
        idSach = int(tree.item(luaChon)["values"][0])    
        for sach in DANHSACH_DanhSachCacSach.DsSachObject:
            if sach.id == idSach:
                CHUCNANG_Method.xoaFile(sach.duongDan)
        
        DsSachObjectSauKhiXoa = [sach for sach in DANHSACH_DanhSachCacSach.DsSachObject if sach.id != idSach]
        DANHSACH_DanhSachCacSach.capNhatLaiDanhSach(DsSachObjectSauKhiXoa)
        DANHSACH_DanhSachCacSach.luuVaoFileJson()
        CHUCNANG_Method.taiSachLenTreeView(tree)
        messagebox.showinfo("Thành công", "Xoá sách thành công!")

def capNhatSachWindow(frame, tree): 
    luaChon = tree.selection()
    if not luaChon:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cuốn sách để cập nhật!")
        return

    idSach = int(tree.item(luaChon)["values"][0])
    sachCanCapNhat = next((sach for sach in DANHSACH_DanhSachCacSach.DsSachObject if sach.id == idSach), None)

    # Độ phân giải của frame chính
    mainFrameWidth = frame.winfo_screenwidth()
    mainFrameHeight = frame.winfo_screenheight()

    # Thông tin của frame cập nhật thông tin
    capNhatWindowWidth = int(mainFrameWidth * 0.47)
    capNhatWindowHeight = int(mainFrameHeight * 0.39)
    viTriX = int(mainFrameWidth / 2 - capNhatWindowWidth / 2)
    viTriY = int(mainFrameHeight / 2 - capNhatWindowHeight / 2)

    # Window cập nhật sách
    capNhatWindow = tk.Toplevel(frame)
    capNhatWindow.title("Cập nhật sách")
    capNhatWindow.geometry(f"{capNhatWindowWidth}x{capNhatWindowHeight}+{viTriX}+{viTriY}") 
    capNhatWindow.resizable(False, False)
    capNhatWindow.config(bg="#f4f4f4")
    capNhatWindow.transient(frame)           
    capNhatWindow.grab_set()                
    capNhatWindow.focus_set()  

    # Style
    style = ttk.Style()

    # Font chung cho các Label và Entry
    style.configure("capNhatWindow.TLabel", font=("Segoe UI", 15, "bold"), padding=5, background = "lightblue")
    style.configure("capNhatWindow.TEntry", font=("Segoe UI", 16), padding=5, background = "lightblue")
    style.configure("capNhatWindow.TButton", background="#FFFFFF", foreground="#1976D2", font=("Segoe UI", 10, "bold"), borderwidth=1)

    # Background cho các frame
    style.configure("capNhatWindow.Form.TFrame", background="lightblue", borderwidth=1, relief="groove") 
    style.configure("capNhatWindow.Button.TFrame", background = "#f4f4f4") 

    # Font cho tiêu đề form
    style.configure("capNhatWindow.FormTitle.TLabel", font=("Segoe UI", 18, "bold"), foreground="#0056b3", background = "#f4f4f4")

    # Căn giữa nội dung form
    capNhatWindow.grid_rowconfigure(0, weight=1) # Row cho tiêu đề (nếu có)
    capNhatWindow.grid_rowconfigure(1, weight=1) # Row cho form chính
    capNhatWindow.grid_rowconfigure(2, weight=1) # Row cho nút
    capNhatWindow.grid_columnconfigure(0, weight=1)
   
    # Title
    title_label = ttk.Label(capNhatWindow, text="CẬP NHẬT SÁCH", style="capNhatWindow.FormTitle.TLabel")
    title_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
    
    # Frame chứa các entry để người dùng nhập vào
    capNhatFrame = ttk.Frame(capNhatWindow, style="capNhatWindow.Form.TFrame", padding=(20, 20, 20, 20))
    capNhatFrame.grid(row=1, column=0, padx=50, pady=10, sticky="nsew")

    # Cấu hình các cột trong capNhatFrame
    capNhatFrame.grid_columnconfigure(0, weight=1) # Cột cho Labels
    capNhatFrame.grid_columnconfigure(1, weight=3) # Cột cho Entries
    capNhatFrame.grid_columnconfigure(2, weight=1) # Cột cho nút Browse

    # Tiêu Đề
    ttk.Label(capNhatFrame, text="Tiêu Đề:", style="capNhatWindow.TLabel").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    tenEntry = ttk.Entry(capNhatFrame, style="capNhatWindow.TEntry") 
    tenEntry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=5) 

    # Tác Giả
    ttk.Label(capNhatFrame, text="Tác Giả:", style="capNhatWindow.TLabel").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    tacGiaEntry = ttk.Entry(capNhatFrame, style="capNhatWindow.TEntry")
    tacGiaEntry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

    # Năm Xuất Bản
    ttk.Label(capNhatFrame, text="Năm Xuất Bản:", style="capNhatWindow.TLabel").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    namXBEntry = ttk.Entry(capNhatFrame, style="capNhatWindow.TEntry")
    namXBEntry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

    # Đường Dẫn PDF
    ttk.Label(capNhatFrame, text="Đường Dẫn PDF:", style="capNhatWindow.TLabel").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    duongDanEntry = ttk.Entry(capNhatFrame, style="capNhatWindow.TEntry")
    duongDanEntry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

    # Nút Duyệt File
    nutBrowse = ttk.Button(capNhatFrame, text="Browse...", command=lambda: CHUCNANG_Method.chonFilePdf(duongDanEntry, capNhatFrame), style="capNhatWindow.TButton")
    nutBrowse.grid(row=3, column=2, sticky="e", padx=(0, 5), pady=5)

    # Hiển thị thông tin cũ trong Entry trước khi cập nhật
    tenEntry.insert(0, sachCanCapNhat.ten)  
    tacGiaEntry.insert(0, sachCanCapNhat.tacGia)  
    namXBEntry.insert(0, sachCanCapNhat.namXB)  
    duongDanEntry.insert(0, sachCanCapNhat.duongDan) 

    # Hàm xử lý cập nhật
    def luuCapNhat():
        sachCanCapNhat.ten = tenEntry.get()
        sachCanCapNhat.tacGia = tacGiaEntry.get()
        sachCanCapNhat.namXB = namXBEntry.get()
        sachCanCapNhat.duongDan = duongDanEntry.get()
        DANHSACH_DanhSachCacSach.luuVaoFileJson()  
        CHUCNANG_Method.taiSachLenTreeView(tree)  
        capNhatWindow.destroy()
        messagebox.showinfo("Thành công", "Cập nhật sách thành công!")

    # Frame nút cập nhật và Hủy 
    nutFrame = ttk.Frame(capNhatWindow, style="capNhatWindow.Button.TFrame") 
    nutFrame.grid(row=2, column=0, pady=(5, 50), sticky="s")

    # Cấu hình các cột trong nút frame
    nutFrame.grid_columnconfigure(0, weight=1)
    nutFrame.grid_columnconfigure(1, weight=1)
    
    # Nút Cập nhật
    capNhatButton = ttk.Button(nutFrame, text="Cập Nhật Sách", command=luuCapNhat, style="capNhatWindow.TButton")
    capNhatButton.grid(row=0, column=0, padx=30, pady=5)

    # Nút Hủy
    huyButton = ttk.Button(nutFrame, text="Hủy Bỏ", command=capNhatWindow.destroy, style="capNhatWindow.TButton")
    huyButton.grid(row=0, column=1, padx=30, pady=5)

    capNhatWindow.wait_window()

selected_books = set()  # Lưu các ID sách đã chọn

def timSachOnlineWindow(frame, tree):
    """Mở cửa sổ nhập từ khóa, hiển thị danh sách API, cho phép chọn nhiều sách để lưu"""
    # Độ phân giải của frame chính
    mainFrameWidth = frame.winfo_screenwidth()
    mainFrameHeight = frame.winfo_screenheight()

    # Thông tin của frame tìm sách online
    timSachWindowwWidth = int(mainFrameWidth * 0.42)
    timSachWindowHeight = int(mainFrameHeight * 0.46)
    viTriX = int(mainFrameWidth / 2 - timSachWindowwWidth / 2)
    viTriY = int(mainFrameHeight / 2 - timSachWindowHeight / 2)

    # Window tìm sách online
    timSachWindow = tk.Toplevel(frame)
    timSachWindow.title("Tìm sách online")
    timSachWindow.geometry(f"{timSachWindowwWidth}x{timSachWindowHeight}+{viTriX}+{viTriY}") 
    timSachWindow.resizable(False, False)
    timSachWindow.config(bg="lightblue")
    timSachWindow.transient(frame)           
    timSachWindow.grab_set()                
    timSachWindow.focus_set()  

    # Style
    style = ttk.Style()
    style.configure("timSachFrame.TFrame", background = "lightblue")

    timSachFrame = ttk.Frame(timSachWindow, padding=10, style="timSachFrame.TFrame")
    timSachFrame.pack(fill="both", expand=True)

    ttk.Label(timSachFrame, text="Nhập tên sách:", font=("Arial", 12)).pack(pady=5)
    tuKhoaEntry = ttk.Entry(timSachFrame, font=("Arial", 12))
    tuKhoaEntry.pack(pady=5)

    treeTimKiem = ttk.Treeview(timSachFrame, columns=("ID", "Tiêu đề", "Tác giả", "Năm XB"), show="headings", height=8)
    treeTimKiem.pack(pady=5)

    # Đặt tiêu đề cột
    treeTimKiem.heading("ID", text="ID")
    treeTimKiem.heading("Tiêu đề", text="Tiêu đề")
    treeTimKiem.heading("Tác giả", text="Tác giả")
    treeTimKiem.heading("Năm XB", text="Năm XB")

    # Định dạng cột
    treeTimKiem.column("ID", width=100, anchor="center")
    treeTimKiem.column("Tiêu đề", width=400, anchor="w")
    treeTimKiem.column("Tác giả", width=300, anchor="w")
    treeTimKiem.column("Năm XB", width=200, anchor="center")

    # Biến để lưu trữ danh sách các đối tượng Sach từ API
    _sach_online_results_cache = []

    def timVaHienThi():
        """Tìm sách từ API và hiển thị với ID bắt đầu từ 1"""
        nonlocal _sach_online_results_cache 
        tu_khoa = tuKhoaEntry.get().strip()
        if not tu_khoa:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa!")
            return

        _sach_online_results_cache = CHUCNANG_Method.timSachOnline(tu_khoa)

        if not _sach_online_results_cache:
            messagebox.showerror("Lỗi", "Không tìm thấy sách nào!")
            return

        # Xóa dữ liệu cũ trong Treeview
        for item in treeTimKiem.get_children():
            treeTimKiem.delete(item)

        # Hiển thị sách từ API
        for i, sach in enumerate(_sach_online_results_cache):
            treeTimKiem.insert("", tk.END, iid=str(i), values=(i + 1, sach.ten, sach.tacGia, sach.namXB))

    def laySachDaChon():
        """Lấy sách đã chọn từ danh sách tìm kiếm và lưu vào hệ thống"""
        selected_items_iids = treeTimKiem.selection() 
        if not selected_items_iids:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một sách để thêm!")
            return

        sach_chon_list = []
        id_max_hien_tai = max([sach.id for sach in DANHSACH_DanhSachCacSach.docFileJson()], default=0)

        for iid in selected_items_iids:
            index_in_cache = int(iid)
            sach_duoc_chon = _sach_online_results_cache[index_in_cache]

            id_max_hien_tai += 1

            sachMoi = Sach(
                id=id_max_hien_tai,
                ten=sach_duoc_chon.ten,
                tacGia=sach_duoc_chon.tacGia,
                namXB=sach_duoc_chon.namXB,
                duongDan=sach_duoc_chon.duongDan 
            )
            sach_chon_list.append(sachMoi)

        # Lưu sách đã chọn vào JSON
        DANHSACH_DanhSachCacSach.DsSachObject.extend(sach_chon_list)
        DANHSACH_DanhSachCacSach.luuVaoFileJson()

        # Cập nhật danh sách chính trong giao diện chính
        CHUCNANG_Method.taiSachLenTreeView(tree)

        messagebox.showinfo("Thành công", f"Đã thêm {len(sach_chon_list)} sách vào kho sách!")
        timSachWindow.destroy()

    ttk.Button(timSachFrame, text="Tìm sách online", command=timVaHienThi).pack(side="top", pady=10, padx=10)
    ttk.Button(timSachFrame, text="Thêm vào kho sách", command=laySachDaChon).pack(side="top", pady=10, padx=10)


