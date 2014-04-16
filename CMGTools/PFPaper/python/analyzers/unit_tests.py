import unittest
from CMGTools.PFPaper.analyzers.Component import Component
from CMGTools.PFPaper.analyzers.ParticleTypes import particleType

class TestComponent(unittest.TestCase):

    def setUp(self):
        self.h1 = Component( 211, 1, 0.2, 20., 40.)
        self.h2 = Component( 211, 1, 0.2, 20., 40.)
        self.h3 = Component( -211, 1, 0.2, 20., 40.)
        self.h4 = Component( 211, 1, 0.2, 20., 40.)
        self.gam = Component( 22, 1, 0.1, 10., 20.)
        self.nh = Component( 130, 1, 0.1, 10., 20.)
            
    def test_dummy(self):
        self.assertTrue( True )

    def test_sum_fails(self):
        self.assertRaises( ValueError, self.h1.__iadd__, self.gam)

    def test_sum_succeeds(self):
        self.h1 += self.h2
        self.assertEqual( self.h1,
                          Component( 211, 2, 0.4, 40, 80) )

##     def test_write_protection(self):
##         self.assertRaises( AttributeError, setattr, self.h1, 'fraction', 0. )


    def test_print(self):
        self.assertEqual( str( Component( -2141, 3, 0.55135, 1.0, 1.0) ),
                          'component -2141:   3  0.55  1.00  1.00' )



class MockParticle(object):
    def __init__(self, pdgId, charge):
        self._pdgId = pdgId
        self._charge = charge
    def pdgId(self): return self._pdgId
    def charge(self): return self._charge
    


class TestParticleTypes(unittest.TestCase):

    def test_types(self):
        self.assertEqual(1, particleType( MockParticle(211, 1) ) )
        self.assertEqual(1, particleType( MockParticle(-211, -1) ) )
        self.assertEqual(4, particleType( MockParticle(22, 0) ) )
        self.assertEqual(5, particleType( MockParticle(130, 0) ) )
        self.assertEqual(6, particleType( MockParticle(1, 0) ) )
        self.assertEqual(7, particleType( MockParticle(2, 0) ) )

    

if __name__ == '__main__':

    unittest.main()
