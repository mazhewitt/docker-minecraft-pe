import mc_setup
import http.client
import unittest
import os

class TestServerSetup(unittest.TestCase):
    def test_retreive_url(self):
        download_url = mc_setup.grab_download_url("https://www.minecraft.net/en-us/download/server/bedrock/") 
        self.assertTrue(download_url, "https://www.minecraft.net/bedrockdedicatedserver/bin-linux/bedrock-server-1.21.42.01.zip")

    def test_download(self):
        download_url = mc_setup.grab_download_url("https://www.minecraft.net/en-us/download/server/bedrock/")
        server_zip = "server.zip" 
        mc_setup.download_server(download_url, server_zip)
        os.stat("server.zip")

if __name__ == '__main__':
    unittest.main()