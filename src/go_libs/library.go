package main

/*
#include <stdint.h>
#include <stdlib.h>
*/
import "C"
import (
    "unsafe"
    "image"
    "github.com/Mamdasn/im2dhistgo"
)

//export im2dhist_file
func im2dhist_file(arg *C.char) *C.uint32_t {
    goArg := C.GoString(arg)
    twodhist := im2dhistgo.Im2dhist_file(goArg)

    // Allocate memory for the array in C
    cArray := C.malloc(C.size_t(len(twodhist)) * C.size_t(unsafe.Sizeof(C.uint32_t(0))))
    cArrayPtr := (*[65536]C.uint32_t)(cArray)

    // Copy Go array to C array
    for i, v := range twodhist {
        cArrayPtr[i] = C.uint32_t(v)
    }

    return (*C.uint32_t)(cArray)
}

func byte2Gray(data *byte, width, height int) *image.Gray {
    // Create a slice from the pointer
    imgData := (*[1 << 28]byte)(unsafe.Pointer(data))[:width*height : width*height]

    // Create a new Gray image of the specified dimensions
    img := image.NewGray(image.Rect(0, 0, width, height))

    // Copy the grayscale data into the image
    copy(img.Pix, imgData)

    return img
}

//export im2dhist_data
func im2dhist_data(data *byte, width, height int, w int) *C.uint32_t {

    layer := byte2Gray(data, width, height)

    twodhist := im2dhistgo.Im2dhist(layer, w)

    // Allocate memory for the array in C
    cArray := C.malloc(C.size_t(len(twodhist)) * C.size_t(unsafe.Sizeof(C.uint32_t(0))))
    cArrayPtr := (*[65536]C.uint32_t)(cArray)

    // Copy Go array to C array
    for i, v := range twodhist {
        cArrayPtr[i] = C.uint32_t(v)
    }

    return (*C.uint32_t)(cArray)
}


//export imhist_data
func imhist_data(data *byte, width, height int) *C.uint32_t {

    layer := byte2Gray(data, width, height)

    imhist := im2dhistgo.Imhist(layer)

    // Allocate memory for the array in C
    cArray := C.malloc(C.size_t(len(imhist)) * C.size_t(unsafe.Sizeof(C.uint32_t(0))))
    cArrayPtr := (*[256]C.uint32_t)(cArray)

    // Copy Go array to C array
    for i, v := range imhist {
        cArrayPtr[i] = C.uint32_t(v)
    }

    return (*C.uint32_t)(cArray)
}

//export freeMemory
func freeMemory(ptr unsafe.Pointer) {
	C.free(ptr)
}

func main() {}
