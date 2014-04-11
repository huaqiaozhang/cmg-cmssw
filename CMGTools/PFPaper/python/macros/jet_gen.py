from ROOT import TProfile, TH2F, TH1F
from CMGTools.RootTools.PyRoot import * 
from CMGTools.RootTools.Style import *
from ROOT import TF1

from time import sleep

sRed.markerSize = 0.8
sRed.markerStyle = 4

class Profile( object ):
    def __init__(self, h2d):
        self.mean = h2d.ProfileX()
        self.rms = rmsX(h2d) 
        

    
fun_respt = TF1('fun_respt', 'sqrt( ([0]/x)**2 + ([1]*sqrt(x)/x)**2 + ([2])**2 )', 30, 200)



class Residual(object):
    
    def __init__(self, name, xtitle, nx, xmin, xmax, ny, ymin, ymax ):
        self.name = name
        
        self.h2d = TH2F( self.name, self.name,
                         nx, xmin, xmax,
                         ny, ymin, ymax)
        self.h2d.SetXTitle( xtitle )
        self.canvas = None
                         
    def fill(self, tree, var, cut):
        tree.Draw('{var}>>+{hname}'.format(var=var, hname=self.name),
                  cut, 'goff')
        
    def fit(self):
        self.h2d.FitSlicesY()
        self.mean = gDirectory.Get(self.name + '_1')
        self.mean.SetTitle('')
        self.sigma = gDirectory.Get(self.name + '_2')
        self.sigma.SetTitle('')
        self.armean = self.h2d.ProfileX()
        self.rms = rmsX( self.h2d )

    def fit_resolution(self, function_name):
        results = self.sigma.Fit(function_name, 'S', 'goff')
        fun = self.sigma.GetFunction( function_name )
        chi2 = fun.GetChisquare()
        ndf = fun.GetNDF()
        print self.name, function_name, chi2/ndf
        return results 

    def draw(self, style=sRed):
        self.canvas = TCanvas(self.name, self.name, 800, 800)
        self.canvas.Divide(2,2)
        self.canvas.cd(1)
        self.h2d.Draw('col')
        self.canvas.cd(2)
        draw(self.mean, self.h2d.GetXaxis().GetTitle(), 'response', 
             0.6, 1.1, 20, 200, style, gPad)
        self.armean.SetLineColor(style.lineColor)
        self.armean.Draw('same')
        self.canvas.cd(3)
        draw(self.sigma, self.h2d.GetXaxis().GetTitle(), 'resolution',
             0, 0.2, 20, 200, style, gPad) 
        self.rms.SetLineColor(style.lineColor)
        self.rms.Draw('same')


def rmsX( h2d, graphics=False ):
    '''Returns a TH1D containing, for each x bin of h2d (1d histo along y),
    the rms and the uncertainty on the RMS. 
    '''
    hist = TH1D( '_'.join( [ h2d.GetName(), 'rmx'] ),
                 ';{xtitle};RMS'.format(xtitle=h2d.GetXaxis().GetTitle()),
                 h2d.GetNbinsX(), h2d.GetXaxis().GetXmin(), h2d.GetXaxis().GetXmax() )
    for bin in range( h2d.GetNbinsX() ):
        bin += 1
        proj = h2d.ProjectionY('',bin, bin, '')
        rms = proj.GetRMS()
        err = proj.GetRMSError()
        if graphics:
            proj.Draw()
            gPad.Update()
            print bin, rms, err
        hist.SetBinContent( bin, rms )
        hist.SetBinError( bin, err )
    return hist


def draw(hist, xtitle, ytitle, ymin, ymax, xmin, xmax, style, pad=None):
    if pad is None:
        pad = TCanvas(hist.GetName(), hist.GetName(),
                      600, 600)
    hist.SetStats(0)
    hist.SetXTitle(xtitle)
    hist.SetYTitle(ytitle)
    style.formatHisto(hist) 
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



    nbinsx = 50
    nbinsy = 100

    plot_vs_pt_barrel =  Residual('plot_vs_pt_barrel', 'p_{T} (GeV)',
                                  nbinsx, 20, 200, nbinsy, 0, 3)
    plot_vs_pt_barrel.fill( chain,
                 'jet1_pt / jet1_genJet_pt : jet1_genJet_pt',
                 'jet1_genJet_pt>0 && abs(jet1_eta)<1.4')
    plot_vs_pt_barrel.fill( chain,
                 'jet2_pt / jet2_genJet_pt : jet2_genJet_pt',
                 'jet2_genJet_pt>0 && abs(jet2_eta)<1.4')
    plot_vs_pt_barrel.fit()
    results = plot_vs_pt_barrel.fit_resolution('fun_respt')
    plot_vs_pt_barrel.draw()




##     plot_vs_pt_endcaps =  Residual('plot_vs_pt_endcaps', 'p_{T} (GeV)',
##                                    nbinsx, 0, 200, nbinsy, 0, 3)
##     plot_vs_pt_endcaps.fill( chain,
##                  'jet1_pt / jet1_genJet_pt : jet1_genJet_pt',
##                  'jet1_genJet_pt>0 && abs(jet1_eta)>1.6 && abs(jet1_eta)<2.9')
##     plot_vs_pt_endcaps.fill( chain,
##                  'jet2_pt / jet2_genJet_pt : jet2_genJet_pt',
##                  'jet2_genJet_pt>0 && abs(jet2_eta)>1.6 && abs(jet2_eta)<2.9')
##     plot_vs_pt_endcaps.fit()
##     plot_vs_pt_endcaps.sigma.Fit('fun_respt')
##     plot_vs_pt_endcaps.draw()


##     plot_vs_pt_hf =  Residual('plot_vs_pt_hf', 'p_{T} (GeV)',
##                               nbinsx, 0, 200, nbinsy, 0, 3)
##     plot_vs_pt_hf.fill( chain,
##                  'jet1_pt / jet1_genJet_pt : jet1_genJet_pt',
##                  'jet1_genJet_pt>0 && abs(jet1_eta)>3.1 && abs(jet1_eta)<4.8')
##     plot_vs_pt_hf.fill( chain,
##                  'jet2_pt / jet2_genJet_pt : jet2_genJet_pt',
##                  'jet2_genJet_pt>0 && abs(jet2_eta)>3.1 && abs(jet2_eta)<4.8')
##     plot_vs_pt_hf.fit()
##     plot_vs_pt_hf.sigma.Fit('fun_respt')
##     plot_vs_pt_hf.draw()




##     plot_vs_eta =  Residual('plot_vs_eta', '#eta',
##                             nbinsx, -5, 5, nbinsy, 0, 3)
##     plot_vs_eta.fill( chain,
##                       'jet1_pt / jet1_genJet_eta : jet1_genJet_eta',
##                       'jet1_genJet_pt>20')
##     plot_vs_eta.fill( chain,
##                       'jet2_pt / jet2_genJet_pt : jet2_genJet_eta',
##                       'jet2_genJet_pt>20')
##     plot_vs_eta.fit()
##     plot_vs_eta.draw()


    
