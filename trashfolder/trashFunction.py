# from bs4 import BeautifulSoup
# from lxml import etree

# # Example HTML content
# html_content = '''
# <div>
#     <p>Hello, <strong>World!</strong></p>
#     <p>This is an example</p>
# </div>
# '''

# # Create a BeautifulSoup object
# soup = BeautifulSoup(html_content, 'html.parser')

# # Convert BeautifulSoup object to an lxml object
# soup_lxml = etree.HTML(str(soup))

# # Define the XPath expression to find the <strong> tag
# xpath_expression = "/html/body/div[6]/section/div[3]/span[1]

# # Use lxml's xpath method to find elements based on XPath
# result = soup_lxml.xpath(xpath_expression)

# if result:
#     # Get the text of the first found element (if any)
#     element_text = result[0].text.strip()
#     print(element_text)  # Output: World!
# else:
#     print("Element not found")


from bs4 import BeautifulSoup

# Example HTML content
html_content = '''
<div class="example" zone="Asia">
    <p class="content">Paragraph 1</p>
    <p class="content">Paragraph 2</p>
</div>
'''

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find the <div> element with class="example" and zone="Asia"
desired_element = soup.find('div', class_='example', zone='Asia')

# Print the found element
print(desired_element)



# publish time for investing
#     "publishedDateTime": {
#         "by": "xpath",
#         "id": "",
#         "tag": "",
#         "class": "",
#         "attributes": {},
#         "xpath": "/html/body/div[6]/section/div[3]/span[1]"
#     }


#publish time for asahi 
# ,
#     "publishedDateTime": {
#         "by": "body",
#         "id": "",
#         "tag": "p",
#         "class": "EnLastUpdated",
#         "attributes": {},
#         "xpath": ""
#     }