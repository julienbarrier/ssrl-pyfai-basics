# Basic code for integrating multiple images at different tth using pyFAI.MultiGeometry
def plot_100k(files, centerx, centery, sdd, name, wavelength=.992e-10, Qchidir='./plots/'):
    """
    Return Q,I and save the Q-Chi plot to Qchidir.
    Takes a list of filenames (use find_scans), centerx and centery, the sdd (in meters),
    wavelength (in meters), sample name, and the directory to save a Q-chi image.
    """
    
    import pyFAI
    from pyFAI.multi_geometry import MultiGeometry
    from copy import deepcopy
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Check this is right? The mono energy should be in the spec file (no filetype)
    w1 = wavelength
    
    # Create a new detector. You should also be able to import the pilatus 100k from pyFAI.detectors
    # but be careful, this has the angles defined differently (i.e.: positive tth = negative rot2)
    det = pyFAI.detectors.Detector(172e-6, 172e-6)
    det.max_shape=(487,195)

    poni1 = (487-centerx) * 172e-6
    poni2 = centery * 172e-6

    # Define ai for scan 1
    ai = pyFAI.AzimuthalIntegrator(dist=sdd, poni1=poni1, poni2=poni2,
                                  detector=det)
    ai.set_wavelength(w1)
    # If you want to play with tilts, set the initial ai.rot1, rot2, rot3 here.
    ai.rot1 = 0 *  np.pi/180
    ai.rot2 = -6 * np.pi/180
    ai.rot3 = 0 *  np.pi/180

    imgs = []
    ais = []
    step = 1 * np.pi/180
    # For each scan, move rot2 and create a new ai using deepcopy
    for i in range(54):
        fn = files[i]
        img = read_raw_100k(fn)
        my_ai = deepcopy(ai)
        my_ai.rot2 -= i * step
        imgs.append(img)
        ais.append(my_ai)
        if i == 5: plt.imshow(img, origin='lower')

    mg = MultiGeometry(ais, unit="q_A^-1", radial_range=(0.5,5))
    
    Q,I = mg.integrate1d(imgs,5000)
    
    # This creates and plots a Q-chi image
    sns.set_style("white")
    I2D, Q2D, chi = mg.integrate2d(imgs, 1000, 360)
    fig2 = plt.figure(figsize=(10,6))
    plt.imshow(I2D[245:295], origin="lower", 
           extent=[Q2D.min(), Q2D.max(), 0, chi.max()],
           aspect='auto', cmap='hot')
    plt.xlabel('Q / $\\AA ^{-1}$', fontsize=20)
    plt.tick_params(axis='x', which='major', labelsize=16)
    plt.ylabel('chi / $\\AA ^{-1}$', fontsize=20)
    plt.tick_params(axis='y', which='major', labelsize=16)
    plt.xlim(0.5,2.5)
    plt.title("{} Q vs chi".format(name), fontsize=24)
    figname = "{}_Q_chi.png".format(name)
    plt.savefig(Qchidir + figname)
    plt.close(fig2)
    
    return Q,I
