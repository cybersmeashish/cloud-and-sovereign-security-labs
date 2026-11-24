import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from site_service import decision,serve_cases
class SiteTests(unittest.TestCase):
 def state(self,**patch):
  s={"policy_present":True,"now":10,"expires":60,"bundle_epoch":7,"required_epoch":7};s.update(patch);return s
 def test_valid_local_case(self):self.assertEqual(decision(self.state(),"staff-A")[0],200)
 def test_missing_and_expired_policy_fail_closed(self):
  self.assertEqual(decision(self.state(policy_present=False),"staff-A")[0],503);self.assertEqual(decision(self.state(now=60),"staff-A")[0],503)
 def test_revoked_or_restored_epoch_fail_closed(self):
  self.assertEqual(decision(self.state(required_epoch=8),"staff-A")[0],503);self.assertEqual(decision(self.state(bundle_epoch=6),"staff-A")[0],503)
 def test_cross_case_or_unknown_actor_denied(self):
  self.assertEqual(decision(self.state(),"staff-B")[0],403);self.assertEqual(decision(self.state(),"unknown")[0],403)
 def test_actual_loopback_statuses(self):self.assertEqual(len(serve_cases()),7)
