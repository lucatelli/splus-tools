import pylab as pl
import numpy as np

def imshow(img, sigma=3, contours=0, bar=None, aspect='equal', extent=None, vmin=None, vmax=None, use_median=False):
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
