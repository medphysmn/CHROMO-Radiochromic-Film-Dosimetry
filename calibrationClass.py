# -*- coding: utf-8 -*-
import numpy as np
import sys
sys.path.append(".")
from constants import *

class calibrationClass:
    def __init__(self, calibrationImage, redChannel, greenChannel, blueChannel, calibration_dose, treatment_number):
        self.calibrationImage = calibrationImage
        self.xshapeimage = int(calibrationImage.shape[0]/2)
        self.yshapeimage = int(calibrationImage.shape[0]/2)
        self.calibration_dose = float(calibration_dose)
        
        self.calibrationRed = np.mean(calibrationImage[self.xshapeimage-dimRoiCalibration:self.xshapeimage+dimRoiCalibration, self.yshapeimage-dimRoiCalibration:self.yshapeimage+dimRoiCalibration , redChannel]).astype(float)
        self.calibrationGreen = np.mean(calibrationImage[self.xshapeimage-dimRoiCalibration:self.xshapeimage+dimRoiCalibration, self.yshapeimage-dimRoiCalibration:self.yshapeimage+dimRoiCalibration , greenChannel]).astype(float)
        self.calibrationBlue = np.mean(calibrationImage[self.xshapeimage-dimRoiCalibration:self.xshapeimage+dimRoiCalibration, self.yshapeimage-dimRoiCalibration:self.yshapeimage+dimRoiCalibration , blueChannel]).astype(float)
        
        self.treatment_number = treatment_number
