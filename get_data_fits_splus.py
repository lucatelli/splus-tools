#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""

Date = '09/2020'
Geferson Lucatelli

Usage:
$ python3 get_data_fits_splus.py /path/to/catalogue.csv /path/to/output_dir/
Your catalogue.csv must have #ID,RA,DEC.

  ____      _      _____ ___ _____ ____         _       _        
 / ___| ___| |_   |  ___|_ _|_   _/ ___|     __| | __ _| |_ __ _ 
| |  _ / _ \ __|  | |_   | |  | | \___ \    / _` |/ _` | __/ _` |
| |_| |  __/ |_   |  _|  | |  | |  ___) |  | (_| | (_| | || (_| |
 \____|\___|\__|  |_|   |___| |_| |____/    \__,_|\__,_|\__\__,_|
 _          ____        ____  _    _   _ ____  
(_)_ __    / ___|      |  _ \| |  | | | / ___| 
| | '_ \   \___ \ _____| |_) | |  | | | \___ \ 
| | | | |   ___) |_____|  __/| |__| |_| |___) |
|_|_| |_|  |____/      |_|   |_____\___/|____/

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
from sys import argv

import splusdata
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from astropy.nddata import Cutout2D
from astropy.wcs import WCS
import astropy.io.fits as pf
import getpass
# from tqdm.notebook import tqdm

#remove warnings
import warnings
warnings.filterwarnings("ignore")

name = getpass.getpass(prompt='Username Login at S-PLUS cloud:')
password = getpass.getpass(prompt='Password:')

tt = conn.get_tap_tables()

def grab_images():
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

    def get_cuts_faster(ID,RA,DEC,Radius=256,band="R",path_to_save='./'):
        """For this work, you should have the exact coordinates and ID of 
        the targets inside S-PLUS.
        """
        if Radius >= 600:
            print("**********>>>>>>>>>Limiting image size because pre-value is too high.")
            Radius = 600
    #     cat_all = pd.DataFrame()
        try:
            if not os.path.exists(save_path+band+'/'+ID+"_"+band+".fits"):
                hdu = conn.get_cut(RA,DEC,int(Radius),band) ## image FITS cuts - RA, DEC, Radius, band
                wcs  = WCS(hdu[1].header)
                data = hdu[1].data
                # pf.writeto(save_path+IDS.iloc[i]+"_R.fits",data,header=hdu[1].header,overwrite=True)
                pf.writeto(save_path+band+'/'+ID+"_"+band+".fits",data,header=hdu[1].header,overwrite=True)
                # pf.close()
        except:
            # print("Maybe, your object coordinate is not in S-PLUS database.")
            print("Error in obtaining ObjID=",ID," RA,DEC=(",RA,",",DEC,")")
            pass


    file = str(argv[1])
    _file_name = os.path.splitext(os.path.basename(file))
    file_name = _file_name[0]+_file_name[1]
    #where to save the stamps
    # save_path = "path_to_where_to_save_the_stamps/"+file_name.replace(".csv","")+"/"
    # save_path = str(argv[2])+_file_name[0].replace(".csv","")+"/"
    save_path = str(argv[2])+_file_name[0]+"/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    try:
        ra     = get_data(File=file,param='RA')
    except:
        ra     = get_data(File=file,param='#RA')

    try:
        dec     = get_data(File=file,param='DEC')
    except:
        dec     = get_data(File=file,param='DEC\n')
    
    try:
        IDs = getstr(File=file,string='ID')
    except:
        try:
            IDs = getstr(File=file,string='#ID')
        except:
            # IDs = np.arange(1,len(ra)+1).astype(str)
            IDs = []
            for i in range(len(ra)):
                radec = ra[i].astype(str) +'_'+ dec[i].astype(str)
                IDs.append(radec)
            IDs=np.asarray(IDs)

    try:
        ai = get_data(File=file,param='A')
        bi = get_data(File=file,param='B')
        Radius = 15*np.sqrt(ai**2.0+bi**2.0)
    except:
        size = 100
        Radius = np.ones(len(IDs))
        Radius =Radius*size

    # BAND = ["Z","U","G","F660","F861","I","F378","F395","F410","F430","F515"]
    BAND = ["R","G"]

    for band in BAND:
        print("Downloading images for the",band,' band.')
        if not os.path.exists(save_path+band):
            os.makedirs(save_path+band)

        """
        In principle, you can set NProc to a high value, because the download speed
        for each single image is not to high, but you can download many of them
        at once. However, connection stability may prevent you to download the
        data properly. Also, it may overload the the servers. I tested
        with NProc=16 and it seems to be working fine.
        For example, to download ~18000 images (256x256), it takes about 30minutes.
        """
        shift = 0#0.00194444
        NProc = 32
        processed_list = Parallel(n_jobs=NProc)(\
                         delayed(get_cuts_faster)(\
                            IDs[k],ra[k],dec[k]+shift,Radius[k],band,\
                            path_to_save=save_path) for k in tqdm(range(len(IDs))))
        def try_missing():
            """
            If any error occured during the first try, this function will check for
            those missing images and will try tro download it again.
            """
            print('----------------------')
            print('Checking missing files')
            print('----------------------')
            IDs_Re = []
            ra_Re = []
            dec_Re = []
            Radius_Re = []
            for k in range(len(IDs)):
                # if not os.path.exists(save_path+band+"/"+IDs[k]+"_"+band+".fits"):
                if not os.path.exists(save_path+band+"/"+IDs[k]+"_"+band+".fits"):
                    IDs_Re.append(IDs[k])
                    ra_Re.append(ra[k])
                    dec_Re.append(dec[k])
                    Radius_Re.append(Radius[k])
                else:
                    pass
            if len(IDs_Re)>0:
                print('-----------------------------------------------------')
                print(len(IDs_Re),'missing files. Trying to grab them again.')
                print('-----------------------------------------------------')
                NProc = 6 #small value to avoid connections issues.
                processed_list = Parallel(n_jobs=NProc)(\
                                delayed(get_cuts_faster)(\
                                    IDs_Re[k],ra_Re[k],dec_Re[k]+shift,Radius_Re[k],band,\
                                    path_to_save=save_path) for k in tqdm(range(len(IDs_Re))))
                print('Done.')
            else:
                print('-----------------')
                print('No missing files.')
                print('Done.')
                print('-----------------')
        try_missing()

if __name__ == '__main__':
    grab_images()
