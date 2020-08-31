#!/usr/bin/python
"""
Date = '2020 01 28'
Geferson Lucatelli
"""
import numpy as np
import multiprocessing
import requests

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

def get_stripes(STRIPE,band):
    """
    Assuming that all url's (root_url) are in the same format.
    """
    path_to_save = ""
    root_url = "http://datalab.noao.edu/svc/cutout?col=splus_dr1&siaRef="
    url = root_url + str(STRIPE) + "_" + str(band) + "_swp.fz"
    print("Downloading  "+STRIPE+" from "+url)
    try:
        r = requests.get(url)
        with open(path_to_save+STRIPE+"_"+band+"_swp.fits",'wb') as f:
            f.write(r.content)
        f.close()
        return(r.content)
    except:
        try:
            r = requests.get(url)
            with open(path_to_save+STRIPE+"_"+band+"_swp.fits",'wb') as f:
                f.write(r.content)
            f.close()
            return(r.content)
        except:
            print("Error downloading field",STRIPE,'in a second try.')
            return("Error")


bands = ["G","I","R","U","Z","F861","F660","F515","F430","F410","F395","F378"]


NProc = 6
#the number of your computer threads. But in this case,
#since downloading does not require cpupower, set to
#the number of bands, for example.

pool = multiprocessing.Pool( NProc )
tasks = []
for STRIPE in STRIPES:
    for band in bands:
	    tasks.append((STRIPE,band))

results = [pool.apply_async( get_stripes, t ) for t in tasks]
for result in results:
    Filename = result.get()
pool.close()
pool.join()
