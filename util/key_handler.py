import cv2 as cv

EXIT = 0
NOOP = 1
SAVE = 2

CURRENT_MODE = NOOP

def get_operation():
    global CURRENT_MODE
    key = cv.waitKey(20)
    if key == -1:
        if CURRENT_MODE == SAVE:
            CURRENT_MODE = NOOP
    else:
        if key == 115:
            CURRENT_MODE = SAVE
        if key == 27:
            CURRENT_MODE = EXIT
    return CURRENT_MODE
