import scrapy
import json
import re
from urllib.parse import urlencode


class FlippaSpider(scrapy.Spider):
    name = "flippa_shopify"
    allowed_domains = ["flippa.com"]
    base_domain = "https://flippa.com"

    def __init__(self,
                 keyword="shopify",
                 sale_method="auction,classified",
                 status="open",
                 property_type=("website,fba,saas,ecommerce_store,plugin_and_extension,"
                                "ai_apps_and_tools,youtube,ios_app,android_app,game,crypto_app,"
                                "social_media,newsletter,service_and_agency,service,"
                                "projects_and_concepts,other"),
                 revenue_generating="T,F"):
        self.keyword = keyword
        self.sale_method = sale_method
        self.status = status
        self.property_type = property_type
        self.revenue_generating = revenue_generating

    def build_url(self, page):
        params = {
            "query[keyword]": self.keyword,
            "button": "",
            "search_template": "most_relevant",
            "page[number]": str(page),
            "filter[sale_method]": self.sale_method,
            "filter[status]": self.status,
            "filter[property_type]": self.property_type,
            "filter[revenue_generating]": self.revenue_generating,
        }
        return f"{self.base_domain}/search?{urlencode(params)}"

    def start_requests(self):
        yield scrapy.Request(
            url=self.build_url(1),
            headers={"User-Agent": "Mozilla/5.0"},
            callback=self.parse,
            meta={"page": 1},
        )

    def parse(self, response):
        page = response.meta["page"]
        data_card = re.search(r"const STATE = ({.*?});\s*const", response.text, re.DOTALL)

        if not data_card:
            self.logger.info(f"No STATE JSON on page {page} — stopping.")
            return

        try:
            state_json = json.loads(data_card.group(1))
            list_of_data = state_json.get("results", [])

            if not list_of_data:
                self.logger.info(f"No list_of_data found on page {page} — stopping.")
                return

            for item in list_of_data:
                relative_url = item.get("listing_url", "")
                full_url = f"{self.base_domain}{relative_url}" if relative_url else None

                yield {
                    "title": item.get("title"),
                    "price": item.get("price"),
                    "profit_average": item.get("profit_average"),
                    "revenue_average": item.get("revenue_average"),
                    "monetization": item.get("monetization"),
                    "property_type": item.get("property_type"),
                    "category": item.get("category"),
                    "country_name": item.get("country_name"),
                    "site_age_years": item.get("formatted_age_in_years"),
                    "url": full_url,
                    "source_page_url": response.url,
                }

            next_page = page + 1
            self.logger.info(f"Proceeding to page {next_page}")
            yield scrapy.Request(
                url=self.build_url(next_page),
                headers={"User-Agent": "Mozilla/5.0"},
                callback=self.parse,
                meta={"page": next_page},
            )

        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error on page {page}: {e}")
