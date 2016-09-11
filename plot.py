#########################################
# Peter McGill September 2016           #
# code to plot multi output from starpy #
#########################################


import numpy as N
import corner as c
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter,MultipleLocator, FormatStrFormatter
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from statsmodels.nonparametric.smoothers_lowess import lowess
plt.style.use('idl.mplstyle')
plt.figure(figsize=(6.95,6.8))
#img = mpimg.imread('201052.jpg')
from smooth import smooth

#definelims
TAUMAX = 4
TAUMIN = 0
TQMAX = 10
TQMIN = 0
BINS = 200

#data processing
#create uniform 2d hist for output weights to be overlaid.
dat = [[i,j] for i in N.arange(TQMAX/BINS,TQMAX+TQMAX/BINS,TQMAX/BINS) for j in N.arange(TAUMAX/BINS,TAUMAX+TAUMAX/BINS,TAUMAX/BINS)]
dat = N.transpose(dat)
x = dat[:1].flatten()
y = dat[1:2].flatten()



weighted = N.load('z-0.5-1.0-low-del.npy')
#tq_mcmc, tau_mcmc,  = map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]), zip(*N.percentile(samples, [16,50,84],axis=0    )))



xweights = N.sum(weighted,axis=1)
yweights = N.sum(N.transpose(weighted),axis=1)

weighted = weighted.flatten()

#set up grid for 2d hist and marginal 1d hists.
gs1 = gridspec.GridSpec(2,2,width_ratios=[3,1],
                       height_ratios=[1,3])
axScatter = plt.subplot(gs1[2])
gs1.update(hspace=0.00,wspace=0.0)
axScatter.minorticks_on()
axScatter.set_xlabel(r'$t_{q}$')
axScatter.set_ylabel(r'$\tau$')

axHistX = plt.subplot(gs1[0])
axHistX.set_xlim(TQMIN, TQMAX)
axHistX.xaxis.set_major_formatter( NullFormatter() )
axHistX.yaxis.set_major_formatter( NullFormatter() )
#axHistX.plot([tq_mcmc[0],tq_mcmc[0]],[0,1000],color='blue')

axHistY = plt.subplot(gs1[3])
axHistY.set_ylim(TAUMIN,TAUMAX)
axHistY.xaxis.set_major_formatter( NullFormatter() )
axHistY.yaxis.set_major_formatter( NullFormatter() )
#axHistY.plot([0,1000],[tau_mcmc[0],tau_mcmc[0]],color='blue')

#axPic = plt.subplot(gs1[1])
#axPic.imshow(img)
#axPic.axis('off')

#perform smoothing of data
#unsmooth = N.histogram(x,bins=BINS,weights=weighted,range=[TQMIN,TQMAX])[0]
#x = N.transpose(lowess(unsmooth, N.arange(TQMAX/BINS,TQMAX+TQMAX/BINS,TQMAX/BINS), is_sorted=True, frac=0.025, it=0))[1]
#print(x)
#plot histogram
c.hist2d(x,y,ax=axScatter,weights=weighted,range=[[TQMIN,TQMAX],[TAUMIN,TAUMAX]],bins=BINS,max_n_ticks=8,normed=True,smooth=2)
axScatter.text(0.5,0.5,r'$0.5<z<1.0$')
axScatter.text(0.5,0.3,r'$\log(1+\delta)<-0.25$')

#axScatter.hist2d(x,y,weights=weighted,range=[[TQMIN,TQMAX],[TAUMIN,TAUMAX]],bins=150,normed=True)
#axScatter.plot([tq_mcmc[0],tq_mcmc[0]],[0,5],color='blue')
#axScatter.plot([0,100],[tau_mcmc[0],tau_mcmc[0]],color='blue')

#perform smoothing of data
#unsmooth = np.histogram(x,bins=BINS,weights=weighted,range=[TQMIN,TQMAX])[0]

#weighted = smooth(weighted)


axHistY.plot(yweights,N.arange(TAUMAX/BINS,TAUMAX + TAUMAX/BINS,TAUMAX/BINS),color='Black')
axHistX.plot(N.arange(TQMAX/BINS,TQMAX + TQMAX/BINS,TQMAX/BINS),xweights,color='Black')
#axHistX.hist(x,color='black',histtype='step',bins=BINS,weights=xweights,range=[TQMIN,TQMAX])
#axHistY.hist(y,color='black',histtype='step',orientation='horizontal',bins=BINS,weights=yweights,range=[TAUMIN,TAUMAX])

plt.savefig('z-0.5-1.0-low-del.pdf')
