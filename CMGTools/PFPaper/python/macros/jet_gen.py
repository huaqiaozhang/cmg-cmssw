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

    
fun_respt = TF1('fun_respt',
                'sqrt( ([0]/x)**2 + '
                '( [1]/sqrt(x) )**2 + '
                '([2])**2 )',
                100, 1000)

gaussian = TF1('gaussian','gaus',0.2, 2)

class Residual(object):
    
    def __init__(self, name, tree, xtitle, binsx, binsy, canx=800, cany=800,
                 logx=False, style=sRed):
        self.name = name
        self.tree = tree
        self.tree.SetScanField(500)
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
        self.style=style
                         
    def fill(self, var, cut, scanvars=None, scancut='1'):
        self.tree.Draw('{var}>>+{hname}'.format(var=var, hname=self.name),
                       cut, 'goff')
        if scanvars:
            self.tree.Scan(scanvars,
                           '({cut} && {scancut})'.format(cut=cut,
                                                         scancut=scancut),
                           'colsize=20 precision=3' )

    def fit_slice(self, ibin):
        slice = self.h2d.ProjectionY( '{name}_bin_{bin}'.format(name=self.name,
                                                                bin = ibin), ibin, ibin )
        results = slice.Fit('gaus','Q','',0.2,2)
        return results 
        # gPad.Update()

            
    def fit(self):
        # self.h2d.FitSlicesY(gaussian,0,-1,0,'R')
        # self.mean = gDirectory.Get(self.name + '_1')
        # self.sigma = gDirectory.Get(self.name + '_2')
        # self.mean.SetTitle('')
        # self.sigma.SetTitle('')
        for i in range(self.h2d.GetNbinsX()):
            ibin = i+1
            self.fit_slice(ibin)
        self.sigma.Divide(self.mean)
        self.armean = self.h2d.ProfileX()
        self.rms = rmsX( self.h2d )
        self.rms.Divide(self.mean)
        self.style.formatHisto(self.mean)
        self.style.formatHisto(self.sigma)


    def fit_resolution(self, function_name):
        results = self.sigma.Fit(function_name, 'S', 'goff')
        fun = self.sigma.GetFunction( function_name )
        chi2 = fun.GetChisquare()
        ndf = fun.GetNDF()
        print self.name, function_name, chi2/ndf
        return results 


    def draw(self):
        self.canvas = TCanvas(self.name, self.name, self.canx, self.cany )
        self.canvas.Divide(2,2)
        
        self.canvas.GetPad(2).SetGridx()
        self.canvas.GetPad(2).SetGridy()            

        self.canvas.GetPad(3).SetLogx()
        self.canvas.GetPad(3).SetGridx()
        self.canvas.GetPad(3).SetGridy()            
        
        self.canvas.cd(1)
        self.h2d.Draw('col')
        self.canvas.cd(2)
        draw(self.mean, self.h2d.GetXaxis().GetTitle(), 'response', 
             0.5, 1.1, self.style, gPad)
        self.armean.SetLineColor(self.style.lineColor)
        self.armean.Draw('same')
        self.canvas.cd(3)
        draw(self.sigma, self.h2d.GetXaxis().GetTitle(), 'resolution',
             0, 0.45, self.style, gPad) 
        self.rms.SetLineColor(self.style.lineColor)
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




def build_plot( name, file_pattern, binsx, binsy, ptcut, dr2cut, style):
    chain = Chain(None, file_pattern)
    plot =  Residual(name, chain, 'p_{T} (GeV)',
                     binsx, binsy, logx=True, style=style)
    plot.fill(
        'jet1_et / jet1_genJet_et : jet1_genJet_et',
        'jet1_genJet_et>0 && abs(jet1_eta)<1.4 && jet1_et>{ptcut} && jet1_genJet_dr2<{dr2cut}'.format( ptcut=ptcut, dr2cut=dr2cut),
        scanvars='jet1_et:jet1_eta:jet1_genJet_et:jet1_genJet_eta:sqrt(jet1_genJet_dr2)',
        scancut='jet1_genJet_et>10 && jet1_genJet_et<20' )
    plot.fill(
        'jet2_et / jet2_genJet_et : jet2_genJet_et',
        'jet2_genJet_et>0 && abs(jet2_eta)<1.4 && jet2_et>{ptcut} && jet2_genJet_dr2<{dr2cut}'.format( ptcut=ptcut, dr2cut=dr2cut),
        scanvars='jet2_et:jet2_eta:jet2_genJet_et:jet2_genJet_eta:sqrt(jet2_genJet_dr2)',
        scancut='jet2_genJet_et>10 && jet2_genJet_et<20'  ) 
    # plot.fit()
    # results = plot.fit_resolution('fun_respt')
    return plot

  
if __name__ == '__main__':

    import sys

    xmin, xmax, binsize = 10., 300., 10.
    binsx_low = np.linspace( xmin, xmax, (xmax-xmin)/binsize+1)
    xmin, xmax, binsize = 350., 1000., 50.
    binsx_high = np.linspace( xmin, xmax, (xmax-xmin)/binsize+1)
    binsx = np.concatenate( [binsx_low, binsx_high] )    
    nbinsy = 200
    binsy = np.linspace( 0, 2, nbinsy+1)

    if len( sys.argv )<2:
        print ''' usage: jet_gen.py <pattern1> [pattern2]
        patterns = <calo or pf>:wildcard_path
        '''
        sys.exit(1)

    args = sys.argv[1:]

    def process_chain( arg ):
        jettype, file_pattern = arg.split(':')
        style = sRed
        ptcut = 5
        dr2cut = 0.01
        if jettype=='calo':
            style = sBlue
            ptcut = 3
            dr2cut = 0.04
        plot = build_plot( '{jettype}_barrel'.format(jettype=jettype), file_pattern,
                           binsx, binsy,
                           ptcut=ptcut,
                           dr2cut=dr2cut,
                           style=style)
        plot.draw()
        return plot

    plot0 = process_chain( args[0] )
    if len(args)==2:
        plot1 = process_chain( args[1] )
    

    
