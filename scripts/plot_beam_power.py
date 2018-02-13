import math
#import tools.myplot
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy
import json

NUM_BEAMS=15
PLOT = True

directory= '' #'sim_event_runs/'
filename = '../output/event_dict_2018-2-13-a.json'
with open(directory+filename, 'r') as f:
    event_dict = json.load(f)

theta=[]
beam0=[]
beam1=[]
beam2=[]
totalbeam=[]
for i in range(len(event_dict['1.0'])):
    theta.append(event_dict['1.0'][str(i)]['theta'])
    beam0.append(event_dict['1.0'][str(i)]['max_power0'])
    beam1.append(event_dict['1.0'][str(i)]['max_power1'])
    beam2.append(event_dict['1.0'][str(i)]['max_power2'])
    totalbeam.append(event_dict['1.0'][str(i)]['total_max_power'])

beam0=numpy.array(beam0)
beam1=numpy.array(beam1)
beam2=numpy.array(beam2)
totalbeam=numpy.array(totalbeam)
theta=numpy.rad2deg(theta)

sum_beam = totalbeam[:,6] + totalbeam[:,7] + totalbeam[:,8]
plt.figure()
#plt.plot(theta, sum_beam)
plt.plot(theta, totalbeam[:,6])
plt.plot(theta, beam0[:,6]+beam1[:,6])


#plt.plot(theta, totalbeam[:,7])
#plt.plot(theta, totalbeam[:,8])

plt.figure()
for i in range(8,10):    
    #plt.plot(theta, beam0[:,i], 'green')
    #plt.plot(theta, beam1[:,i], 'blue')
    plt.plot(theta, beam2[:,i], 'orange')
    #plt.plot(theta, totalbeam[:,i], color='black')    
    #plt.plot(theta, beam0[:,i]+beam1[:,i], color='black')

plt.show()
    
            
