# ssrl-pyfai-basics

set of documents to help explain/facilitate data processing of 
scattering/diffraction data from ssrl using pyFAI

## Description
The aim of this document is to explain how to use pyFAI.goniometer for
calibrating the position of the detector from the goniometer encoders at SSRL.

Those data have been acquired at 7-2 at SSRL in March 2018 by Natalie Geise
using a Pilatus 300kw detector and LaB6 as calibrant. 61 images have been
acquired in theta-two theta geometry from th = 2.5 and tth = 5 to th = 19.5 and
tth = 39 degrees. The motor positions are registered in the .pdi files and in
the .csv file for the entire scan.

A prior manual calibration (using pyFAI-calib2) may be performed on 5 images -
scans 9, 23, 32, 43, 50. Those images had ring each in them (1,3,5,7,9 th rings).
The control points extrated during this initial calibration has been used as a
starting point for this calibration. Then more images have been added to make
the model more robust.

from http://www.silx.org/doc/pyFAI/dev/usage/tutorial/Goniometer/Rotation-Pilatus100k/Multi120_Pilatus100k.html




To adapt you need to:
* adjust alignment folder
* put csv file in alignment folder, make sure the right column in the csv file is being used (this is noted in the code in the functon get angle)
* rough manual calibration for a few images/rings (use image-j to convert raw to tif, then used pyfai-calib2 to calibrate - save poni files and .npt which contains the control points (marked points along rings that you id'ed) in alignment folder
* check size of imgs - should be the detector size
    * pilatus 300kw is
        * w = 1475
        * h = 195
    * pilatus 100k is
        * w = 495
        * h = 195


## Authors
- [Natalie Geise](https://github.com/nataliegeise), SLAC National Accelerator Laboratory
- [Julien Barrier](https://github.com/julienbarrier), SLAC National Accelerator Laboratory

## Changelog
### 2018-06-29
- Definition of new functions to compatibility with Pilatus 100k detector (SSRL
    BL 2-1)
- calibration LaB6 patterns from Pilatus 300k detector (SSRL BL 7-2)

### 2018-06-26
- multigeometry alignment
- creation
