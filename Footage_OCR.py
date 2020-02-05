import pytesseract
import sys
import os
import cv2
import numpy as np
from Footage_Capture import get_workfolder

path = get_workfolder()
tempnum = 0


class Enhance_Image():

    def frame_to_grayscale(frame_path):
        grayscale_frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
        return grayscale_frame

    def crop_frame(frame, x0, y0, x1, y1):
        cropped_frame = frame[y0:y1, x0:x1]
        return cropped_frame

    def enhance_image(frame):
        bil = cv2.bilateralFilter(frame, 9, 6, 20)
        med = cv2.GaussianBlur(bil, (5, 5), 0)*1.9-180
        return med


class Parse_Data():

    def __init__(self, folder_name, start_frame, finish_frame, fps=30):
        self.folder_name = folder_name
        self.start_frame = start_frame
        self.finish_frame = finish_frame
        self.fps = fps
        self.speed_list = []

    def get_path(self, frame_number):
        frame_path = path + self.folder_name + '//'[:-1] + \
            self.folder_name + 'frame_' + str(frame_number) + '.jpg'
        return frame_path

    def _get_speed(self, frame):
        text = pytesseract.image_to_string(frame)
        return text

    # def get_grayscales(self):
    #     grayscales = []
    #     for frame_number in range(self.start_frame, self.finish_frame):
    #         path = self.get_path(frame_number)
    #         grayscales.append(Enhance_Image.frame_to_grayscale(path))
    #     return grayscales

    # def get_cropped(self, grayscales, x0, y0, x1, y1):
    #     cropped = [Enhance_Image.crop_frame(
    #         frame, x0, y0, x1, y1) for frame in grayscales]
    #     return cropped

    def get_list_of_speeds(self):
        for x in range(self.start_frame, self.finish_frame):
            path = self.get_path(x)
            grayscale = Enhance_Image.frame_to_grayscale(path)
            cropped = Enhance_Image.crop_frame(grayscale, 120, 490, 293, 560)
            cropped = Enhance_Image.enhance_image(cropped)
            self.speed_list.append(self._get_speed(cropped))

    def output_to_file(self):
        log = open('./log.txt', 'w')
        if self.speed_list:
            for entry in self.speed_list:
                log.write(entry + '\n')


if __name__ == '__main__':
    legreg = Parse_Data('P01_Leclerc_Russia', 700, 900, fps=50)
    legreg.get_list_of_speeds()
    legreg.output_to_file()
