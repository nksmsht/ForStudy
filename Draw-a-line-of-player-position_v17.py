
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


#messagebox.showinfo("画像の選択", "フィールド平面図を選択してください．")
#input_img = "D:/testdir/field.png"
#getpng()

messagebox.showinfo("csvファイルの選択", "広告と選手の距離を広告検出枠を単位として表したcsvファイルを選択してください．")
input_csv = getcsv()
if input_csv == "":
    sys.exit()

messagebox.showinfo("広告ファイルの選択", "広告サイズのcsvファイルを選択してください．")
input_ad = getcsv()
if input_ad == "":
    sys.exit()

messagebox.showinfo("保存先の選択", "保存先のフォルダを選択してください．")
output_dir = getpath()
if output_dir == "":
    sys.exit()

inputdata = simpledialog.askstring("Input Box", "カメラ位置Xの値を入力してください",)
print("simpledialog",inputdata)
PointX = int(inputdata)
if PointX == "":
    sys.exit()

inputdata = simpledialog.askstring("Input Box", "カメラ位置Yの値を入力してください",)
print("simpledialog",inputdata)
PointY = int(inputdata)
if PointY == "":
    sys.exit()



# csvファイルのリスト化
# 項目（基準の広告, 画像上の距離）
with open(input_csv, encoding="utf8", errors='ignore') as f:
        reader = csv.reader(f)
        l = [row for row in reader]
# 確認
#print("フレーム内の選手位置csvファイルの全ての行のリスト化が終了-l")
#print(*l, sep="\n")



# csvファイル（広告）のリスト化
# 項目（広告名, 方角(時計), x1, y1, x2, y2, x中央, y中央, 幅　）
with open(input_ad, encoding="utf8", errors='ignore') as f:
        reader = csv.reader(f)
        ad = [row for row in reader]
# 広告座標のcsvファイル内の「広告名」以外をint型に変形
for i in range(5):
    for j in range(1, 9):
        ad[i][j] = int(ad[i][j])
# 確認
#print("csvファイル（広告）の全ての行のリスト化が終了-ad")
#print(*ad, sep="\n")


# フレーム内の選手位置csvファイルを1行ずつ読んで，直線を描画し，新たな画像ファイル(png)として保存．
# 画像ファイルの読み込み
#imgCV = cv2.imread(input_img)
# 確認のための画像表示　このためだけの関数あり
#cv2_imshow_fullscreen("fullscreen", imgCV , True) # フルスクリーン表示
#cv2_imshow_fullscreen("window", imgCV , False) # ウィンドウ表示



# 描画開始!! ############################################################################################
# 画像をnumpy配列に変換 ###

# カメラ位置の(x,y)座標を作成

# csvファイルを作成 ファイル名は
inputdata = simpledialog.askstring("Input Box", "作成するファイル名を入力してください",)
print("simpledialog",inputdata)
FILE_NAME = inputdata
if FILE_NAME == "":
    sys.exit()

filename = output_dir + "/" + FILE_NAME + ".csv"
f = open(filename, "w")
writer = csv.writer(f)

count = 0
for f in l:
    # f[1]を指定する際のエラー対策
    if len(f) <= 1:
        f.append("EMPTY")
        f.append("EMPTY")
    print(count)
    if f[1] == ad[0][0]:
        #------------------------------------------------------------------------------------------------------------------------------
        """広告がりそな銀行の場合"""
        line_X = ad[0][6]+int(float(ad[0][8])*float(f[2]))   #ここの1と3番目の数字を変更
        # fieldの範囲外に出たら定数に変更
        if line_X <= 0:
            line_X = 0
        elif line_X >= 6730:
            line_X = 6730
        # Y座標
        line_Y = ad[0][7]
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([count, PointX, PointY, line_X, line_Y])
    #------------------------------------------------------------------------------------------------------------------------------
        """広告がパナソニックの場合"""
    elif f[1] == ad[1][0]:
        #print(ad[0][0])
        # 線分の始まりと終わりを計算
        # スタート地点
        line_X = ad[1][6]+int(float(ad[1][8])*float(f[2]))
        if line_X <= 0:
            line_X = 0
        elif line_X >= 6730:
            line_X = 6730
        # ゴール地点
        line_Y = ad[1][7]
        # 選手位置の線分を描画
        """
        lined_img = cv2.line(field_img,                     #競技場のMAP
                            (PointX, PointY),               #カメラ位置の座標
                            (line_X,                         #ad(中央X)-ad(幅)*ad(倍率)
                            line_Y),                        #ad(中央Y)
                            (0, 255, 0),                    #線分の色
                            50)                             #線分の幅
        
        # 確認のための表示
        #cv2_imshow_fullscreen("fullscreen", lined_img , True)
        imgName = output_dir + "/image" + str('{0:05d}'.format(count)) + ".jpg"
        cv2.imwrite(imgName, lined_img)"""
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([count, PointX, PointY, line_X, line_Y])
    #------------------------------------------------------------------------------------------------------------------------------
        """広告が「三井住友銀行」(="M")の場合"""
    elif f[1] == ad[2][0]:                                    #ここの1番目の数字を変更
        #print(ad[0][0])
        # 線分の始まりと終わりを計算
        # スタート地点
        line_X = ad[2][6]+int(float(ad[2][8])*float(f[2]))   #ここの1と3番目の数字を変更
        if line_X <= 0:
            line_X = 0
        elif line_X >= 6730:
            line_X = 6730
        # ゴール地点
        line_Y = ad[2][7]                                    #ここの1番目の数字を変更
        # 選手位置の線分を描画
        """
        lined_img = cv2.line(field_img,                     #競技場のMAP
                            (PointX, PointY),               #カメラ位置の座標(最初に入力するのでそのまま)
                            (line_X,                         #ad(中央X)-ad(幅)*ad(倍率)  広告によって式が異なる
                            line_Y),                        #ad(中央Y)                  広告によって式が異なる
                            (0, 255, 0),                    #線分の色
                            50)                             #線分の幅
        
        # 確認のための結果表示
        #cv2_imshow_fullscreen("fullscreen", lined_img , True)
        imgName = output_dir + "/image" + str('{0:05d}'.format(count)) + ".jpg"
        cv2.imwrite(imgName, lined_img)  """
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([count, PointX, PointY, line_X, line_Y])
    #------------------------------------------------------------------------------------------------------------------------------
        """広告が「大阪ガス」(="O")の場合"""
    elif f[1] == ad[3][0]:                                    #ここの1番目の数字を変更
        #print(ad[0][0])
        # 線分の始まりと終わりを計算
        # スタート地点
        line_X = ad[3][6]+int(float(ad[3][8])*float(f[2]))   #ここの1と3番目の数字を変更
        if line_X <= 0:
            line_X = 0
        elif line_X >= 6730:
            line_X = 6730
        # ゴール地点
        line_Y = ad[3][7]                                    #ここの1番目の数字を変更
        # 選手位置の線分を描画
        """
        lined_img = cv2.line(field_img,                     #競技場のMAP
                            (PointX, PointY),               #カメラ位置の座標(最初に入力するのでそのまま)
                            (line_X,                         #ad(中央X)-ad(幅)*ad(倍率)  広告によって式が異なる
                            line_Y),                        #ad(中央Y)                  広告によって式が異なる
                            (0, 255, 0),                    #線分の色
                            50)                             #線分の幅
        
        # 確認のための結果表示
        #cv2_imshow_fullscreen("fullscreen", lined_img , True)
        imgName = output_dir + "/image" + str('{0:05d}'.format(count)) + ".jpg"
        cv2.imwrite(imgName, lined_img) """
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([count, PointX, PointY, line_X, line_Y])
    #------------------------------------------------------------------------------------------------------------------------------
        """広告が「阪急電鉄」(="H")の場合"""
    elif f[1] == ad[4][0]:                                    #ここの1番目の数字を変更
        #print(ad[0][0])
        # 線分の始まりと終わりを計算
        # スタート地点
        line_X = ad[4][6]+int(float(ad[4][8])*float(f[2]))   #ここの1と3番目の数字を変更
        if line_X <= 0:
            line_X = 0
        elif line_X >= 6730:
            line_X = 6730
        # ゴール地点
        line_Y = ad[4][7]                                    #ここの1番目の数字を変更
        # 選手位置の線分を描画
        """
        lined_img = cv2.line(field_img,                     #競技場のMAP
                            (PointX, PointY),               #カメラ位置の座標(最初に入力するのでそのまま)
                            (line_X,                         #ad(中央X)-ad(幅)*ad(倍率)  広告によって式が異なる
                            line_Y),                        #ad(中央Y)                  広告によって式が異なる
                            (0, 255, 0),                    #線分の色
                            50)                             #線分の幅
        
        # 確認のための結果表示
        #cv2_imshow_fullscreen("fullscreen", lined_img , True)
        imgName = output_dir + "/image" + str('{0:05d}'.format(count)) + ".jpg"
        cv2.imwrite(imgName, lined_img) """
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([count, PointX, PointY, line_X, line_Y])
    #------------------------------------------------------------------------------------------------------------------------------
        """ 東の関大広告 """
        """ 広告が「関西大学」(="K")の場合
        if f[1] == ad[5][0]:                                    #ここの1番目の数字を変更
            #print(ad[0][0])
            # 線分の始まりと終わりを計算
            # スタート地点        
            line_X = ad[4][6]-int(float(ad[4][8])*float(f[2]))   #ここの1と3番目の数字を変更
            # ゴール地点
            line_Y = ad[4][7]                                    #ここの1番目の数字を変更
            # 選手位置の線分を描画
            lined_img = cv2.line(field_img,                     #競技場のMAP
                                (PointX, PointY),               #カメラ位置の座標(最初に入力するのでそのまま)
                                (line_X,                         #ad(中央X)-ad(幅)*ad(倍率)  広告によって式が異なる
                                line_Y),                        #ad(中央Y)                  広告によって式が異なる
                                (0, 255, 0),                    #線分の色
                                50)                             #線分の幅
            
            # 確認のための結果表示
            #cv2_imshow_fullscreen("fullscreen", lined_img , True)
            imgName = output_dir + "/image" + str('{0:05d}'.format(count)) + ".jpg"
            cv2.imwrite(imgName, lined_img) """
    #------------------------------------------------------------------------------------------------------------------------------
        """else:
            imgName = output_dir + "/image" + str('{0:05d}'.format(count)) + ".jpg"
            cv2.imwrite(imgName, field_img)"""
    #------------------------------------------------------------------------------------------------------------------------------
    else:
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([count])
    #del field_img
    count +=1

f.close
print("フレーム数は合計" + str(count) + "フレームでした．")

