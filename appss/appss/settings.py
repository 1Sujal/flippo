# Scrapy settings for mindbadkyo project

BOT_NAME = "appss"

SPIDER_MODULES = ["appss.spiders"]
NEWSPIDER_MODULE = "appss.spiders"

# Do NOT obey robots.txt for API scraping
ROBOTSTXT_OBEY = False

# Use scrapy-impersonate for TLS + JA3 spoofing
DOWNLOAD_HANDLERS = {
    "http": "scrapy_impersonate.ImpersonateDownloadHandler",
    "https": "scrapy_impersonate.ImpersonateDownloadHandler",
}

# Let impersonate pick the User-Agent
USER_AGENT = None

# Required for curl_cffi-based requests
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Logging level
LOG_LEVEL = "INFO"

# Output encoding
FEED_EXPORT_ENCODING = "utf-8"

# Disable cookies
COOKIES_ENABLED = False

# Optional: auto-throttle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Optional: disable Telnet
TELNETCONSOLE_ENABLED = False
