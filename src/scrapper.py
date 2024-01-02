import requests
import re
import os
import logging

from lxml.html import fromstring
from lxml import etree

from utils import load_yaml, sanitize


class Scrapper:
    def __init__(self, url=None, main_xpath="//main", domain_path=None, **kwargs):
        self.url = url
        self.xpath = main_xpath
        self.top_lvl_domain = self.load_domains()

    def load_domains(self, path="domains.yaml"):
        path = os.path.join("configs", path)
        config = load_yaml(path)
        return config.get("top-lvl-domain", [])

    def process_url(self):
        domain_match = re.search(r"\.[a-z]+$", self.url)
        if domain_match:
            return

        schema_match = [] if "http" in url else ["https://", "http://"]

        for domain in self.top_lvl_domain:
            for schema in schema_match:
                url = schema + self.url + domain
                try:
                    response = requests.get(url)

                    self.url = url
                    logging.info(f"Find working url {self.url}")
                except requests.exceptions.MissingSchema as e:
                    continue
                except Exception as e:
                    logging.error(f"Find an error {e}")

    def download_content(self, url, main_xpath):
        logging.info(f"Getting content from url")
        self.url = url
        self.xpath = main_xpath
        logging.info(f"Main XPATH {self.xpath}")

        if not self.url:
            return ""

        response = requests.get(self.url)
        response_text = response.text
        logging.info(f"Get content with length {len(response_text)}")
        return response_text

    def run(self, url=None, xpath=None, modify_result=False, process_url=False, keep_html=False):
        if process_url:
            self.process_url()

        url = url or self.url
        xpath = xpath or self.xpath
            
        response_text = self.download_content(url=url, main_xpath=xpath)

        if modify_result:
            html_tree = fromstring(response_text)
            main_tags = html_tree.xpath(xpath)

            if keep_html:
                result = map(lambda x: etree.tostring(x, pretty_print=True), main_tags())
            else:
                result = map(lambda x: x.text_content(), main_tags)
            response_text = "\n".join(result)
        response_text = sanitize(response_text)
        return response_text