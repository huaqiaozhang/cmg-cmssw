from ROOT import TProfile, TH2F, TH1F
from CMGTools.RootTools.PyRoot import * 



class JetGenPlotter( object ):
    
    def __init__(self, name, file_pattern):
        self.name = name
        self.chain = Chain(None, file_pattern)
        
        self.res_eta = TH2F( self.hname('res_eta'), self.hname('res_eta'),
                                 20, -5, 5, 50, 0, 2)
        
        self.chain.Project( self.res_eta.GetName(),
                            '(jet1_pt*jet1_rawFactor/jet1_genJet_pt):jet1_genJet_eta')
        
        
    def hname(self, hname):
        return '_'.join( [self.name, hname] )
    

if __name__ == '__main__':

    import sys

    args = sys.argv[1:]

    file_pattern = args[0]
    plot = JetGenPlotter( 'plot', file_pattern )
    
