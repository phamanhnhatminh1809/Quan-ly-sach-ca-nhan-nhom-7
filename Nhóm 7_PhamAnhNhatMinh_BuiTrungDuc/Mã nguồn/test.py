from pdf2image import convert_from_path
import os
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
import re
duongDan = "https://openlibrary.org/works/OL2908639W"

def layAnhBiaTuCache(duongDanToiAnhCache):
    try:
        anhBiaTuPdf = Image.open(duongDanToiAnhCache)

        anhBiaPILImage = anhBiaTuPdf.resize((400, 500), Image.Resampling.NEAREST)
        anhBiaImageTk = ImageTk.PhotoImage(anhBiaPILImage)
        return anhBiaImageTk
    except Exception as e:
        print(e)

def luuAnhBiaVaoCache(anhBia, duongDanToiAnhCache):
    try:
        anhBia[0].save(duongDanToiAnhCache, "PNG")
    except Exception as e:
        print(e)



def layAnhBiaTuAPI(duongDanToiLinkSach):
    def thayTheKyTu(chuoi, kyTuMoi, viTri):
        return chuoi[:viTri] + kyTuMoi + chuoi[viTri+1:]
    tenSachTrongDuongDan = duongDanToiLinkSach[30:]
    duongDanToiAnhCache = os.path.join("Cache", f"{tenSachTrongDuongDan}.png")

    if not os.path.exists(duongDanToiAnhCache):
        reponse = requests.get(duongDanToiLinkSach)
        soup = BeautifulSoup(reponse.text, 'html.parser')
        theChuaAnh = soup.find("div", class_="SRPCover bookCover")
        linkAnhBia = theChuaAnh.find('a')['href']
        linkAnhBia = "https:" + linkAnhBia
        linkAnhBia = thayTheKyTu(linkAnhBia, "M", -5)

        taiAnh = requests.get(linkAnhBia)
        anhBia = Image.open(BytesIO(taiAnh.content))
        anhBia = anhBia.resize((300, 400), Image.NEAREST)
        luuAnhBiaVaoCache(taiAnh, duongDanToiAnhCache)
    
    return layAnhBiaTuCache(duongDanToiAnhCache)

print(layAnhBiaTuAPI(duongDan))