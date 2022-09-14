import glob as gb
import numpy as np

#variabili d'ambiente
path="C:/Users/Imalytics/Desktop/chromo/scansPoliProva/" #/home/pcdti1/Scrivania/gafchromicfilm/CHROMO/scansPoli/' 
calibration_list = gb.glob(path+"CALIBRATION/calibration*")  
unexposed_calibration_list = gb.glob(path+"CALIBRATION/unexposed_calibration*")
treatment_list = gb.glob(path+"TREATMENT/treatment*")
unexposed_treatment_list = gb.glob(path+"TREATMENT/unexposed_treatment*")
maxdose_treatment_list = gb.glob(path+"TREATMENT/maxdose_treatment*")
outputPath = path + 'OUTPUT'

maxdoseRecalibration = 6 #DOSE MASSIMA DI RICALIBRAZIONE (Gy)

resolution = 25.4
dpi = 150
dpiResolution = resolution/dpi

dimRoiCalibration = 5 # roi per dose di calibrazione
dimensioneRoiPixel = 10 #es. 4=> 4x4

doseRawImageOutputFormat = 'tiff'
isodoseDifferenceGy = 0.1 #DIFFERENZA ISODOSI DI VISUALIZZAZIONE (Gy)
cmap = 'rainbow' #colore figure

redChannel=2 #ORDINE RGB
greenChannel=1 #ORDINE RGB
blueChannel=0 #ORDINE RGB

p0red = -10., 200., 3. #da cambiare eventualmente il punto iniziale
p0red1 = -10., 300., 3. #da cambiare eventualmente il punto iniziale
p0green = -10., 300., 3. #da cambiare eventualmente il punto iniziale
p0green1 = -10., 300., 3. #da cambiare eventualmente il punto iniziale
p0blue = -10., 300., 3. #da cambiare eventualmente il punto iniziale
p0blue1 = -10., 300., 3. #da cambiare eventualmente il punto iniziale
a0multichannel = np.array([0, 1000, 5]) #da cambiare eventualmente il punto iniziale
a0multichannel1 = np.array([-10, 200, 3]) #da cambiare eventualmente il punto iniziale
