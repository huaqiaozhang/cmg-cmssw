import copy
import os 
import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps

# from CMGTools.H2TauTau.triggerMap import pathsAndFilters
from CMGTools.RootTools.RootTools import * 
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle

pathsAndFilters = []

printAna = cfg.Analyzer(
    'PrintAnalyzer'
    )

eventSelector = cfg.Analyzer(
    'EventSelector',
    toSelect = [
      # 204,
      2464
    # here put the event numbers (actual event numbers from CMSSW)
    ],
    iEv = True
    )


jsonAna = cfg.Analyzer(
    'JSONAnalyzer',
    )

vertexAna = cfg.Analyzer(
    'VertexAnalyzer',
    goodVertices = 'offlinePrimaryVertices',
    vertexWeight = None,
    fixedWeight = 1,
    verbose = False
    )

pfAna = cfg.Analyzer(
    'PFAnalyzer',
    src_pfCandidates = 'particleFlow',
    src_ecalClusters = 'particleFlowClusterECAL',
    src_blocks = 'particleFlowBlock'
    )



jetAna = cfg.Analyzer(
    'PFPaperJetAnalyzer',
    # jetHandle = ('ak5CaloJets', 'std::vector< reco::CaloJet >'),
    jetHandle = ('ak5PFJets', 'std::vector< reco::PFJet >'),
    genJetHandle = ('ak5GenJets', 'std::vector< reco::GenJet >'),
    genParticleHandle = ('genParticles', 'std::vector< reco::GenParticle >'),
    jetPt = 1.,
    jetEta = 5.0,
    )


treeProducer = cfg.Analyzer(
     'PFTreeProducer'
     )


###############################################################################


# from CMGTools.ZJetsTutorial.samples.run2012.ewk import TTJets as comp
from CMGTools.RootTools.utils.getFiles import getFiles

QCD = cfg.Component(
    'QCD',
    # files = ['RECO.root'],
    files = getFiles(
      '/QCDFlatPt/5_3_14_automc_noPU/AODSIM_RECOSIM_DISPLAY',
      'cmgtools', 'aod.*root', useCache=False),
    splitFactor = 12
    )
QCD.isMC = True
comp = QCD


###############################################################################



selectedComponents = [comp]

sequence = cfg.Sequence( [
    # pfAna,
    # eventSelector,
    jsonAna,
    vertexAna,
    jetAna,
    # printAna,
    treeProducer,
   ] )


# set test = 0 to run all jobs, in case you are using pybatch.py
test = 1
if test==1:
    # test a single component, using a single thread.
    # necessary to debug the code, until it doesn't crash anymore
    comp.files = comp.files[:10]
    selectedComponents = [comp]
    comp.splitFactor = 10
elif test==2:    
    # test all components (1 thread per component.
    # important to make sure that your code runs on any kind of component
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.files = comp.files[:3]

# creation of the processing configuration.
# we define here on which components to run, and
# what is the sequence of analyzers to run on each event. 
config = cfg.Config( components = selectedComponents,
                     sequence = sequence )

printComps(config.components, True)
