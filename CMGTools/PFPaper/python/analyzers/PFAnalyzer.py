import operator 
from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from CMGTools.RootTools.statistics.Counter import Counter, Counters
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from CMGTools.RootTools.physicsobjects.GenericObject import GenericObject
from CMGTools.RootTools.physicsobjects.PhysicsObject import PhysicsObject

class PFCandidate(PhysicsObject):
    pass

class PFCluster(GenericObject):
    def __str__(self):
        tmp = '{className} : {layer:>3}, eta = {eta:5.2f}, E = {energy:5.2f}'
        return tmp.format( className = self.__class__.__name__,
                           layer = self.layer(),
                           energy = self.energy(),
                           eta = self.eta() )


def sort_deposits( rechits_or_clusters ):
    '''Sort a collection of energy deposits by layer, and then by energy.
    returns a dictionary with key=layer id and value = list or deposits
    ordered by decreasing energy.
    '''
    sorted = dict() 
    # sort by layer (e.g. separate ECAL barrel and ECAL endcap rechits)
    for item in rechits_or_clusters: 
        sorted.setdefault( item.layer(), []).append(item)
    # sort by decreasing energy
    for thelist in sorted.values():
        thelist.sort( key=lambda x: x.energy(), reverse=True)
    return sorted


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
        self.handles['ecalClusters'] =  AutoHandle(
            self.cfg_ana.src_ecalClusters,
            'std::vector<reco::PFCluster>'
            )

    def beginLoop(self):
        super(PFAnalyzer,self).beginLoop()        

        
    def process(self, iEvent, event):
        self.readCollections( iEvent )
        
        event.pfCandidates = map( PFCandidate,
                                  self.handles['pfCandidates'].product() ) 
        
        all_clusters = map( PFCluster,
                        self.handles['ecalClusters'].product() ) 
        sorted_clusters = sort_deposits( all_clusters )

        event.EBClusters = sorted_clusters[-1]
        event.ECClusters = sorted_clusters[-2]
        
        return True

