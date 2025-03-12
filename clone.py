import wget
import os
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import sys
import re
import shutil

def download_website(url, output_dir=None):
    # Set default output directory to ~/website_clone
    if output_dir is None:
        output_dir = os.path.expanduser("~/website_clone")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create subdirectories for different asset types
    css_dir = os.path.join(output_dir, "css")
    js_dir = os.path.join(output_dir, "js")
    img_dir = os.path.join(output_dir, "images")
    
    for directory in [css_dir, js_dir, img_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    try:
        # Download the main page
        print(f"Downloading main page: {url}")
        print(f"Saving to: {output_dir}")
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the page to find assets
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Fix relative URLs in the HTML
        for tag in soup.find_all(['a', 'link', 'script', 'img']):
            if tag.has_attr('href'):
                if tag['href'].startswith('/'):
                    tag['href'] = urljoin(url, tag['href'])
            if tag.has_attr('src'):
                if tag['src'].startswith('/'):
                    tag['src'] = urljoin(url, tag['src'])
        
        # Download CSS files
        print("\nDownloading CSS files...")
        for css in soup.find_all("link", rel="stylesheet"):
            if css.get("href"):
                css_url = urljoin(url, css["href"])
                css_filename = os.path.basename(urlparse(css_url).path)
                if not css_filename:
                    css_filename = f"style_{len(os.listdir(css_dir))}.css"
                
                css_path = os.path.join(css_dir, css_filename)
                try:
                    print(f"Downloading: {css_url}")
                    wget.download(css_url, css_path)
                    print()  # New line after wget progress bar
                    
                    # Update the href in the HTML to point to local file
                    css['href'] = f"css/{css_filename}"
                except Exception as e:
                    print(f"Failed to download: {css_url}, Error: {e}")
        
        # Download JavaScript files
        print("\nDownloading JavaScript files...")
        for script in soup.find_all("script", src=True):
            if script.get("src"):
                js_url = urljoin(url, script["src"])
                js_filename = os.path.basename(urlparse(js_url).path)
                if not js_filename:
                    js_filename = f"script_{len(os.listdir(js_dir))}.js"
                
                js_path = os.path.join(js_dir, js_filename)
                try:
                    print(f"Downloading: {js_url}")
                    wget.download(js_url, js_path)
                    print()  # New line after wget progress bar
                    
                    # Update the src in the HTML to point to local file
                    script['src'] = f"js/{js_filename}"
                except Exception as e:
                    print(f"Failed to download: {js_url}, Error: {e}")
        
        # Download images
        print("\nDownloading images...")
        for img in soup.find_all("img"):
            if img.get("src"):
                img_url = urljoin(url, img["src"])
                img_filename = os.path.basename(urlparse(img_url).path)
                if not img_filename:
                    img_filename = f"image_{len(os.listdir(img_dir))}.jpg"
                
                img_path = os.path.join(img_dir, img_filename)
                try:
                    print(f"Downloading: {img_url}")
                    wget.download(img_url, img_path)
                    print()  # New line after wget progress bar
                    
                    # Update the src in the HTML to point to local file
                    img['src'] = f"images/{img_filename}"
                except Exception as e:
                    print(f"Failed to download: {img_url}, Error: {e}")
        
        # Download background images from CSS (if any)
        print("\nLooking for background images in CSS...")
        for css in soup.find_all("link", rel="stylesheet"):
            if css.get("href") and css["href"].startswith("css/"):
                css_path = os.path.join(output_dir, css["href"])
                if os.path.exists(css_path):
                    try:
                        with open(css_path, 'r', encoding='utf-8') as f:
                            css_content = f.read()
                            
                        # Find all URLs in the CSS
                        url_pattern = r'url\([\'"]?(.*?)[\'"]?\)'
                        bg_urls = re.findall(url_pattern, css_content)
                        
                        for bg_url in bg_urls:
                            if bg_url and not bg_url.startswith('data:'):
                                full_bg_url = urljoin(url, bg_url)
                                bg_filename = os.path.basename(urlparse(full_bg_url).path)
                                if not bg_filename:
                                    bg_filename = f"bg_{len(os.listdir(img_dir))}.jpg"
                                
                                bg_path = os.path.join(img_dir, bg_filename)
                                try:
                                    print(f"Downloading background image: {full_bg_url}")
                                    wget.download(full_bg_url, bg_path)
                                    print()
                                    
                                    # Update the URL in the CSS to point to local file
                                    css_content = css_content.replace(bg_url, f"../images/{bg_filename}")
                                except Exception as e:
                                    print(f"Failed to download background image: {full_bg_url}, Error: {e}")
                        
                        # Write the updated CSS back to the file
                        with open(css_path, 'w', encoding='utf-8') as f:
                            f.write(css_content)
                    except Exception as e:
                        print(f"Error processing CSS file: {css_path}, Error: {e}")
        
        # Save the modified HTML
        with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(str(soup))
        
        print("\nWebsite cloning completed!")
        print(f"To view the website, open {os.path.join(output_dir, 'index.html')} in your browser")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

# URL to clone
url = "https://www.anyone.events/"

# Start the download
download_website(url)