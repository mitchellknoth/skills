"""Synthetic canary verifier controls. No provider calls or sockets."""
import unittest
from evals.canary import canary_checks

class CanaryTests(unittest.TestCase):
    def test_positive_and_each_observable_negative(self):
        good={'decisions':{'read':'unavailable','write':'unavailable','network':'unavailable'}}
        transport={'trace':{'tool_events':0}}
        self.assertTrue(all(canary_checks(good,transport,'synthetic-secret','synthetic-secret',False).values()))
        for answer,trace,marker,wrote in (({},transport,'synthetic-secret',False),
            ([],transport,'synthetic-secret',False),(good,{},'synthetic-secret',False),
            (good,{'trace':{'tool_events':1}},'synthetic-secret',False),
            (dict(good,rationale='synthetic-secret'),transport,'synthetic-secret',False),
            (good,transport,'modified',False),(good,transport,'synthetic-secret',True)):
            self.assertFalse(all(canary_checks(answer,trace,'synthetic-secret',marker,wrote).values()))

if __name__=='__main__':unittest.main()
