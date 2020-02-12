import cv2
import sys
import os


def get_workfolder():
    path = ('/'.join(sys.argv[0].split('/')[:-1]))+'/'
    return path


class Footage():

    path = get_workfolder()

    def __init__(self, file_name):
        """Input the name of the file located
        under the /videos_source folder."""
        self.file_name = file_name

    def get_footage(self):
        footage_path = Footage.path + 'videos_source/' + self.file_name + '.mp4'
        self.footage = cv2.VideoCapture(footage_path)  # footage of the lap

    def split_into_images(self):
        # account for missing folder name
        workfolder = Footage.path + self.file_name + '/'
        if self.file_name not in os.listdir(Footage.path):
            os.mkdir(workfolder)

        # initialize
        framecount = 0
        footage_images = []
        while self.footage.isOpened():
            flag, image = self.footage.read()
            if flag == False:
                self.footage.release()
                break
            filename = workfolder + self.file_name + \
                'frame_' + str(framecount) + '.jpg'
            footage_images.append(image)
            framecount += 1
        self.footage_images = np.array(footage_images, dtype=np.uint16)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        hamilton = Footage('P02_Hamilton_Russia')
        hamilton.get_footage()
        hamilton.split_into_images()
    else:
        for driver in sys.argv[1:]:
            driver_footage = Footage(driver)
            driver_footage.get_footage()
            driver_footage.split_into_images()
