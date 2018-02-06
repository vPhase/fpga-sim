
#directory="/project/avieregg/gno_analysis/anechoic_test_analysis/data_16_march/"
directory="test_data/"
#directory="/project/avieregg/gno_analysis/anechoic_test_analysis/data_15_march_2016/"

#basefilenames = ["160317_024344_telewave_hba_3ant_noise"]

#basefilename = "160316_110044_telewave_hba_space_0"
#basefilenames = ["160316_110938_telewave_hba_space_1"]
#basefilename = "160316_111631_telewave_hba_space_2"
#basefilename = "160316_112421_telewave_hba_space_3"
#basefilename = "160316_113715_telewave_hba_space_4v2"
#basefilename="160316_114405_telewave_hba_space_5"

#basefilename="160316_120557_telewave_lba_space_0"
#basefilename="160316_121219_telewave_lba_space_1"
#basefilename="160316_121912_telewave_lba_space_2"
#basefilename="160316_122653_telewave_lba_space_3"
#basefilename="160316_123422_telewave_lba_space_4"

#basefilename="160316_064931_ara_vpol_space0_v3"
#basefilename="160316_065730_ara_vpol_space1"
#basefilename="160316_070550_ara_vpol_space2"
#basefilename="160316_071309_ara_vpol_space3"
#basefilename="160316_071852_ara_vpol_space4"

#basefilename='160317_032956_telewave_hba_snr6'
#basefilenames=['160317_025550_telewave_hba_snr0']
#basefilename="160317_030155_telewave_hba_snr1"
#160317_030659_telewave_hba_snr2
#160317_031204_telewave_hba_snr3
#basefilename='160317_031840_telewave_hba_snr4'
#basefilename='160317_032956_telewave_hba_snr6'
#basefilename = "160316_113033_telewave_hba_space_4"

#basefilenames=["160317_032902_telewave_hba_snr6_avg"]
basefilenames=["160317_020105_ara_vpoltx_snr10_avg"]
#basefilenames=['160317_022052_ara_vpoltx_fullband_avg']

#####use this file for ARA simulations
#basefilenames=['160317_014032_ara_vpoltx_snr7_avg']

#basefilenames=["160317_032902_telewave_hba_snr6_avg",
#               "160317_020105_ara_vpoltx_snr10_avg"]
'''
basefilenames=["160317_032902_telewave_hba_snr6_avg",
               "160317_051426_telewave_hba_16deg_avg",
               "160317_052325_telewave_hba_8deg_avg"]
'''
'''
basefilenames = [
    '160317_031204_telewave_hba_snr3',
    '160317_030659_telewave_hba_snr2',
    '160317_030155_telewave_hba_snr1',
    '160317_025550_telewave_hba_snr0',
    '160317_031840_telewave_hba_snr4',
    '160317_032454_telewave_hba_snr5',
    '160317_032956_telewave_hba_snr6'
]
'''

'''
basefilenames = [
    '160317_004654_ara_vpoltx_snr0',
    '160317_010126_ara_vpoltx_snr1',
    '160317_011519_ara_vpoltx_snr3',
    '160317_010934_ara_vpoltx_snr2',
    '160317_020208_ara_vpoltx_snr10',
    '160317_012144_vpoltx_snr4',
    '160317_015627_ara_vpoltx_snr9',
    '160317_012901_ara_vpoltx_snr5',
    '160317_014954_ara_vpoltx_snr8',
    '160317_013539_ara_vpoltx_snr6',
    '160317_014138_ara_vpoltx_snr7']
'''
#basefilenames=['160317_031840_telewave_hba_snr4']
#basefilenames=['160317_025550_telewave_hba_snr0']
#basefilenames=['160317_030155_telewave_hba_snr1']
#basefilenames = ["160317_032421_telewave_hba_snr5_avg"]
#basefilenames=['160317_012719_ara_vpoltx_snr5_avg']

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

