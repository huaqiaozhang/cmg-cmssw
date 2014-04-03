import copy
import os 
import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps

# from CMGTools.H2TauTau.triggerMap import pathsAndFilters
from CMGTools.RootTools.RootTools import * 

pathsAndFilters = []

eventSelector = cfg.Analyzer(
    'EventSelector',
    toSelect = [
    # here put the event numbers (actual event numbers from CMSSW)
    ]
    )

pfAna = cfg.Analyzer(
    'PFAnalyzer',
    src_pfCandidates = 'particleFlow',
    src_ecalClusters = 'particleFlowClusterECAL',
    src_blocks = 'particleFlowBlock'
    )



treeProducer = cfg.Analyzer(
     'PFTreeProducer'
     )


###############################################################################


from CMGTools.RootTools.utils.getFiles import getFiles

QCD = cfg.Component(
    'QCD',
    files = getFiles(
      '/RelValQCD_FlatPt_15_3000/CMSSW_5_3_12_patch2-START53_LV2-v1/GEN-SIM-RECO',
      'CMS', '.*root')
    )

# for faster testing, use a local file: 
localFile = 'RECO.root'
if os.path.isfile(localFile):
    QCD.files = [localFile]
    

###############################################################################



selectedComponents = [QCD]

sequence = cfg.Sequence( [
    pfAna,
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
