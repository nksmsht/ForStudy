import os
import glob
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import re
import math
import shutil
import csv
import pprint
import pandas as pd
import sys



# パス取得の関数
def getpath():
        idir = 'PC'
        file_path = tkinter.filedialog.askdirectory(initialdir = idir)
        return file_path

def getcsv():
        typ = [('csvファイル','*.csv')] 
        dir = 'PC'
        fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir) 
        return fle


# =============================================================================
# =============================================================================

# pathを2つ選択させる
messagebox.showinfo("フォルダの選択", "csvファイル（広告）のあるフォルダを選択してください．")
input_dir1 = getpath()
if input_dir1 == "":
    sys.exit()
messagebox.showinfo("フォルダの選択", "csvファイル（person）のあるフォルダを選択してください．")
input_dir2 = getpath()
if input_dir2 == "":
    sys.exit()

# path1と2が同じ場合は強制終了
if input_dir1 == input_dir2:
    print("選択した2つのpathが同じ?!")
    sys.exit()
    

# ファイル内すべてをリスト化
files1 = os.listdir(input_dir1)
files1 = sorted(files1)
files2 = os.listdir(input_dir2)
files2 = sorted(files2)
#print(files)


# 作成先を設定する．
messagebox.showinfo("フォルダの選択", "作成先のフォルダを選択してください．")
output_dir = getpath()
if output_dir == "":
    sys.exit()




# 指定したフォルダのパスを取得
for csvfile1 in files1:
        if ".csv" in csvfile1:
                for csvfile2 in files2:
                        if ".csv" in csvfile2:
                                if str(csvfile1) == str(csvfile2):
                                        print(csvfile1)

                                        # csvファイルの絶対パスを作成
                                        path1 = input_dir1 + "/" + csvfile1
                                        path2 = input_dir2 + "/" + csvfile2

                                        #csvファイル内の全データをリスト化（行と列の2次元配列）
                                        l = []
                                        with open(path1) as f:
                                                reader = csv.reader(f)
                                                l = [row for row in reader]
                                        #print(*l, sep="\n")

                                        r = []
                                        with open(path2) as f:
                                                reader = csv.reader(f)
                                                r = [row for row in reader]
                                        #print(*r, sep="\n")

                                        #tmpリストを作って，csv1と2のデータをappend
                                        tmp = []                
                                        for line1 in l:
                                                tmp.append(line1)
                                        for line2 in r:
                                                tmp.append(line2)        
                                        #print(*tmp, sep="\n")
                                        #print("\n" + "\n" + "\n")

                                        # 新たなcsvファイルを作成して保存
                                        newcsv = output_dir + "/" + csvfile1
                                        file = open(newcsv, "w", newline="")
                                        w = csv.writer(file)
                                        for row in tmp:
                                                w.writerow(row)
                                        file.close()
                
