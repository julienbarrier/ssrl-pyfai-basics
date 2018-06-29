import glob

# fuction to load the files
def find_scans(indir,fbase):
    '''return the raw files in directory indir with expression fbase'''
    scans = glob.glob(indir+'*'+fbase+'*.raw')
    scans.sort()
    print('found %s scans'%len(scans))
    return(scans)

def find_dirs(d):
    '''list the directories in directory d'''
    import os
    # uncomment next line in windows environments:
    directories = [os.path.join(d,o + '/') #.replace('\\','/')
                   for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    directories.sort()
    return directories

#function to read the raw files that SSRL saves
def read_raw_300k(fn, w=w, h=h):
    try:
        with open(fn, 'r') as f:
            img = np.fromfile(f, dtype=np.int32)
        img = np.reshape(img, (h,w), order='C')
        return img
    except:
        print('Error reading file: %s'%fn)
        return(None)

def read_raw_100k(fn, w,h):
    '''pad two olumns on right and left with zeros'''
    try:
        with open(fn, 'r') as f:
            img = np.fromfile(f, dtype=np.int32)
        img = np.reshape(img, (h,w), order='C')
        img[:2,:] = 0
        img[-2:,:] = 0
        img = np.flipud(img.T)
        return img
    except:
        print('Error reading file: %s'%fn)
        return(None)
