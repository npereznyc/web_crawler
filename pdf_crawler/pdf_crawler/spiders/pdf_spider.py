import os
import re
import scrapy
from urllib.parse import urlparse, urljoin
import logging
from scrapy.linkextractors import LinkExtractor
from scrapy.http import TextResponse

class PdfSpider(scrapy.Spider):
    name = "pdf_spider"
    start_urls = ["https://www.pjm.com/planning/services-requests/interconnection-queues.aspx"]  
    download_folder = "pdf_downloads" 

    def parse(self, response):
        content_type = response.headers.get('Content-Type')

        if b'text/html' in content_type:
            # Process HTML content
            link_extractor = LinkExtractor()
            links = link_extractor.extract_links(response)
            for link in links:
                yield response.follow(link.url, self.parse)

        elif b'application/pdf' in content_type:
            # Process PDF content
            file_url = response.url
            file_extension = os.path.splitext(file_url)[-1].lower()
            if file_extension == '.pdf':
                file_name = file_url.split("/")[-1]
                file_path = os.path.join("pdfs", file_name)
                self.logger.info(f"Saving PDF: {file_name}")
                if not os.path.exists("pdfs"):
                    os.makedirs("pdfs")
                with open(file_path, "wb") as f:
                    f.write(response.body)
        else:
            self.logger.info(f"Skipping non-text, non-pdf content: {response.url}")

        # pdf_links = response.css("a[href$='.pdf']::attr(href)").getall()
        # for pdf_link in pdf_links:
        #     yield scrapy.Request(
        #         response.urljoin(pdf_link),
        #         self.save_pdf,
        #         meta={"file_name": pdf_link.split("/")[-1]}
        #     )
        # if pdf_links:
        #     logging.info(f"Found {len(pdf_links)} PDF links on {response.url}")
        # else:
        #     logging.info(f"No PDF links found on {response.url}")

        # # Follow other links
        # start_url_domain = urlparse(self.start_urls[0]).netloc
        # other_links = response.css("a[href]::attr(href)").getall()

        # for link in other_links:
        #     link_parsed = urlparse(link)
        #     link_domain = link_parsed.netloc
        #     link_scheme = link_parsed.scheme

        #     absolute_link = response.urljoin(link)  # Convert the relative link to an absolute link
        #     absolute_link_parsed = urlparse(absolute_link)
        #     absolute_link_domain = absolute_link_parsed.netloc
        #     absolute_link_scheme = absolute_link_parsed.scheme

        #     if (not absolute_link_domain or absolute_link_domain == start_url_domain) and absolute_link_scheme in ['http', 'https']:
        #         yield response.follow(absolute_link, self.parse)

    def save_pdf(self, response):
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        pdf_link = response.url
        filename = response.meta["file_name"]
        yield {
            'file_urls': [pdf_link],
            'file_name': filename
        }