import imgaug as ia
from imgaug import augmenters as iaa
import imgaug.augmenters as iaa


def get():
    def sometimes(aug): return iaa.Sometimes(1, aug)

    # 参考url:https://githubja.com/aleju/imgaug
    return iaa.Sequential(
        [
            # 横幅を0.4~1.0倍 or 縦幅を1.0~2.0倍
            iaa.OneOf([
                sometimes([
                    iaa.ScaleX ((0.5, 1.0))
                ]),
                sometimes([
                iaa.ScaleY ((1.0, 2.0)),
                ])
            ]),

            sometimes([
                # せん断Y（±25度の範囲でランダムに加工）
                iaa.ShearY((-25.0, 25.0))
                # 回転（±5度の範囲でランダムに加工）
                #iaa.Rotate((-5.0, 5.0))
            ]),
            
        ],
        random_order=True
        )
