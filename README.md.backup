# splus-tools
Some scripts to help with the S-PLUS data.
All script uses the `splusdata` python package found in here https://github.com/Schwarzam/splusdata. 
Descriptions of the functions in this repository are described bellow. Some general updates will come soon.


## Obtainig fits images in iDR3 (current data release)

To download fits images from S-PLUS cloud, just use `get_data_fits_splus.py`. 
For that, you will need to have a file (e.g. `my_galaxies.csv`) with information of your targets. The file must contain the following column names: 

`RA,DEC`

ID is not mandatory, but if you provide it, you can get organized better. 
For example, 


```
$ cat my_galaxies.csv
#ID,RA,DEC,
M77,40.6699,-0.0132,
iDR3.STRIPE82-0002.057486,0.05329615441370631,1.1202572109221862,
iDR3.STRIPE82-0005.038845,3.025305291664389,-0.4151865917717107,
iDR3.STRIPE82-0007.025765,3.632581584275741,-0.7375334501888078,
iDR3.STRIPE82-0015.043450,10.15762757372187,-0.3308202123182916,
iDR3.STRIPE82-0170.027067,358.54201220042313,0.3828517710478816,
iDR3.STRIPE82-0168.004182,357.5462040416795,0.096651758673875,
```
Sizes of images are set by changing the value of `size=128`. Or, if you would like to have variable sizes for each source, just add the semi-major and semi-minor axis from S-PLUS catalogue to yor `my_galaxies.csv` file, so that 
```
$ cat my_galaxies.csv
#ID,RA,DEC,A,B,
....
```

Therefore, the image size will be 

![](eq1.png) 

To select filters that are going to be downloaded, just change the list given by 

`BAND = ["R","Z","U","G","F660","F861","I","F378","F395","F410","F430","F515"]`

If you want to download large ammount of data in parallel, use `NProc`, you can set it to 32 for example (default value), however do not go further than that, because it will use a lot of RAM and also may make the SPLUS cloud unresponsive. 

So, finally, to download the data just do

``` $python3 get_data_fits_splus.py my_galaxies.csv path/to/save/data #e.g. ./``` 


## Obtainig colour images in iDR3 (current data release)

The process is the same. I have duplicated the code from obtaining fits images for distinction purposes. Just changed the part where color images are set instead of fits. 

Just use: 

```$python3 get_data_color_splus.py my_galaxies.csv path/to/save/data #e.g. ./```


## Features

### Missing Files
If some problem happened during the download of some target, the code will try to download it again at the end. If still it is not possible, is that because there is some problem with the source inside the S-PLUS cloud. This will be investigated more in the future. 

### Continue from where I stopped. 
If for some reason you stoped the code, or other issue happened, if you run the code again with the same file and folder, it will continue from the downloaded target from that file. So already downloaded files will not by modified. However, if you want to change the size of the images, you can set another save folder or delete the one that you are already using.


