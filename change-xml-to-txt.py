import os
import glob
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import re
import math



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

# 小数点以下6桁にする関数
def checkF(num):
        if(len(num) < 8):
                # 桁数を取得する．
                count = 8 - int(len(num))
                i = 0
                # 8桁に足りない分だけ，0を後ろに付け足す．
                for i in range(count):
                        num += "0"
                return num    
        else:
                return num   



# =============================================================================
# =============================================================================

# labelingのpredefined_classes.txtを読み込み
messagebox.showinfo("クラスデータの取得", "labelingのclasses.txtを選択してください．")
path = gettxt()
f = open(path, 'r')


# 各行のラベルをリスト化（まだ，改行の/nが含まれている）
class_sample = f.readlines()
# /nを削除する．
# ここで，ラベリングのクラスのリスト化が終了した．
labeling_classes = [item.strip() for item in class_sample]
print(labeling_classes)


# xmlファイルのあるディレクトリを選択する．
# メッセージの表示
messagebox.showinfo("フォルダの選択", "xmlファイルがあるフォルダを選択してください．")
# xmlファイルがあるディレクトリパスを取得する
input_dir = getpath()
#input_dir = "D:\sample2"
# txtファイルの保存先を設定する．（今は同じディレクトリに保存）
output_dir = input_dir


# xmlファイル（元データ）の削除確認
# res = yesならxmlを削除，noなら そのままにする．
res = messagebox.askquestion("確認", "xmlファイルを削除しますか？")



files = input_dir
# 選択したフォルダ内のxmlファイルのパスをリストに保存する．
files = glob.glob(input_dir + "/*.xml")
# 表示して，確認する
for file in files:
        # ファイル名を表示する．
        print(file)
        # xmlファイルの文字列を読み込む．
        f = open(file, encoding="utf8", errors='ignore')
        # 文字列をxmlに保存する．
        xml = f.read()
        f.close
        #print(xml)



        # 画像の横幅と縦幅の取得
        ImgWidth = int(re.search('(?<=<width>).*(?=\</width>)', xml).group())
        ImgHeight = int(re.search('(?<=<height>).*(?=\</height>)', xml).group())


        #
        #それぞれのデータをリスト化する
        #

        # nameデータのリスト化
        Name_list = []
        # クラスの名前（name）を全て取得
        for name in re.findall('(?<=<name>).*(?=\</name>)', xml):
                Name_list.append(name)
        #print(Name_list)

        # xminデータのリスト化
        xmin_list = []
        for xmin in re.findall('(?<=<xmin>).*(?=\</xmin>)', xml):
                xmin_list.append(xmin)
        #print(xmin_list)

        # yminデータのリスト化
        ymin_list = []
        for ymin in re.findall('(?<=<ymin>).*(?=\</ymin>)', xml):
                ymin_list.append(ymin)
        #print(ymin_list)

        # xmaxデータのリスト化
        xmax_list = []
        for xmax in re.findall('(?<=<xmax>).*(?=\</xmax>)', xml):
                xmax_list.append(xmax)
        #print(xmax_list)

        # ymaxデータのリスト化
        ymax_list = []
        for ymax in re.findall('(?<=<ymax>).*(?=\</ymax>)', xml):
                ymax_list.append(ymax)
        #print(ymax_list)



        # ----------ここまでで，必要なデータのリスト化は完了----------#




        # 小数点以下の桁数を選択
        f = 6

        #-----txtの作成-----#


        # パスの指定
        path = output_dir
        # パス文字からxmlファイルネームを取得
        xmlFileName = os.path.basename(file)
        # 確認        
        # print(xmlFileName)

        # txtファイルパスの作成
        # ~~.xmlを~~.txtに変更
        txtFileName = file.replace(".xml", ".txt")
        # txtファイルの作成
        f = open(txtFileName, 'w')



        # ----------データの計算----------#



        #int x, X, y, Y, Width, widthRate, Height, HeightRate

        for i in range(len(Name_list)):
                # データの計算(以下，それぞれのデータ)
                # label, X, Y, width, height

                # X,Yは画像に対する割合らしい．そのため，4K画像の場合は
                # xを横幅（3840），yを縦幅（2160）で除す．
                x = (int(xmin_list[i]) + int(xmax_list[i])) /2
                X = round(x / float(ImgWidth), 6)
                y = (int(ymin_list[i]) + int(ymax_list[i])) /2
                Y = round(y / float(ImgHeight), 6)
                # 横幅を求める
                Width = int(xmax_list[i]) - int(xmin_list[i])
                WidthRate = round(Width / ImgWidth, 6)
                # 縦幅を求める
                Height = int(ymax_list[i]) - int(ymin_list[i])
                HeightRate = round(Height / ImgHeight, 6)

                # txtの1文字目の調査
                segmented = ""
                for label in labeling_classes:
                        if Name_list[i] == label:
                                segmented = labeling_classes.index(label)


                f.write(str(segmented) + " " + checkF(str(X)) + " " + checkF(str(Y)) + " " + checkF(str(WidthRate)) + " "+ checkF(str(HeightRate)))

                if i != len(Name_list):
                        f.write("\n")
        
        f.close()

        # xmlファイルの削除
        if(res == "yes"):
                os.remove(file)