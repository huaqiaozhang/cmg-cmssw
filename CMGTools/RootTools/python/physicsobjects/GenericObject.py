import copy


class GenericObject(object):
    '''Extends an object, in particular a C++ object read
    from an EDM file.'''

    def __init__(self, obj):
        self.obj = obj
        super(GenericObject, self).__init__()

    def __copy__(self):
        '''Very dirty trick, the obj is deepcopied...'''
        # print 'call copy', self
        obj = copy.deepcopy( self.obj )
        newone = type(self)(obj)
        newone.__dict__.update(self.__dict__)
        newone.obj = obj
        return newone        

    def __getattr__(self,name):
        '''all attributes from self.obj are transferred to this class.
        '''
        return getattr(self.obj, name)

    def __str__(self):
        tmp = '{className}'
        return tmp.format( className = self.__class__.__name__ )
