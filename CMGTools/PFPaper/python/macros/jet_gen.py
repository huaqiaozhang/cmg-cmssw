from ROOT import TProfile, TH2F, TH1F
from CMGTools.RootTools.PyRoot import * 
from CMGTools.RootTools.Style import *
from ROOT import TF1

import numpy as np

from time import sleep

styles = [sBlue, sRed]
for style in styles:
    style.markerSize = 0.8
    style.markerStyle = 4


class Profile( object ):
    def __init__(self, h2d):
        self.mean = h2d.ProfileX()
        self.rms = rmsX(h2d) 
        

    
fun_respt = TF1('fun_respt',
                'sqrt( ([0]/x)**2 + '
                '( [1]/sqrt(x) )**2 + '
                '([2])**2 )',
                100, 1000)

class Residual(object):
    
    def __init__(self, name, xtitle, binsx, binsy, canx=800, cany=800, logx=False):
        self.name = name
        self.logx = logx
        nx = len(binsx)-1
        ny = len(binsy)-1
        self.h2d = TH2F( self.name, self.name,
                         nx, binsx, ny, binsy)
        self.h2d.SetXTitle( xtitle )
        self.h2d.binsx = binsx
        self.canvas = None
        self.canx=canx
        self.cany=cany
                         
    def fill(self, tree, var, cut):
        tree.Draw('{var}>>+{hname}'.format(var=var, hname=self.name),
                  cut, 'goff')


    def fit_slice(self, ibin):
        slice = self.h2d.ProjectionY( '{name}_bin_{bin}'.format(name=self.name,
                                                                bin = ibin), ibin, ibin )
        slice.Fit('gaus')
        gPad.Update()
            

    def fit(self):
        self.h2d.FitSlicesY()
        self.mean = gDirectory.Get(self.name + '_1')
        self.mean.SetTitle('')
        self.sigma = gDirectory.Get(self.name + '_2')
        self.sigma.SetTitle('')
        self.sigma.Divide(self.mean)
        self.armean = self.h2d.ProfileX()
        self.rms = rmsX( self.h2d )
        self.rms.Divide(self.mean)

    def fit_resolution(self, function_name):
        results = self.sigma.Fit(function_name, 'S', 'goff')
        fun = self.sigma.GetFunction( function_name )
        chi2 = fun.GetChisquare()
        ndf = fun.GetNDF()
        print self.name, function_name, chi2/ndf
        return results 

    def draw(self, style):
        self.canvas = TCanvas(self.name, self.name, self.canx, self.cany )
        self.canvas.Divide(2,2)
        if self.logx:
            for ipad in range(4):
                self.canvas.cd(ipad+1)
                gPad.SetLogx()
                gPad.SetGridx()
                gPad.SetGridy()
        self.canvas.cd(1)
        self.h2d.Draw('col')
        self.canvas.cd(2)
        draw(self.mean, self.h2d.GetXaxis().GetTitle(), 'response', 
             0.5, 1.1, style, gPad)
        self.armean.SetLineColor(style.lineColor)
        self.armean.Draw('same')
        self.canvas.cd(3)
        draw(self.sigma, self.h2d.GetXaxis().GetTitle(), 'resolution',
             0, 0.45, style, gPad) 
        self.rms.SetLineColor(style.lineColor)
        self.rms.Draw('same')
        self.canvas.cd(4)
        gPad.SetLogx(0)
        self.fit_slice(1)


def rmsX( h2d, graphics=False ):
    '''Returns a TH1D containing, for each x bin of h2d (1d histo along y),
    the rms and the uncertainty on the RMS. 
    '''
    hist = TH1D( '_'.join( [ h2d.GetName(), 'rmx'] ),
                 ';{xtitle};RMS'.format(xtitle=h2d.GetXaxis().GetTitle()),
                 h2d.GetNbinsX(), h2d.binsx )
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


def draw(hist, xtitle, ytitle, ymin, ymax, style, pad=None, options=''):
    if pad is None:
        pad = TCanvas(hist.GetName(), hist.GetName(),
                      600, 600)
    hist.SetStats(0)
    hist.SetXTitle(xtitle)
    hist.SetYTitle(ytitle)
    style.formatHisto(hist) 
    hist.Draw(options)
    hist.GetYaxis().SetRangeUser(ymin, ymax)
    # hist.GetXaxis().SetRangeUser(xmin, xmax)
    formatPad(pad)
    pad.Update()
    return pad


def build_plot( name, file_pattern, binsx, binsy, ptcut):
    chain = Chain(None, file_pattern)
    plot =  Residual(name, 'p_{T} (GeV)',
                     binsx, binsy, logx=True)
    plot.fill(
        chain,
        'jet1_pt / jet1_genJet_pt : jet1_genJet_pt',
        'jet1_genJet_pt>0 && abs(jet1_eta)<1.4 && jet1_pt>{ptcut} && jet1_dr2<0.01'.format(
        ptcut=ptcut
        ) )
    plot.fill(
        chain,
        'jet2_pt / jet2_genJet_pt : jet2_genJet_pt',
        'jet2_genJet_pt>0 && abs(jet2_eta)<1.4 && jet2_pt>{ptcut} && jet2_dr2<0.01'.format(
        ptcut=ptcut
        ) ) 
    plot.fit()
    # results = plot.fit_resolution('fun_respt')
    return plot


if __name__ == '__main__':

    import sys

    binsx_low = np.linspace( 10, 300, 30)
    binsx_high = np.linspace( 350, 1000, 14)
    binsx = np.concatenate( [binsx_low, binsx_high] )    
    nbinsy = 100
    binsy = np.linspace( 0, 3, nbinsy+1)

    args = sys.argv[1:]
    pf_file_pattern = args[0]
    pf_plot = build_plot( 'pf_barrel', pf_file_pattern, binsx, binsy,
                          ptcut=1)
    pf_plot.draw(sRed)
    if len(args)==2:
        calo_file_pattern = args[1]
        calo_plot = build_plot( 'calo_barrel', calo_file_pattern, binsx, binsy,
                                ptcut=1)
        calo_plot.draw(sBlue)

    # chain.SetAlias('jet1_dr2', '(jet1_eta - jet1_genJet_eta)**2 + (jet1_phi-jet1_genJet_phi)**2')
    # chain.SetAlias('jet2_dr2', '(jet2_eta - jet2_genJet_eta)**2 + (jet2_phi-jet2_genJet_phi)**2')
    



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
##                       'jet1_pt>20')
##     plot_vs_eta.fill( chain,
##                       'jet2_pt / jet2_genJet_pt : jet2_genJet_eta',
##                       'jet2_pt>20')
##     plot_vs_eta.fit()
##     plot_vs_eta.draw()


    
