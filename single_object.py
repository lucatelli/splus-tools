#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Date = '2020 02 06'
Geferson Lucatelli
"""
from __future__ import division
import numpy as np
import astropy.io.fits as pf
import matplotlib.pyplot as plt
from astropy.nddata import Cutout2D
from astropy.wcs import WCS
import imshow_func as fimshow

def get_data(param=None,File=None,HEADER=0):
    """
    Get a numerical variable from a table.

    HEADER: if ==1, display the file's header.
    """
    infile = open(File, 'r')
    firstLine = infile.readline()
    header=firstLine.split(',')
    if HEADER==1:
        print(header)
    else:
        ind=header.index(param)
        return np.loadtxt(File,usecols=(ind),comments="#", delimiter=",", \
            unpack=False)

def getstr(string,File):
    """
    Get a string column.
    """
    infile = open(File, 'r')
    firstLine = infile.readline()
    header=firstLine.split(',')
    ind=header.index(string)
    return np.loadtxt(File,dtype='str',usecols=(ind),comments="#", \
        delimiter=",", unpack=False)

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

def get_gal_single(ID,band,file,size=256,save_plot=True,show=False):
    """
    Use this function to obtain a specific object id.

    Example:

    import cut_images as cuti

    file = your_galaxy_table.csv
    # e.g. > SPLUS_SQGTool_DR1_mag-17_p_gal_sw_0.7-1.0.csv

    #In S-PLUS standard tables. Please, modify \
    #bellow the variables and labels as you need for other tables.

    target = "SPLUS.STRIPE82-0170.35936.griz"

    #Note that the target need to be in the table.

    data = cuti.get_gal_single(target,"R",file=file,show=True)

    """
    f = file
    IDs      = getstr('ID',f)
    idx      = np.where(IDs==ID)[0]
    # print IDs
    field    = getstr('#FIELD',f)[idx][0]
    # print field
    x0       = get_data(param='X',File=f)[idx]
    y0       = get_data(param='Y',File=f)[idx]
    # ISOarea  = get_data(param='ISOarea',File=f)[idx]
    # size     = 256#int(2*ISOarea)
    base = "/run/media/sagauga/data/data/splus/STRIPES/STRIPE82_fields/" #the SPLUS fields folder.
    file_fits = base+field+'_'+band+'_swp.fits'
    print(file_fits)
    hdu = pf.open(file_fits)
    wcs = WCS(hdu[1].header)
    data = hdu[1].data
    data_cut = Cutout2D(data, position=(x0,y0), size=(size,size), wcs=wcs)
    hdu[1].data = data_cut.data
    hdu[1].header.update(data_cut.wcs.to_header())

    save_path = ""

    pf.writeto(save_path+ID+'_'+band+'.fits',data_cut.data, \
        header=hdu[1].header,overwrite=True)

    if save_plot is True:
        fimshow.imshow(((data_cut.data)),sigma=1.5,contours=0,bar=True)
        plt.gray()
        plt.savefig(save_path+ID+'_'+band+'.svg', bbox_inches='tight')
        # plt.savefig(save_path+IDs[i]+'_'+band+'.png',dpi=150, bbox_inches='tight')
        if show is True:
            plt.show()
        plt.clf()
        plt.close()

    # plt.imshow(np.log(data_cut.data))
    # plt.show()
    return data_cut

file = "/run/media/sagauga/data/data/splus/STRIPES/STRIPE82_fields/SPLUS_SQGTool_DR1_mag-17_p_gal_sw_0.7-1.0.csv"
target = "SPLUS.STRIPE82-0001.08015.griz"#example
data = get_gal_single(target,"R",file=file,save_plot=True,show=True)
