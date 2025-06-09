import os
import subprocess
import webbrowser
import requests

import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from bs4 import BeautifulSoup
from io import BytesIO

import DANHSACH_DanhSachCacSach
import DOITUONG_Sach

API_URL = "https://openlibrary.org/search.json"

# GIAODIEN_Main
def taiSachLenTreeView(tree):
    sach_list = DANHSACH_DanhSachCacSach.docFileJson()

    for item in tree.get_children():
        tree.delete(item)

    for sach in sach_list:
        tree.insert("", tk.END, values=(sach.id, sach.ten, sach.tacGia, sach.namXB))

def timSach(noiDungTimKiem, tree):
    noiDung = noiDungTimKiem.get().strip().lower()  # Lấy nội dung tìm kiếm và chuyển thành chữ thường
    if not noiDung:
        taiSachLenTreeView(tree)
        return

    # Tách tiêu chí và giá trị tìm kiếm
    tieuChi = None
    ketQua = None

    if noiDung.startswith("id:"):
        tieuChi = "id"
        ketQua = noiDung[3:].strip()
    elif noiDung.startswith("tiêu đề: "):
        tieuChi = "tiêu đề"
        ketQua = noiDung[8:].strip()
    elif noiDung.startswith("tác giả:"):
        tieuChi = "tác giả"
        ketQua = noiDung[8:].strip()
    elif noiDung.startswith("năm xuất bản: "):
        tieuChi = "năm xuất bản"
        ketQua = noiDung[13:].strip() 
    elif noiDung.startswith("nxb:"):
        tieuChi = "năm xuất bản"
        ketQua = noiDung[4:].strip()

    # Xóa tất cả các mục hiện tại trong TreeView
    for sach in tree.get_children():
        tree.delete(sach)

    # Kiểm tra và tìm kiếm trong TreeView
    found = False
    for sach in DANHSACH_DanhSachCacSach.DsSachObject:
        if tieuChi == "id" and str(sach.id) == ketQua:
            tree.insert("", tk.END, values=(sach.id, sach.ten, sach.tacGia, sach.namXB))
            found = True
        elif tieuChi == "tiêu đề" and ketQua in sach.ten.lower():
            tree.insert("", tk.END, values=(sach.id, sach.ten, sach.tacGia, sach.namXB))
            found = True
        elif tieuChi == "tác giả" and ketQua in sach.tacGia.lower():
            tree.insert("", tk.END, values=(sach.id, sach.ten, sach.tacGia, sach.namXB))
            found = True
        elif tieuChi == "năm xuất bản" and str(sach.namXB) == str(ketQua):
            tree.insert("", tk.END, values=(sach.id, sach.ten, sach.tacGia, sach.namXB))
            found = True

    # Nếu không có tiêu chí, tìm kiếm theo ký tự
    if not tieuChi:
        for sach in DANHSACH_DanhSachCacSach.DsSachObject:
            if noiDung.isdigit():
                if int(noiDung) == sach.id or (noiDung in str(sach.namXB)):
                    tree.insert("", tk.END, values=(sach.id, sach.ten, sach.tacGia, sach.namXB))
                    found = True
            else:
                if (noiDung in sach.ten.lower()) or (noiDung in sach.tacGia.lower()):
                    tree.insert("", tk.END, values=(sach.id, sach.ten, sach.tacGia, sach.namXB))
                    found = True

    if not found:
        messagebox.showinfo("Kết quả", "Không tìm thấy kết quả phù hợp")
    
def docSach(tree):
    luaChon = tree.selection()
    if not luaChon:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cuốn sách để đọc!")
        return

    idSach = int(tree.item(luaChon)["values"][0])

    for sach in DANHSACH_DanhSachCacSach.DsSachObject:
        if sach.id == idSach:
            duongDan = sach.duongDan
            break
    else:
        messagebox.showerror("Lỗi", "Không tìm thấy sách trong danh sách.")
        return

    if duongDan.startswith("https://openlibrary.org"): 
        webbrowser.open(duongDan)  
    else:
        duongDanTuyetDoi = os.path.abspath(duongDan)
        if not os.path.exists(duongDanTuyetDoi):
            messagebox.showerror("Lỗi", f"File PDF không tồn tại:\n{duongDanTuyetDoi}")
            return

        try:
            edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            if os.path.exists(edge_path):
                subprocess.Popen([edge_path, duongDanTuyetDoi])
            else:
                webbrowser.open(duongDanTuyetDoi)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở file PDF.\n{str(e)}")

def chonTuCay(event):
    pass

# GIAODIEN_Window
# xemThongTinSachWindow(frame, tree)
def layAnhBiaTuFile(duongDan):
    poppler_path = "poppler/"
    try:
        # Đọc file PDF để kiểm tra số trang
        pdf = PdfReader(duongDan)
        if len(pdf.pages) == 0:
            print("PDF không có trang nào.")
            return None

        # Chuyển trang đầu tiên thành hình ảnh
        images = convert_from_path(duongDan, first_page=1, last_page=1, dpi=200, poppler_path=poppler_path)

        # Chuyển đổi sang đối tượng PIL Image và thay đổi kích thước
        img = images[0].resize((400, 500), Image.Resampling.LANCZOS)
        
        # Tạo đối tượng ImageTk.PhotoImage
        tk_image = ImageTk.PhotoImage(img)
        return tk_image
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        return None

def layAnhBiaTuAPI(duongDan):
    def thayTheKyTu(chuoi, kyTuMoi, viTri):
        return chuoi[:viTri] + kyTuMoi + chuoi[viTri+1:]
    try:
        reponse = requests.get(duongDan)
        soup = BeautifulSoup(reponse.text, 'html.parser')
        theChuaAnh = soup.find("div", class_="SRPCover bookCover")
        linkAnhBia = theChuaAnh.find('a')['href']
        linkAnhBia = "https:" + linkAnhBia
        linkAnhBia = thayTheKyTu(linkAnhBia, "M", -5)

        taiAnh = requests.get(linkAnhBia)
        anhBia = Image.open(BytesIO(taiAnh.content))
        anhBia = anhBia.resize((300, 400), Image.NEAREST)
    except:
        return None
    return anhBia


def kiemTraSachCoLayTuAPI(path):
    if "openlibrary.org" in path:
        return True
    return False

# themSachWindow(frame, tree)
def chonFilePdf(duongDanEntry, window): 
    """Mở hộp thoại chọn file PDF và điền đường dẫn vào Entry."""
    duongDanFile = filedialog.askopenfilename(
        parent=window, 
        title="Chọn file PDF",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    if duongDanFile:
        duongDanEntry.delete(0, tk.END)
        duongDanEntry.insert(0, duongDanFile)


# xoaSachWindow(tree)
def xoaFile(path):
    if kiemTraSachCoLayTuAPI(path) == False:
        try:
            os.remove(path)
        except Exception as e:
            messagebox.showwarning("Lỗi", f"Đã xảy ra lỗi. Tên lỗi: {e}")


# timSachOnlineWindow(tree)
def timSachOnline(tu_khoa):
    """Tìm sách từ Open Library API nhưng chỉ lưu nếu người dùng chọn"""
    params = {"title": tu_khoa, "limit": 10}
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        sach_list = []
        id_max_hien_tai = max([sach.id for sach in DANHSACH_DanhSachCacSach.docFileJson()], default=0)

        for item in data.get("docs", []):
            id_max_hien_tai += 1
            sachMoi = DOITUONG_Sach.Sach(
                id=id_max_hien_tai,
                ten=item.get("title", "Không có tiêu đề"),
                tacGia=", ".join(item.get("author_name", ["Không có tác giả"])),
                namXB=item.get("first_publish_year", "Không rõ"),
                duongDan=f"https://openlibrary.org{item.get('key', '')}"
            )
            sach_list.append(sachMoi)

        return sach_list  # Trả về danh sách, không tự động lưu!
    else:
        return None
