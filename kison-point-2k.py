
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


messagebox.showinfo("画像の選択", "フィールド平面図を選択してください．")
input_img = getpng()
if input_img == "":
    sys.exit()

messagebox.showinfo("フレーム内の選手位置csvファイルの選択", "フレーム内の選手位置csvファイルを選択してください．")
input_csv = getcsv()
if input_csv == "":
    sys.exit()

messagebox.showinfo("保存先の選択", "保存先のフォルダを選択してください．")
output_dir = getpath()
if output_dir == "":
    sys.exit()





# csvファイルのリスト化
# 項目（基準の広告, 画像上の距離）
with open(input_csv, encoding="utf8", errors='ignore') as f:
        reader = csv.reader(f)
        l = [row for row in reader]
# 確認
#print("フレーム内の選手位置csvファイルの全ての行のリスト化が終了-l")
#print(*l, sep="\n")




# 描画開始!! ############################################################################################
# 画像をnumpy配列に変換 ###

# カメラ位置の(x,y)座標を作成

count = 1
for f in l:
    # f[1]を指定する際のエラー対策
    if len(f) <= 1:
        for i in range(2):
            f.append("EMPTY")
    print(count)
    #print(*f, sep="\n")

    field_img = np.array(Image.open(str(input_img)))
    height = field_img.shape[0]
    width = field_img.shape[1]
#------------------------------------------------------------------------------------------------------------------------------

    #既存の手法による選手位置の描画（円）
    if f[1] != ("" and "EMPTY"):
        X = int(f[1])
        Y = int(f[2])
        cv2.circle(field_img, (X, Y), 40, (0,0,255), thickness=30, lineType=cv2.LINE_4)
        

    imgName = output_dir + "/image" + str('{0:05d}'.format(count)) + ".jpg"
    field_img = cv2.resize(field_img, (int(width*0.285), int(height*0.285)))
    cv2.imwrite(imgName, field_img)

#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
    del field_img
    count +=1
