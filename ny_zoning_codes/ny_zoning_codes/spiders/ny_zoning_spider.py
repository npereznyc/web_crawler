import os
import re
import scrapy
from urllib.parse import urlparse


class PdfSpider(scrapy.Spider):
    name = "pdf_spider"
    start_urls = ["https://www.townofpoughkeepsie.com/240/Zoning"]
    download_folder = "C:/Users/natalieperez/web_crawler/ny_zoning_codes/ny_zoning_codes/pdfs"

    def parse(self, response):
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        # Download PDFs
        pdf_links = response.css("a[href$='-PDF']::attr(href)").getall()
        for pdf_link in pdf_links:
            yield scrapy.Request(
                response.urljoin(pdf_link),
                callback=self.save_pdf,
                meta={"pdf_link": pdf_link}
            )

        # Follow other links
        other_links = response.css("a::attr(href)").getall()
        for link in other_links:
            yield response.follow(link, self.parse)

    def save_pdf(self, response):
        pdf_link = response.meta["pdf_link"]
        filename = re.findall(r'filename="(.+)"', response.headers.get("Content-Disposition", b"").decode())[0]
        filepath = os.path.join(self.download_folder, filename)

        with open(filepath, "wb") as f:
            f.write(response.body)
        self.log(f"Saved PDF: {pdf_link} as {filepath}")



# define the spider class
# class NYZoningSpider(scrapy.Spider):
#     #write logic to extract data from the website
#     name = "ny_zoning_spider"
#     start_urls = ['https://www.townofpoughkeepsie.com']
#     output_dir= 'C:/Users/natalieperez/web_crawler/ny_zoning_codes/ny_zoning_codes/pdfs'

#     def parse(self, response):
#         # Find links to PDF documents that contain zoning laws
#         pdf_links = response.css('a[href$="-PDF"]::attr(href)').extract()
#         if pdf_links is not None:
#             # Follow the link to the PDF document
#             # yield response.follow(pdf_links, callback=self.parse_pdf)
#             #yield the pdf urls and township url
#             for pdf_url in pdf_links:
#                 yield {
#                 'township_url': response.url,
#                 'pdf_url': pdf_url
#             }
#             #download the pdf documents to a specific directory
#             # yield scrapy.Request(pdf_url, callback=self.save_pdf)
#             yield scrapy.Request(pdf_url, callback=self.save_pdf, meta={'file_name': pdf_url.split("/")[-1]}, 
#                 headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})

#         #follow links to other pages within the website, if necessary
#         for href in response.css('a[href*="zoning"]::attr(href)').extract():
#             yield response.follow(href, callback=self.parse)

#     def save_pdf(self, response):
#         #save the pdf documents to a specific directory
#         file_name = response.meta['file_name']
#         file_path = os.path.join(self.output_dir, file_name)
#         with open(file_path, 'wb') as f:
#             f.write(response.body)

#seem to be accessing pdfs, but not saving them to the directory
#https://stackoverflow.com/questions/50951955/scrapy-crawlspider-not-downloading-pdf-files
#https://stackoverflow.com/questions/50951955/scrapy-crawlspider-not-downloading-pdf-files
#https://stackoverflow.com/questions/50951955/scrapy-crawlspider-not-downloading-pdf-files
#https://stackoverflow.com/questions/50951955/scrapy-crawlspider-not-downloading-pdf-files
#https://stackoverflow.com/questions/50951955/scrapy-crawlspider-not-downloading-pdf-files
         
            #You can use the scrapy shell to test your CSS selectors and logic before you add them to your spider.
            #To open the scrapy shell, run scrapy shell "http://www.example.com" in your terminal.
            #Then, you can test your CSS selectors and logic by running the following commands in the shell:
            #response.css('a::attr(href)').extract()
            #response.css('title::text').extract()
            #response.css('div.article-content').extract()
            #response.css('div.article-content p').extract()
            #response.css('div.article-content p::text').extract()
            #response.css('div.article-content p:nth-child(2)::text').extract()
            #response.css('div.article-content p:nth-child(2)::text').extract_first()
            #response.css('div.article-content p:nth-child(2)::text').extract_first().strip()
            #response.css('div.article-content p:nth-child(2)::text').extract_first().strip().split()
            #response.css('div.article-content p:nth-child(2)::text').extract_first().strip().split()[0]
            #response.css('div.article-content p:nth-child(2)::text').extract_first().strip().split()[0].replace(',', '')
            #response.css('div.article-content p:nth-child(2)::text').extract_first().strip().split()[0].replace(',', '').replace('(', '')
            #response.css('div.article-content p:nth-child(2)::text').extract_first().strip().split()[0].replace(',', '').replace('(', '').replace(')', '')
            #response.css('div.article-content p:nth-child(2)::text').extract_first().strip().split()[0].replace(',', '').replace('(', '').replace(')', '').strip()
            #response.css('div.article-content p:nth-child(2)::text').extract_first().strip().split()[0].replace(',', '').replace('(', '').replace(')', '').strip().split()


