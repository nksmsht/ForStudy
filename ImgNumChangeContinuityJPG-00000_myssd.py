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
#
# messagebox.showinfo("フォルダの選択", "連番にしたい画像ファイル（だけ）があるフォルダを選択してください．")
# xmlファイルがあるディレクトリパスを取得する
input_dir = getpath()
files = os.listdir(input_dir)
files = sorted(files)

i = 1
image = "image"

for line in files:
        print(line)
       
        inputimg = input_dir + "/" + line
        outputimg= input_dir + "/" + image + str('{0:05d}'.format(i)) + ".jpg"

        shutil.move(inputimg, outputimg)
        i += 1