# Website Cloner and Local Server

This project contains scripts to clone a website and run it locally on your computer.

## Scripts

1. **clone.py** - Downloads a website and its assets
2. **fix_missing_images.py** - Replaces missing images with placeholders
3. **serve.py** - Runs a local web server to view the cloned website

## How to Use

### Step 1: Clone the Website

Run the following command to clone the website:

```bash
python3 clone.py
```

This will create a `website_clone` directory in your home folder (`~/website_clone`) with the downloaded website files.

### Step 2: Fix Missing Images

Some images might be protected and can't be downloaded. Run this script to replace them with placeholders:

```bash
python3 fix_missing_images.py
```

### Step 3: Run the Local Server

Start the local web server to view the website:

```bash
python3 serve.py
```

This will automatically open your default web browser to http://localhost:8000/ where you can view the cloned website.

Press Ctrl+C in the terminal to stop the server when you're done.

## Customizing

To clone a different website, edit the URL in `clone.py`:

```python
# URL to clone
url = "https://your-website-url.com/"
```

Then run the scripts again following the steps above.

## File Locations

- The cloned website is saved to: `~/website_clone`
- All scripts are located in the "Website II" folder

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - wget
  - requests
  - beautifulsoup4

You can install these packages with:

```bash
pip install wget requests beautifulsoup4
```

## Notes

- Some websites have protection against scraping/cloning
- JavaScript functionality might be limited in the cloned version
- This is for educational purposes only 
