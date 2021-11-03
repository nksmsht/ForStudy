import os
import glob
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import re
import math
import shutil



# パス取得の関数
def getpath():
        idir = 'PC'
        file_path = tkinter.filedialog.askdirectory(initialdir = idir)
        return file_path

def gettxt():
        typ = [('テキストファイル','*.txt')] 
        dir = 'PC'
        fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir) 
        return fle



# =============================================================================
# =============================================================================

# 画像とxmlファイルのあるディレクトリを選択する．
# メッセージの表示
messagebox.showinfo("フォルダの選択", "画像とxmlファイルがあるフォルダを選択してください．")
# xmlファイルがあるディレクトリパスを取得する
input_dir = getpath()

# 移動先を設定する．（今は同じディレクトリに保存）
messagebox.showinfo("フォルダの選択", "移動先のフォルダを選択してください．")
output_dir = getpath()

# エクセルをコピーしたテキストの読み込み
#PicNumTrans_txt_path = input_dir + "/" + "PicNumTrans.txt"
#f = open(PicNumTrans_txt_path, "r")

files = os.listdir(input_dir)
files2 = os.listdir(input_dir)



for check in files:
        i = 0
        #print(check)
        for check2 in files2:
                j = 0
                #print(check2)
                if ".png" in check:
                        #print(".png")
                        if ".xml" in check2:
                                #print("xml")
                                png = check.replace(".png", "")
                                xml = check2.replace(".xml", "")
                                if png == xml:
                                        filepath = input_dir
                                        #print(input_dir)
                                        inputpng = input_dir + "/" + str(check)
                                        print(inputpng)
                                        inputxml = input_dir + "/" + str(check2)
                                        #print(inputxml)
                                        

                                        shutil.move(inputpng, output_dir)
                                        shutil.move(inputxml, output_dir)
                j += 1                
                        
