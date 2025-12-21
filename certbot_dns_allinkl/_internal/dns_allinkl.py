import logging
from typing import Any
from typing import Optional

import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

try:
    from kasserver import KasServer
except ImportError:
    # Allow import for basic setuptools operations even if kasserver is missing
    KasServer = None

logger = logging.getLogger(__name__)

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for All-Inkl."""

    description = 'Obtain certificates using a DNS TXT record with All-Inkl.'
    ttl = 60

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._kas_client = None

    @classmethod
    def add_parser_arguments(cls, add: Any, default_propagation_seconds: int = 120) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add('credentials', help='All-Inkl KAS credentials INI file.')

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            'credentials',
            'All-Inkl credentials INI file',
            {
                'kas_user': 'KAS username/login',
                'kas_password': 'KAS password',
            }
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        # Note: 'record_aux' is typically priority. KAS API usually expects 0 for TXT.
        # TTL is not evidently exposed in add_dns_record signature (fqdn, record_type, record_data, record_aux).
        self._get_kas_client().add_dns_record(
            fqdn=validation_name,
            record_type='TXT',
            record_data=validation,
            record_aux=0
        )

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        # WARNING: delete_dns_record signature is (fqdn, record_type).
        # This implies it might delete ALL TXT records for this FQDN.
        try:
            self._get_kas_client().delete_dns_record(
                fqdn=validation_name,
                record_type='TXT'
            )
        except Exception as e:
            logger.warning('Failed to delete DNS record: %s', e)

    def _get_kas_client(self) -> "KasServer":
        import os
        if not self._kas_client:
            if KasServer is None:
                raise errors.PluginError("kasserver library is not installed.")
            
            # kasserver uses environment variables for configuration
            os.environ['KASSERVER_USER'] = self.credentials.conf('kas_user')
            os.environ['KASSERVER_PASSWORD'] = self.credentials.conf('kas_password')
            
            self._kas_client = KasServer()
        return self._kas_client
