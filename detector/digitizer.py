import numpy as np

def digitize(wave, num_bits=3, dynrange=1.0, ped=0.5, zero=True):
    '''
    emulate digitization, return waveform in adc counts 
    '''
    mv_lsb   = dynrange / pow(2,num_bits)   #mV/lsb
    digitized_wave = []
    vert_array = np.arange(0, pow(2, num_bits))
    
    for i in range(len(wave)):
            
        bit_temp  = 0
        wave_temp = wave[i] + ped
        
        if wave_temp >=  (ped+dynrange/2):
            wave_temp = dynrange #pow(num_bits,2)-1
            
        elif wave_temp <= (ped-dynrange/2):
            wave_temp = 0.0
        #    
        #else:
        temp = np.where(vert_array < (wave_temp/mv_lsb - 1) )[0]
        if len(temp):
            wave_temp = np.where(vert_array < (wave_temp/mv_lsb ) )[0][-1]
        else:
            wave_temp = 0
        #for vert in range(pow(2,num_bits)):
        #    if wave_temp < mv_lsb * (vert+1):
        #        wave_temp = vert
        #        break
        
        if zero:
            wave_temp = wave_temp - pow(2,num_bits)/2 + 0.5
            
        digitized_wave.append(wave_temp)                   

    return np.array(digitized_wave)

def numpyDigitize(wave, num_bits, dynrange=1.0, ped=0.5, zero=True):
    '''
    this is a better way to do it
    '''
    vert_array = np.arange(1, pow(2, num_bits)) * dynrange / (pow(2, num_bits))
    digitized_wave=np.array(np.digitize(wave+ped, vert_array, right=False), dtype=np.int)

    if zero:
        digitized_wave -= pow(2, num_bits)/2
    return digitized_wave
    
if __name__=='__main__':
    #import myplot
    import matplotlib.pyplot as plt
    import noise
    
    thermal_noise = noise.ThermalNoise(0.12, 0.85, filter_order=(4,6), v_rms=0.5, fbins=4096)
    mynoise = thermal_noise.makeNoiseWaveform()

    #plt.plot(mynoise[1], mynoise[2][0])
    #plt.show()

    bits=5
    pedestal = 0.5
    dv = digitize(np.real(mynoise[2][0]), num_bits=bits, ped=pedestal)
    dw = numpyDigitize(np.real(mynoise[2][0]), num_bits=bits, ped=pedestal)
    
    plt.figure()
    #plt.plot(mynoise[1], dv, 'o')
    plt.plot(mynoise[1], dw, '^')
    plt.ylim([-8.5, 8.5])
    plt.grid()

    plt.figure()
    plt.hist(dw, bins=np.arange(-pow(2, bits)/2, pow(2, bits)/2+1))
    plt.show()
