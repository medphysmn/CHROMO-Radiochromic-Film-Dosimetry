# -*- coding: utf-8 -*-

class doseClass:
    def __init__(self, dosefiltered, mindos, maxdos, avgdos, stddos, half_maximum_xdos, half_maximum_ydos, dose_center, bkgxdos, bkgydos):
        self.dosefiltered = dosefiltered
        self.mindos = mindos
        self.maxdos = maxdos
        self.avgdos = avgdos
        self.stddos = stddos
        self.half_maximum_xdos = half_maximum_xdos
        self.half_maximum_ydos = half_maximum_ydos
        self.dose_center = dose_center
        self.bkgxdos = bkgxdos
        self.bkgydos = bkgydos
