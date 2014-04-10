import copy
import os 
import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps

# from CMGTools.H2TauTau.triggerMap import pathsAndFilters
from CMGTools.RootTools.RootTools import * 
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle

pathsAndFilters = []

eventSelector = cfg.Analyzer(
    'EventSelector',
    toSelect = [
    # here put the event numbers (actual event numbers from CMSSW)
    ]
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
    # jetCol = 'ak5PFJets',
    # genJetCol = 'ak5GenJets',
    jetHandle = AutoHandle('ak5PFJets', 'std::vector< reco::PFJet >'),
    genJetHandle = AutoHandle('ak5GenJets', 'std::vector< reco::GenJet >'),
    genParticleHandle = AutoHandle('genParticles', 'std::vector< reco::GenParticle >'),
    jetPt = 20.,
    jetEta = 4.7,
    btagSFseed = 123456,
    relaxJetId = True, 
    )


treeProducer = cfg.Analyzer(
     'PFTreeProducer'
     )


###############################################################################


from CMGTools.RootTools.utils.getFiles import getFiles

QCD = cfg.Component(
    'QCD',
    files = getFiles(
      '/store/cmst3/user/cmgtools/CMG/QCDFlatPt/5_3_14_automc_noPU/AODSIM_RECOSIM_DISPLAY',
      'cmgtools', 'aod.*root')
    )
QCD.isMC = True

# for faster testing, use a local file: 
localFile = 'RECO.root'
if os.path.isfile(localFile):
    QCD.files = [localFile]
    

###############################################################################



selectedComponents = [QCD]

sequence = cfg.Sequence( [
    # pfAna,
    jsonAna,
    vertexAna,
    jetAna,
    treeProducer,
   ] )


# set test = 0 to run all jobs, in case you are using pybatch.py
test = 1
if test==1:
    # test a single component, using a single thread.
    # necessary to debug the code, until it doesn't crash anymore
    comp = QCD
    comp.files = comp.files[:10]
    selectedComponents = [comp]
    comp.splitFactor = 1
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
