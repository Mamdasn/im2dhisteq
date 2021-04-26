from im2dhist import im2dhist, imhist
import numpy as np

def im2dhisteq(image, w_neighboring=6):
    [h, w] = image.shape
    V = image.copy()
    V_hist = imhist(V)

    H_in = im2dhist(V, w_neighboring=6)

    CDFx = np.cumsum(np.sum(H_in, axis=0)).reshape(-1, 1) # Kx1

    # normalizes CDFx
    CDFxn = (255*CDFx/CDFx[-1]).reshape(-1)

    PDFxn = np.zeros_like(CDFxn)
    PDFxn[0] = CDFxn[0]
    PDFxn[1:] = np.diff(CDFxn)
    
    X_transform = np.zeros((256))
    X_transform[np.where(V_hist > 0)] = PDFxn
    CDFxn_transform = np.cumsum(X_transform).reshape(-1)


    # bins = np.array([i for i in range(0, 256)]).reshape(-1)
    bins = np.arange(256)
    # uses linear interpolation of cdf to find new pixel values
    image_equalized = np.floor(np.interp(V.flatten(), bins, CDFxn_transform).reshape(h, w)).astype(np.uint8)

    return image_equalized


def vid2dhisteq(image, w_neighboring=6, Wout_list=np.zeros((10))):
    [h, w] = image.shape
    V = image.copy()
    V_hist = imhist(V)

    H_in = im2dhist(V, w_neighboring=6)

    CDFx = np.cumsum(np.sum(H_in, axis=0)).reshape(-1, 1) # Kx1

    # normalizes CDFx
    CDFxn = (255*CDFx/CDFx[-1]).reshape(-1)

    PDFxn = np.zeros_like(CDFxn)
    PDFxn[0] = CDFxn[0]
    PDFxn[1:] = np.diff(CDFxn)
    
    X_transform = np.zeros((256))
    X_transform[np.where(V_hist > 0)] = PDFxn
    CDFxn_transform = np.cumsum(X_transform).reshape(-1)

    Win = H_in.shape[0]
    Gmax = 1.5 # 1.5 .. 2
    Wout = min(255, Gmax*Win)
    if np.where(Wout_list>0)[0].size==Wout_list.size:
        Wout = (np.sum(Wout_list)+Wout) / (1+Wout_list.size)

    F = V.copy().reshape(-1)
    Ftilde = Wout * CDFxn_transform[F]/CDFxn_transform[-1]
    
    Madj = np.mean(V) - np.mean(Ftilde)
    Ftilde = Ftilde + Madj

    Ftilde = np.where(Ftilde>=0, Ftilde, np.zeros_like(Ftilde))
    Ftilde = np.where(Ftilde<=255, Ftilde, 255*np.ones_like(Ftilde))
    Ftilde = Ftilde.astype(np.uint8)

    image_equalized = Ftilde.reshape(h, w)

    return image_equalized, Wout