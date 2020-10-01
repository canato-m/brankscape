import numpy as np
import cv2 as cv
# import os,sys
CAP_PATH = input('Input file name:') + ".mp4"
CAP = cv.VideoCapture(CAP_PATH)
WIDTH = CAP.get(cv.CAP_PROP_FRAME_WIDTH)
HEIGHT = CAP.get(cv.CAP_PROP_FRAME_HEIGHT)
FRAME_COUNT = CAP.get(cv.CAP_PROP_FRAME_COUNT)
FRAME_RATE = CAP.get(cv.CAP_PROP_FPS)
VIDEO_LENGTH = FRAME_COUNT / FRAME_RATE


def make_color_arr(cap):
    if not cap.isOpened():
        return
    img = []
    print('Original video imported as')
    print(str(int(WIDTH)) + '×' + str(int(HEIGHT)) + '(Pixel)')
    print(str(int(FRAME_RATE)) + 'FPS ' + str(int(FRAME_COUNT)) + 'Frame')
    print(str(VIDEO_LENGTH) + 'Sec.')
    LOAD_FPS = int(input('Input frame rate ( original:' + str(int(FRAME_RATE)) + 'FPS ) :'))
    print('\nThe video imported as ' + str(int(LOAD_FPS)) + 'FPS')
    RATIO = int(FRAME_RATE / LOAD_FPS)
    framenum = 0
    while True:
        framenum += 1
        ret, frame = cap.read()
        if ret and framenum % RATIO == 0:
            img.append(frame)
            if framenum % FRAME_RATE == 0:
                framenum = 0
        elif ret is False:
            imgs = format_color_arr(img, WIDTH, HEIGHT, VIDEO_LENGTH * LOAD_FPS)
            return imgs


def format_color_arr(arr, width, height, frame_count):
    a, b, c = int(width), int(height), int(frame_count)
    arrr = [[] * c for i in range(a * b)]
    arrg = [[] * c for i in range(a * b)]
    arrb = [[] * c for i in range(a * b)]
    print("\nArray formated as")
    print(str(len(arrr)) + "Pixel")
    for frame in arr:
        x = 0
        for row in frame:
            for pixel in row:
                arrr[x].append(pixel[0])
                arrg[x].append(pixel[1])
                arrb[x].append(pixel[2])
                x += 1

    print("\nArray set as")
    print(str(len(arrr)) + "Pixel")
    print(str(len(arrr[0])) + "Frame")
    narr = [arrr, arrg, arrb]
    return narr


def mode(arr):
    narr = np.array(arr)
    nnarr = [[] for i in range(3)]
    x = -1
    for channel in narr:
        x += 1
        for pixel in channel:
            count = np.bincount(pixel)
            mode = np.argmax(count)
            nnarr[x].append(mode)
    print('\nPixel moded.')
    return nnarr


def reconstruct(arr, width, height):
    a, b = int(width), int(height)
    img = []
    x = 0
    for row in range(b):
        inrow = []
        for pixel in range(a):
            inrow.append([arr[0][x], arr[1][x], arr[2][x]])
            x += 1
        img.append(inrow)
    print('Reconstructed.')
    nimg = np.array(img, dtype=np.uint8)
    cv.imwrite('result.tif', nimg)
    # nnimg = cv.cvtColor(nimg, cv.COLOR_BGRA2BGR)
    return img


color_arr = make_color_arr(CAP)
mode_arr = mode(color_arr)
reconstruct(mode_arr, WIDTH, HEIGHT)
print('Finished.')
