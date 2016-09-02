import numpy as N
import corner as c
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter,MultipleLocator, FormatStrFormatter
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
plt.style.use('idl.mplstyle')
plt.figure(figsize=(6.95,6.8))
#img = mpimg.imread('201052.jpg')

#definelims
TAUMAX = 4
TAUMIN = 0
TQMAX = 14
TQMIN = 0
BINS = 150
#data processing
dat = [[i,j] for i in N.arange(TQMAX/BINS,TQMAX+TQMAX/BINS,TQMAX/BINS) for j in N.arange(TAUMAX/BINS,TAUMAX+TAUMAX/BINS,TAUMAX/BINS)]
dat = N.transpose(dat)
x = dat[:1].flatten()
y = dat[1:2].flatten()



weighted = N.load('out.npy')
#tq_mcmc, tau_mcmc,  = map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]), zip(*N.percentile(samples, [16,50,84],axis=0    )))

weighted = weighted.flatten()

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

c.hist2d(x,y,ax=axScatter,weights=weighted,range=[[TQMIN,TQMAX],[TAUMIN,TAUMAX]],bins=BINS,max_n_ticks=8,normed=True)

#axScatter.hist2d(x,y,weights=weighted,range=[[TQMIN,TQMAX],[TAUMIN,TAUMAX]],bins=150,normed=True)
#axScatter.plot([tq_mcmc[0],tq_mcmc[0]],[0,5],color='blue')
#axScatter.plot([0,100],[tau_mcmc[0],tau_mcmc[0]],color='blue')

axHistX.hist(x,color='black',histtype='step',bins=BINS,weights=weighted,range=[TQMIN,TQMAX])
axHistY.hist(y,color='black',histtype='step',orientation='horizontal',bins=BINS,weights=weighted,range=[TAUMIN,TAUMAX])

plt.savefig('feature.pdf')
