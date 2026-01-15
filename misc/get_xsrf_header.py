from bs4 import BeautifulSoup

file_path = 'misc/page_source.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# collecting the xsrf token header from the page source:
soup = BeautifulSoup(html_content, 'html.parser')
hidden_input_value = soup.find('input', {'name': '__XSRF-TOKEN'})['value']
print("XSRF Token Value:", hidden_input_value)
