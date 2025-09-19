import os
import tempfile

UPLOAD_FOLDER = 'static/uploads' # Folder to store uploaded files
ALLOWED_EXTENSIONS = ['jpg', 'png', 'gif', 'jpeg'] # Allowed images


class UploadImage:
  """Image uploading object"""
  def __init__(self):
    self.imagepath = ""
    self.upload_success = None

  def allowed_file(self, filename):
    return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
  def upload_image(self, file):
    """
    Uploads image and save it to static folder
    
    file(obj): The file object to be uploaded
    """
    if file and self.allowed_file(file.filename):
      # file_path = os.path.join(UPLOAD_FOLDER, file.filename)
      # file.save(file_path) # save file
      # self.imagepath = file_path # store path in object

      # Save to temp file
      with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
          file.save(tmp.name)
          self.imagepath = tmp.name

      self.upload_success = True
    else:
      self.upload_success = False
  
  def delete_file(self, filepath):
    """
    Delete a specified files

    filepath(str): The path of the file to be deleted
    """
    os.remove(path=filepath)