import os
import requests
import re
from lxml.html import fromstring
# Local imports
from src.llm import LLMmodel

# llm = LLMmodel()
# llm.set_paramteres(os.path.join('.', 'models', 'llama13b.gguf'))

url = "https://en.wikipedia.org/wiki/Niels_Bohr"
response = requests.get(url)
response.text

html_root = fromstring(response.text)
elements = html_root.xpath('//main') 
html_article = elements[0].text_content()


from lxml import etree
print(etree.tostring(elements[0], pretty_print=True))

# prompt = f"Summarize text \n`{html_cleared_article}`"

# print(f"[+] Prompt {len(prompt)} : \n{prompt}")
# result = llm.get_prompt(prompt)
# print(f"[+] Result: \n{result}")