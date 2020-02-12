import pytesseract
import cv2
from Footage_Capture import get_workfolder

path = get_workfolder()

class Enhance_Image():

    def frame_to_grayscale(frame_path):
        grayscale_frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
        return grayscale_frame

    def crop_frame(frame, x0, y0, x1, y1):
        cropped_frame = frame[y0:y1, x0:x1]
        return cropped_frame

    def enhance_image(frame):
        bil = cv2.bilateralFilter(frame, 9, 25, 10)-5
        return bil


class Parse_Data():

    def __init__(self, folder_name, start_frame, finish_frame, sample_rate):
        self.folder_name = folder_name
        self.start_frame = start_frame
        self.finish_frame = finish_frame
        self.speed_list = []
        self.sample_rate = sample_rate

    def get_path(self, frame_number):
        frame_path = path + self.folder_name + '//'[:-1] + \
            self.folder_name + 'frame_' + str(frame_number) + '.jpg'
        return frame_path

    def _get_speed(self, frame):
        text = pytesseract.image_to_string(frame, lang = 'Formula1')
        return text

    def get_list_of_speeds(self):
        for x in range(self.start_frame, self.finish_frame, self.sample_rate):
            path = self.get_path(x)
            grayscale = Enhance_Image.frame_to_grayscale(path)
            cropped = Enhance_Image.crop_frame(grayscale,  110, 465, 305, 558)
            cropped = Enhance_Image.enhance_image(cropped)
            self.speed_list.append(self._get_speed(cropped))

if __name__ == '__main__':
    legreg = Parse_Data('P01_Leclerc_Russia', 221, 4803)
    legreg.get_list_of_speeds()
