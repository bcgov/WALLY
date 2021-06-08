import os
import zipfile

ALLOWED_FILE_TYPES = ('.png', '.pdf', '.csv', '.txt')

def zipdir(path, filename):
    """
    Zips together all files in a directory
    """
    zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(ALLOWED_FILE_TYPES):
                zipf.write(os.path.join(root, file), 
                          os.path.relpath(os.path.join(root, file), 
                                          os.path.join(path, '..')))
    zipf.close()

