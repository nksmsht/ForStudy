import imgaug as ia
from imgaug import augmenters as iaa


def get():
    def sometimes(aug): return iaa.Sometimes(1, aug)

    return iaa.Sequential(
        [
            sometimes(iaa.Affine(

                # 平行移動
                #translate_percent={'x': (-0.2, 0.2), 'y': (-0.2, 0.2)},
                # 回転
                rotate = (-10, 10),
                # せん断
                shear = (-20, 20),
                # 拡縮
                scale = (0.5, 2)
                #scale={'x': (0.5, 2.0), 'y': (0.5, 2.0)},   # x > 0.86y
                # 縦横比
                scaleX = (1.0, 1.5)

                
                #以下，初期
                # use nearest neighbour or bilinear interpolation (fast)
                #order=[0, 1],
                # if mode is constant, use a cval between 0 and 255
                #cval=(0, 255),
                # use any of scikit-image's warping modes (see 2nd image from the top for examples)
                #mode=ia.ALL
            ))
        ],
        random_order=True
    )
