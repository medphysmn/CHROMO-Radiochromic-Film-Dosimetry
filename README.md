# CHROMO: a software for a FAST AND SIMPLE Radiochromic Film MULTICHANNEL DOSIMETRY

![dose_3ch_treatment_2_figure](https://user-images.githubusercontent.com/37676343/190626086-d4be6463-c8da-4c30-b5a4-cdbf007e2b81.png)
![dose_3ch_treatment_1_figure](https://user-images.githubusercontent.com/37676343/190626423-846be746-c353-45a9-86cb-7cedfd05f95c.png)
![response-dose_calibration_plot_3ch](https://user-images.githubusercontent.com/37676343/190626240-cdd8e9b2-7795-47c5-ae68-9ba0eb4379e1.png)
![dose-response_recalibrated_plot_treatment_1](https://user-images.githubusercontent.com/37676343/190626267-4b32af33-a64d-43ae-973a-4f6b99b768bf.png)

A python based software used to measure radiochromic film dose using an efficient calibration and single scan recalibration method [1]. This method is reported and recomended as one of the possible dosimetry methods by the American Association of Physicists in Medicine (AAPM) 2020 Report [2]

**FEATURES**:

- **SCAN DENOISING** with Median and Wiener Filters [4] [5]
- **MULTICHANNEL DOSIMETRY** [1] 
- **FILM CALIBRATION with rational curve** [1] 
- **CORRECTION OF LATERAL RESPONSE ARTIFACT** [3] (TODO!!!)
- **INTRA SCAN RECALIBRATION** [1]
- **RESULT DOSE IMAGES IN DIFFERENT FORMATS**
- **PLOTS OF THE RESULTS**
- **DOSIMETRY OF MULTIPLE SCANS AT THE SAME TIME**

NO WARRANTY, USE AT OWN RISK.

[1] Lewis D, Micke A, Yu X, Chan MF. An efficient protocol for radiochromic film dosimetry combining calibration and measurement in a single scan. Med Phys. 2012 Oct;39(10):6339-50. doi: 10.1118/1.4754797. PMID: 23039670; PMCID: PMC9381144.

[2] Niroomand-Rad A, Chiu-Tsao ST, Grams MP, Lewis DF, Soares CG, Van Battum LJ, Das IJ, Trichter S, Kissick MW, Massillon-Jl G, Alvarez PE, Chan MF. Report of AAPM Task Group 235 Radiochromic Film Dosimetry: An Update to TG-55. Med Phys. 2020 Dec;47(12):5986-6025. doi: 10.1002/mp.14497. Epub 2020 Oct 30. PMID: 32990328.

[3] Lewis D, Chan MF. Correcting lateral response artifacts from flatbed scanners for radiochromic film dosimetry. Med Phys. 2015 Jan;42(1):416-29. doi: 10.1118/1.4903758. PMID: 25563282; PMCID: PMC5148133.

[4] Devic, Slobodan & Tomic, Nada & Soares, Célia & Podgorsak, Ervin. (2009). Optimizing the Dynamic Range Extension of a Radiochromic Film Dosimetry System. Medical physics. 36. 429-37. 10.1118/1.3049597. 

[5] Méndez, Ignasi & Rovira-Escutia, Juan & Casar, Bozidar. (2021). A protocol for accurate radiochromic film dosimetry using Radiochromic.com. Radiology and Oncology. 55. 369-378. 10.2478/raon-2021-0034. 

