#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 _____ ______  ___  ______    _____       ______ _     _   _ _____ 
|  __ \| ___ \/ _ \ | ___ \  /  ___|      | ___ \ |   | | | /  ___|
| |  \/| |_/ / /_\ \| |_/ /  \ `--. ______| |_/ / |   | | | \ `--. 
| | __ |    /|  _  || ___ \   `--. \______|  __/| |   | | | |`--. \
| |_\ \| |\ \| | | || |_/ /  /\__/ /      | |   | |___| |_| /\__/ /
 \____/\_| \_\_| |_/\____/   \____/       \_|   \_____/\___/\____/ 
 ________  ___  ___  _____  _____ _____ 
|_   _|  \/  | / _ \|  __ \|  ___/  ___|
  | | | .  . |/ /_\ \ |  \/| |__ \ `--. 
  | | | |\/| ||  _  | | __ |  __| `--. \
 _| |_| |  | || | | | |_\ \| |___/\__/ /
 \___/\_|  |_/\_| |_/\____/\____/\____/ 
                                        
Date = '2020 08 31'
Geferson Lucatelli
"""
from __future__ import division
import numpy as np
import pylab as pl
import astropy.io.fits as pf
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings("ignore")
from progress.bar import Bar
import requests
import multiprocessing
from tqdm import tqdm
from joblib import Parallel, delayed


def get_data(File,param=None,HEADER=0):
    """
    Get a numerical variable from a table.

    HEADER: if ==1, display the file's header.
    """
    infile = open(File, 'r')
    firstLine = infile.readline()
    header=firstLine.split(',')
    if HEADER==1:
        print(header)
        return(header)
    else:
        ind=header.index(param)
        return np.loadtxt(File,usecols=(ind),comments="#", delimiter=",", \
            unpack=False)


def getstr(File,string=None,HEADER=0):
    """
    Get a string variable from a table.
    May work for float as well.
    """
    infile = open(File, 'r')
    firstLine = infile.readline()
    header=firstLine.split(',')
    if HEADER==1:
        print(header)
        return(header)
    else:
        ind=header.index(string)
        return np.loadtxt(File,dtype='str',usecols=(ind),comments="#", \
        delimiter=",", unpack=False)

# file = 'cut_FULL_SAMPLE.csv'
file_path = ""
file_name = "example.csv"
file = file_path + file_name

#where to save the stamps
# save_path = "path_to_where_to_save_the_stamps/"+file_name.replace(".csv","")+"/"
save_path = ""+file_name.replace(".csv","")+"/"


if not os.path.exists(save_path):
    os.makedirs(save_path)

IDs    = getstr(File=file,string='ID')

try:
    fields = getstr(File=file,string='#FIELD')
except:
    fields = []
    for i in range(0,len(IDs)):
        fields.append(IDs[i][6:19])#Drop the IDs of the objects, get only field.
    fields = np.asarray(fields)

ra     = get_data(File=file,param='RA')
dec     = get_data(File=file,param='Dec')


# BAND = ["R",'G','I','Z','U','F378','F395','F410','F430','F515','F660','F861']
BAND = ["G","R","I"]



def get_images_ra_dec(STRIPE,ID,ra,dec,band,path_to_save = ""):
    """
    Assuming that all url's (root_url) are in the same format.
    """

    root_url = "https://datalab.noao.edu/svc/cutout?col=splus_dr1&siaRef="
    # root_url = "https://datalab.noao.edu/svc/cutout?col=splus_dr1&siaRef="
    url = root_url + str(STRIPE) + "_" + str(band) + "_swp.fz"
    
    """The size 0.0389565 corresponds to an image of 256x256 pixels."""
    url_pos = url+"&extn=1&POS="+str(ra)+","+str(dec)+"&SIZE=0.0389565,0.0389565"
    
    # &extn=1&POS=1.0296,-0.8641&SIZE=0.0389565,0.0389565&preview=false
    # print("Downloading Image (ra,dec)=(",ra,dec,") in "+STRIPE+" from "+url_pos)
    try:
        r = requests.get(url_pos,verify=True,timeout=1500)
        # with open(path_to_save+"SPLUS."+STRIPE+"-"+ID+".griz_"+band+".fits",'wb') as f:
        with open(path_to_save+band+"/"+ID+"_"+band+".fits",'wb') as f:
            f.write(r.content)
        f.close()
    except:
        try:
            r = requests.get(url_pos,verify=True,timeout=1500)
            # with open(path_to_save+"SPLUS."+STRIPE+"-"+ID+".griz_"+band+".fits",'wb') as f:
            with open(path_to_save+band+"/"+ID+"_"+band+".fits",'wb') as f:
                f.write(r.content)
            f.close()
        except:
            print('---------------------------------------')
            print('requests.get timeout error.')
            print('Skipping ID=',ID)
            print('Trying again later')
            print('---------------------------------------')


#do the loop for each object in 'file' and for each filter 'band'.
for band in BAND:
    print("Downloading images for the",band,' band.')
    if not os.path.exists(save_path+band):
        os.makedirs(save_path+band)
    
    """
    In principle, you can set NProc to a high value, because the download speed 
    for each single image is not to high, but you can download many of them 
    at once. However, connection stability may prevent you to download the 
    data properly. Also, it may overload the NOAO datalab servers. I tested 
    with NProc=48 and it seems to be working fine. 
    For example, to download ~18000 images (256x256), it takes about 30minutes. 
    """
    NProc = 48 
    processed_list = Parallel(n_jobs=NProc)(\
                     delayed(get_images_ra_dec)(\
                        fields[k],IDs[k],ra[k],dec[k],band,\
                        path_to_save=save_path) for k in tqdm(range(len(IDs))))


    #try again for files that were not downloaded. 
    def try_missing():
        """
        If any error occured during the first try, this function will check for 
        those missing images and will try tro download it again.
        """
        print('----------------------')
        print('Checking missing files')
        print('----------------------')
        fields_Re = [] 
        IDs_Re = []
        ra_Re = []
        dec_Re = []
        for k in range(len(IDs)):
            if not os.path.exists(save_path+band+"/"+IDs[k]+"_"+band+".fits"):
                fields_Re.append(fields[k])
                IDs_Re.append(IDs[k])
                ra_Re.append(ra[k])
                dec_Re.append(dec[k])
            else:
                pass
        if len(IDs_Re)>0:
            print('-----------------------------------------------------')
            print(len(IDs_Re),'missing files. Trying to grab them again.')
            print('-----------------------------------------------------')
            NProc = 3 #small value to avoid connections issues.
            processed_list = Parallel(n_jobs=NProc)(\
                            delayed(get_images_ra_dec)(\
                                fields_Re[k],IDs_Re[k],ra_Re[k],dec_Re[k],band,\
                                path_to_save=save_path) for k in tqdm(range(len(IDs_Re))))
            print('Done.')
        else:
            print('-----------------')
            print('No missing files.')
            print('Done.')
            print('-----------------')
    try_missing()
