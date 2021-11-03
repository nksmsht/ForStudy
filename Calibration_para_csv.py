import cv2
import matplotlib.pyplot as plt
import numpy as np
import glob


square_size = 2      # 正方形の1辺のサイズ[cm]
pattern_size = (7, 7)  # 交差ポイントの数

reference_img = 20 # 参照画像の枚数

pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 ) #チェスボード（X,Y,Z）座標の指定 (Z=0)
pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
pattern_points *= square_size
objpoints = []
objpoints2 = []
imgpoints = []


TMP_FOLDER_PATH = "D:\\calibration\\tmp\\"
MTX_PATH = TMP_FOLDER_PATH + "mtx.csv"
DIST_PATH = TMP_FOLDER_PATH + "dist.csv"


# キャリブレーションCSVファイルを上書き保存する関数
def saveCalibrationFile(mtx, dist, mtx_path, dist_path):
    np.savetxt(mtx_path, K, delimiter = ',', fmt="%0.14f") #カメラ行列の保存
    np.savetxt(dist_path, d, delimiter =',', fmt="%0.14f")#歪み係数の保存




#「ファイル内全て」のパスを設定
files = glob.glob("D:\\Calibration\\img\\*")
#ファイル内の全てを読込み
i = 0
for objpoints in files:

    #画像の読込み
    capture = cv2.imread(objpoints) 

#while len(objpoints) < reference_img:
# 画像の取得
    #ret1, 　←なんかあるけど無視！ retは動画像の読込みの可否 T/F
    img = capture

    height = img.shape[0]
    width = img.shape[1]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # チェスボードのコーナーを検出
    ret1, corner = cv2.findChessboardCorners(gray, pattern_size)
    # コーナーがあれば
    print("detected coner!")
    print(objpoints2)
    print(str(len(objpoints2)+1) + "/" + str(reference_img))
    term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
    cv2.cornerSubPix(gray, corner, (5,5), (-1,-1), term)
    imgpoints.append(corner.reshape(-1, 2))   
    #appendメソッド：リストの最後に因数のオブジェクトを追加
    objpoints2.append(pattern_points)

    #cv2.imshow('image', img)
    # 毎回判定するから 200 ms 待つ．遅延するのはココ
    if cv2.waitKey(200) & 0xFF == ord('q'):
        break



ret1 = True

print("calculating camera parameter...")
# 内部パラメータを計算
ret, K, d, r, ts = cv2.calibrateCamera(objpoints2, imgpoints, gray.shape[::-1], None, None)

# 計算結果を保存
np.save("mtx", K) # カメラ行列
np.save("dist", d.ravel()) # 歪みパラメータ
# 計算結果を表示
print("RMS = ", ret)
print("mtx = \n", K)
print("dist = ", d.ravel())

###
### 以下,追加
###

# ファイルの保存
save = input("保存しますか？ -> Yes / No >>> ")
if save == "y" or "Y" or "yes" or "Yes" or "YES":
    # K=mtx, d=dist.ravel() ???
    #saveCalibrationFile(K, d, MTX_PATH, DIST_PATH)
    saveCalibrationFile(K, d, MTX_PATH, DIST_PATH)
    print("保存しました.")

print("終了します．")

