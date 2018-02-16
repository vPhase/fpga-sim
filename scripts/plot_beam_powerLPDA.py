import math
import myplot
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy
import json

NUM_BEAMS=21
PLOT = True

directory= '' #'sim_event_runs/'
filename = '../output/event_dict_2018-2-15-a.json'
with open(directory+filename, 'r') as f:
    event_dict = json.load(f)

theta=[]
beam0=[]
totalbeam=[]
for i in range(len(event_dict['1.0'])):
    theta.append(event_dict['1.0'][str(i)]['theta'])
    beam0.append(event_dict['1.0'][str(i)]['max_power0'])
    totalbeam.append(event_dict['1.0'][str(i)]['total_max_power'])

beam0=numpy.array(beam0)
totalbeam=numpy.array(totalbeam)
theta=numpy.rad2deg(theta)



plt.figure()
for i in range(NUM_BEAMS):    
    plt.plot(theta, beam0[:,i], 'o--',c='black')
    #plt.plot(theta, totalbeam[:,i], color=cm.Paired(i*15), lw=3)   

plt.grid(True)
plt.xlabel('Elevation Angle [deg]')
plt.ylabel('Power [sq. ADC]')
plt.show()
    
            
