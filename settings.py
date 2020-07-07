import os

UPLOAD_DIRECTORY = 'store'


try:
    os.makedirs(UPLOAD_DIRECTORY)
except FileExistsError:
    pass
