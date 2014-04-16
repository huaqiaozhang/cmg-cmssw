import random
from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from CMGTools.RootTools.physicsobjects.PhysicsObject import PhysicsObject
from CMGTools.RootTools.utils.DeltaR import cleanObjectCollection, matchObjectCollection
from CMGTools.RootTools.statistics.Counter import Counter, Counters
from CMGTools.RootTools.physicsobjects.PhysicsObjects import GenParticle
from CMGTools.RootTools.utils.DeltaR import deltaR2


class Jet(PhysicsObject):
    '''Jet class designed to wrap an uncorrected reco::Jet of any type.'''
    def __init__(self, physobj):
        super(Jet,self).__init__(physobj)

    # for now, a default, dummy component
    class DummyComponent(object):
        def fraction(self):
            return -1
    dummy_component = DummyComponent()

    def component( self, dummy ):
        return self.__class__.dummy_component

    def rawFactor(self):
        '''returns 1 (correction factor for uncorrected jets)'''
        return 1.



class GenJet(PhysicsObject):
    pass



class PFPaperJetAnalyzer( Analyzer ):
    """Analyze jets ;-)

    This analyzer filters the jets that do not correspond to the leptons
    stored in event.selectedLeptons, and puts in the event:
    - jets: all jets passing the pt and eta cuts
    - cleanJets: the collection of clean jets
    - bJets: the bjets passing testBJet (see this method)

    Example configuration:


    jetAna = cfg.Analyzer(
        'PFPaperJetAnalyzer',
        jetHandle = ('ak5PFJets', 'std::vector< reco::PFJet >'),
        genJetHandle = ('ak5GenJets', 'std::vector< reco::GenJet >'),
        genParticleHandle = ('genParticles', 'std::vector< reco::GenParticle >'),
        jetPt = 10.,
        jetEta = 4.7,
    )

    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(PFPaperJetAnalyzer,self).__init__(cfg_ana, cfg_comp, looperName)

    def declareHandles(self):
        super(PFPaperJetAnalyzer, self).declareHandles()

        self.handles['jets'] = AutoHandle( * self.cfg_ana.jetHandle )
        if self.cfg_comp.isMC:
            self.mchandles['genParticles'] = AutoHandle( * self.cfg_ana.genParticleHandle ) 
            self.mchandles['genJets'] = AutoHandle( * self.cfg_ana.genJetHandle ) 

    def beginLoop(self):
        super(PFPaperJetAnalyzer,self).beginLoop()
        self.counters.addCounter('jets')
        count = self.counters.counter('jets')
        count.register('all events')
        count.register('at least 2 good jets')
        count.register('at least 2 clean jets')

        
    def process(self, iEvent, event):
        
        self.readCollections( iEvent )
        cmgJets = self.handles['jets'].product()

        allJets = []
        event.jets = []
        event.cleanJets = []

        leptons = []
        if hasattr(event, 'selectedLeptons'):
            leptons = event.selectedLeptons
            
        for cmgJet in cmgJets:
            jet = Jet( cmgJet )
            allJets.append( jet )

##             if genJets:
##                 # Use DeltaR = 0.25 matching like JetMET
##                 pairs = matchObjectCollection( [jet], genJets, 0.25*0.25)
##                 if pairs[jet] is None:
##                     jet.genJet = None
##                 else:
##                     jet.genJet = pairs[jet]
                    
            if self.testJet( jet ):
                event.jets.append(jet)
                
        self.counters.counter('jets').inc('all events')

        event.cleanJets, dummy = cleanObjectCollection( event.jets,
                                                        masks = leptons,
                                                        deltaRMin = 0.5 )
        
        if self.cfg_comp.isMC:
            genJets = map( GenJet, self.mchandles['genJets'].product() )
            genStatus3 = [ GenParticle(ptc) for ptc in self.mchandles['genParticles'].product() \
                           if ptc.status()==3 ]
            dr2max = 0.5*0.5
            match_genJets = matchObjectCollection( event.jets, genJets, dr2max )
            match_genParticle3 = matchObjectCollection( event.jets, genStatus3, dr2max)
            for jet in event.jets:
                jet.genJet = match_genJets[jet]
                jet.genParticle3 = match_genParticle3[jet]
            
        
        event.jets30 = [jet for jet in event.jets if jet.pt()>30]
        event.cleanJets30 = [jet for jet in event.cleanJets if jet.pt()>30]
        
        if len( event.jets30 )>=2:
            self.counters.counter('jets').inc('at least 2 good jets')
               
        if len( event.cleanJets30 )>=2:
            self.counters.counter('jets').inc('at least 2 clean jets')

        if len(event.cleanJets)<2:
            return True

        return True


        
    def testJet( self, jet ):
        return jet.pt() > self.cfg_ana.jetPt and \
               abs( jet.eta() ) < self.cfg_ana.jetEta 


