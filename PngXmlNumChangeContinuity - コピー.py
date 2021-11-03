import os
import glob
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import re
import math
import shutil
import tkinter.simpledialog as simpledialog



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
messagebox.showinfo("フォルダの選択", "連番にしたいpngとxmlがあるフォルダを選択してください．")
# xmlファイルがあるディレクトリパスを取得する
input_dir = getpath()

inputdata = simpledialog.askstring("Input Box", "連番の前にくるnameを入力してください",)
print("simpledialog",inputdata)

files = os.listdir(input_dir)
files2 = os.listdir(input_dir)

p = 1
x = 1

image = "image"
xml = "xml"
check1 = ""
check2 = ""

for line in files:
        for line2 in files2:
                #print(line)
                if ".png" in line:
                        check1 = line.replace(".png", "")
                        if ".xml" in line2:
                                check2 = line2.replace(".xml", "")
                                if check1 == check2:

                                        inputimg = input_dir + "/" + line
                                        if p < 10:
                                                outputimg= input_dir + "/" + inputdata + "0000" + str(p) + ".png"
                                        elif 10 <= p and p < 100:
                                                outputimg= input_dir + "/" + inputdata + "000" + str(p) + ".png"
                                        elif 100 <= p and p < 1000:
                                                outputimg= input_dir + "/" + inputdata + "00" + str(p) + ".png"
                                        else:
                                                outputimg= input_dir + "/" + inputdata + "0" + str(p) + ".png"
                                        shutil.move(inputimg, outputimg)
                                        print(inputimg + "=>" + outputimg)
                                        p += 1

                                        inputxml = input_dir + "/" + line2
                                        if x < 10:
                                                outputxml= input_dir + "/" + inputdata + "0000" + str(x) + ".xml"
                                        elif 10 <= x and x < 100:
                                                outputxml= input_dir + "/" + inputdata + "000" + str(x) + ".xml"
                                        elif 100 <= x and x < 1000:
                                                outputxml= input_dir + "/" + inputdata + "00" + str(x) + ".xml"
                                        else:
                                                outputxml= input_dir + "/" + inputdata + "0" + str(x) + ".xml"
                                        #outputimg= input_dir + "/" + inputdata + str(x) + ".xml"
                                        shutil.move(inputxml, outputxml)
                                        print(inputxml + "=>" + outputxml)
                                        x += 1



