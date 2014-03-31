import copy
from CMGTools.RootTools.physicsobjects.Particle import Particle

#COLIN should make a module for lorentz vectors (and conversions)
#instanciating template
from ROOT import Math
PtEtaPhiE4DLV = Math.PtEtaPhiE4D(float)
PtEtaPhiM4DLV = Math.PtEtaPhiM4D(float)


class PhysicsObject(Particle):
    '''Extends the cmg::PhysicsObject functionalities.'''

    def __init__(self, physObj):
        self.physObj = physObj
        super(PhysicsObject, self).__init__()

    def __copy__(self):
        '''Very dirty trick, the physObj is deepcopied...'''
        # print 'call copy', self
        physObj = copy.deepcopy( self.physObj )
        newone = type(self)(physObj)
        newone.__dict__.update(self.__dict__)
        newone.physObj = physObj
        return newone        

    def scaleEnergy( self, scale ):
        p4 = self.physObj.p4()
        p4 *= scale 
        self.physObj.setP4( p4 )  
        
    def __getattr__(self,name):
        '''all attributes from self.physObj are transferred to this class.
        '''
        return getattr(self.physObj, name)

