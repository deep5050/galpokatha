import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import unquote
from time import sleep


DOMAIN = "https://https://www.ebanglalibrary.com"

HEADERS =  {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

current_path = "bibhutibhushan-bandopadhyay"

## manual entry if not found  ######################        
story_author = "বিভূতিভূষণ বন্দ্যোপাধ্যায়"
####################################################

def fetch_novel_sections_url(story_url):
    # Send the request with the user agent header
    response = requests.get(story_url, headers=HEADERS)
    # Parse the HTML with Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')

    story_title = soup.find('h1',{'class':'page-header-title'}).text
    try:
        story_author_div = soup.find('div',{'class':'page-header-description'})
        story_author = story_author_div.find('p').text
        story_author = story_author.split(' – ')[1]
    except:
        pass

 
    story_author_dir = story_author.strip().replace(" ","-")
    story_title_dir = story_title.strip().replace(" ","-")

    print(f"Creating story: {story_title} : {story_author}")

    if not os.path.exists(story_author_dir):
        os.mkdir(story_author_dir)
    
    story_path = os.path.join(story_author_dir,story_title_dir)

    if not os.path.exists(story_path):
        os.mkdir(story_path)

    story_sections = soup.find_all('h2',{'class': 'entry-title entry-title-archive'})
    i = 1
    for story in story_sections:
        story_head = story.text
        story_url = story.find('a',{'class':'entry-title-link'})['href']
        print(f"Downloading section {i} ...")
        fetch_story_sections(story_url, story_path, i)
        i += 1
        sleep(2)
    print("Completed !!")
    # write complete story

    # # Name of output file to which all files will be appended
    # output_file = f"{story_title_dir}.md"

    # # Open output file for writing
    # with open(output_file, "w") as outfile:
    #     # Loop through files in directory
    #     for filename in os.listdir(story_path):
    #         # Skip directories
    #         if os.path.isdir(filename):
    #             continue
    #         with open(os.path.join(story_path, filename), "r") as infile:
    #             outfile.write(infile.read())


def fetch_story_sections(section_url,out_path,section_no):
    # create small markdown files under the path 
    # Send the request with the user agent header
    response = requests.get(section_url, headers=HEADERS)
    # Parse the HTML with Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')
    story_div = soup.find('div',{'class':'entry-content entry-content-single'})
    story_lines = story_div.find_all('p')

    # make file
    story_text = ""
    for story_line in story_lines:
        temp_text = story_line.text
        temp_text = temp_text.strip()
        if temp_text == ".":
            continue
        story_text += f"{temp_text}\n\n"
    
    out_file = os.path.join(out_path,str(section_no))
    with open(out_file,'w') as f:
        f.write(story_text)
    

url = ""
with open('url','r') as f:
    url = f.read()

fetch_story_sections_url(url)
