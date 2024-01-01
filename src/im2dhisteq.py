import numba
import numpy as np
import sys
import os

file_path = os.path.realpath(__file__)
src_dir = os.path.dirname(file_path)
library_path = os.path.join(src_dir, 'go_libs', 'library.so')
if os.path.exists(library_path):
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


def vid2dhisteq(image, w_neighboring=6, Wout_list=np.zeros((10))):
    h, w = image.shape

    V = image
    CDFxn_transform, H_in = transformer(image, w_neighboring=w_neighboring)

    Win = H_in.shape[0]
    Gmax = 1.5  # 1.5 .. 2
    Wout = min(255, Gmax * Win)
    if np.where(Wout_list > 0)[0].size == Wout_list.size:
        Wout = (np.sum(Wout_list) + Wout) / (1 + Wout_list.size)

    F = V.ravel().astype(np.uint16)
    Ftilde = Wout * CDFxn_transform[F]

    Madj = np.mean(V) - np.mean(Ftilde)
    Ftilde = Ftilde + Madj

    Ftilde = np.where(Ftilde >= 0, Ftilde, np.zeros_like(Ftilde))
    Ftilde = np.where(Ftilde <= 255, Ftilde, 255 * np.ones_like(Ftilde))
    Ftilde = Ftilde.astype(np.uint8)

    image_equalized = Ftilde.reshape(h, w)

    return image_equalized, Wout
