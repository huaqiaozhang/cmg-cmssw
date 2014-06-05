#!/bin/env python


def var( tree, varName, type=float ):
    tree.var(varName, type)

def fill( tree, varName, value ):
    tree.fill( varName, value )

# simple particle

def bookParticle( tree, pName ):
    var(tree, '{pName}_pt'.format(pName=pName))
    var(tree, '{pName}_eta'.format(pName=pName))
    var(tree, '{pName}_phi'.format(pName=pName))
    var(tree, '{pName}_charge'.format(pName=pName))
    var(tree, '{pName}_energy'.format(pName=pName))
    var(tree, '{pName}_et'.format(pName=pName))

def fillParticle( tree, pName, particle ):
    fill(tree, '{pName}_pt'.format(pName=pName), particle.pt() )
    fill(tree, '{pName}_eta'.format(pName=pName), particle.eta() )
    fill(tree, '{pName}_phi'.format(pName=pName), particle.phi() )
    fill(tree, '{pName}_charge'.format(pName=pName), particle.charge() )
    fill(tree, '{pName}_energy'.format(pName=pName), particle.energy() )
    fill(tree, '{pName}_et'.format(pName=pName), particle.et() )

def bookGenParticle(tree, pName):
    bookParticle(tree, pName)
    var(tree, '{pName}_pdgId'.format(pName=pName))
    
def fillGenParticle( tree, pName, particle ):
    fillParticle( tree, pName, particle )
    fill(tree, '{pName}_pdgId'.format(pName=pName), particle.pdgId() )

# di-tau

def bookDiLepton(tree):
    var( tree, 'visMass')
    var( tree, 'svfitMass')
    var( tree, 'pZetaMET')
    var( tree, 'pZetaVis')
    var( tree, 'pZetaDisc')
    var( tree, 'mt')
    var( tree, 'met')


def fillDiLepton(tree, diLepton):
    fill(tree, 'visMass', diLepton.mass())
    fill(tree, 'svfitMass', diLepton.massSVFit())
    fill(tree, 'pZetaMET', diLepton.pZetaMET())
    fill(tree, 'pZetaVis', diLepton.pZetaVis())
    fill(tree, 'pZetaDisc', diLepton.pZetaDisc())
    fill(tree, 'mt', diLepton.mTLeg2())
    fill(tree, 'met', diLepton.met().pt())

    
# lepton

def bookLepton( tree, pName ):
    bookParticle(tree, pName )
    var(tree, '{pName}_relIso05'.format(pName=pName))
    var(tree, '{pName}_dxy'.format(pName=pName))
    var(tree, '{pName}_dz'.format(pName=pName))
##     var(tree, '{pName}_weight'.format(pName=pName))
##     var(tree, '{pName}_triggerWeight'.format(pName=pName))
##     var(tree, '{pName}_triggerEffData'.format(pName=pName))
##     var(tree, '{pName}_triggerEffMC'.format(pName=pName))
##     var(tree, '{pName}_recEffWeight'.format(pName=pName))

def fillLepton( tree, pName, lepton ):
    fillParticle(tree, pName, lepton )
    fill(tree, '{pName}_relIso05'.format(pName=pName), lepton.relIsoAllChargedDB05() )
    fill(tree, '{pName}_dxy'.format(pName=pName), lepton.dxy() )
    fill(tree, '{pName}_dz'.format(pName=pName), lepton.dz() )
##     fill(tree, '{pName}_weight'.format(pName=pName), lepton.weight )
##     fill(tree, '{pName}_triggerWeight'.format(pName=pName), lepton.triggerWeight )
##     fill(tree, '{pName}_triggerEffData'.format(pName=pName), lepton.triggerEffData )
##     fill(tree, '{pName}_triggerEffMC'.format(pName=pName), lepton.triggerEffMC )
##     fill(tree, '{pName}_recEffWeight'.format(pName=pName), lepton.recEffWeight )


# muon


def bookMuon( tree, pName ):
    bookLepton(tree, pName )
    var(tree, '{pName}_mvaIso'.format(pName=pName))
    var(tree, '{pName}_looseId'.format(pName=pName))
    var(tree, '{pName}_tightId'.format(pName=pName))

def fillMuon( tree, pName, muon ):
    fillLepton(tree, pName, muon)
    fill(tree, '{pName}_mvaIso'.format(pName=pName), muon.mvaIso() )
    fill(tree, '{pName}_looseId'.format(pName=pName), muon.looseId() )
    fill(tree, '{pName}_tightId'.format(pName=pName), muon.tightId() )


# electron


def bookEle( tree, pName ):
    bookLepton(tree, pName )
    var(tree, '{pName}_mvaIso'.format(pName=pName))
    var(tree, '{pName}_mvaTrigV0'.format(pName=pName))
    var(tree, '{pName}_mvaNonTrigV0'.format(pName=pName))
    var(tree, '{pName}_looseId'.format(pName=pName))
    var(tree, '{pName}_tightId'.format(pName=pName))

def fillEle( tree, pName, ele ):
    fillLepton(tree, pName, ele)
    fill(tree, '{pName}_mvaIso'.format(pName=pName), ele.mvaIso() )
    fill(tree, '{pName}_mvaTrigV0'.format(pName=pName), ele.sourcePtr().electronID("mvaTrigV0") )
    fill(tree, '{pName}_mvaNonTrigV0'.format(pName=pName), ele.sourcePtr().electronID("mvaNonTrigV0") )
    fill(tree, '{pName}_looseId'.format(pName=pName), ele.looseIdForEleTau() )
    fill(tree, '{pName}_tightId'.format(pName=pName), ele.tightIdForEleTau() )


# tau 

def bookTau( tree, pName ):
    bookLepton(tree, pName )
    var(tree, '{pName}_veryLooseIso'.format(pName=pName))
    var(tree, '{pName}_looseIso'.format(pName=pName))
    var(tree, '{pName}_mediumIso'.format(pName=pName))
    var(tree, '{pName}_tightIso'.format(pName=pName))

    var(tree, '{pName}_againstMuonTight'.format(pName=pName))    
    var(tree, '{pName}_againstElectronLoose'.format(pName=pName))    

    var(tree, '{pName}_byLooseIsoMVA'.format(pName=pName))    
    var(tree, '{pName}_againstElectronMVA'.format(pName=pName))    
    var(tree, '{pName}_againstElectronTightMVA2'.format(pName=pName))
    var(tree, '{pName}_againstElectronMedium'.format(pName=pName))    
    var(tree, '{pName}_againstMuonLoose'.format(pName=pName))    

    var(tree, '{pName}_rawMvaIso'.format(pName=pName))
    var(tree, '{pName}_looseMvaIso'.format(pName=pName))
    var(tree, '{pName}_mediumMvaIso'.format(pName=pName))
    var(tree, '{pName}_tightMvaIso'.format(pName=pName))
   
    var(tree, '{pName}_EOverp'.format(pName=pName))
    var(tree, '{pName}_decayMode'.format(pName=pName))

def fillTau( tree, pName, tau ):
    fillLepton(tree, pName, tau)
    fill(tree, '{pName}_veryLooseIso'.format(pName=pName),
         tau.tauID("byVLooseCombinedIsolationDeltaBetaCorr"))
    fill(tree, '{pName}_looseIso'.format(pName=pName),
         tau.tauID("byLooseCombinedIsolationDeltaBetaCorr"))
    fill(tree, '{pName}_mediumIso'.format(pName=pName),
         tau.tauID("byMediumCombinedIsolationDeltaBetaCorr"))
    fill(tree, '{pName}_tightIso'.format(pName=pName),
         tau.tauID("byTightCombinedIsolationDeltaBetaCorr"))

    fill(tree, '{pName}_againstMuonTight'.format(pName=pName),
         tau.tauID("againstMuonTight"))
    fill(tree, '{pName}_againstElectronLoose'.format(pName=pName),
         tau.tauID("againstElectronLoose"))

    fill(tree, '{pName}_byLooseIsoMVA'.format(pName=pName),
         tau.tauID("byLooseIsoMVA"))
    fill(tree, '{pName}_againstElectronMVA'.format(pName=pName),
         tau.tauID("againstElectronMVA"))
    fill(tree, '{pName}_againstElectronTightMVA2'.format(pName=pName),
         tau.tauID("againstElectronTightMVA2"))
    fill(tree, '{pName}_againstElectronMedium'.format(pName=pName),
         tau.tauID("againstElectronMedium"))
    fill(tree, '{pName}_againstMuonLoose'.format(pName=pName),
         tau.tauID("againstMuonLoose"))

    fill(tree, '{pName}_rawMvaIso'.format(pName=pName),
         tau.tauID("byRawIsoMVA"))
    fill(tree, '{pName}_looseMvaIso'.format(pName=pName),
         tau.tauID("byLooseIsoMVA"))
    fill(tree, '{pName}_mediumMvaIso'.format(pName=pName),
         tau.tauID("byMediumIsoMVA"))
    fill(tree, '{pName}_tightMvaIso'.format(pName=pName),
         tau.tauID("byTightIsoMVA"))

    fill(tree, '{pName}_rawMvaIso'.format(pName=pName),
         tau.tauID("byRawIsoMVA"))
    fill(tree, '{pName}_EOverp'.format(pName=pName),
         tau.calcEOverP())
    fill(tree, '{pName}_decayMode'.format(pName=pName),
         tau.decayMode())


# jet


def bookParticleJet( tree, pName):
    '''For all kinds of jets.
    For pf and gen jets, the component variables are filled.
    For calo jets, they are filled and dummy.
    '''
    bookParticle(tree, pName )
    var(tree, '{pName}_chFrac'.format(pName=pName))
    var(tree, '{pName}_eFrac'.format(pName=pName))
    var(tree, '{pName}_muFrac'.format(pName=pName))
    var(tree, '{pName}_gammaFrac'.format(pName=pName))
    var(tree, '{pName}_h0Frac'.format(pName=pName))
    var(tree, '{pName}_hhfFrac'.format(pName=pName))
    var(tree, '{pName}_ehfFrac'.format(pName=pName))
    var(tree, '{pName}_rawFactor'.format(pName=pName))    
    var(tree, '{pName}_genJet_dr2'.format(pName=pName))    
    var(tree, '{pName}_genPart3_dr2'.format(pName=pName))    
    

def bookJet( tree, pName ):
    bookParticleJet(tree, pName ) 
    bookParticle(tree, '{pName}_leg'.format(pName=pName))
    bookParticleJet(tree, '{pName}_genJet'.format(pName=pName))
    bookGenParticle(tree, '{pName}_genPart3'.format(pName=pName))


def fillParticleJet( tree, pName, jet ):
    fillParticle(tree, pName, jet )
    fill(tree, '{pName}_chFrac'.format(pName=pName), jet.component(1).fraction() )
    fill(tree, '{pName}_eFrac'.format(pName=pName), jet.component(2).fraction() )
    fill(tree, '{pName}_muFrac'.format(pName=pName), jet.component(3).fraction() )
    fill(tree, '{pName}_gammaFrac'.format(pName=pName), jet.component(4).fraction() )
    fill(tree, '{pName}_h0Frac'.format(pName=pName), jet.component(5).fraction() )
    fill(tree, '{pName}_hhfFrac'.format(pName=pName), jet.component(6).fraction() )
    fill(tree, '{pName}_ehfFrac'.format(pName=pName), jet.component(7).fraction() )
    fill(tree, '{pName}_rawFactor'.format(pName=pName), jet.rawFactor() )


def fillJet( tree, pName, jet ):
    fillParticleJet(tree, pName, jet )
    if hasattr(jet, 'leg') and jet.leg:
        fillParticle(tree, '{pName}_leg'.format(pName=pName), jet.leg )
    genJet_dr2 = -1
    if hasattr(jet, 'genJet') and jet.genJet:
        fillParticleJet(tree, '{pName}_genJet'.format(pName=pName), jet.genJet )
        genJet_dr2 = jet.genJet_dr2
    fill(tree, '{pName}_genJet_dr2'.format(pName=pName), genJet_dr2 )
    genPart3_dr2 = -1
    if hasattr(jet, 'genParticle3') and jet.genParticle3:
        fillGenParticle(tree, '{pName}_genPart3'.format(pName=pName), jet.genParticle3 )
        genPart3_dr2 = jet.genParticle3_dr2
    fill(tree, '{pName}_genPart3_dr2'.format(pName=pName), genPart3_dr2 )
        
   
