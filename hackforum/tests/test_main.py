
import unittest
import subprocess
import requests
import time



class Test(unittest.TestCase):
    BASE_URL = "http://localhost:8080/"
    
    @classmethod  
    def setUpClass( cls ):
        
        subprocess.run(["python3", './hackforum/main_init.py'], check=True)
        cls.process = subprocess.Popen(['python3', './hackforum/main.py'])
        time.sleep(0.2)
        for loop in range(100):
            try:
               req = requests.get( cls.BASE_URL )
               break
            except Exception as e:
                print(e)
            

    @classmethod      
    def tearDownClass( cls ):
        time.sleep(0.2)
        print("Killing process .. ")
        cls.process.kill()
        cls.process.wait()


    def setUp( self ):
        self.session = requests.Session()

    
    def get_check( self, url, expect=200, **kwargs ):
       req = self.session.get( self.BASE_URL + url, **kwargs )       
       self.assertEqual( req.status_code , expect )
       print("Page GET %s - %d OK" % ( url, expect ))
       return req.content.decode("utf-8")
    
    def post_check( self, url, expect=200, **kwargs ):
        req = self.session.post( self.BASE_URL + url, **kwargs )   
        self.assertEqual( req.status_code , expect )
        print("Page POST %s - %d OK" % ( url, expect ))
    
    def do_login( self, username, password ):
        self.post_check( "login", data = {'username': username, 'password' : password} )
            
    def do_login_admin( self, password='p' ):
        return self.do_login( "admin", password )
        
    def check_no_login( self ):
        self.get_check( "", allow_redirects = False, expect=303)
        
    def test_0_login( self ):
        self.check_no_login()
        self.do_login_admin()
        self.get_check( "" )
        self.get_check("logout")
        self.check_no_login()
    
    def test_0_login_invalid( self ):
        self.do_login_admin( password="XXX" )
        self.check_no_login()
        
    
    def test_1_post_comment( self ):
        self.do_login_admin()
        page = self.get_check("")
        unique_str = "This is my first comment"
        assert( unique_str not in page )
        self.post_check("", data = { "comment" : unique_str } )
        page = self.get_check("")
        assert( unique_str in page )

    
    def test_2_add_user( self ):
        self.do_login_admin()
        self.get_check("admin")
        self.post_check("admin", data = { "username" : "ted", "password" : "12345", "level" : "0" } )
        self.session = requests.Session()
        self.check_no_login()
        self.do_login("ted", "12345")
        self.get_check("")
        
        



if __name__=="__main__":
    unittest.main()
