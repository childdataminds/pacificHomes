from bs4 import BeautifulSoup
import glob,json


def products_detail():
    # Get all HTML files in the directory
    html_files = glob.glob("templates/products_details/*.html")  # Adjust the path as needed
    data = {}
    for file in html_files:
        file_name = file.split("/")[-1].split(".")[0]
        data[file_name] = {}
        with open(file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Find the main div with class 'images-cover'
        images_cover = soup.find("div", class_="images-cover")
        
        if images_cover:
            # Find all sub-divs with class 'image-item static-item'
            image_items = images_cover.find_all("div", class_="image-item static-item")
            data[file_name]["images"] = []
            for item in image_items:
                # Get the <img> tag inside the sub-div
                img_tag = item.find("img")

                if img_tag and img_tag.has_attr("lazy"):
                    data[file_name]["images"].append(img_tag['lazy'].split("/")[-1])
        # Finding Name
        data[file_name]["name"] = soup.find("h1",class_="e_h1-14 s_subtitle").text
        
        # Finding Desc
        data[file_name]["desc"] = soup.find("div",class_="e_richText-29 s_title clearfix").text

        # Detail
        data[file_name]["detail"] = soup.find("div",class_="p_infoItem p_detail").find("p").text
        print(data[file_name]["detail"])
    with open("image_data.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

def product_catagory():
    # Get all HTML files in the directory
    html_files = glob.glob("templates/products_list/*.html")  # Adjust the path as needed
    data = {}
    for file in html_files:
        file_name = file.split("/")[-1].split(".")[0]
        data[file_name] = {}
        with open(file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Find the main div with class 'images-cover'
        images_cover = soup.find("div", class_="p_list")
        
        if images_cover:
            # Find all sub-divs with class 'image-item static-item'
            image_items = images_cover.find_all("div", class_="cbox-5 p_loopitem")
            data[file_name]["products"] = []
            for item in image_items:
                # Get the <img> tag inside the sub-div
                img_tag = item.find("a")

                if img_tag and img_tag.has_attr("href"):
                    data[file_name]["products"].append(img_tag['href'].split("/")[-1].split(".")[0])
        # Finding Name
        print("File: ",file_name)
        try:
            data[file_name]["name"] = soup.find("p",class_="e_text-4 s_title").text
            print(data[file_name]["name"])
        except:
            print("Failed")
        
        
  
    with open("catagory_data.json", "w", encoding="utf-8") as json_file:
       json.dump(data, json_file, indent=4)
product_catagory()
 
