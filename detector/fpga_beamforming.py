import detector.geometry as geometry
import config as cfg

import math
import numpy as np

def doFPGABeamForming(wfms, subbeam0=True, subbeam1=False, subbeam2=False):
    '''
    input 'wfms' should already have sampling rate set to appropriate rate
    '''
    coherent_sums_0=[]
    coherent_sums_1=[]
    coherent_sums_2=[]

    for i in range(cfg.NUM_FPGA_BEAMS):
        _coherent_sums_0 = np.zeros(len(wfms[0]))
        _coherent_sums_1 = np.zeros(len(wfms[0]))
        _coherent_sums_2 = np.zeros(len(wfms[0]))
        for j in range(geometry.nantenna):
            if subbeam0 and cfg.subbeam_0_codes[j] != 99:
                _coherent_sums_0 += np.roll(wfms[j], cfg.subbeam_0_delays[i]*cfg.subbeam_0_codes[j])
            if subbeam1 and cfg.subbeam_1_codes[j] != 99:
                _coherent_sums_1 += np.roll(wfms[j], cfg.subbeam_1_delays[i]*cfg.subbeam_1_codes[j])
            if subbeam2 and cfg.subbeam_2_codes[j] != 99:
                _coherent_sums_2 += np.roll(wfms[j], cfg.subbeam_2_delays[i]*cfg.subbeam_2_codes[j])
                
        coherent_sums_0.append(_coherent_sums_0)
        coherent_sums_1.append(_coherent_sums_1)
        coherent_sums_2.append(_coherent_sums_2)

    return coherent_sums_0, coherent_sums_1, coherent_sums_2

def doFPGAPowerCalcSingleBeam(beam, sum_length=16, interval=8):
    num_frames = int(math.floor((len(beam)-sum_length) / interval))
        
    power = np.zeros(num_frames)
    for frame in range(num_frames):
        for i in range(frame*interval, frame*interval + sum_length):
            power[frame] += (beam[i] * beam[i]) #/ sum_length
    return power

def doFPGAPowerCalcAllBeams(beam, sum_length, interval):
    beam_powers = []
    for i in range(cfg.NUM_FPGA_BEAMS):
        beam_powers.append(doFPGAPowerCalcSingleBeam(beam[i], sum_length, interval)  )
     
        #total_power.append(np.sum([power_beam8, power_beam4a, power_beam4b],axis=0,dtype=np.int))

    return np.array(beam_powers,dtype=int)

