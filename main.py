import util.camera as camera
import util.args as arguments
import util.key_handler as key_handler
import cv2 as cv
import util.image_saver as image_saver

if __name__ == "__main__":
    args = arguments.parse_args()
    camera.start_camera(frame_size=(args.width, args.height))
    while True:
        op = key_handler.get_operation()
        if op == key_handler.EXIT:
            exit()
        im = camera.get_frame()
        if op == key_handler.SAVE:
            image_saver.save_image(im, im, im , [im])
        cv.imshow("Image", im)
        cv.waitKey(5)