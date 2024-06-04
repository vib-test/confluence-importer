from bs4 import BeautifulSoup
#from markdownify import markdownify as md
import os

#def transform_code(confluence_val):
#    return confluence_val
#    if confluence_val == 'js':
#        return 'javascript'
#    return confluence_val

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
        if link.has_attr('href'):
            if link.has_attr('class') and link['class'] == 'external-link':
                continue
            else:
                if '/wiki/spaces/nxcloud/pages' in link['href']:
                        new_href = link['href'].split('/wiki/spaces/nxcloud/pages/', 1)[1]
                        split_href = new_href.split('/')
                        if len(split_href) > 1:
                            new_href = split_href[1].replace('+', '-')+ '_' + split_href[0] + '.md'
                            link['href']= new_href
                        else:
                            new_href=split_href[0]+'.md'
                            link['href']=new_href
                else:
                    link['href'] = link['href'].replace('.html', '.md')
                index_of_hash = link['href'].rfind('#')
                if index_of_hash == -1:
                    continue
                else:
                    split_hash = [link['href'][:index_of_hash], link['href'][index_of_hash+1:]]
                    pre_hash = split_hash[0]
                    post_hash = split_hash[1]
                    replaced_post_hash = post_hash.replace("-(", "-").replace(")-", "-").replace("(", "-").replace(")", "-").replace("'", "").lower()
                    link['href']= pre_hash + "#" + replaced_post_hash
            link['href'] = link['href'].replace('%2C', '%252C')
        else:
            print('link without href',link)
            

    # Convert image tags to <figure> tags
    for img in main_content_div.find_all('img'):
        img.wrap(soup.new_tag('figure'))
    
    #attachments
    for link in main_content_div.find_all('a'):
        #print('link', link)
        if link.has_attr('class'):
            #print('class', link['class'])
            if link['class'][0] == 'confluence-embedded-file':
                src = link['href']
                #print('file neing addded')
                link.replace_with('{{% file src=\"{0}\" %}}'.format(src))
    
    #code blocks
    for code in main_content_div.find_all('pre'):
        if code.has_attr('class') and code.has_attr('data-syntaxhighlighter-params'):
            if code['class'][0] == 'syntaxhighlighter-pre':
                brush = code['data-syntaxhighlighter-params'].split(';')[0]
                value = brush[brush.index(':') + 2:]
                new_code_tag = soup.new_tag('code', **{'class':'lang-{0}'.format(value)})
                new_code_tag.string = code.text
                code.string.replace_with(new_code_tag)
    
    # Preserving Column widths approach 1. Didn't work
    
    #for colgroup in main_content_div.find_all('colgroup'):
    #    colgroup.wrap(soup.new_tag('thead'))
    #    colgroup.name='tr'
    
    #for col in main_content_div.find_all('col'):
    #    print('col', col)
    #    if col.has_attr('style'):
    #        width_str= col['style']
    #        width = int(float(width_str[len("width: "):-(len("px")+1)]))
    #        col['width']=str(width)
    #        del col['style']
    #    col.name = 'th'
    
    #width_arr = []
                
    #Preserving column widths approach 2. Also didn't work

    #for col in main_content_div.find_all('col'):
    #    if col.has_attr('style'):
    #        width_str= col['style']
    #        width = int(float(width_str[len("width: "):-(len("px")+1)]))
    #        print("width", width)
    #        width_arr.append(width)
    #index = 0
    #for th in main_content_div.find_all('th'):
    #    if index > len(width_arr) -1 :
    #        break
    #    th['width']= str(width_arr[index])
    #    del th['class']
    #    index+=1
    

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
    #content = md(content)

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

summary_file = 'SUMMARY.md'
replace_html_with_md(summary_file)

