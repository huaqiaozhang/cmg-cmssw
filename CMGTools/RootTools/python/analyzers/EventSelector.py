from CMGTools.RootTools.fwlite.Analyzer import Analyzer


class EventSelector( Analyzer ):
    """Skips events that are not in the toSelect list.

    Example:

    eventSelector = cfg.Analyzer(
      'EventSelector',
      toSelect = [
       1239742,
       38001,
       159832
      ],
      iEv = False
    )

    The process function of this analyzer returns False if the event number
    is not in the toSelect list.

    If the optional parameter iEv is False, put in this list the actual
    CMS event numbers obtained by doing:
       iEvent.eventAuxiliary().id().event()
    If iEv is True, put in the list the number of events processed in this
    framework (the first processed event being event number 0)

    This analyzer is typically inserted at the beginning of the analyzer
    sequence to skip events you don't want.
    We use it in conjonction with an
      import pdb; pdb.set_trace()
    statement in a subsequent analyzer, to debug a given event in the
    toSelect list.

    This kind of procedure if you want to synchronize your selection
    with an other person at the event level. 
    """

    def process(self, iEvent, event):
        run = iEvent.eventAuxiliary().id().run()
        lumi = iEvent.eventAuxiliary().id().luminosityBlock()
        eId = iEvent.eventAuxiliary().id().event()
        if self.cfg_ana.iEv:
            eId = event.iEv
        if eId in self.cfg_ana.toSelect:
            # raise ValueError('found')
            print 'Selecting', run, lumi, eId
            return True 
        else:
            return False
