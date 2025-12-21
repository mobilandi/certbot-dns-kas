# Certbot DNS All-Inkl Plugin

This is a certbot plugin for the All-Inkl DNS service. It allows you to use the `dns-01` challenge with Let's Encrypt.

## Installation

```bash
pip install certbot-dns-allinkl
```

## Usage

1. Create a credentials file (e.g., `credentials.ini`):
   ```ini
   dns_allinkl_kas_user = your_kas_user
   dns_allinkl_kas_password = your_kas_password
   ```

2. Run Certbot:
   ```bash
   certbot certonly \
     --authenticator dns-allinkl \
     --dns-allinkl-credentials credentials.ini \
     -d example.com
   ```
