################### README ##########################
This document details the segmentation of organs from DICOM CT data files using read_contour.py.

Before you proceed:
* You need to have matplotlib and dicom libraries of PYTHON installed in your local machine.

Step-by-Step "How TO"
1. Define working directory
   The working directory is the directory where you store DICOM CT data files (image files and structure file).
   
2. Dimension follows the default settings of Canberra Hospital.
   Adjust the dimension if necessary.
   
3. Define parameters.
   A. Serial number of each organ.
      - This can be found using PyDicom:
      data = dicom.read_file('your_structure_file')
      organ_name = data.StructureSetROISequence[array_index].ROIName
      serial_number = data.StructureSetROISequence[array_index].ROINumber
      
   B. ID of CT files (the last three digits of a given CT file)
      - first : dataID_ini
      - final : dataID_fin
      - step  : dataID_step
      
   C. CT-structure filename
   
4. Centre of "fake dose".
   This will be modified to include more realistic dose distribution using detailed calculations.