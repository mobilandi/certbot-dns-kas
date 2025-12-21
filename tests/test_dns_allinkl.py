import sys
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from certbot.plugins import dns_test_common
from certbot.plugins import dns_common_test
from certbot.tests import util as test_util

from certbot_dns_allinkl._internal.dns_allinkl import Authenticator

class AuthenticatorTest(test_util.TempDirTestCase, dns_common_test.DNSAuthenticatorTest):

    def setUp(self):
        super().setUp()
        self.config = mock.MagicMock(dns_allinkl_credentials='path/to/credentials.ini')
        self.auth = Authenticator(self.config, 'dns-allinkl')
        
        self.auth.credentials = mock.MagicMock()
        self.auth.credentials.conf.side_effect = lambda x: 'mock_value'

        self.mock_client = mock.MagicMock()
        # Mock the _kas_client property or the class instantiation
        self.auth._kas_client = self.mock_client

    def test_perform(self):
        self.auth._perform('example.com', '_acme-challenge.example.com', 'token')
        self.mock_client.add_dns_record.assert_called_with(
            fqdn='_acme-challenge.example.com',
            record_type='TXT',
            record_data='token',
            record_aux=0
        )

    def test_cleanup(self):
        self.auth._cleanup('example.com', '_acme-challenge.example.com', 'token')
        self.mock_client.delete_dns_record.assert_called_with(
            fqdn='_acme-challenge.example.com',
            record_type='TXT'
        )

    @mock.patch('certbot_dns_allinkl._internal.dns_allinkl.KasServer')
    @mock.patch.dict('os.environ', {}, clear=True)
    def test_get_kas_client(self, mock_kas):
        self.auth._kas_client = None
        self.auth._get_kas_client()
        
        import os
        self.assertEqual(os.environ['KASSERVER_USER'], 'mock_value')
        self.assertEqual(os.environ['KASSERVER_PASSWORD'], 'mock_value')
        mock_kas.assert_called_once()


if __name__ == '__main__':
    unittest.main()
