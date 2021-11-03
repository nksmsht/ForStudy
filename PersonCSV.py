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
import datetime



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


# 人物のクラス名を設定
person = "person"
# csvファイルのカウント
csv_count = 0
# 広告の検出精度の境界
#per = 90
# 人物のX座標を記憶
#person_point = 0


# csvファイルのあるディレクトリを選択
# メッセージの表示
messagebox.showinfo("フォルダの選択", "csvファイルがあるフォルダを選択してください．")
# csvファイルがあるディレクトリパスを取得する
input_dir = getpath()


# ファイル内すべてをリスト化
files = os.listdir(input_dir)
files = sorted(files)
#print(files)


# 作成先を設定する．
messagebox.showinfo("フォルダの選択", "作成先のフォルダを選択してください．")
output_dir = getpath()




# 指定したフォルダのパスを取得
for csvfile in files:
        if ".csv" in csvfile:
                #print(csvfile)
                # csvファイルの絶対パスを作成
                path = input_dir + "/" + csvfile
                print(path)

                #csvファイル内の全データをリスト化（行と列の2次元配列）
                l = []
                with open(path) as f:
                        reader = csv.reader(f)
                        l = [row for row in reader]
                #print(*l, sep="\n")

                # personでない行は削除
                tmp = []                
                #print(*l, sep="\n")
                for line in l:
                        #print(line)
                        try:
                                if line[1] == person:
                                        tmp.append(line)
                        except:
                                tmp.append("")

                        """else:
                                tmp.append("")"""
                        
                #print(*tmp, sep="\n")

                # 新たなcsvファイル（同じファイル名にすることで上書きする）を作成して保存
                newcsv = output_dir + "/" + csvfile
                file = open(newcsv, "w", newline="")
                w = csv.writer(file)
                for row in tmp:
                        w.writerow(row)
                file.close()
                del tmp
                del l
                
