import os
import re
from bs4 import BeautifulSoup
import base64

# Configuration
WEBSITE_DIR = os.path.expanduser("~/website_clone")
HTML_FILE = os.path.join(WEBSITE_DIR, "index.html")
IMG_DIR = os.path.join(WEBSITE_DIR, "images")

# Base64 encoded small placeholder image (1x1 pixel transparent PNG)
PLACEHOLDER_IMAGE_BASE64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

def create_placeholder_svg(width, height, text):
    """Create an SVG placeholder with text"""
    svg = f'''
    <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#f0f0f0"/>
        <text x="50%" y="50%" font-family="Arial" font-size="14" text-anchor="middle" dominant-baseline="middle" fill="#888">
            {text}
        </text>
    </svg>
    '''
    return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode('utf-8')).decode('utf-8')}"

def fix_missing_images():
    if not os.path.exists(HTML_FILE):
        print(f"Error: HTML file not found at {HTML_FILE}")
        print("Please run clone.py first to create the website clone.")
        return
    
    print(f"Fixing missing images in {HTML_FILE}...")
    
    # Read the HTML file
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Fix image tags
    img_count = 0
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src.startswith('images/'):
            img_path = os.path.join(WEBSITE_DIR, src)
            if not os.path.exists(img_path) or os.path.getsize(img_path) == 0:
                # Get image dimensions
                width = img.get('width', '300')
                height = img.get('height', '200')
                alt_text = img.get('alt', 'Image')
                
                # Create placeholder
                placeholder = create_placeholder_svg(width, height, alt_text or "Image")
                img['src'] = placeholder
                img['data-original-src'] = src
                img_count += 1
    
    # Fix CSS background images
    css_dir = os.path.join(WEBSITE_DIR, "css")
    if os.path.exists(css_dir):
        for css_file in os.listdir(css_dir):
            if css_file.endswith('.css'):
                css_path = os.path.join(css_dir, css_file)
                try:
                    with open(css_path, 'r', encoding='utf-8') as f:
                        css_content = f.read()
                    
                    # Find background-image URLs
                    url_pattern = r'background-image:\s*url\([\'"]?(\.\.\/images\/[^\'"]+)[\'"]?\)'
                    matches = re.findall(url_pattern, css_content)
                    
                    for match in matches:
                        img_path = os.path.join(WEBSITE_DIR, match.replace('../', ''))
                        if not os.path.exists(img_path) or os.path.getsize(img_path) == 0:
                            # Replace with placeholder
                            css_content = css_content.replace(
                                f"background-image: url({match})", 
                                f"background-image: url({PLACEHOLDER_IMAGE_BASE64})"
                            )
                    
                    # Write updated CSS
                    with open(css_path, 'w', encoding='utf-8') as f:
                        f.write(css_content)
                        
                except Exception as e:
                    print(f"Error processing CSS file {css_path}: {e}")
    
    # Write the updated HTML
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Fixed {img_count} missing images with placeholders.")
    print("Website is now ready to be viewed locally.")

if __name__ == "__main__":
    fix_missing_images() 