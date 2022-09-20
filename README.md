# CHROMO: a software for a FAST AND SIMPLE Radiochromic Film single scan MULTI-CHANNEL DOSIMETRY

A python based software used to measure radiochromic film dose using an efficient **calibration** and **single scan recalibration** method [1]. This method [1] is reported and recomended as one of the possible dosimetry methods by the American Association of Physicists in Medicine (AAPM) 2020 Report [2]

![dose_3ch_treatment_1_figure](https://user-images.githubusercontent.com/37676343/190628150-f0b8dfe2-b822-4ce6-9236-46927fa47b77.png)
![dose_3ch_treatment_2_figure](https://user-images.githubusercontent.com/37676343/190628154-678fc275-1263-4095-b27c-98fac5691747.png)
![dose-response_calibration_plot_3ch](https://user-images.githubusercontent.com/37676343/191226479-07865ec4-4e3a-4ebe-ac49-8ba509f119a4.png)
![dose-response_recalibrated_plot_treatment_1](https://user-images.githubusercontent.com/37676343/190628158-6697023a-e6f1-40ad-b349-cd3728982d0a.png)


**FEATURES**:

- **MULTI-CHANNEL DOSIMETRY** of multiple scans at the same time [1] [2] 
- **SINGLE-CHANNEL DOSIMETRY** of multiple scans at the same time [2]
- **DOSIMETRY WITH FAST INTRA SCAN RECALIBRATION METHOD** of multiple scans at the same time [1] [2]
- **FILM CALIBRATION WITH DIFFERENT FITTING FUNCTIONS** [2] 
- **SCAN DENOISING** with Median and Wiener Filters [4] [5]
- **CORRECTION OF LATERAL RESPONSE ARTIFACT** [3] (TODO)
- **RESULT DOSE IMAGES IN DIFFERENT FORMATS**
- **PLOTS OF THE RESULTS**

sudo chmod 777 denoiser.py

[1] Lewis D, Micke A, Yu X, Chan MF. An efficient protocol for radiochromic film dosimetry combining calibration and measurement in a single scan. Med Phys. 2012 Oct;39(10):6339-50. doi: 10.1118/1.4754797. PMID: 23039670; PMCID: PMC9381144.

[2] Niroomand-Rad A, Chiu-Tsao ST, Grams MP, Lewis DF, Soares CG, Van Battum LJ, Das IJ, Trichter S, Kissick MW, Massillon-Jl G, Alvarez PE, Chan MF. Report of AAPM Task Group 235 Radiochromic Film Dosimetry: An Update to TG-55. Med Phys. 2020 Dec;47(12):5986-6025. doi: 10.1002/mp.14497. Epub 2020 Oct 30. PMID: 32990328.

[3] Lewis D, Chan MF. Correcting lateral response artifacts from flatbed scanners for radiochromic film dosimetry. Med Phys. 2015 Jan;42(1):416-29. doi: 10.1118/1.4903758. PMID: 25563282; PMCID: PMC5148133.

[4] Devic, Slobodan & Tomic, Nada & Soares, Célia & Podgorsak, Ervin. (2009). Optimizing the Dynamic Range Extension of a Radiochromic Film Dosimetry System. Medical physics. 36. 429-37. 10.1118/1.3049597. 

[5] Méndez, Ignasi & Rovira-Escutia, Juan & Casar, Bozidar. (2021). A protocol for accurate radiochromic film dosimetry using Radiochromic.com. Radiology and Oncology. 55. 369-378. 10.2478/raon-2021-0034. 

NO WARRANTY, USE AT OWN RISK.

