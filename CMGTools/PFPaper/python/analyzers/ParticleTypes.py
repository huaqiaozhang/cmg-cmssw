
def particleType( particle ):
    '''returns the particle type (as in PFCandidate).
    The type is deduced from the pdgId, so the function works for both
    PFCandidates and GenParticles.
    
    /// particle types
     enum ParticleType {
       X=0,     // undefined
       h,       // charged hadron
       e,       // electron 
       mu,      // muon 
       gamma,   // photon
       h0,      // neutral hadron
       h_HF,        // HF tower identified as a hadron
       egamma_HF    // HF tower identified as an EM particle
     };

    '''
    id = abs( particle.pdgId() )
    if particle.charge()==0:
        if id==22:
            return 4
        elif id==1:
            return 6
        elif id==2:
            return 7
        else:
            return 5
    else:
        if id==11:
            return 2
        elif id==13:
            return 3
        else:
            return 1
