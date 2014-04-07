'''A simple test macro.
'''
from DataFormats.FWLite import Events
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle

from CMGTools.PFPaper.analyzers.PFBlock import *

events = Events('RECO.root')

block_handle = AutoHandle('particleFlowBlock', 'std::vector< reco::PFBlock >' ) 

nev = 10

pblock = None
ccblock = None

for iev, event in enumerate( events ) :
    block_handle.Load( event )
    blocks = map( PFBlock, block_handle.product() )
    if len(blocks)==0:
        continue
    ccblock = blocks[0].obj
    pblock = blocks[0]
    if iev == nev:
        break 

print pblock
print ccblock
