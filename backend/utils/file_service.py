#!/usr/bin/python3
"""module for file dealing utils"""
import base64
import os

home_directory = os.environ.get('HOME')
UPLOAD_DIR = f'{home_directory}/uploads/courses'
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'ico'}
    return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_folders_if_not_exists():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)


def save_image(image, course_id):
    if image and allowed_file(image.filename):
        create_folders_if_not_exists()
        image_filename = f"{course_id}.png"
        image_path = os.path.join(UPLOAD_DIR, image_filename)
        image.save(image_path)
        return image_path
    else:
        return None
    
    
def save_base64_image(base64_data, filename):
    try:
        decoded_data = base64.b64decode(base64_data)
        create_folders_if_not_exists()
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, 'wb') as file:
            file.write(decoded_data)

        return file_path
    except Exception as e:
        raise e
