import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from PIL import Image, ImageDraw, ImageFont
import os

# Specify the list of URLs
url_list = [
    "https://distedavim.com/m/klinikler/hedef-doganevler.frm.000288.tr",
    "https://distedavim.com/m/klinikler/yeni-atalar.frm.000327.tr",
    # "https://distedavim.com/m/klinikler/as-marmara.frm.000295.tr",
    # "https://distedavim.com/m/klinikler/vien.frm.000325.tr",
    # "https://distedavim.com/m/klinikler/dentistart.frm.000329.tr",
    # "https://distedavim.com/m/klinikler/billur-bahcevan.frm.000326.tr"
]

titles = []
subtitles = []

# Configure Chrome options and enable DevTools
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (without opening a browser window)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Specify the path to ChromeDriver executable
chromedriver_path = "C:/Users/hadi/Downloads/chromedriver_win322/chromedriver.exe"

# Instantiate ChromeDriver with DevTools
chrome_service = Service(chromedriver_path)
chrome_service.command_line_args()
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Enable DevTools
driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
    "deviceScaleFactor": 1,
    "mobile": True,
    "width": 375,
    "height": 745
})

def takeScreenshot() :
    id = 0

    # Visit each URL and take a screenshot
    for url in url_list:
        id += 1
        driver.get(url)
        time.sleep(2)  # Wait for 2 seconds for the page to load
         # Extract the title and subtitle elements
        title_element = driver.find_element(By.CSS_SELECTOR, "[class*='itemPageHeader_title__']")
        subtitle_element = driver.find_element(By.CSS_SELECTOR, "[class*='itemPageHeader_subtitle__']")
        
        # Append the text values to the respective lists
        titles.append(title_element.text)
        subtitles.append(subtitle_element.text)
        
        screenshot_data = driver.execute_cdp_cmd("Page.captureScreenshot", {})

        # Convert and save the screenshot
        screenshot_bytes = base64.b64decode(screenshot_data["data"])
        screenshot_path = f"./screenshots/{id}.png"
        with open(screenshot_path, "wb") as f:
            f.write(screenshot_bytes)
        
        print(f"Screenshot saved: {screenshot_path}")


takeScreenshot()

def mergeImage() :
    directory = "screenshots"

    # Template image path
    template_path = "./template/template.png"

    # Open the template image
    template_image = Image.open(template_path)

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        # Check if the file is an image
        if filename.endswith(".png"):
            # Image path
            image_path = os.path.join(directory, filename) 
            # Open the image
            image = Image.open(image_path)
            # Resize the image to fit within the template
            resized_image = image.resize((500, 1000))
            # Create a new image with the same mode as the template
            new_image = Image.new(template_image.mode, template_image.size)
            # Paste the template image on top of the new image
            new_image.paste(template_image, (0, 0), template_image)
            # Paste the resized image onto the new image
            new_image.paste(resized_image, (292, 604))
            # Save the modified image with a new filename
            output_path = os.path.join("./merges", filename)
            new_image.save(output_path)

mergeImage()


def addText() :
    
    # Directory containing the images
    directory = './merges'

    index = 0

    # Get a list of all files in the directory
    file_list = os.listdir(directory)

    # Iterate over each file in the directory
    for filename in file_list:
        # Check if the file is a regular file
        if os.path.isfile(os.path.join(directory, filename)):
            # Open the image
            image = Image.open(os.path.join(directory, filename))

            # Create a drawing object
            draw = ImageDraw.Draw(image)

           # Define the main text and font properties
            main_text = titles[index]
            main_font_path = "./gilmer/gilmer-bold.otf"
            main_font_size = 1
            main_font = ImageFont.truetype(main_font_path, main_font_size)

            # Define the subtext and font properties
            sub_text = subtitles[index]
            sub_font_path = "./gilmer/gilmer-regular.otf"
            sub_font_size = 1
            sub_font = ImageFont.truetype(sub_font_path, sub_font_size)

            if index < len(titles) - 1 :
                index += 1

            # Get the dimensions of the image
            image_width, image_height = image.size

              # Calculate the maximum width for the text
            max_text_width = int(image_width * 0.7)

            # Find the appropriate main font size that fits the main text within the maximum width
            while main_font.getsize(main_text)[0] < max_text_width:
                main_font_size += 1
                main_font = ImageFont.truetype(main_font_path, main_font_size)

            # Find the appropriate sub font size that fits the subtext within the maximum width
            while sub_font.getsize(sub_text)[0] < max_text_width:
                sub_font_size += 1
                sub_font = ImageFont.truetype(sub_font_path, sub_font_size)

            # Calculate the position to center the main text horizontally
            main_text_width, main_text_height = draw.textsize(main_text, font=main_font)
            main_text_x = (image_width - main_text_width) // 2

            # Define the position where the main text will be placed
            main_text_position = (main_text_x, 75)

            # Define the color of the main text (optional)
            main_text_color = (255, 255, 255)  # white color

            # Add the main text to the image
            draw.text(main_text_position, main_text, font=main_font, fill=main_text_color)

            # Calculate the position to center the subtext horizontally
            sub_text_width, sub_text_height = draw.textsize(sub_text, font=sub_font)
            sub_text_x = (image_width - sub_text_width) // 2

            # Calculate the position to place the subtext below the main text
            sub_text_y = main_text_position[1] + main_text_height + 10

            # Define the position where the subtext will be placed
            sub_text_position = (sub_text_x, sub_text_y)

            # Define the color of the subtext (optional)
            sub_text_color = (255, 255, 255)  # white color

            # Add the subtext to the image
            draw.text(sub_text_position, sub_text, font=sub_font, fill=sub_text_color)

            # Save the modified image
            image.save(os.path.join("./withtext", filename))

addText()

print("Titles:", titles)
print("Subtitles:", subtitles)

# Quit the browser
driver.quit()
