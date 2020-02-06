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

def getpmodels(param=None,File=None,HEADER=0):
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



def get_gal_single(ID,band,file,size=256,show=False):
    """
    Use this function to obtain a specific object id.

    Example:

    import cut_images as cuti

    file = your_galaxy_table.csv
    #In S-PLUS standard tables. Please, modify \
    #bellow the variables and labels as you need for other tables.

    target = "SPLUS.STRIPE82-0170.35936.griz"

    #Note that the target need to be in the table.

    cuti.get_gal_single(target,"R",file=file,show=True)

    """
    f = file
    IDs      = getstr('ID',f)
    idx      = np.where(IDs==ID)[0]
    field    = getstr('#FIELD',f)[idx][0]
    x0       = getpmodels(param='X',File=f)[idx]
    y0       = getpmodels(param='Y',File=f)[idx]
    # ISOarea  = getpmodels(param='ISOarea',File=f)[idx]
    # size     = 256#int(2*ISOarea)

    your_path_do_data = "STRIPES/" #insert the path to data.
    file_fits = your_path_do_data+field+'_'+band+'_swp.fits'
    print(file_fits)

    hdu = pf.open(file_fits)
    wcs = WCS(hdu[1].header)
    data = hdu[1].data
    data_cut = Cutout2D(data, position=(x0,y0), size=(size,size), wcs=wcs)
    hdu[1].data = data_cut.data
    hdu[1].header.update(data_cut.wcs.to_header())

    your_save_path = "your_save_path"
    pf.writeto(your_save_path+ID+'_'+band+'.fits',data_cut.data, \
        header=hdu[1].header,overwrite=True)

    if show is True:
        plt.imshow(np.log(abs(data_cut.data)))
        plt.show()
        plt.clf()
        plt.close()

    return data_cut
