from im2dhist import im2dhist as im2dhist
from im2dhist import imhist
import numba 
import numpy as np

@numba.njit()
def im2dhisteq(image, w_neighboring=6):
    V = image.copy()
    [h, w] = V.shape
    V_hist = imhist(V)
    H_in = im2dhist(V, w_neighboring=w_neighboring)
    CDFx = np.cumsum(np.sum(H_in, axis=0)) # Kx1

    # normalizes CDFx
    CDFxn = (255*CDFx/CDFx[-1])

    PDFxn = np.zeros_like(CDFxn)
    PDFxn[0] = CDFxn[0]
    PDFxn[1:] = np.diff(CDFxn)

    X_transform = np.zeros((256))
    X_transform[np.where(V_hist > 0)] = PDFxn.copy()
    CDFxn_transform = np.cumsum(X_transform)


    bins = np.arange(256)
    # use linear interpolation of cdf to find new pixel values
    image_equalized = np.floor(np.interp(V.flatten(), bins, CDFxn_transform).reshape(h, w)).astype(np.uint8)

    return image_equalized


@numba.njit()
def vid2dhisteq(image, w_neighboring=6, Wout_list=np.zeros((10), dtype=np.uint16)):
    h, w = image.shape
    V = image.astype(np.uint16)
    V_hist = imhist(V)

    H_in = im2dhist(V, w_neighboring=6)

    CDFx = np.cumsum(np.sum(H_in, axis=0)) # Kx1

    # normalizes CDFx
    CDFxn = (CDFx/CDFx[-1])

    PDFxn = np.zeros_like(CDFxn)
    PDFxn[0] = CDFxn[0]
    PDFxn[1:] = np.diff(CDFxn)

    X_transform = np.zeros((256), dtype=np.float64) 
    X_transform[V_hist > 0] = PDFxn.copy()
    CDFxn_transform = np.cumsum(X_transform).astype(np.float64)

    Win = H_in.shape[0]
    Gmax = 1.5 # 1.5 .. 2
    Wout = min(255, Gmax*Win)
    if np.where(Wout_list>0)[0].size==Wout_list.size:
        Wout = (np.sum(Wout_list)+Wout) / (1+Wout_list.size)

    F = V.ravel().astype(np.uint16)
    Ftilde = Wout * CDFxn_transform[F]

    Madj = np.mean(V) - np.mean(Ftilde)
    Ftilde = Ftilde + Madj

    Ftilde = np.clip(Ftilde, 0, 255).astype(np.uint8)

    image_equalized = Ftilde.reshape(h, w)

    return image_equalized, Wout
