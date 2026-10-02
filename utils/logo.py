import requests
import os

# List of image URLs
urls = [
    "https://cdn.prod.website-files.com/6741bb619f38c5e9b8a35659/6866b1454f8d49ff48b9f7e9_a0459f88c1fe61fa6c8ca72e27d911b0_Frame%202095585491.svg",
    "https://cdn.prod.website-files.com/6741bb619f38c5e9b8a35659/6866b14675dacb31eb368515_341437be66cba853bff50983862409c5_Raspberry%20Pi.svg",
    "https://cdn.prod.website-files.com/6741bb619f38c5e9b8a35659/6866b145e263cdcc3313d8d3_621eff59ce483cc6436babc4900375e2_Gazebo.svg",
    "https://cdn.prod.website-files.com/6741bb619f38c5e9b8a35659/6866b146609c09cf9be6af67_24e048a600e9d84590f304f406a145fa_ChatGPT%20Image%20Jul%202%2C%202025%2C%2005_51_28%20PM%201.svg",
    "https://cdn.prod.website-files.com/6741bb619f38c5e9b8a35659/6866b145ce4eb31b2acc86b4_0b6278719f9400e44307fdbda0faaf25_OpenCV.svg",
    "https://cdn.prod.website-files.com/6741bb619f38c5e9b8a35659/6866b145bed6dde96daf9a8d_50151f9f816cf772f35aa614291b2f2a_Frame%202095585493.svg",
    "https://cdn.prod.website-files.com/6741bb619f38c5e9b8a35659/6866b146dc0649578c225def_cc3a627ac9848a802dd97fe713850726_Corel%20I%20Draw.svg",
    "https://cdn.prod.website-files.com/6741bb619f38c5e9b8a35659/6866b14672e55902791489fd_75570877f1db594242bb56b9efa05ad5_Mask%20group.svg",
    "https://cdn.prod.website-files.com/6741bb619f38c5e9b8a35659/6866b145ce2388e9fd59f760_2f31c3a509ea909de3a5e60780d1f967_Python.svg",
    "https://cdn.prod.website-files.com/6741bb619f38c5e9b8a35659/6866b1464230eb2b5e6ec72c_b5b9b80602281df9ebf630da6ec6ce4f_simple-icons_cplusplus.svg"
]

# Folder to save images
os.makedirs("images", exist_ok=True)

# Download each image
for url in urls:
    filename = os.path.join("images", url.split("/")[-1].split("?")[0])
    print(f"Downloading {filename} ...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download {url}")

print("All downloads complete!")
