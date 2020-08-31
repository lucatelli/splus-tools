#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 _______          _________   _______  ______  
(  ____ \|\     /|\__   __/  / ___   )(  __  \ 
| (    \/| )   ( |   ) (     \/   )  || (  \  )
| |      | |   | |   | |         /   )| |   ) |
| |      | |   | |   | |       _/   / | |   | |
| |      | |   | |   | |      /   _/  | |   ) |
| (____/\| (___) |   | |     (   (__/\| (__/  )
(_______/(_______)   )_(     \_______/(______/ 
 _______         _______  _                 _______ 
(  ____ \       (  ____ )( \      |\     /|(  ____ \
| (    \/       | (    )|| (      | )   ( || (    \/
| (_____  _____ | (____)|| |      | |   | || (_____ 
(_____  )(_____)|  _____)| |      | |   | |(_____  )
      ) |       | (      | |      | |   | |      ) |
/\____) |       | )      | (____/\| (___) |/\____) |
\_______)       |/       (_______/(_______)\_______)

Date = '2020 05 22'
Geferson Lucatelli
There is an improvement in this code.
"""
from __future__ import division
import numpy as np
import pylab as pl
import astropy.io.fits as pf
import matplotlib.pyplot as plt
from astropy.nddata import Cutout2D
from astropy.wcs import WCS
import os
import warnings
warnings.filterwarnings("ignore")
from progress.bar import Bar

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

def _imshow(img, sigma=3, contours=0, bar=None, aspect='equal', extent=None, vmin=None, vmax=None, use_median=False):
    """
    improved version of pl.imshow,

    shows image with limits sigma above and below mean.

    optionally show contours and colorbar
    """

    def mad(x):
       return np.median( np.abs( x - np.median(x)) )

    # deals with NaN and Infinity
    img[np.where(np.isnan(img))]=0.0
    img[np.where(np.isinf(img))]=0.0


    # wether to use median/mad or mean/stdev.
    # note that mad ~ 1.5 stdev
    if use_median==False:
      if vmin==None:
         vmin = img.mean() - sigma * img.std()
      if vmax==None:
         vmax = img.mean() + sigma * img.std()
    else:
      if vmin==None:
         vmin = np.median(img) - 1.5*sigma * mad(img)
      if vmax==None:
         vmax = np.median(img) + 1.5*sigma * mad(img)


    pl.imshow(img, vmin=vmin, vmax=vmax, origin='lower', aspect=aspect, extent=extent, interpolation=None)

    if bar != None:
        pl.colorbar(pad=0)

    if contours >0:
        pl.contour(img, contours, colors='k', linestyles='solid', aspect=aspect, extent=extent)


def convert_input_file_to_comma_separated(File):
    """
    If the data of the input file is space separated (single, multi or tab),
    this function will try to convert it to comma separated values.

    NOTE: I need to implement properly this function.
    """
    import pandas as pd
    d = pd.read_csv(File,delim_whitespace=True)
    new_File = File+"_pandas.csv"
    d.to_csv(new_File, sep=",",index=False)
    return new_File

def get_gal_multiple(field,band,fields,IDs,x0,y0,base,save_path):
    """
    Perform the cut task for each galaxy ID inside each field.
    """
    idx = np.where(fields==field)[0]
    bar = Bar('', max=len(idx))
    try:
        #read the FIELD.fits file
        file_fits = base+field+'_'+band+'_swp.fits'
        print("Reading File...:", file_fits)
        hdu  = pf.open(file_fits)
        wcs  = WCS(hdu[1].header)
        data = hdu[1].data
        size = int(256)
        print("Creating",len(idx), "stamps in field",field)

        for i in idx:
            # print("Cut task for >> ", IDs[i])
            try:
                data_cut = Cutout2D(data, position=(x0[i],y0[i]), size=(size,size), \
                    wcs=wcs)
                hdu[1].data = data_cut.data
                hdu[1].header.update(data_cut.wcs.to_header())
                pf.writeto(save_path+band+'/'+IDs[i]+'_'+band+'.fits',data_cut.data, \
                    header=hdu[1].header,overwrite=True)


                plot_and_save = False
                if plot_and_save is True:
                    if not os.path.exists(save_path+band+'/figs/'):
                        os.makedirs(save_path+band+'/figs/')
                    _imshow((np.log(data_cut.data)),sigma=5.5,contours=0,bar=True)
                    plt.gray()
                    plt.savefig(save_path+band+'/figs/'+IDs[i]+'_'+band+'.svg', bbox_inches='tight')
                    # plt.savefig(save_path+band+'/figs/'+IDs[i]+'_'+band+'.png',dpi=150, bbox_inches='tight')
                    plt.clf()
                    plt.close()
                bar.next()
            except:
                print("Error in ID=",IDs[i])
    except:
        print("An error ocurred for field ", field)
    bar.finish()


STRIPES = ["STRIPE82-0001","STRIPE82-0002","STRIPE82-0003","STRIPE82-0004","STRIPE82-0005",
           "STRIPE82-0006","STRIPE82-0007","STRIPE82-0008","STRIPE82-0009","STRIPE82-0010",
           "STRIPE82-0011","STRIPE82-0012","STRIPE82-0013","STRIPE82-0014","STRIPE82-0015",
           "STRIPE82-0016","STRIPE82-0017","STRIPE82-0018","STRIPE82-0019","STRIPE82-0020",
           "STRIPE82-0021","STRIPE82-0022","STRIPE82-0023","STRIPE82-0024","STRIPE82-0025",
           "STRIPE82-0026","STRIPE82-0027","STRIPE82-0028","STRIPE82-0029","STRIPE82-0030",
           "STRIPE82-0031","STRIPE82-0032","STRIPE82-0033","STRIPE82-0034","STRIPE82-0035",
           "STRIPE82-0036","STRIPE82-0037","STRIPE82-0038","STRIPE82-0039","STRIPE82-0040",
           "STRIPE82-0041","STRIPE82-0042","STRIPE82-0043","STRIPE82-0044","STRIPE82-0045",
           "STRIPE82-0046","STRIPE82-0047","STRIPE82-0048","STRIPE82-0049","STRIPE82-0050",
           "STRIPE82-0051","STRIPE82-0052","STRIPE82-0053","STRIPE82-0054","STRIPE82-0055",
           "STRIPE82-0056","STRIPE82-0057","STRIPE82-0058","STRIPE82-0059","STRIPE82-0060",
           "STRIPE82-0061","STRIPE82-0062","STRIPE82-0063","STRIPE82-0064","STRIPE82-0065",
           "STRIPE82-0066","STRIPE82-0067","STRIPE82-0068","STRIPE82-0069","STRIPE82-0070",
           "STRIPE82-0071","STRIPE82-0072","STRIPE82-0073","STRIPE82-0074","STRIPE82-0075",
           "STRIPE82-0076","STRIPE82-0077","STRIPE82-0078","STRIPE82-0079","STRIPE82-0080",
           "STRIPE82-0081","STRIPE82-0082","STRIPE82-0083","STRIPE82-0084","STRIPE82-0085",
           "STRIPE82-0086","STRIPE82-0087","STRIPE82-0088","STRIPE82-0089","STRIPE82-0090",
           "STRIPE82-0091","STRIPE82-0092","STRIPE82-0093","STRIPE82-0094","STRIPE82-0095",
           "STRIPE82-0096","STRIPE82-0097","STRIPE82-0098","STRIPE82-0099","STRIPE82-0100",
           "STRIPE82-0101","STRIPE82-0102","STRIPE82-0103","STRIPE82-0104","STRIPE82-0105",
           "STRIPE82-0106","STRIPE82-0107","STRIPE82-0108","STRIPE82-0109","STRIPE82-0110",
           "STRIPE82-0111","STRIPE82-0112","STRIPE82-0113","STRIPE82-0114","STRIPE82-0115",
           "STRIPE82-0116","STRIPE82-0117","STRIPE82-0118","STRIPE82-0119","STRIPE82-0120",
           "STRIPE82-0121","STRIPE82-0122","STRIPE82-0123","STRIPE82-0124","STRIPE82-0125",
           "STRIPE82-0126","STRIPE82-0127","STRIPE82-0128","STRIPE82-0129","STRIPE82-0130",
           "STRIPE82-0131","STRIPE82-0132","STRIPE82-0133","STRIPE82-0134","STRIPE82-0135",
           "STRIPE82-0136","STRIPE82-0137","STRIPE82-0138","STRIPE82-0139","STRIPE82-0140",
           "STRIPE82-0141","STRIPE82-0142","STRIPE82-0143","STRIPE82-0144","STRIPE82-0145",
           "STRIPE82-0146","STRIPE82-0147","STRIPE82-0148","STRIPE82-0149","STRIPE82-0150",
           "STRIPE82-0151","STRIPE82-0152","STRIPE82-0153","STRIPE82-0154","STRIPE82-0155",
           "STRIPE82-0156","STRIPE82-0157","STRIPE82-0158","STRIPE82-0159","STRIPE82-0160",
           "STRIPE82-0161","STRIPE82-0162","STRIPE82-0163","STRIPE82-0164","STRIPE82-0165",
           "STRIPE82-0166","STRIPE82-0167","STRIPE82-0168","STRIPE82-0169","STRIPE82-0170"]


# file = 'cut_FULL_SAMPLE.csv'
file_path = "/home/lucatelli/Documents/"
file_name = "example.csv"
file = file_path + file_name

#where to save the stamps
# save_path = "path_to_where_to_save_the_stamps/"+file_name.replace(".csv","")+"/"
save_path = "/run/media/lucatelli/storage_wd_2/"+""+file_name.replace(".csv","")+"/"

#where your FIELDs files are located.
# base = "path_to_fields/" #e.g. /media/data/SPLUS_fields/
base = "/run/media/lucatelli/data/data/splus/STRIPES/STRIPE82_fields/" #this is for my computer

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

x0     = get_data(File=file,param='X')

try:
    y0     = get_data(File=file,param='Y')
except:
    #in case Y is at the last collum.
    y0     = get_data(File=file,param='Y\n')

# BAND = ["R",'G','I','Z','U','F378','F395','F410','F430','F515','F660','F861']
BAND = ["R"]

#do the loop for each object in 'file' and for each filter 'band'.
for band in BAND:

    if not os.path.exists(save_path+band):
        os.makedirs(save_path+band)

    for field in STRIPES:
        get_gal_multiple(field,band,fields,IDs,x0,y0,base,save_path)
