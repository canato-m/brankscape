import numpy as np
import cv2 as cv
from tqdm import tqdm
print('\nStart.')
CAP_PATH = input('\nInput file name:') + ".mp4"
OUT_PATH = input('\nOutput file name:') + ".png"
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
    print('\nThe video imported as ' + str(int(WIDTH)) + '×' + str(int(HEIGHT)) + '(Pixel)')
    print(str(int(FRAME_COUNT)) + 'Frame ' + str(VIDEO_LENGTH) + 'Sec.')
    LOAD_FPS = int(input('Input frame rate ( original:' + str(int(FRAME_RATE)) + 'FPS ) :'))
    print('Importing Video as ' + str(int(LOAD_FPS)) + 'FPS')
    RATIO = int(FRAME_RATE / LOAD_FPS)
    framenum = 0
    while True:
        framenum += 1
        ret, frame = cap.read()
        # frame = int(frame)   np.array(frame, dtype=np.uint8)
        if ret and framenum % RATIO == 0 and frame is not None:
            hsv = frame  # cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img.append(hsv)
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
    print("\nArray formated as " + str(len(arrr)) + "Pixel.")
    print("\nArray setting...")
    for frame in tqdm(arr):
        x = 0
        for row in frame:
            for pixel in row:
                arrr[x].append(pixel[0])
                arrg[x].append(pixel[1])
                arrb[x].append(pixel[2])
                x += 1
    print("Array set as " + str(len(arrr)) + "Pixel " + str(len(arrr[0])) + "Frame.")
    narr = [arrr, arrg, arrb]
    return narr


def mode(arr, width, height):
    a, c = int(width), int(height)
    narr = np.array(arr)
    img = []
    arrr, arrg, arrb = narr[0], narr[1], narr[2]
    x = 0
    print("\nColor analyzing...")
    for row in tqdm(range(c)):
        inrow = []
        for pixel in range(a):
            if cv_(arr[0][x]) <= 1.5:
                count = np.bincount(arrr[x])
                mode = np.argmax(count)
                r = mode
                instantarr, instantarr2 = arrg[x][arrr[x] == r], arrb[x][arrr[x] == r]
                count = np.bincount(instantarr)
                mode = np.argmax(count)
                g = mode
                instantarr3 = instantarr2[instantarr == g]
                count = np.bincount(instantarr3)
                mode = np.argmax(count)
                b = mode
                inrow.append([r, g, b])
                x += 1
            else:
                # print(cv)
                inrow.append([0, 0, 0])
                x += 1
        img.append(inrow)
    print('\nColor analyzed.')
    return img


def cv_(arr):
    '''cvarr = np.ndarray(arr, dtype=np.uint8)
    std = np.std(cvarr)
    ave = np.mean(cvarr)
    cv = np.divide(std, ave, out=np.zeros_like(std), where=ave != 0)'''
    return 1


def write(arr):
    nimg = np.array(arr, dtype=np.uint8)
    print(type(nimg))
    print(nimg.shape)
    cv.imwrite(OUT_PATH, arr, [cv.IMWRITE_PNG_COMPRESSION, 9])


color_arr = make_color_arr(CAP)
del CAP
mode_arr = mode(color_arr, WIDTH, HEIGHT)
del color_arr
write = write(mode_arr)
print('Finished.')
