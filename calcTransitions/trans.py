
import numpy as np
import Scientific.IO.NetCDF as Dataset
import cv2
import sys

def main():
    
    dataDir = '/home/ctorney/Dropbox/fishPredation/'
    # open netcdf file
    
    trialName = "MVI_" +  str(sys.argv[1])
    
    #trialName = "MVI_3371"
    NUMFISH = 4
    ncFileName = dataDir + "tracked/linked" + trialName + ".nc"    
    f = Dataset.NetCDFFile(ncFileName, 'r')
    
    # get the positions variable
    trXY = f.variables['trXY']
    trackList = []
    trackList = np.empty_like (trXY)
    np.copyto(trackList,trXY)
    [trackIndex,timeIndex]=np.nonzero(trackList[:,:,0])
    
    # get the movie frame numbers
    fid = f.variables['fid']
    fishIDs = []
    fishIDs = np.empty_like(fid)
    np.copyto(fishIDs, fid)
    cid = f.variables['certID']
    certIDs = []
    certIDs = np.empty_like(cid)
    np.copyto(certIDs, cid)
    
    
    
    
    # these variables store the index values when a track is present
    [trackIndex,timeIndex]=np.nonzero(trackList[:,:,0])
    
    print 'TIME:F0 (arm,uncert):F1 (arm,uncert):F2 (arm,uncert):F3 (arm,uncert)'
    arms = cv2.imread('arms.png',0)
    fishArm = np.zeros(NUMFISH)
    fishCert = np.zeros(NUMFISH)
    
    for t in range(np.min(timeIndex),np.max(timeIndex)):
        liveTracks = trackIndex[timeIndex[:]==t]
     #   img = cv2.imread('arms.png',1)
        for tr in liveTracks:
            xp = trackList[tr, t,0]
            yp = trackList[tr, t,1]
            
     #       cv2.circle(img,(xp,yp), 6, (0,120,255), -1)
            
            fishCert[fishIDs[tr,t]] = min( certIDs[tr,0],1.0)
            fishArm[fishIDs[tr,t]] = int(round(float(arms[((yp,xp))])/(0.5*255.0)))
    
        outStr = str(t) + ' '    
        for fsh in range(NUMFISH):
            outStr = outStr + '(' + str(int(fishArm[fsh])) + ', {0:.2f}) '.format(fishCert[fsh])
    
            
        print outStr
            
    #    resized = cv2.resize(img, ((int(img.shape[1]*0.5),int(img.shape[0]*0.5))), interpolation = cv2.INTER_AREA)
    
        #cv2.imshow('image',resized)
        #cv2.waitKey(10)
    
    #cv2.destroyAllWindows()
    
    
    
    
    f.close()

if __name__ == "__main__":
    main()
