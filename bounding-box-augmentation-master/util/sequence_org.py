import imgaug as ia
from imgaug import augmenters as iaa


def get():
    def sometimes(aug): return iaa.Sometimes(0.5, aug)

    return iaa.Sequential(
        [            
            sometimes(iaa.Affine(
                # scale images to 80-120% of their size, individually per axis
                scale={'x': (0.8, 1.2), 'y': (0.8, 1.2)},
                # translate by -20 to +20 percent (per axis)
                translate_percent={'x': (-0.2, 0.2), 'y': (-0.2, 0.2)},
                rotate=(-45, 45),  # rotate by -45 to +45 degrees
                shear=(-16, 16),  # shear by -16 to +16 degrees
                # use nearest neighbour or bilinear interpolation (fast)
                order=[0, 1],
                # if mode is constant, use a cval between 0 and 255
                cval=(0, 255),
                # use any of scikit-image's warping modes (see 2nd image from the top for examples)
                mode=ia.ALL
            )),
        ],
        random_order=True
    )
