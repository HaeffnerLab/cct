"""get_data - A module to read data from the datavaule

This is collection of classes and functions to read data from the
datavault. Contains:

MeasDay - Load easily data and parameters from an entire day 

ReadData - Load a specific dataset 

"""

import numpy as np
import pylab as pl
import os
try:
    from treedict import TreeDict
except ImportError:
    TreeDict = dict

def getbasepath():
    try:
        dv_dir = os.environ['DV_PATH']
    except KeyError:
        dv_dir = "/home/cct/LabRAD/cct/data/"
    basepath = dv_dir + 'Experiments.dir'
    basepath2 = dv_dir + "ScriptScanner.dir"
    print basepath
    return basepath, basepath2

BASEPATH, BASEPATH2 = getbasepath()

def Value(x,y):
    return x

class MeasDay():
    """An object for analyzing data fro a specific day
    usage: MeasDay(,date, basepath=BASEPATH, add_path=BASEPATH2, experiments=None)

    BASEPATH and BASEPATH2 are taken from the environment variable DV_PATH 
    if DV_PATH is not set, the default CCT datavault path is assumed

    experiments is a list of subdirectories, that provide valid
    Experiments. Default are all Experiments in
    DV_PATH/Experiments.dir except for "Excitation_729.dir"

    Examples:
    >>> a = MeasDay('2014Jun08')
    Imports the data from the entire day

    >>> a.show_files() 
    prints all files from the day

    >>> a.param_dict['2256_41']
    returns a dictionary with all the parameters for the measurement '2256_41'
   
    >>> a.read_file('2256_41')
    returns a numpy array of the dataset consisting of [x, y, std(y)]

    >>> a.plot_file('2256_41')
    plots the data

    """
    def __init__(self,date, basepath=BASEPATH, add_path=BASEPATH2, experiments=None):
        self.date = date
        self.file_dict = generate_file_list(date, basepath=basepath, add_path=add_path, 
                                            experiments=experiments)
        self.file_list = self.file_dict.keys()
        self.param_dict = self._get_param_dict()
        
    def show_files(self):
        for time_str in self.file_list:
            params = self.param_dict[time_str]
            if params != {}:
                try:
                    print(self._get_param_str(params, time_str))
                except:
                    pass

    def read_file(self, time_str):
        this_path = self.file_dict[time_str]
        rd = ReadData(self.date, time_str=time_str, direct_path=this_path)
        return rd.data

    def plot_file(self,time_str,fmt=None):
        d1 = self.read_file(time_str)
        pl.errorbar(d1[:,0],d1[:,1],d1[:,2],fmt=fmt)
        params = self.param_dict[time_str]
        try:
            pl.xlabel(params['Scanned Value'])
            pl.ylabel('Excitation')
        except:
            pass

    def _get_param_dict(self):
        param_dict = {}
        for time_str in self.file_list:
            params = get_parameters(time_str, self.file_dict)
            param_dict[time_str] = params
        return param_dict

    def _get_param_str(self, params, time_str=None):
        str1 = params['Title']
        date_index = str1.find(self.date)
        str1 = str1[0:date_index].strip()
        if time_str != None:
            str1 = time_str + ' ' + str1
        return str1
        

def generate_file_list(date, basepath=BASEPATH, add_path=BASEPATH2, experiments=None):
    if experiments == None:
        dirlist = os.listdir(basepath)
        dirlist.remove('Excitation729.dir')   
    else:
        dirlist = experiments
    dirlist += [add_path]
    datedir_list = []
    for dirname in dirlist:
        datedir = BASEPATH +'/'+dirname +'/' + date +'.dir'
        if os.path.isdir(datedir):
            
            datedir_list.append(datedir)
    print datedir_list
    add_path = add_path+'/' + date +'.dir'
    if (os.path.isdir(add_path)):
            datedir_list.append(add_path)
    time_dict = {}

    for dirname in datedir_list:
        time_list = os.listdir(dirname)
        for time_str in time_list:
            key = time_str.strip('.dir')
            if time_dict.has_key(key):
                print "Warning Key " + str(key) + " already used: " + dirname +'/'+time_str
                print "Existing entry: " + str(time_dict[key])
            if os.path.splitext(key)[1] == '':
                time_dict[key] = dirname +'/' + time_str
    return time_dict

def get_parameters(time, time_dict):
    import ConfigParser
    Config = ConfigParser.ConfigParser()
    dirname = time_dict[time]
    dirlist = os.listdir(dirname)
    dirlist.remove("session.ini")
    param_dict = TreeDict()
    for fname in dirlist:
        if os.path.splitext(fname)[1] == '.ini':
                Config.read(dirname +'/'+fname)
        for sect in Config.sections():
            option_list = Config.options(sect)
            if 'Parameter' in sect:
                dstr = 'data = '+Config.get(sect,'data')
                exec(dstr)
                mykey = Config.get(sect,'label')
                mykey = mykey.replace('-','_')
                param_dict[mykey] = data
            param_dict['Scanned_Value'] = Config.get('Independent 1','label') 
            param_dict['Title'] = Config.get('General','title') 
    return param_dict

class ReadData():
    def __init__(self, date, time_str=None, experiment=None,  basepath = BASEPATH, 
                 get_errors=True, direct_path=None):
        self.basepath = basepath
        self.date = date
        self.experiment = experiment
        self.get_errors = get_errors
        if time_str != None:
            self.get_data(time_str, experiment, direct_path=direct_path)
    
    def calcerror(self, data, nr_of_cycles=100):
        return np.sqrt(data*(1-data)/nr_of_cycles)
        
    def get_data(self, time_str, experiment=None, basepath=BASEPATH, direct_path=None):
        if experiment == None:
            experiment = self.experiment
        if direct_path == None:
            pathname = self.basepath+ '/' + experiment + ".dir/" + self.date + '.dir/' + time_str + '.dir/'
        else:
            pathname = direct_path + '/'
        
        self.data = None
        fl = os.listdir(pathname)
        fl.sort()
        for files in fl:
            if files.endswith("csv"):
                print files
                if self.data == None:
                    self.data = np.loadtxt(pathname + files,delimiter=',')
                else:
                    a2 = self.data
                    a1 =  np.loadtxt(pathname + files,delimiter=',')
                    d0 = np.zeros((a2.shape[0],a2.shape[1]+a1.shape[1]-1))
                    d0[:,0:a2.shape[1]] = a2
                    d0[:,a2.shape[1]:] = a1[:,1:]
                    self.data = d0


        if self.get_errors == False:
            return self.data
        else:
            a = np.zeros((self.data.shape[0],self.data.shape[1]+1))
            a[:,0:-1] = self.data
            a[:,2] = self.calcerror(a[:,1])
            self.data = a
            return a



    def get_images(self, time_str, experiment=None, basepath=BASEPATH, direct_path=None):
        if experiment == None:
            experiment = self.experiment
        if direct_path == None:
            pathname = self.basepath+ '/' + experiment + ".dir/" + self.date + '.dir/' + time_str + '.dir/'
        else:
            pathname = direct_path + '/'

        fh = open(pathname + 'images.npy')
        data_list = []
        n_im = 0
        try:
            while(True):
                im = np.load(fh)
                data_list.append(im)
                n_im += 1
        except IOError:
            print "Loaded " + str(n_im) + " images"
        return data_list

