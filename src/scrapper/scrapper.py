import requests
import re
import os
import logging

from lxml.html import fromstring
from lxml import etree

from src.chaincraft.utils import load_yaml, sanitize
from ChainCraft.src.chaincraft.module import Module


class Scrapper(Module):
    def __init__(self, url=None, main_xpath="//main", domain_path=None, **kwargs):
        self.url = url
        self.xpath = main_xpath
        self.top_lvl_domain = None
        super().__init__()

    def setup(self, path="domains.yaml"):
        path = os.path.join("configs", path)
        config = load_yaml(path)
        return config.get("top-lvl-domain", [])

    def _setup_url(self, url):
        if not self.top_lvl_domain:
            self.setup()
        domain_match = re.search(r"\.[a-z]+$", url)
        if domain_match:
            return

        schema_match = [] if "http" in url else ["https://", "http://"]

        for domain in self.top_lvl_domain:
            for schema in schema_match:
                url = schema + url + domain
                try:
                    response = requests.get(url)

                    return url
                except requests.exceptions.MissingSchema as e:
                    continue
                except Exception as e:
                    logging.error(f"Find an error {e}")
                    raise e

    def _download_url(self, url, main_xpath):
        self.url = url
        self.xpath = main_xpath

        if not self.url:
            return ""

        response = requests.get(self.url)
        response_text = response.text
        return response_text
    
    def _sanitize_url(self, response_text, xpath, keep_html):
        html_tree = fromstring(response_text)
        main_tags = html_tree.xpath(xpath)

        if keep_html:
            result = map(lambda x: etree.tostring(x, pretty_print=True), main_tags())
        else:
            result = map(lambda x: x.text_content(), main_tags)
        response_text = "\n".join(result)
        response_text = sanitize(response_text)
        return response_text

    def process(self, url=None, xpath=None, modify_result=False, process_url=False, keep_html=False):
        url = url or self.url
        xpath = xpath or self.xpath
            
        if process_url:
            logging.info(f"Starting searching for correct domain")
            url = self._setup_url(url)
            logging.info(f"Find url {url}")

        response_text = self._download_url(url=url, main_xpath=xpath)

        if modify_result:
            logging.info(f"Extracting only specific xpath {xpath} and keeping html {str(keep_html)}")
            response_text = self._sanitize_url(response_text, xpath, keep_html)
        
        logging.info(f"Returning content with length {len(response_text)}")
        return response_text