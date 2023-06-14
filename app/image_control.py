from PIL import Image
import shutil
import os

def copy_image(image_path):
    """
    Function used for making a copy of the selected image for plant.
    After the path to image is selected, if there is no image inside the 'images' folder 
    with the name as the selected image it will make a copy of the image inside the 'images' folder

    """
    #name.ext
    filename = os.path.basename(image_path)

    folder_path = os.path.dirname(image_path)
    folder_path = os.path.abspath(folder_path)

    images_folder_path = os.path.abspath("./images")

    #print(f"Path to folder of image: {folder_path}")
    #print(image_path)
    #print(f"Path to images folder: {images_folder_path}")


    # if the image is in the images folder then return OK and don't copy
    if folder_path == images_folder_path:
        return "OK"
        


    # if there is no image with the same name in images folder
    if filename not in os.listdir("./images/"):
        destination_path = r"./images/" + filename
        try:
            shutil.copy(image_path, destination_path)
            print("Image copied")
            return "OK"
    
        except Exception as e:
            print(e)
        else:
         pass
    else:
        #if there is an image with the same name, check if they are the same
        if open(image_path,"rb").read() == open(r"./images/"+filename,"rb").read():
            print("Images are same.")
            return "OK"
        
        else:
            #if they are not the same, add prefix "new" to the filename
            prefix = "new"

            #check if the new filename is still in the folder, add prefix if it is
            while filename in os.listdir("./images/"):
                filename = prefix + filename
                destination_path = r"./images/" + filename
            #print(destination_path)
            try:
                shutil.copy(image_path, destination_path)
                print("Image copied")

                #return destination path for use in filename
                print(destination_path)
                return destination_path
            except Exception as e:
                print(e)
            else:
                pass


def open_image(image_path):
    """
    Function used to return Image object to a button for displaying the image on the button
    @params
    image_path
    """
    try:
        image= Image.open(image_path)
        return image
    except Exception as e:
        print(e)
        # Returns default image if image_path raises an exception. Will break if default image is deleted from the /images/ folder
        image= Image.open("./images/default.jpg")
        return image
    else:
        pass