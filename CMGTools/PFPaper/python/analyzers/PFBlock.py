from CMGTools.RootTools.physicsobjects.GenericObject import GenericObject


class PFBlockElement(GenericObject):

    def __str__(self):
        header = [ super(PFBlockElement, self).__str__() ] 
        header.append( str( self.type() ) )
        return ' '.join(header)
        
        

class PFBlock(GenericObject):

    def __init__(self, obj):
        self.pelements = map( PFBlockElement, obj.elements() )
        super(PFBlock, self).__init__(obj)

    def __str__(self):
        theStr = [ super(PFBlock, self).__str__() ]
        theStr = []
        theStr.extend([ str(elem) for elem in self.pelements ])
        return '\n'.join( theStr ) 

   
def sort_elements(self):
    self.selems = dict()
    for elem in self.pelements:
        self.selems.setdefault( elem.type(), []).append( elem )
    return self.selems


## def block_analysis(self, sorted_elements): 
##     itracks = sorted_elements.get(1)
##     if itracks is None:
##         return False
##     iassoc = 
##     return True
