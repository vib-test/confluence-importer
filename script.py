from bs4 import BeautifulSoup
import os

def process_html_file(html_file):
    print('Processing file', html_file)
    # Load HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse HTML using Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove all content outside of the div with id "main-content"
    main_content_div = soup.find(id='main-content')

    # Remove query parameters from image URLs
    for img in main_content_div.find_all('img'):
        img['src'] = img['src'].split('?')[0]
    
    # Convert links to html pages to md
    for link in main_content_div.find_all('a'):
        #print('link thyoe', type(link))
        if link.has_attr('href'):
            if link.has_attr('class') and link['class'] == 'external-link':
                continue
            else:
                if '/wiki/spaces/ISMS/pages' in link['href']:
                        new_href = link['href'].split('/wiki/spaces/ISMS/pages/', 1)[1]
                        split_href = new_href.split('/')
                        if len(split_href) > 1:
                            new_href = split_href[1].replace('+', '-')+ '_' + split_href[0] + '.md'
                            link['href']= new_href
                        else:
                            new_href=split_href[0]+'.md'
                            link['href']=new_href
                else:
                    link['href'] = link['href'].replace('.html', '.md')
            link['href'] = link['href'].replace('%2C', '%252C')
        else:
            print('link without href',link)
            

    # Convert image tags to <figure> tags
    for img in main_content_div.find_all('img'):
        print('img', type(img))
        img.wrap(soup.new_tag('figure'))

    # Change file extension to .md
    md_file = os.path.splitext(html_file)[0] + '.md'

    # Remove empty lines
    html_content = '\n'.join(line for line in str(main_content_div).splitlines() if line.strip())

    # Write modified content to .md file
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

# List all HTML files in the current directory
html_files = [file for file in os.listdir() if file.endswith('.html')]

# Process each HTML file
for html_file in html_files:
    process_html_file(html_file)

def replace_html_with_md(file_path):
    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace '.html' with '.md'
    content = content.replace('.html', '.md')

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

summary_file = 'SUMMARY.md'
replace_html_with_md(summary_file)
