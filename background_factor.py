import numpy as np
import matplotlib.pyplot as plt
import os
from astropy.stats import sigma_clip

f = open('list.txt')
#64 elements in the table
j=f.readlines()
f.close()

a = [line.split('\n')[0] for line in j]


name_band_y='f098m'
name_band_j='f125w'
name_band_h='f160w'
name_band_v1='f606w'
name_band_v2='f600lp'

b='0835+2456'

name_preffix='preliminary_sources_'
name_suffix1='.cat'
name_suffix2='_2.cat'

def std_flux_aper(name_band,number_cat):
    f = open(name_preffix+number_cat+'_'+name_band+name_suffix2)
    for i in xrange(26):    
        header = f.readline()
    k = f.readlines()
    f.close()
    flux_aper=np.zeros(len(k))
    i=0
    for line in k:
        flux_aper[i]=line.split()[5]
        if flux_aper[i]<-5 or flux_aper[i]>5:
            flux_aper[i]=0
        i=i+1
    flux_aper_2 = sigma_clip(flux_aper,3)
    return np.std(flux_aper_2)

def med_flux_aper_err(name_band,number_cat):
    f=open(name_preffix+number_cat+'_'+name_band+name_suffix1)
    for i in xrange(42):    
        header = f.readline()
    k = f.readlines()
    f.close()
    i=0
    flux_aper_err=np.zeros(len(k))
    for line in k:
        flux_aper_err[i]=line.split()[13]
        i=i+1
    return np.median(flux_aper_err)

factor_y=np.zeros(len(j))+0
factor_j=np.zeros(len(j))+0
factor_h=np.zeros(len(j))+0
factor_v1=np.zeros(len(j))+99
factor_v2=np.zeros(len(j))+99

#a[0]=b
#for i in xrange(len(j)):

g = open("factor_background_test4.txt", "w")
#for i in xrange(1):
for i in xrange(len(j)):
    factor_y[i]=std_flux_aper(name_band_y,a[i])/med_flux_aper_err(name_band_y,a[i])
    factor_j[i]=std_flux_aper(name_band_j,a[i])/med_flux_aper_err(name_band_j,a[i])
    factor_h[i]=std_flux_aper(name_band_h,a[i])/med_flux_aper_err(name_band_h,a[i])
    if os.path.isfile(name_preffix+a[i]+'_'+name_band_v1+name_suffix2) and os.path.exists(name_preffix+a[i]+'_'+name_band_v1+name_suffix2): #and os.path.isfile(name_preffix+a[i]+'_'+name_band_v1+name_suffix1) and os.path.exists(name_preffix+a[i]+'_'+name_band_v1+name_suffix1):
        print name_preffix+a[i]+'_'+name_band_v1+name_suffix2
        print name_preffix+a[i]+'_'+name_band_v1+name_suffix1
        factor_v1[i]=std_flux_aper(name_band_v1,a[i])/med_flux_aper_err(name_band_v1,a[i])
    if os.path.isfile(name_preffix+a[i]+'_'+name_band_v2+name_suffix2) and os.path.exists(name_preffix+a[i]+'_'+name_band_v2+name_suffix2): #and os.path.isfile(name_preffix+a[i]+'_'+name_band_v2+name_suffix1) and os.path.exists(name_preffix+a[i]+'_'+name_band_v2+name_suffix1):
        print name_preffix+a[i]+'_'+name_band_v2+name_suffix2
        print name_preffix+a[i]+'_'+name_band_v2+name_suffix1
        factor_v2[i]=std_flux_aper(name_band_v2,a[i])/med_flux_aper_err(name_band_v2,a[i])
    g.write("%s %f %f %f %f %f\n"%(a[i],factor_y[i],factor_j[i],factor_h[i],factor_v1[i],factor_v2[i]))

print np.mean(factor_y), np.mean(factor_j), np.mean(factor_h), np.median(factor_v1), np.median(factor_v2)
