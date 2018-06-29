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
