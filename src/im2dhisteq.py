from im2dhist import im2dhist
import numpy as np


def imhist(image):
    hist, bins = np.histogram(image.reshape(1, -1), bins=256, range=(0, 255))
    return (np.asarray(hist), np.asarray(bins[0:-1]))
    
def im2dhisteq(image, w_neighboring=6, showProgress = True):
    [h, w] = image.shape
    V = image
    V_hist, _ = imhist(V)

    X = (V_hist > 0) * [i for i in range(1, 257)]
    X = X[X>0]
    K = len(X)

    H_in = im2dhist(V, w_neighboring=6, showProgress = True)

    CDFx = np.cumsum(np.sum(H_in, axis=0)).reshape(-1, 1) # Kx1

    # normalizes CDFx
    CDFxn = (255*CDFx/CDFx[-1]).reshape(-1)

    X_transform = np.zeros((256))
    X_transform[np.where(V_hist > 0)] = np.insert(np.diff(CDFxn), 0, CDFxn[0])
    CDFxn_transform = np.cumsum(X_transform).reshape(-1)


    bins = np.array([i for i in range(0, 256)]).reshape(-1)
    # use linear interpolation of cdf to find new pixel values
    image_equalized = np.floor(np.interp(V.flatten(), bins, CDFxn_transform).reshape(h, w)).astype(np.uint8)

    return image_equalized
