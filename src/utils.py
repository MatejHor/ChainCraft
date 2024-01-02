import yaml
import re

def load_yaml(path, mode='rb'):
    with open(path, mode) as file:
        return yaml.safe_load(file)
    

def sanitize(string):
    sanitized = re.sub(r' |[\t]*', '', string)
    sanitized = re.sub(r'[\n]+', '\n', sanitized)
    return sanitized