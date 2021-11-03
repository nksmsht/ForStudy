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
import sys

import cv2
import numpy as np
from matplotlib import pyplot as plt
import tkinter.simpledialog as simpledialog

# ポリゴンは諦めた
#import shapely
#from shapely.geometry import Point
#from shapely.geometry.polygon import Polygon


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



# 変換前の対応点（真上から見た画像）
points1 = [[1927, 842], [2940, 976], [2032, 1284], [982, 1002]] 
# 変換後の対応点（斜めの画像）
points2 = [[1295, 1263], [2737, 1263], [2737, 2667], [1295, 2667]]  
# 1と2から変換行列Mを求める
M = cv2.getPerspectiveTransform(np.float32(points1), np.float32(points2))  
#print(M)

# ポリゴンの代わりに平面図上の領域の最大と最小を設定
# 射影変換後に領域内かどうかを確認する
x_max = 6319
x_min = 290
y_max = 3469
y_min = 460

new_x = 0
new_y = 0

# csvファイルのカウント
csv_count = 0

# csvファイルのあるディレクトリを選択
# メッセージの表示
messagebox.showinfo("フォルダの選択", "csvファイルがあるフォルダを選択してください．")
# csvファイルがあるディレクトリパスを取得する
input_dir = getpath()
if input_dir == "":
    sys.exit()
# ファイル内すべてをリスト化
files = os.listdir(input_dir)
# 昇順に並び替え（念のために）
files = sorted(files)

# 作成先を設定する．
messagebox.showinfo("フォルダの選択", "作成先のフォルダを選択してください．")
output_dir = getpath()
if output_dir == "":
    sys.exit()

# csvファイルを作成 ファイル名は入力
inputdata = simpledialog.askstring("Input Box", "作成するファイル名を入力してください",)
print("simpledialog",inputdata)
FILE_NAME = inputdata
if FILE_NAME == "":
    sys.exit()

filename = output_dir + "/" + FILE_NAME + ".csv"
f = open(filename, "w")
writer = csv.writer(f)

write_checker = "OFF"


# 指定したフォルダのパスを1つずつ使用
for csvfile in files:
    
    # csvファイルか確認
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

            for list1 in l:
                    list1[4] = int(list1[4].replace("%", ""))
            #print(l)
            #np.sort(l, axis=4)
            l = sorted(l, reverse=True, key=lambda x: x[4])
            #print(l)

            # 分類確率の高い順にcsvファイル内の行を並び替え => 最も分類確率の高いpersonを選手として扱う
 
            
            for L in l:
                
                # 射影変換 #################################################################

                # personだけ射影変換
                if (L[1] == "person" and write_checker == "OFF"):

                    # 撮影者が画面左端に長時間映ってしまったので，if500<で取り除く
                    if (500 < int(L[5])):
                        # 変換したい座標値(x, y)を入力
                        x = int((int(L[6])+int(L[5]))/2)
                        y = int(L[8])
                        pts = np.float32([x, y]).reshape(-1,1,2)

                        # 座標値の変換
                        pts_trains = cv2.perspectiveTransform(pts, M)
                        #print(pts_trains)


                        # pts_trains（3次元配列）からx,y座標を個別に取り出す
                        new_x = int(pts_trains[0][0][0])
                        new_y = int(pts_trains[0][0][1])
                        #print (new_x)
                        #print (new_y)

                # 求めた平面図上の座標がポリゴン内のものか確認
                if (x_min < new_x and new_x < x_max and y_min < new_y and new_y < y_max):
                    person_X = new_x
                    person_Y = new_y
                    write_checker = "ON"
                
                ############################################################################

            # ファイルに記入
            if write_checker == "ON":
                    with open(filename, "a", newline="") as f:
                            writer = csv.writer(f)
                            writer.writerow([csv_count, person_X, person_Y])
            else:
                    with open(filename, "a", newline="") as f:
                            writer = csv.writer(f)
                            writer.writerow([csv_count])

            write_checker = "OFF"
            csv_count += 1

f.close()
print("csvファイルの合計は" + str(csv_count) + "個でした．")