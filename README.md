# splus-tools
Some scripts to help with the S-PLUS data. 
Descriptions of the functions in this repository are described bellow. Some general updates will come soon.


## 1 Get S-PLUS Stripe82 Fields

Download all S-PLUS STRIPE82 DR1 image fields. Set `path_to_save=''` equal to your destination directory in order to save the tada. Then, just do: 

`python3 get_stripes.py`

OBS: `NProc` is the number of parallel files to be downloaded. 

## 2 Get single objects

Get image stamps for specific objects with `get_single.py`. You must provide where your fields .fits files are located (e.g. STRIPE82-XXX\_filter_swp.fits). Set the path with `base=path-to/DR1-fields`. Finally, you  must have some catalogue from S-PLUS that contain the informations `#FIELD`, `ID`, `X` and `Y` of that particular object you want to create the stamp. To run the code, just: 

`python3 single_object.py  catalogue-file.csv ID BAND `

For example, 

`python3 single_object.py  example.csv SPLUS.STRIPE82-0118.37943.griz R `


## 3 Get multiple images. 
Use `cut_images.py` to obtain multiple images from a catalogue table. Inside the file, just
set the name of the catalogue file in `file_name`. For example, `file_name=example.csv`. You must also provide the location of the .fits fields files as before. To run it, just: 

`python3 cut_images.py`

## 4 Grab images directly from https://datalab.noao.edu
Use the code `grab_splus_images.py` with a catalogue containing the `ID`, `FIELD`, `RA` and `DEC` quantities to grab images directly from the datalab.noao.edu servers. The variable `file_name=example` is the catalogue file. To run it, just do:

`python3 grab_splus_images.py`
