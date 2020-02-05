import numpy as np
import cv2
import sys
import os


def get_workfolder():
    path = ('/'.join(sys.argv[0].split('/')[:-1]))+'/'
    return path


class Footage():

    path = get_workfolder()

    def __init__(self, file_name):
        """Input the name of the file located under the /videos_source folder."""

        self.file_name = file_name
        self.footage = None

    def get_footage(self):
        
        footage_path = Footage.path + 'videos_source/' + self.file_name + '.mp4'
        self.footage = cv2.VideoCapture(footage_path)  # footage of the lap

    def split_into_images(self):
        # account for missing folder name

        workfolder = Footage.path + self.file_name + '/'
        if self.file_name not in os.listdir(Footage.path):
            os.mkdir(workfolder)

        # initialize

        flag = True
        framecount = 0
        while self.footage.isOpened():
            flag, image = self.footage.read()
            filename = workfolder + self.file_name + \
                'frame_' + str(framecount) + '.jpg'
            cv2.imwrite(filename, image)
            framecount += 1

if __name__ == '__main__':
    Leclerc = Footage('R02_Vettel_Bahrain')
    Leclerc.get_footage()
    Leclerc.split_into_images()
