from astropy.table import Table
import os.path
import numpy
import csv
import fnmatch
import os
import matplotlib.pyplot as plt
import numpy as N

smoothCol= 't01_smooth_or_features_a01_smooth_weighted_fraction'
featureCol = 't01_smooth_or_features_a02_features_or_disk_weighted_fraction'
master = Table.read('GZ+UVISTA.fits',format='fits')
BINS = 150
PROB = N.log(0.2)
TAUMIN = 0
TAUMAX = 4
TQMIN = 0
TQMAX = 14

#redshift cut
#zmask1 = master['z_peak'] > 0.0
#zmask2 = master['z_peak'] < 0.5
#s/n >5
#usemask = master['USE_1'] == 1
#mask = (zmask1 == 1) & (zmask2 == 1) & (usemask == 1)

#master = master[mask]


#for monitering progress out ouput.
length = len(master['ID'])
j=1;

#create key to table row.
dict = dict(zip(master['ID'],numpy.arange(len(master['ID']))))

#print(master['z_peak'][dict[195754]])

#initalize output data
sampleWeightByFeature = numpy.zeros((40000,2))
H = N.zeros((BINS,BINS))

#fence post
#i = master['ID'][0]
#filenameSample ='samples_' + str(i) + '_' + str(master['ra'][dict[i]]) + '_' + str(master['dec'][dict[i]]) + '.npy'
#sample = numpy.load('../dataout/samples/'+ filenameSample)
#total =  master[featureCol][dict[i]]*sample

#iterate over all sample
for i in master['ID']:
     #keep track of percent progress.
     percent = float(j)/length * 100
     print(str(percent) + "%")
     
     #load in smaples and posterior logrithmic probabilities.
     filenameSample ='samples_' + str(i) + '_' + str(master['ra'][dict[i]]) + '_' + str(master['dec'][dict[i]]) + '.npy'
     sample = numpy.load('../dataout/samples/'+ filenameSample)
     lnprobname ='lnprob_run_'+ str(i) + '_' + str(master['ra'][dict[i]]) + '_' + str(master['dec'][dict[i]]) + '.npy'
     lnprob = numpy.load('../dataout/lnprob/'+lnprobname)

     #remove walkers with probability less than PROB.
     probmask = lnprob[:] < PROB
     lnprob = lnprob[probmask]
     sample = sample[probmask]
 
     #change sample format from [[x_1,y_2],[x_2,y_2]....] to [x_1,x_2,x_3,..],[y_1,y_2,y_3,...]
     #for hist2d plot.
     samp = N.transpose(sample)
     x = samp[:1].flatten()
     y = samp[1:2].flatten()
     
     #calaculate normalised bin heights for walkers in one sample, weight by lnprob.
     Hcurrent =  N.histogram2d(x, y, range=[[TQMIN,TQMAX],[TAUMIN,TAUMAX]],bins=BINS,weights=N.exp(lnprob[:]),normed=True)[0]
     
     #remove extreme outlier bing hieghts:
     if Hcurrent.max() <200:
        H+= master[smoothCol][dict[i]]*Hcurrent
     j = j +1


 
numpy.save('out',H)

