import os
import errno
import shutil
from PIL import Image
from PIL.ExifTags import TAGS

class Photorganizer:
	def __init__(self, root, dest):
	    if dest[-1] == '/':
	        dest = dest[:-1]
	    rootdir = root
	    filelist = []
	    for root, dirs, files in os.walk(rootdir):
	        for filename in files:
		    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.JPG') or filename.endswith('.jpeg'):
		        filePath = os.path.join(root, filename)
		        filelist.append(filePath)
	    for image in filelist:
	        self.organize_image(image, dest)
	    print str(len(filelist)) + " files organized"
	
	def check_params(self, exif, params):
	    validparam = ''
	    count = 0
	    for param in params:
		validparam = param
		if not exif.get(param):
		    count += 1
		    if count >= len(params):
		        return False
		else:
		    return validparam

	def create_change_dir(self, path):
	    try:
		os.makedirs(path)
		os.chdir(path)
	    except OSError as exception:
		if exception.errno != errno.EEXIST:
		    print "Something went wrong!"
		    raise
		else:
		    os.chdir(path)
	    return os.getcwd()

	def organize_image(self, src, dest):
	    cwd = os.getcwd()
	    img = Image.open(src)
	    exif_data = img._getexif()
	    exif = {}
	    try:
		    for tag, value in exif_data.items():
		        decoded = TAGS.get(tag, tag)
		        exif[decoded] = value
	    except AttributeError:
	    	return
	    params = ['DateTimeOriginal','DateTimeDigitized', 'DateTime']
	    validparam = self.check_params(exif, params)
	    if not validparam:
		    return
	    else:
		    date = exif[validparam].split(' ')[0].split(':')
		    currpath = dest
		    for dateparam in date:
		        currpath = self.create_change_dir(currpath + '/' + dateparam)
		    shutil.copy(src, currpath)
		    os.chdir(cwd)

