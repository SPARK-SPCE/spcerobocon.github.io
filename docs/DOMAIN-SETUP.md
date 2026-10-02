# Deploying a GitHub Pages Site on a Custom Domain Using BigRock, Cloudflare, and GitHub Pages

This document explains in detail how to connect a custom domain purchased from BigRock with a GitHub Pages site, while using Cloudflare for DNS management and SSL. It is intended as a reference for future students or team members who may need to repeat this setup. Every step is explained conceptually and practically.

---

## BigRock: Updating Nameservers

When you purchase a domain from BigRock, it comes with BigRock’s own nameservers. Nameservers are responsible for telling the internet where to look up DNS records for your domain. By default, BigRock controls DNS, but BigRock’s DNS hosting does not provide easy HTTPS support for GitHub Pages. Therefore, we delegate DNS to Cloudflare.

Steps to update nameservers:

* Log into the BigRock dashboard.
* Go to the domain management page for the domain (e.g., spark.com).
* Find the “Nameservers” section.
* Replace the default BigRock nameservers with the two provided by Cloudflare (for example: `alice.ns.cloudflare.com` and `bob.ns.cloudflare.com`).
* Save the changes.

At this point, BigRock only acts as the registrar (it holds ownership of the domain). The actual DNS resolution is now controlled entirely by Cloudflare. Nameserver changes usually take effect within 30 minutes to a few hours, but may take up to 24–48 hours globally.

---

## Cloudflare: DNS Records and SSL

Cloudflare will serve two roles: managing DNS records and providing HTTPS via its free universal SSL certificates.

### Configuring DNS records

In the Cloudflare dashboard under the DNS tab, add the following records:

* Four A records for the root domain pointing to GitHub Pages servers:

  ```
  A   @   185.199.108.153
  A   @   185.199.109.153
  A   @   185.199.110.153
  A   @   185.199.111.153
  ```
* One CNAME record for the `www` subdomain pointing to the GitHub Pages domain:

  ```
  CNAME   www   mummanajagadeesh.github.io
  ```

The `@` symbol means the root domain (`spark.com`). The CNAME makes `www.spark.com` an alias for your GitHub Pages address.

Delete any leftover DNS records that point to old hosting providers (such as `162.215.226.6`), since they interfere with correct resolution.

For both the A records and the CNAME, enable the orange cloud proxy in Cloudflare. This ensures Cloudflare issues SSL certificates and serves your traffic through its global CDN.

### Configuring SSL

In Cloudflare, open the SSL/TLS settings:

* Set the SSL mode to **Full**.
* Enable “Always Use HTTPS” so that HTTP requests are automatically redirected to HTTPS.
* Enable “Automatic HTTPS Rewrites” to fix mixed content issues.

This ensures that all visitors see a secure HTTPS version of the site, even before GitHub’s own certificate is active.

---

## GitHub Pages: Custom Domain Settings

In your GitHub repository:

* Open **Settings ↗ Pages**.
* Enter `spark.com` as the custom domain.
* Save the setting.
* At the root of your repository, create a file named `CNAME` containing only:

  ```
  spark.com
  ```

GitHub will now verify your DNS configuration. Once it detects the correct DNS pointing to GitHub’s servers, it will attempt to issue its own SSL certificate using Let’s Encrypt.

Initially, GitHub may display “Enforce HTTPS — unavailable” because the SSL certificate has not been issued yet. This usually resolves within several hours once DNS propagation is complete. After that, you will be able to check the box to enforce HTTPS inside GitHub Pages.

---

## Understanding the Concepts

**Nameservers**
Nameservers are like the directory that tells browsers which DNS provider to ask for information about your domain. By setting nameservers in BigRock to Cloudflare, all DNS queries for your domain are answered by Cloudflare.

**DNS Records**
DNS records are mappings that convert domain names to IP addresses or other domain names. GitHub Pages requires four A records pointing to their server IPs for root domains, and a CNAME for subdomains such as `www`.

**SSL Certificates**
SSL certificates allow HTTPS to work. Cloudflare immediately provides a universal SSL certificate for your domain, which covers visitors right away. GitHub Pages later issues its own Let’s Encrypt certificate once the DNS setup is stable.

---

## Useful Commands to Check Progress

While waiting for propagation, you can use these commands:

* Check where the domain is pointing:

  ```bash
  nslookup spark.com
  ```

  or

  ```bash
  dig spark.com +noall +answer
  ```

* Check the `www` subdomain:

  ```bash
  nslookup www.spark.com
  ```

* Check if the site responds over HTTP:

  ```bash
  curl -I http://spark.com
  ```

* Check if HTTPS is working (ignoring certificate errors temporarily):

  ```bash
  curl -kI https://spark.com
  ```

* Inspect SSL certificate details:

  ```bash
  openssl s_client -connect spark.com:443
  ```

If these commands show the GitHub IP addresses (185.199.x.x) and return a valid HTTP or HTTPS response, your setup is correct.

---

## Final Result

Once the steps are complete and propagation has finished, your site will be fully accessible at:

* `https://spark.com`
* `https://www.spark.com`

Cloudflare ensures HTTPS works immediately, and eventually GitHub Pages will also provide its own HTTPS enforcement option.
