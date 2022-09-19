# -*- coding: utf-8 -*-
import numpy as np
import sys
sys.path.append(".")
from constants import *

class fitResultsSingleChannel:
    def __init__(self, redFit, greenFit, blueFit):
        self.redFit = redFit
        self.greenFit = greenFit
        self.blueFit = blueFit
