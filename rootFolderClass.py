#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob as gb
import shutil
import os

class rootFolderClass:
    def __init__(self, path):
        self.path = path
        self.dataPath =path + 'data/'
        self.denoiserFolder =path + 'denoiser/'
        self.denoiserPath = self.denoiserFolder + 'denoise.py'
        self.outputPath = self.dataPath + 'OUTPUT/'
        self.nonFilteredCalibrationPath = self.dataPath + "CALIBRATION/"
        self.calibrationPath = self.outputPath + "_CALIBRATION_FILTERED/"
        self.nonFilteredTreatmentPath = self.dataPath + "TREATMENT/"
        self.treatmentPath = self.outputPath + "_TREATMENT_FILTERED/"
        self.redPath = self.outputPath + "RED/"
        self.greenPath = self.outputPath + "GREEN/"
        self.bluePath = self.outputPath + "BLUE/"
        self.tchPath = self.outputPath + "3CH/"
        
        self.unexposed_calibration_list = gb.glob(self.calibrationPath + "unexposed_calibration*")
        self.treatment_list = gb.glob(self.treatmentPath + "treatment*")
        self.unexposed_treatment_list = gb.glob(self.treatmentPath + "unexposed_treatment*")
        self.maxdose_treatment_list = gb.glob(self.treatmentPath + "maxdose_treatment*")
        self.calibration_list = gb.glob(self.calibrationPath+"calibration*")  
        self.nonFilteredTreatment_list = gb.glob(self.nonFilteredTreatmentPath+"treatment*")  
        self.nonFilteredCalibration_list = gb.glob(self.nonFilteredCalibrationPath+"calibration*")  
        
