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
per = 80

# 一定のクラス分類率以上の広告リスト
KK80list = []
# 一定のクラス分類率以下の広告リスト
KK79list = []
# personのリスト
personlist = []
# csvに出力する広告クラス
KKclass = ""
# csvに出力する広告を単位とした距離
KK_per_distance = 0
# 広告のX座標を記憶
KKXzahyou = float(0)
# 人物のX座標を記憶
personXzahyou = 0
# 広告とpersonの距離
KK_person_distance = 0

KK_width = 0

# csvファイルのあるディレクトリを選択
# メッセージの表示
messagebox.showinfo("フォルダの選択", "csvファイルがあるフォルダを選択してください．")
# csvファイルがあるディレクトリパスを取得する
input_dir = getpath()
# ファイル内すべてをリスト化
files = os.listdir(input_dir)
files = sorted(files)



# 作成先を設定する．
messagebox.showinfo("フォルダの選択", "作成先のフォルダを選択してください．")
output_dir = getpath()



# csvファイルを作成 ファイル名は日付になる
now = datetime.datetime.now()
filename = output_dir + "/all_" + now.strftime("%y%m%d_%H%M") + ".csv"
f = open(filename, "w")
writer = csv.writer(f)



# 指定したフォルダのパスをcsvfileに入れる
for csvfile in files:
        #print(csvfile) 

        #l.clear()
        #personXzahyou = 0
        #KKXzahyou = 0
        #ersonlist.clear()
        KK80list.clear()
        KK79list.clear()
        #KK_person_distance = 0
        #KK_per_distance = 0
        #KKclass = ""
        #KK_width = 0
        #name2 = 0             

        # ファイルパスがcsv
        # ファイルのなら処理
        if ".csv" in csvfile:
                # csvファイルの絶対パスを作成
                path = input_dir + "/" + csvfile
                print(path)

                #csvファイル内の全データをリスト化
                with open(path) as f:
                        reader = csv.reader(f)
                        l = [row for row in reader]
                
                l = list(filter(None, l))
                # personの面積をnameにappendするためのカウント
                person_count = 0

                # リスト内をさらにリスト化（行単位にリスト化される。）
                # nameよりclassの方がよかったかもしれません．
                if len(l) != 0:
                        # 人物の場合、一番大きい窓枠を使用する。
                    for name in l:
                        if (name[1] == person):
                                #personlist.append(name)
                                height = int(name[8]) - int(name[7])
                                width = int(name[6]) - int(name[5])
                                area = height * width
                                # nameにaeraをくっつけてからpersonlistにくっつける
                                name2 = name
                                name2.append(area)
                                personlist.append(name2)
                                person_count += 1
                        
                        # 広告の場合、"最も人物に近い確率90%以上"のもの or 90未満で最も確率の高い->近いもの
                        elif (name[1] == "R" or "P" or "M" or "O" or "H"):
                                # %の削除
                                # 確率per以上・以下で分類
                                # per以上ならover，以下ならunderにappend
                                name[4] = int(name[4].replace("%", ""))
                                if(name[4] < per):
                                        KK79list.append(name)
                                elif(name[4] >= per):
                                        KK80list.append(name)
                                else:
                                        print("", end="")
                        else:
                                print("", end="")
                


                # 人物が写っていない場合は，次のパスへ

                # 人物が複数いる場合は，リストを降順に並び替え（検出枠の面積が最も大きいものを選手とする。）
                # リスト内の空の要素を削除
                personlist = list(filter(None, personlist))
                if len(personlist)!=0:
                        personlist = sorted(personlist, reverse=True, key=lambda x: x[9])

                        # csvファイルの行リスト内を並べ替え
                        # 一定の確率（クラス分類）以上ある矩形はpersonに近いものから降順に整理
                        # personの矩形のX座標中央の値を取得
                        personXzahyou = (int(personlist[0][6]) + int(personlist[0][5])) / 2
                        

                        # 広告りすと2種類が無い場合は終了
                        if len(KK80list)==0 and len(KK79list)==0:
                            print("", end="")


                        # per%以上の広告リストがある時
                        elif len(KK80list)!=0 and len(personlist)!=0:
                                # personの検出枠のX座標中央の値に対して、最も近くに位置する広告を探索
                                # adX_listにadのX座標中点を計算し結合
                                KK80count = 0
                                KK80list2 = list(KK80list)
                                KK80list3 = list(KK80list)
                                KK80list.clear
                                for j in KK80list2:
                                        # X座標上での人物と広告の絶対値を算出


                                        #print(j)

                                        KKXzahyou = (int(j[6]) + int(j[5]))/2



                                        KK_person_distance = abs(KKXzahyou - personXzahyou)
                                        KK80tmp = KK80list3[KK80count].append(KK_person_distance)
                                        KK80list.append(KK80tmp)
                                        KK80count +=1

                                # 絶対値（人物と広告の距離）を昇順に整理
                                if len(KK80list)>=2:
                                        # 念のため空のリスト要素を削除
                                        KK80list = list(filter(None, KK80list))
                                        # リストの9番目の要素（personとの距離の絶対値で昇順）
                                        KK80list = sorted(KK80list, reverse=False, key=lambda x: x[9])

                                KK_width = int(KK80list[0][6]) - int(KK80list[0][5])
                                KK_per_distance = KK80list[0][9] / KK_width
                                # 人物X座標中央が広告よりも左なら負の値に変更
                                if (int(personlist[0][6]) + int(personlist[0][5])) <= (int(KK80list[0][6]) + int(KK80list[0][5])):
                                        KK_per_distance = KK_per_distance * -1
                                # クラスを決定
                                KKclass = KK80list[0][1]


                        # 80%以下しかないとき，クラス分類率を降順に並べ替え
                        elif len(KK79list)!=0 and len(personlist)!=0:
                                KK79list = sorted(KK79list, reverse=True, key=lambda x: x[4])
                                # 広告のX座標の横幅・広告と人物の中央間距離を計算
                                # 第一候補の広告のX座標中央を算出

                                # 第一候補の広告と人物の距離の絶対値を算出
                                KK_width = int(KK79list[0][6]) - int(KK79list[0][5])
                                KK_person_distance = abs((int(KK79list[0][6]) + int(KK79list[0][5]))/2 - personXzahyou)
                                KK_per_distance = KK_person_distance / KK_width
                                # 人物X座標中央が広告よりも左なら負の値に変更
                                if (int(personlist[0][6]) + int(personlist[0][5])) <= (int(KK79list[0][6]) + int(KK79list[0][5])):
                                        KK_per_distance = KK_per_distance * -1
                                # クラスを決定
                                KKclass = KK79list[0][1]


                        else:
                                
                                print("", end="")


                # csvファイルに行で書き込み
                if KKclass != "":
                        with open(filename, "a", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerow([csv_count, KKclass, KK_per_distance])
                else:
                        with open(filename, "a", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerow([csv_count])

                csv_count += 1
        l.clear()
        personXzahyou = 0
        KKXzahyou = 0
        personlist.clear()
        KK80list.clear()
        KK79list.clear()
        KK_person_distance = 0
        KK_per_distance = 0
        KKclass = ""
        KK_width = 0
        name2 = 0


# csvファイルを閉じる
f.close()
print("csvファイルの合計は" + str(csv_count) + "個でした。")













        





