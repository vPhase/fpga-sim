from scipy.optimize import curve_fit

import math
import tools.myplot
import matplotlib.pyplot as plt
import numpy
import copy
import sys

def funcExp(x, a, b, c):
    return c - a * numpy.exp(b * x) 

power_data = numpy.load('output/powsums_250ev_2e15length_0.15vrmsscale.npy')
nevent = 250
wfm_length = pow(2,15)
sampling_time=1./1.5 #ns

thresh_array = numpy.arange(5000,25000,100, dtype=int)

hits=[]
for beam in range(power_data.shape[1]):
    hits_in_single_beam=[]
    for thresh in thresh_array:
        hits_in_single_beam.append(len(numpy.where(power_data[:,beam,:] >= thresh)[0]))
    hits.append(hits_in_single_beam)
all_hits = numpy.sum(numpy.array(hits), axis=0)

plt.figure(15)
for i in range(15):
    plt.plot(thresh_array, numpy.array(hits[i])/(nevent*wfm_length*sampling_time*1.e-9), 'o')
plt.plot(thresh_array, all_hits/(nevent*wfm_length*sampling_time*1.e-9), '-',c='black')
plt.yscale('log')
plt.grid(True)


indx=numpy.where(all_hits > 1)[0]
print indx
indx_fit=numpy.where((all_hits > 0.00002*max(all_hits) ) & (all_hits < 0.01*max(all_hits) ))[0]
print indx_fit
##fit using polyfit in semi-log space:
logy = numpy.log(all_hits[indx_fit]/(nevent*wfm_length*sampling_time*1.e-9))
logy_w = numpy.log(1./(numpy.sqrt(all_hits[indx_fit])*nevent*wfm_length*sampling_time*1.e-9))
coeff=numpy.polyfit(thresh_array[indx_fit], logy, w=logy_w, deg=1)
poly = numpy.poly1d(coeff)
#yfit = lambda x : numpy.power(10, poly(thresh_array[indx_fit]))
yfit = lambda x : numpy.exp(poly(thresh_array[indx]))
yfit_extended = lambda x1 : numpy.exp(poly(thresh_array))

plt.figure(1)
#plt.plot(thresh_norm_array[indx], yfit(thresh_norm_array[indx]), '--', color='black', lw=1)

print coeff
'''
##fit using exponential
popt, pcov = curve_fit(funcExp, thresh_array[indx_fit], numpy.array(all_hits[i])[indx_fit]/(nevent*wfm_length*sampling_time*1.e-9) )
print popt
plt.plot(thresh_array[indx_fit], funcExp(thresh_array[indx_fit], *popt), '--', color='black', lw=1.5)
'''

plt.errorbar(thresh_array[indx], all_hits[indx]/(nevent*wfm_length*sampling_time*1.e-9), #xerr=numpy.zeros(len(indx)),
             yerr=1./(numpy.sqrt(all_hits)[indx]*nevent*wfm_length*sampling_time*1.e-9),
             #ecolor='black', elinewidth=2, fmt=None)
             elinewidth=2, fmt='o', ms=2,
             #label='{:.2f}, fitPow={:0.3f}'.format(labels[i], coeff[0]))
             #label='{:.2f}'.format(labels[i]) )
             )

plt.figure(3)
#plt.plot(thresh_array[indx], yfit(thresh_array[indx]), '--', color='red', lw=1)
plt.plot(thresh_array, yfit_extended(thresh_array), '--', color='red', lw=1)
plt.errorbar(thresh_array[indx], all_hits[indx]/(nevent*wfm_length*sampling_time*1.e-9), #xerr=numpy.zeros(len(indx)),
             yerr=1./(numpy.sqrt(all_hits[indx])*nevent*wfm_length*sampling_time*1.e-9),
             ecolor='black', elinewidth=2, fmt='o', ms=2,
             #elinewidth=2, fmt='o', ms=2,
             #label='{:.2f}, fitPow={:0.3f}'.format(labels[i], coeff[0]))
             #label='{:.2f}'.format(labels[i]))
             )
for i in range(15):
    plt.plot(thresh_array, numpy.array(hits[i])/(nevent*wfm_length*sampling_time*1.e-9), 'o', ms=1)

plt.figure(1)
plt.yscale('log')
plt.xscale('log', basex=2)

plt.legend(title='Vrms / Full range', numpoints=1, loc='lower left')
plt.ylabel('Trigger rate [Hz]')
plt.xlabel('Threshold [ADC counts squared]')
plt.title('8-antenna array, 5-bit digitization')
plt.ylim([0.1*numpy.min(all_hits/(nevent*wfm_length*sampling_time*1.e-9)),5*numpy.max(all_hits/(nevent*wfm_length*sampling_time*1.e-9))])
plt.grid()
'''
plt.figure(2)
plt.yscale('log')

plt.legend(title='Vrms / Full range', numpoints=1, loc='upper right')
plt.ylabel('Trigger rate [Hz]')
plt.xlabel('Threshold, sigma')
plt.title('8-antenna array, 5-bit digitization')
plt.ylim([0.1*numpy.min(all_hits/(nevent*wfm_length*sampling_time*1.e-9)),5*numpy.max(all_hits/(nevent*wfm_length*sampling_time*1.e-9))])
plt.grid()
'''

plt.figure(3)
plt.yscale('log')

plt.legend(title='Vrms / Full range', numpoints=1, loc='upper right')
plt.ylabel('Trigger rate [Hz]')
plt.xlabel('Threshold [ADC counts]')
plt.title('8-antenna array, 5-bit digitization')
#plt.ylim([0.1*numpy.min(all_hits/(nevent*wfm_length*sampling_time*1.e-9)),5*numpy.max(all_hits/(nevent*wfm_length*sampling_time*1.e-9))])
plt.xlim([4500, 25000])
plt.ylim([0.2,5e10])
plt.grid()

plt.show()
               

            
