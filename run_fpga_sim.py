import detector.noise as noise
import detector.digitizer as digitizer
import detector.geometry as geometry
import tools.waveform as waveform
import setup
import detector.fpga_beamforming as beamform

import math
import tools.myplot
import matplotlib.pyplot as plt
import numpy
import copy
import json
import sys
import config as cfg

###################
# see config.py for setting options
##################

#want to embed an impulse?
if cfg.ADD_IMPULSE:
    #-- specify scope data file in setup.py from which to take avg. waveform
    #-- load from Tektronix scope data
    if cfg.USE_SCOPE_CSV and cfg.ADD_IMPULSE:
        files = setup.make_list_of_files()
        scope_avg_waveform = setup.setup_use_scope_data(files[0][0],channel=1, fastFrame=False)
        
        impulse=waveform.Waveform(scope_avg_waveform[1], scope_avg_waveform[0])
        impulse.meanSubtract()
        impulse.voltage = numpy.roll(impulse.voltage, 100) #center waveform a bit ad-hoc
        impulse.upsampleFreqDomain(cfg.UPSAMPLE_FACTOR)  

        ##-- uncomment to save to flat text file for next time
        '''
        with open("impulse_upsampled.txt", "w") as f:
            for i in range(len(impulse.time)):
                f.write(str(impulse.time[i])+'\t'+str(impulse.voltage[i])+'\n')
        f.close()
        '''
        
    elif cfg.USE_TXT_TEMPLATE:
        v= numpy.loadtxt(cfg.TXT_TEMPLATE_FILE)
        impulse = waveform.Waveform(v[:,1],v[:,0])

        impulse_vpp=(numpy.max(impulse.voltage)-numpy.min(impulse.voltage))
    impulse.voltage /= impulse_vpp/2.0 #normalize
    
#define noise in frequency domain
if cfg.NOISE:
    print 'generating noise traces...'
    thermal_noise = noise.ThermalNoise(cfg.thermal_noise_freq_low, cfg.thermal_noise_freq_hi, fbins=cfg.WFM_LENGTH, normalize=True,
                                       filter_order=(3,4), time_domain_sampling_rate=cfg.time_domain_sampling_rate)
    noise_traces = thermal_noise.makeNoiseWaveform(ntraces=cfg.nevent*geometry.nantenna)

#simulate..
event_dict={}
all_fpga_power=[]

for snr in cfg.snr_array:
    event_dict[snr]={}
    if cfg.NOISE:
        print "snr = ", snr

    #-- get delays from point-source emitter
    if cfg.THROW_CAL_PULSER:
        point_source_time_delays=[]
        thetas=[]
        for j in range(geometry.nantenna):
            point_source_time_delays.append(
                geometry.timeDifference(geometry.euclideanDistance2D(
                    (geometry.z_cal_pulser, geometry.x_cal_pulser),
                    (geometry.z_ant[j], geometry.x_ant[j]) )))

            if j > 0:
                thetas.append(geometry.getTheta(point_source_time_delays[j]-point_source_time_delays[j-1]))

        point_source_time_delays=numpy.array(point_source_time_delays)-min(point_source_time_delays)
        delay_i = numpy.round(point_source_time_delays / impulse.dt)
        
    #-- otherwise, send perfect plane wave
    else:
        delay_i = numpy.ones(cfg.nevent) * int(cfg.theta_i)
        if not cfg.THROW_ELEVATION and cfg.ADD_IMPULSE:
            theta_static = geometry.getTheta(delay_i*impulse.dt)[0]

        thetas=numpy.zeros(cfg.nevent)
        if cfg.THROW_ELEVATION and cfg.ADD_IMPULSE:
            #-- throw random delays, save the associated theta value
            delay_i = numpy.random.randint(cfg.THROW_DELAY_LO, cfg.THROW_DELAY_HI, size=cfg.nevent) * 1
            delay_i = numpy.sort(delay_i)
            thetas = geometry.getTheta(delay_i*impulse.dt)
    
    for i in range(cfg.nevent):
        event_dict[snr][i]={}

        if i%100==0:
            print 'event', i
        event_data = []

        #-- generate waveforms for each channel
        for jj in range(geometry.nantenna):
            #-- if impulse added, rotate pulse in window according to thrown elevation angle.
            #-- also, add stagger delay here if specified
            if cfg.ADD_IMPULSE:
                impulse_copy=copy.copy(impulse)
                #-- apply pulse time-delay here
                if cfg.THROW_CAL_PULSER:
                    impulse_copy.voltage=numpy.roll(impulse_copy.voltage,int(delay_i[jj]))
                else:
                    impulse_copy.voltage=numpy.roll(impulse_copy.voltage,int(delay_i[i])*geometry.antenna_location[jj])
                #-- add stagger delay, if specified
                if cfg.ADD_STAGGER_DELAY:
                    impulse_copy.voltage = numpy.roll(impulse_copy.voltage,cfg.STAGGER_DELAY*geometry.antenna_location[jj])
                #-- downsample to match thermal noise / digitizer sampling rate
                impulse_copy.downsampleTimeDomain(cfg.DOWNSAMPLE_FACTOR)
                impulse_copy.takeWindow([0,cfg.WFM_LENGTH])
                if cfg.USE_ANTENNA_MODEL:
                    if cfg.THROW_CAL_PULSER:
                        impulse_copy.voltage = impulse_copy.voltage * abs(math.cos(thetas[jj]))
                    else:
                        impulse_copy.voltage = impulse_copy.voltage * abs(math.cos(thetas[i]))

            #-- if noise and impulse, co-add:
            if cfg.NOISE and cfg.ADD_IMPULSE:
                event_wfms = impulse_copy.voltage*snr + numpy.real(noise_traces[2][i*geometry.nantenna+jj])
            #-- if impulse only:
            elif cfg.ADD_IMPULSE:
               event_wfms = impulse_copy.voltage
            #-- if noise only:
            elif cfg.NOISE:
                event_wfms = numpy.real(noise_traces[2][i*geometry.nantenna+jj])

            #-- digitize here, if specified:
            if cfg.DIGITIZE and cfg.NOISE: 
                event_wfms = digitizer.numpyDigitize( cfg.digitize_vrms_scale * event_wfms, num_bits=cfg.digitize_num_bits)
            elif cfg.DIGITIZE:
                event_wfms = digitizer.numpyDigitize( 0.5 * event_wfms, num_bits=cfg.digitize_num_bits)
            
            event_data.append(event_wfms)
            
        #for jj in range(geometry.nantenna):
        #    plt.plot(event_data[jj] - 60*jj)
        #plt.show()

        #-- do beamforming here
        beams = beamform.doFPGABeamForming(event_data, cfg.SUBBEAM_0, cfg.SUBBEAM_1, cfg.SUBBEAM_2)
        if cfg.SUBBEAM_0:
            fpga_power0 = beamform.doFPGAPowerCalcAllBeams(beams[0], cfg.power_calculation_sum_length, cfg.power_calculation_interval)
            total_fpga_power = fpga_power0
            event_dict[snr][i]['max_power0']=numpy.max(fpga_power0, axis=1).tolist()
        if cfg.SUBBEAM_1:
            fpga_power1 = beamform.doFPGAPowerCalcAllBeams(beams[1], cfg.power_calculation_sum_length, cfg.power_calculation_interval)
            total_fpga_power = numpy.sum([total_fpga_power, fpga_power1],axis=0,dtype=numpy.int)
            event_dict[snr][i]['max_power1']=numpy.max(fpga_power1, axis=1).tolist()
        if cfg.SUBBEAM_2:
            fpga_power2 = beamform.doFPGAPowerCalcAllBeams(beams[2], cfg.power_calculation_sum_length, cfg.power_calculation_interval)
            total_fpga_power = numpy.sum([total_fpga_power, fpga_power2],axis=0,dtype=numpy.int)
            event_dict[snr][i]['max_power2']=numpy.max(fpga_power2, axis=1).tolist()

        event_dict[snr][i]['total_max_power']=numpy.max(total_fpga_power, axis=1).tolist()

        #for q in range(15):
        #    plt.plot(beams[2][q])
        #plt.show()

        if cfg.SAVE_POWERSUMS:
            all_fpga_power.append(total_fpga_power)

        if cfg.THROW_CAL_PULSER:
            event_dict[snr][i]['theta'] = thetas
        elif cfg.THROW_ELEVATION:
            event_dict[snr][i]['theta'] = thetas[i]
        #else:
        #    event_dict[snr][i]['theta'] = theta_static

    ##--useful for threshold scans; extrapolating rate vs threshold to lower rates. Only enable when running NOISE only at a single SNR:
    if cfg.SAVE_POWERSUMS:
        numpy.save('output/powsums.npy', numpy.array(all_fpga_power,dtype=int))

#-- this saves the maximum power in each beam for each event
if cfg.SAVE_EVENT_DICT:
    with open(cfg.OUTPUT_JSON_FILENAME,'w') as f:
        json.dump(event_dict,f)

