from CMGTools.RootTools.physicsobjects.PhysicsObject import PhysicsObject
from CMGTools.PFPaper.analyzers.Component import Component
from CMGTools.PFPaper.analyzers.ParticleTypes import particleType


class BaseJet(PhysicsObject):
    '''base jet class, with dummy components, and a correction factor equal to 1'''

    def __init__(self, physobj):
        super(BaseJet,self).__init__(physobj)

    class DummyComponent(object):
        def fraction(self):
            return -1
    dummy_component = DummyComponent()

    def component( self, dummy ):
        return self.__class__.dummy_component

    def rawFactor(self):
        '''returns 1 (correction factor for uncorrected jets)'''
        return 1.

    

class ParticleJet(BaseJet):
    '''particle jet class. the components are computed from the
    list of consistuents. 
    Transparent interface working for PF and gen jets.
    The components are indexed by the particle type, as in the PFCandidate class
    '''
    def __init__(self, physobj):
        super(ParticleJet,self).__init__(physobj)
        self.components = self._buildComponents()
        
    def _buildComponents(self):
        particles = self.getJetConstituents()
        # initialize the component dictionary
        components_by_id = dict()
        for id in range(8):
            components_by_id[id] = Component(id)
        for p in particles:
            id = particleType( p )
            pcomp = Component( id,
                               1,
                               p.energy()/self.energy(),
                               p.energy(),
                               p.pt() )
            components_by_id[id] += pcomp
        return components_by_id

    def component(self, type):
        '''Returns the component for a given type, e.g. 1 for charged hadrons.
        See PFCandidate for more info'''
        return self.components[type]
        


class CaloJet( BaseJet ):
    pass


class GenJet( ParticleJet ):
    pass

class PFJet( ParticleJet ):
    pass 

