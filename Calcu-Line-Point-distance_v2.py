
import os
import glob
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import re
import math
import shutil
import tkinter.simpledialog as simpledialog
import cv2
import csv
import numpy as np
from PIL import Image
import datetime
import sys


# パス取得の関数
def getpath():
        idir = 'PC'
        file_path = tkinter.filedialog.askdirectory(initialdir = idir)
        return file_path

def getpng():
        typ = [('pngファイル','*.png')] 
        dir = 'PC'
        fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir) 
        return fle

def getcsv():
        typ = [('CSVファイル','*.csv')] 
        dir = 'PC'
        fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir) 
        return fle

# opencv:フルスクリーン表示したりしなかったりする関数(確認のためだけにつかう　ほぼいらん)
def cv2_imshow_fullscreen(winname, img, flag_fullscreen):
    if flag_fullscreen:
        cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
        #cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(winname, img)
    cv2.waitKey(0)



# =============================================================================
# =============================================================================

messagebox.showinfo("csvファイルの選択", "1)フレーム番号\n2)カメラX座標\n3)カメラY座標\n4)選手位置X座標\n5)選手位置Y座標\n6)射影変換による選手位置X座標\n7)射影変換による選手位置Y座標\nのcsvファイルを選択してください．")
input_csv = getcsv()
if input_csv == "":
    sys.exit()

messagebox.showinfo("保存先の選択", "保存先のフォルダを選択してください．")
output_dir = "E:/testdir10_PL-distance(s)"#getpath()
if output_dir == "":
    sys.exit()


# csvファイルのリスト化
# 項目（基準の広告, 画像上の距離）
with open(input_csv, encoding="utf8", errors='ignore') as f:
        reader = csv.reader(f)
        l = [row for row in reader]


# 新たなcsvファイルを作成 ファイル名は日付になる
now = datetime.datetime.now()
filename = output_dir + "/all_" + now.strftime("%y%m%d_%H%M%S") + ".csv"
f = open(filename, "w")
writer = csv.writer(f)


# 処理の可視化のためのカウント
count = 0
# 記入スイッチ
write_checker = "OFF"

for L in l:
    print(L)

for L in l:
    print(count)
    """
    # f[1]を指定する際のエラー対策
    if len(f) <= 1:
        for i in range(6):
            f.append("EMPTY")"""
    
    # 計算のために値を代入（直線a(x1, y1)b(x2,y2)と点c(x3, y3)の距離を計算）
    if (L[1] != "" and L[5] != ""):
        x1 = int(L[1])
        y1 = int(L[2])
        x2 = int(L[3])
        y2 = int(L[4])
        x3 = int(L[5])
        y3 = int(L[6])

        u = np.array([x2 - x1, y2 - y1])
        v = np.array([x3 - x1, y3 - y1])
        LLL = abs(np.cross(u, v) / np.linalg.norm(u))
        #print L
        write_checker = "ON"


    if(write_checker == "ON"):
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow((count, L[1], L[2], L[3], L[4], L[5], L[6], LLL))

            write_checker = "OFF"
    
    else:
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow((count,  L[1], L[2], L[3], L[4], L[5], L[6]))

    count +=1

f.close
print("フレーム数は合計" + str(count) + "フレームでした．")

