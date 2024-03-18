import cv2 as cv

EXIT = 0
NOOP = 1
SAVE = 2
CHANGE_LOOKUP = 3

CURRENT_MODE = NOOP

def get_operation():
    global CURRENT_MODE
    key = cv.waitKey(10)
    if key == -1:
        if CURRENT_MODE == SAVE:
            # debounce after save was performed
            CURRENT_MODE = NOOP
        if CURRENT_MODE == CHANGE_LOOKUP:
            CURRENT_MODE = NOOP
    else:
        if key == 115:  
            # s was pressed
            CURRENT_MODE = SAVE
        if key == 27:
            # esc was pressed
            CURRENT_MODE = EXIT
        if key == 108:
            CURRENT_MODE = CHANGE_LOOKUP
    return CURRENT_MODE
