import numpy
#-- configs for run_fpga_sim.py
#-- see detector/geometry.py for a few more options related to the array geometry

DIGITIZE=True    #digitize, or not
digitize_num_bits = 5 #number of bits in beamformer
digitize_vrms_scale = 0.15  #0.125 sets about 4 ADC counts in Vrms, which matches what we plan to run system(?)
time_domain_sampling_rate = 0.66  #ns, for generating noise sample
WFM_LENGTH = pow(2, 14) #512  #pow(2,15) 
NOISE=True   #generate thermal noise


USE_ANTENNA_MODEL = False #Adds simple cos(theta) amplitude correction
THROW_CAL_PULSER = False   # send cal pulser point source (instead of plane wave) from defined position in geometry.py
THROW_ELEVATION = False  #throw plane waves at random directions if True
THROW_DELAY_LO = -150  #Note this delay is added for the fully upsampled waveform
THROW_DELAY_HI = 150   #Note this delay is added for the fully upsampled waveform
theta_i = 100        #if THROW_ELEVATION=False, send plane wave at theta_i
nevent  = 500       #number of events to throw per snr step
SAVE_POWERSUMS = True    #save powersum file to .npy file, only saved for a single snr step.
                          # [Really only useful for generating rate vs. threshold curves]
                          
USE_SCOPE_CSV = False     #load impulse from Tektronix csv file
USE_TXT_TEMPLATE = True   #load impulse from tab-separated txt file (2 columns = time, voltage)
TXT_TEMPLATE_FILE = 'test_data/impulse_upsampled.txt'  #filename required if USE_TXT_TEMPLATE=True
ADD_IMPULSE = False 
SAVE_EVENT_DICT = False  #for further analysis
OUTPUT_JSON_FILENAME='output/event_dict_2018-2-13-d.json'
ADD_STAGGER_DELAY = False  # add extra fiber length delay for each antenna unit
#-- stagger delay due to extra optical fiber lengths at each antenna module (positive value = delay). 
STAGGER_DELAY = 250 #Note this delay is added for the fully upsampled waveform 

#-- careful here. The idea is to upsample the impulse in order to apply fine shifts when throwing
#-- random elevations. Then the impulse is downsampled to the same rate as the generated thermal noise in
#-- order to co-add.
UPSAMPLE_FACTOR = 10  #factor by which to upsample the test impulse (scope data is at 5GSPS)
DOWNSAMPLE_FACTOR = 33 #factor by which to downsample the test impulse
#check: 200 ps / 10 * 33 = 660ps, which matches our 'time_domain_sampling_rate'

thermal_noise_freq_low=0.2 #ghz
thermal_noise_freq_hi=0.75 #ghz

#-----
# beamforming configs here
NUM_FPGA_BEAMS = 15
SUBBEAM_0 = True #how many 'sub-beams' are within each beam (this should always be 'True', unless debugging)
SUBBEAM_1 = True #how many 'sub-beams' are within each beam
SUBBEAM_2 = True #how many 'sub-beams' are within each beam (max 3 right now)
subbeam_0_delays=[0,1,2,3,4, 5, 6, 7, 8, 9,10,11,12,13,14]
subbeam_1_delays=[1,3,5,7,9,11,13,15,17,19,21,23,25,27,29]
subbeam_2_delays=subbeam_1_delays
#-- beam 'codes'. This is the delay multiplier at each antenna. Use 99 for antenna not in coherent sum 
subbeam_0_codes = [ 4, 3, 2, 1, 0, -2, -4]
subbeam_1_codes = [ 2,99, 1,99, 0, -1, -2]
subbeam_2_codes = [99, 2,99, 1,99, -1, 99]

power_calculation_sum_length = 16 #samples
power_calculation_interval   = 8  #samples

#-----------------------------------
#-- list of SNRs to throw in simulation.
#-- To only run a single snr, make a list of one entry (i.e. snr_array=[4.0])
#snr_array = numpy.arange(0.2, 4.1, 0.2)
snr_array = [1.0]  #for noise-only simluation, run a single SNR

    
