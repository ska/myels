
import os
import sys
import unittest

codepath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(codepath))

import rete

class TestOpenMSG(unittest.TestCase):
    def test_status_request(self):
        raw = '*#0*1##'
        msg = rete.OpenMSG.build_status_request('0', '1')
        msg_raw = rete.OpenMSG(raw)

        self.assertEqual(str(msg_raw), raw)
        self.assertEqual(str(msg), raw)

        self.assertTrue(msg.is_sts_req)
        self.assertEqual(msg.who, '0')
        self.assertEqual(msg.where, '1')

        self.assertTrue(msg_raw.is_sts_req)
        self.assertEqual(msg_raw.who, '0')
        self.assertEqual(msg_raw.where, '1')

    def test_standard(self):
        raw = '*0*1*2##'
        msg = rete.OpenMSG.build_standard('0', '1', '2')
        msg_raw = rete.OpenMSG(raw)

        self.assertEqual(str(msg_raw), raw)
        self.assertEqual(str(msg), raw)

        self.assertTrue(msg.is_std)
        self.assertEqual(msg.who, '0')
        self.assertEqual(msg.what, '1')
        self.assertEqual(msg.where, '2')

        self.assertTrue(msg_raw.is_std)
        self.assertEqual(msg_raw.who, '0')
        self.assertEqual(msg_raw.what, '1')
        self.assertEqual(msg_raw.where, '2')

    def test_ack(self):
        raw = '*#*1##'
        msg = rete.OpenMSG.build_ack()
        msg_raw = rete.OpenMSG(raw)

        self.assertEqual(str(msg_raw), raw)
        self.assertEqual(str(msg), raw)

        self.assertTrue(msg.is_ack)
        self.assertTrue(msg_raw.is_ack)

    def test_nack(self):
        raw = '*#*0##'
        msg = rete.OpenMSG.build_nack()
        msg_raw = rete.OpenMSG(raw)

        self.assertEqual(str(msg_raw), raw)
        self.assertEqual(str(msg), raw)

        self.assertTrue(msg.is_nack)
        self.assertTrue(msg_raw.is_nack)

if __name__=='__main__':
    unittest.main()

