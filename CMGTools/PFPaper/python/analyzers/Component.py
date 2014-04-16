class Component(object):
    def __init__(self, id, mult=0, frac=0., energy=0., pt=0.):
        self._id = id
        self._multiplicity = mult
        self._fraction = frac
        self._energy = energy
        self._pt = pt

    def multiplicity(self):
        return self._multiplicity

    def fraction(self):
        return self._fraction

    def energy(self):
        return self._energy

    def pt(self):
        return self._pt

    def __eq__(self, other):
        delta = 1e-9
        if self._id != other._id:
            return False
        attrs = ['_multiplicity', '_fraction', '_energy', '_pt']
        for attr in attrs:
            if abs( getattr(self,attr)-getattr(other, attr) ) > delta:
                return False
        return True
        
    def __iadd__(self, other):
        if self._id != other._id:
            raise ValueError( 'components have different ids: {id1} != {id2}'.format(id1=self._id,
                                                                                     id2=other._id))
        self._multiplicity += other._multiplicity
        self._fraction += other._fraction
        self._energy += other._energy
        self._pt += other._pt
        return self

    def __str__(self):
        return 'component {id:5}: {mult:3} {frac:5.2f} {ener:5.2f} {pt:5.2f}'.format(
            id = self._id,
            mult = self._multiplicity,
            frac = self._fraction,
            ener = self._energy,
            pt = self._pt
            )
    

