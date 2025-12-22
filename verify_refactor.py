import logging
import sys
import time
import os
from certbot_dns_allinkl._internal.dns_allinkl import Authenticator
from unittest import mock

# Configure logging to see our Print/Info statements
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_plugin():
    print("--- Starting Manual Verification of Refactored Plugin ---")
    
    # 1. Load Credentials
    cred_file = "../credentials.ini"
    if not os.path.exists(cred_file):
        print(f"Error: Credentials file not found at {cred_file}")
        return

    print(f"Using credentials from: {cred_file}")
    
    # Mock the Certbot Config object to return our credentials path
    mock_config = mock.MagicMock(dns_allinkl_credentials=cred_file)
    
    # Instantiate Authenticator
    auth = Authenticator(mock_config, "dns-allinkl")
    
    domain = "mobilandi.de" # Replace if your credentials are for a different domain, or assume wildcard
    # Note: KAS API needs valid zone. We'll try a test subdomain.
    test_fqdn = "_acme-challenge-test.home.mobilandi.de" 
    token = "TEST_TOKEN_" + str(int(time.time()))
    
    print(f"\n1. Testing _perform (Add Record)")
    print(f"   FQDN: {test_fqdn}")
    print(f"   Token: {token}")
    
    try:
        auth._perform(domain, test_fqdn, token)
        print("   ✅ _perform executed successfully.")
    except Exception as e:
        print(f"   ❌ _perform FAILED: {e}")
        return

    print("\n   [Waiting 10s for propagation/API latency...]")
    time.sleep(10)
    
    print(f"\n2. Testing _cleanup (Safe Delete)")
    print("   Watch the logs below. You should see 'Deleting TXT record... (ID: ...)'")
    
    try:
        auth._cleanup(domain, test_fqdn, token)
        print("   ✅ _cleanup executed successfully.")
    except Exception as e:
        print(f"   ❌ _cleanup FAILED: {e}")

    print("\n--- Verification Complete ---")
    print("If you saw the ID in the logs, the Safe Cleanup is working!")

if __name__ == "__main__":
    test_plugin()
