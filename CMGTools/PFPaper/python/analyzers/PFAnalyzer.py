import operator 
from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from CMGTools.RootTools.statistics.Counter import Counter, Counters
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from CMGTools.RootTools.physicsobjects.GenericObject import GenericObject
from CMGTools.RootTools.physicsobjects.PhysicsObject import PhysicsObject

class PFCandidate(PhysicsObject):
    pass




class PFAnalyzer( Analyzer ):
    '''Base analyzer for PF analysis.
    Demonstrates how to access the various PF products.
    '''
    

    def declareHandles(self):
        ''' .'''
        super(PFAnalyzer, self).declareHandles()
        self.handles['pfCandidates'] =  AutoHandle(
            self.cfg_ana.src_pfCandidates,
            'std::vector<reco::PFCandidate>'
            )

    def beginLoop(self):
        super(PFAnalyzer,self).beginLoop()        

        
    def process(self, iEvent, event):
        self.readCollections( iEvent )
        
        event.pfCandidates = map( PFCandidate,
                                  self.handles['pfCandidates'].product() ) 
        
        return True

