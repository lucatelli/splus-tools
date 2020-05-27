#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Date = '2020 02 06'
Geferson Lucatelli
"""
from __future__ import division
import numpy as np
import pylab as pl
import astropy.io.fits as pf
import matplotlib.pyplot as plt
from astropy.nddata import Cutout2D
from astropy.wcs import WCS
import imshow_func as fimshow

from sys import argv

def get_object():

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

    def getstr(string,File,HEADER=0):
        """
        Get a string column.
        """
        infile = open(File, 'r')
        firstLine = infile.readline()
        header=firstLine.split(',')
        if HEADER==1:
            print(header)
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

    def get_gal_single(ID,band,file,size=1024,save_plot=True,show=False):
        """
        Use this function to obtain a specific object id.

        Example:
        python3 single_object.py your_galaxy_table.csv SPLUS.STRIPE82-0059.30275.griz F378

        """
        f = file
        IDs      = getstr('ID',f)
        # print(IDs,ID)
        idx      = np.where(IDs==ID)[0]
        # print IDs
        field    = getstr('#FIELD',f)[idx][0]
        # print field
        x0       = get_data(param='X',File=f)[idx]
        y0       = get_data(param='Y',File=f)[idx]
        # ISOarea  = get_data(param='ISOarea',File=f)[idx]
        # size     = 256#int(2*ISOarea)
        base = "path_to/DR1_fields/" #the SPLUS fields folder.
        file_fits = base+field+'_'+band+'_swp.fits'
        # print(file_fits)
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
            _imshow(((data_cut.data)),sigma=1.5,contours=0,bar=True)
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

    file = str(argv[1])
    # file = "table_splus.csv"
    target = str(argv[2])
    band = str(argv[3])
    # target = "SPLUS.STRIPE82-0001.08015.griz"#example
    data = get_gal_single(target,band,file=file,save_plot=True,show=True)

if __name__ == '__main__':
    get_object()
