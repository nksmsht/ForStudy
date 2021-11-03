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
PicNumTrans_txt_path = input_dir + "/" + "PicNumTrans.txt"
f = open(PicNumTrans_txt_path, "r")

for line in f:
        print(line)

        # ファイル名（連番を除く）
        ImgTxt = "image"

        # 移動させたいファイル（2個まで）
        # その1
        PingTxt = ".jpg"
        # その2
        #XmlTxt = ".xml"

        #for PicNum in line:
        line.replace('\n','')
        line = int(line)
        
        if line >= 100:
                line = str(line)
        elif line >= 10:
                line = str("0") + str(line)
        else:
                line = str("00") + str(line)

        
        PicPath = input_dir + "/" + ImgTxt + line + PingTxt
        #XmlPath = input_dir + "/" + ImgTxt + line + XmlTxt
        #print(PicPath)
        #print(XmlPath)
        NewPicPath = output_dir+ "/" + ImgTxt  + line + PingTxt
        #NewXmlPath = output_dir+ "/" + ImgTxt  + line + XmlTxt
        #print(NewPicPath)
        #print(NewXmlPath)
        shutil.move(PicPath, NewPicPath)
        #shutil.move(XmlPath, NewXmlPath)

