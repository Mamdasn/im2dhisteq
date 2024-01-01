import numba
import numpy as np
from go_libs import dll_path_finder


if dll_path_finder.get_dll_path():
    from go_libs import go_lib

    im2dhist = go_lib.get_twodhist_parallel
    imhist = go_lib.get_imhist
else:
    from im2dhist import im2dhist as im2dhist
    from im2dhist import imhist


def transformer(image, w_neighboring=6):
    [h, w] = image.shape
    image_hist = imhist(image)

    H_in = im2dhist(image, w_neighboring)

    CDFx = np.cumsum(np.sum(H_in, axis=0))  # Kx1

    # normalizes CDFx
    CDFxn = CDFx / CDFx[-1]

    PDFxn = np.zeros_like(CDFxn)
    PDFxn[0] = CDFxn[0]
    PDFxn[1:] = np.diff(CDFxn)

    X_transform = np.zeros((256))
    X_transform[np.where(image_hist > 0)] = PDFxn.copy()
    CDFxn_transform = np.cumsum(X_transform)
    return CDFxn_transform, H_in


def im2dhisteq(image, w_neighboring=6):
    [h, w] = image.shape
    V = image.copy()
    CDFxn_transform, _ = transformer(image, w_neighboring=w_neighboring)
    bins = np.arange(256)
    # use linear interpolation of cdf to find new pixel values
    image_equalized = np.floor(
        np.interp(V.flatten(), bins, 255 * CDFxn_transform).reshape(h, w)
    ).astype(np.uint8)

    return image_equalized


@numba.njit()
def apply_transformer_and_mean_brightness(image, H_in, Wout_list, CDFxn_transform):
    h, w = image.shape
    Win = H_in.shape[0]
    Gmax = 1.5  # 1.5 .. 2
    Wout = min(255, Gmax * Win)

    if np.all(Wout_list > 0):
        Wout = (np.sum(Wout_list) + Wout) / (Wout_list.size + 1)

    F = image.ravel().astype(np.uint16)
    Ftilde = np.empty_like(F, dtype=np.float32)

    for i in range(F.size):
        Ftilde[i] = Wout * CDFxn_transform[F[i]]

    sum_image = 0.0
    sum_Ftilde = 0.0
    for i in range(F.size):
        sum_image += image.ravel()[i]
        sum_Ftilde += Ftilde[i]

    mean_image = sum_image / F.size
    mean_Ftilde = sum_Ftilde / F.size

    Madj = mean_image - mean_Ftilde

    for i in range(Ftilde.size):
        Ftilde[i] = Ftilde[i] + Madj
        if Ftilde[i] < 0:
            Ftilde[i] = 0
        elif Ftilde[i] > 255:
            Ftilde[i] = 255

    image_equalized = Ftilde.astype(np.uint8).reshape(h, w)

    return image_equalized, Wout


def vid2dhisteq(image, w_neighboring=6, Wout_list=np.zeros((10))):
    CDFxn_transform, H_in = transformer(image, w_neighboring=w_neighboring)
    image_equalized, Wout = apply_transformer_and_mean_brightness(
        image, H_in, Wout_list, CDFxn_transform
    )

    return image_equalized, Wout
