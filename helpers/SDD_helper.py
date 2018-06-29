def calculate_SDD(ims, tth_start, tth_end, centerx, centery, hw_x = 4, hw_y = 10, pixel_size=172e-6, num_steps=100):
    """
    Fits a series of scans of intensity moving across the detector to calculate SDD.
    Takes in ims (a list of np arrays), the start and end values of tth for the images,
    and the beam centerx and centery.
    The halfwidths are the number of pixels on either side of beam center that are 
    considered. 
    
    Returns SDD in meters
    """
    num_steps +=1 #spec does this automatically
    y_pos = np.zeros(len(ims))
    tth = np.linspace(tth_start,tth_end,num_steps)
    for i in range(len(ims)):
    #for i in range(5):
        im = ims[i]
        # y pixel values
        ys = np.arange(im.shape[0])
        xs = np.arange(im.shape[1])
        
        #trim to a smaller frame around beam center (for instance to avoid other rings)
        trim = im[centery-hw_y:centery+hw_y, centerx-hw_x:centerx+hw_x]
        #ys = ys[centery-hw_y:centery+hw_y]
        #xs = xs[centerx-hw_x:centerx+hw_x]
        #project to a 1D trace
        proj = np.sum(im, axis=1)
        
        # fit the projection
        mod = ConstantModel() + VoigtModel()
        mod.set_param_hint('c', value=50, max=500)
        mod.set_param_hint('center', value=ys[np.argmax(proj)])
        mod.set_param_hint('sigma', value=0.3, max=1)
        mod.set_param_hint('amplitude', value=2000, min=10, max=20000)
        out = mod.fit(proj,x=ys)
        
        y_pos[i] = out.params['center'].value
        
        if i == num_steps/2:
            # find centerx
            projx = np.sum(im, axis=0)
            mod = ConstantModel() + VoigtModel()
            mod.set_param_hint('c', value=50, max=500)
            mod.set_param_hint('center', value=xs[np.argmax(projx)])
            mod.set_param_hint('sigma', value=0.3, max=1)
            mod.set_param_hint('amplitude', value=2000, min=10, max=20000)
            out = mod.fit(projx,x=xs, verbose=False)
            real_centerx = out.params['center'].value
            
            print("at tth {}, centery = {}, centerx = {}".format(tth[i], y_pos[i], real_centerx))
            
            fig = plt.figure()
            plt.imshow(im, aspect='auto', origin='lower')
            plt.xlim(centerx-10,centerx+10)
            plt.ylim(centery-10,centery+10)
            """fig = plt.figure()
            plt.imshow(trim, aspect='auto', origin='lower', 
                      extent=[xs[0], xs[-1], ys[0], ys[-1]])
            fig = plt.figure()
            #out.plot_fit()"""
            
    #fit a line to y_pos to calculate the slope
    #slope = pixels/tth_step
    linmod = LinearModel()
    linout = linmod.fit(y_pos, x=tth, slope=-1, intercept=100)
    fig = plt.figure()
    linout.plot_fit()
    
    slope = abs(linout.params['slope'].value)
    SDD = slope / np.tan(np.pi/180) * pixel_size
    return SDD
