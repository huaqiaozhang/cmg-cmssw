from ROOT import TProfile, TH2F, TH1F
from CMGTools.RootTools.PyRoot import * 
from CMGTools.RootTools.Style import *


class Residual(object):
    
    def __init__(self, name, nx, xmin, xmax, ny, ymin, ymax ):
        self.name = name
        
        self.h2d = TH2F( self.name, self.name,
                         nx, xmin, xmax,
                         ny, ymin, ymax)

        self.canvas = None
                         
    def fill(self, tree, var, cut):
        tree.Draw('{var}>>+{hname}'.format(var=var, hname=self.name),
                  cut, 'goff')
        
    def fit(self):
        self.h2d.FitSlicesY()
        self.mean = gDirectory.Get(self.name + '_1')
        self.sigma = gDirectory.Get(self.name + '_2')

    def draw(self):
        self.canvas = TCanvas(self.name, self.name, 800, 800)
        self.canvas.Divide(2,2)
        self.canvas.cd(1)
        self.h2d.Draw('col')
        self.canvas.cd(2)
        draw(self.mean, ';p_{T} (GeV);response', 0.5, 1.5, 20, 100, sRed, gPad) 
        self.canvas.cd(3)
        draw(self.sigma, ';p_{T} (GeV);#sigma', 0, 0.8, 20, 100, sRed, gPad) 


def draw(hist, title, ymin, ymax, xmin, xmax, style, pad=None):
    if pad is None:
        pad = TCanvas(hist.GetName(), hist.GetName(),
                      600, 600)
    hist.SetStats(0)
    hist.SetTitle(title)
    sRed.formatHisto(hist) 
    hist.Draw()
    hist.GetYaxis().SetRangeUser(ymin, ymax)
    hist.GetXaxis().SetRangeUser(xmin, xmax)
    formatPad(pad)
    pad.Update()
    return pad




if __name__ == '__main__':

    import sys

    args = sys.argv[1:]

    file_pattern = args[0]
    chain = Chain(None, file_pattern)

##     pt1 =  Residual('pt1', 100, 0, 200, 100, 0, 3)
##     pt1.fill( chain,
##               'jet1_pt / jet1_genJet_pt : jet1_genJet_pt',
##               'jet1_genJet_pt>0')
##     pt1.fit()
##     pt1.draw()

##     pt2 =  Residual('pt2', 100, 0, 200, 100, 0, 3)
##     pt2.fill( chain,
##               'jet2_pt / jet2_genJet_pt : jet2_genJet_pt',
##               'jet2_genJet_pt>0')
##     pt2.fit()
##     pt2.draw()


    plot_vs_pt =  Residual('plot_pt', 100, 0, 200, 100, 0, 3)
    plot_vs_pt.fill( chain,
                 'jet1_pt / jet1_genJet_pt : jet1_genJet_pt',
                 'jet1_genJet_pt>0')
    plot_vs_pt.fill( chain,
                 'jet2_pt / jet2_genJet_pt : jet2_genJet_pt',
                 'jet2_genJet_pt>0')
    plot_vs_pt.fit()
    plot_vs_pt.draw()


    plot_vs_eta =  Residual('plot_eta', 100, -5, 5, 100, 0, 3)
    plot_vs_eta.fill( chain,
                      'jet1_pt / jet1_genJet_eta : jet1_genJet_eta',
                      'jet1_genJet_pt>0')
    plot_vs_eta.fill( chain,
                      'jet2_pt / jet2_genJet_pt : jet2_genJet_eta',
                      'jet2_genJet_pt>0')
    plot_vs_eta.fit()
    plot_vs_eta.draw()


    
