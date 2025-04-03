import scrapy
from scrapy_playwright.page import PageCoroutine

class LawsSpider(scrapy.Spider):
    name = "laws_spider"
    start_urls = ["https://laws.moj.gov.sa/en/legislations-regulations?pageNumber=1&pageSize=9&sortingBy=7"]

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "DOWNLOAD_HANDLERS": {"http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                              "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler"},
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True}
    }

    async def parse(self, response):
        # Extract PDF links
        pdf_links = response.css("a[href$='.pdf']::attr(href)").getall()
        for link in pdf_links:
            yield {"pdf_url": response.urljoin(link)}

        # Pagination
        next_page = response.css("a.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, meta={"playwright": True, "playwright_page_coroutines": [PageCoroutine("wait_for_load_state", "load")]})
