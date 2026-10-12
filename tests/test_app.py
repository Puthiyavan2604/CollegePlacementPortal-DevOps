import os, tempfile, unittest
from app import app
class PortalTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  os.environ["DATABASE_PATH"]=os.path.join(self.tmp.name,"test.db")
  app.config["TESTING"]=True
  self.client=app.test_client()
 def tearDown(self):
  self.tmp.cleanup(); os.environ.pop("DATABASE_PATH",None)
 def test_home(self):
  r=self.client.get("/"); self.assertEqual(r.status_code,200); self.assertIn(b"CampusConnect",r.data)
 def test_health(self):
  r=self.client.get("/health"); self.assertEqual(r.status_code,200); self.assertEqual(r.get_json()["status"],"healthy")
 def test_job(self):
  self.assertEqual(self.client.get("/jobs/1").status_code,200)
 def test_unknown_job(self):
  self.assertEqual(self.client.get("/jobs/999").status_code,404)
 def test_apply(self):
  r=self.client.post("/apply/1",data={"full_name":"Test Student","email":"test@example.com","department":"Computer Science and Engineering","graduation_year":"2027"},follow_redirects=True)
  self.assertEqual(r.status_code,200); self.assertIn(b"Application Received",r.data)
if __name__=="__main__": unittest.main()
