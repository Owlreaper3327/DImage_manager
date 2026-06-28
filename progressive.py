"""This secondary string will perform a variant conversion for the main.py 
Allowing the progressive conversion, to save memory and give a propper feedback"""

#Here we'll make the imports
import main as pdf_utils
import os
import img2pdf


#Here we'll define functions

def convert_pdf_progressive(path_to, final_name, imgs):
    """This function will convert the imgs into pdf one to one, to give a propper feedback
    of conversion progress"""

    name_f = final_name + ".pdf"

    path = os.path.join(path_to, name_f)

    cont = 0
    total = len(imgs)

    with open(path, "ab") as final_pdf:

        for img in imgs:

            per = (cont/total) * 100
            print(f"Current conversion progress {per:.2f}%")

            new_img = img
            if img.endswith("webp"):
                name = img.split("/")[-1]
                name = name.split(".")[0]
                new_img = pdf_utils.convert_webp(img, name)

            final_pdf.write(img2pdf.convert(new_img))
            pdf_utils.clean()
            cont += 1

    return