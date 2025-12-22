# Certbot DNS All-Inkl Plugin

This is a Certbot plugin for the **All-Inkl** DNS service (KAS).  
It automates the process of completing `dns-01` challenges by creating and removing TXT records via the KAS API.

> **Disclaimer:** This plugin was developed with the assistance of AI. While it has been verified to work in production environments, please review the code and test carefully before using it in critical systems. Use at your own risk.

## Installation

### Via Pip (PyPI)
*Coming soon...*

### From Source
```bash
pip install git+https://github.com/mobilandi/certbot-dns-allinkl.git
```

## Usage

1. **Create a credentials file** (e.g., `credentials.ini`):
   ```ini
   dns_allinkl_kas_user = your_kas_login
   dns_allinkl_kas_password = your_kas_password
   ```
   *(Ensure this file is only readable by root/owner: `chmod 600 credentials.ini`)*

2. **Run Certbot:**
   ```bash
   certbot certonly \
     --authenticator dns-allinkl \
     --dns-allinkl-credentials credentials.ini \
     -d example.com -d *.example.com
   ```

## Nginx Proxy Manager Integration

To use this plugin with [Nginx Proxy Manager](https://nginxproxymanager.com/), you can install it into the running container.

1. **Enter the container and install:**
   ```bash
   docker exec -it nginx-proxy-manager sh -c "export SETUPTOOLS_USE_DISTUTILS=stdlib && pip install git+https://github.com/mobilandi/certbot-dns-allinkl.git"
   ```

2. **Configure `dns-plugins.json`** (usually in `/app/certbot/dns-plugins.json`):
   ```json
   "allinkl": {
     "name": "All-Inkl",
     "package_name": "certbot-dns-allinkl",
     "version": "==0.1.1",
     "dependencies": "kasserver",
     "credentials": "dns_allinkl_kas_user = your_kas_user\ndns_allinkl_kas_password = your_kas_password",
     "full_plugin_name": "dns-allinkl"
   }
   ```

3. **Restart the container.**

## Development

### Running Tests
```bash
pip install -e .
pip install pytest mock certbot
python -m pytest tests
```

## Credits
Based on the `kasserver` python library.
