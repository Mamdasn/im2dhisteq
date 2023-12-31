import ctypes
import numpy as np
import cv2

# Load the shared library
library = ctypes.CDLL('go_libs/library.so')

# Set up the function return and argument types
library.im2dhist_file.argtypes = [ctypes.c_char_p]
library.im2dhist_file.restype = ctypes.POINTER(ctypes.c_uint32 * 65536)

library.im2dhist_data.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int, ctypes.c_int]
library.im2dhist_data.restype = ctypes.POINTER(ctypes.c_uint * 65536)

library.imhist_data.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int]
library.imhist_data.restype = ctypes.POINTER(ctypes.c_uint * 256)

def get_twodhist_file(im_addr):
    arg = im_addr.encode('utf-8')
    data_ptr = library.im2dhist_file(arg)

    # Dereference the pointer and convert to a numpy array
    twodhist = np.array(data_ptr.contents, dtype=np.uint32).reshape(256, 256)

    # Identify rows that are not all zeros
    non_zero_rows_columns = ~np.all(twodhist == 0, axis=0)
    twodhist = twodhist[non_zero_rows_columns][:, non_zero_rows_columns]

    library.freeMemory(data_ptr)
    return twodhist

def get_twodhist(layer, w=1):
    shape_of_layer = layer.shape
    height, width = shape_of_layer[0], shape_of_layer[1]

    img_ctype = layer.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))

    data_ptr = library.im2dhist_data(img_ctype, width, height, w)

    # Dereference the pointer and convert to a numpy array
    twodhist = np.array(data_ptr.contents, dtype=np.uint32).reshape(256, 256)

    # Identify rows that are not all zeros
    non_zero_rows_columns = ~np.all(twodhist == 0, axis=0)
    twodhist = twodhist[non_zero_rows_columns][:, non_zero_rows_columns]

    library.freeMemory(data_ptr)
    return twodhist

def get_imhist(layer):
    shape_of_layer = layer.shape
    height, width = shape_of_layer[0], shape_of_layer[1]

    img_ctype = layer.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))

    data_ptr = library.imhist_data(img_ctype, width, height)

    # Dereference the pointer and convert to a numpy array
    imhist = np.array(data_ptr.contents, dtype=np.uint32)

    library.freeMemory(data_ptr)
    return imhist
