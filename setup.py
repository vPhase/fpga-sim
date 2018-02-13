
#directory="/project/avieregg/gno_analysis/anechoic_test_analysis/data_16_march/"
directory="test_data/"
#directory="/project/avieregg/gno_analysis/anechoic_test_analysis/data_15_march_2016/"


#basefilenames=["160317_032902_telewave_hba_snr6_avg"]
basefilenames=["160317_020105_ara_vpoltx_snr10_avg"]
#basefilenames=['160317_022052_ara_vpoltx_fullband_avg']

#####use this file for ARA simulations
#basefilenames=['160317_014032_ara_vpoltx_snr7_avg']

#basefilenames=["160317_032902_telewave_hba_snr6_avg",
#               "160317_020105_ara_vpoltx_snr10_avg"]


def make_file_from_channels(directory=directory,
                            basefilename=''):

    files=[directory+basefilename+"_Ch1.csv",
           directory+basefilename+"_Ch2.csv",
           directory+basefilename+"_Ch3.csv",
           directory+basefilename+"_Ch4.csv"]
    return files

def setup_use_scope_data(basefile='', channel=0, fastFrame=True):
    import tools.read_tektronix as read_tek
    #_file=make_file_from_channels(basefilename=basefile)
    _file=basefile
    #return read_tek.read_scope_cvs(str(_file[channel]), Verbose=True)
    return read_tek.read_scope_cvs(str(_file), Verbose=False, fastFrame=fastFrame)

def make_list_of_files(basefilenames=basefilenames):
    list_of_files = []
    for i in range(len(basefilenames)):
        the_files=make_file_from_channels(basefilename=basefilenames[i])
        list_of_files.append(the_files)
    return list_of_files 

if __name__=="__main__":

    #a=make_list_of_files(basefilenames)
    #print a[0][0]
    setup_use_scope_data()

