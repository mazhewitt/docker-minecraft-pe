import mc_setup

import unittest

class TestServerSetup(unittest.TestCase):
    def test_retreive_url(self):
        download_url = mc_setup.grab_download_url("https://www.minecraft.net/en-us/download/server/bedrock/")
        
        self.assertTrue(download_url, "https://minecraft.azureedge.net/bin-linux/bedrock-server-1.16.201.02.zip")

if __name__ == '__main__':
    unittest.main()