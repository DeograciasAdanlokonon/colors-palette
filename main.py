from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from core_engin.image_upload.upload import UploadImage
from core_engin.color_palette import ColorPalette

app = Flask(__name__)
app.config['SECRET_KEY'] = 'djdhl:3qfjnjjKT84DJK'
Bootstrap5(app=app)

def core(image_path, num_colors):
  """
  Returns a data on ColorPalette of an image
  image_path(str): path of an image
  """
  palette = ColorPalette()

  img_array = palette.load_image_as_numpy(image_path=image_path)
  color_palette = palette.get_color_palette(img_array, num_colors)

  if palette.get_color_is_success:
    message = f"Most {num_colors} Colors palette successfully retrieve"
    status = "success"
    image_url = palette.get_base64_image(image_path)
    return color_palette, image_url, message, status
  else:
    status = "danger"
    message = f"No color palette or an error occured"
    return color_palette, image_url, message, status

#ToDo: Home Route - Index
@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    try:
      if 'file' not in request.files:
        return redirect(request.url) # no file choosen
      
      file = request.files['file']
      if file.filename == "":
        return redirect(request.url)
      
      if file and file.filename:
        upload = UploadImage()
        upload.upload_image(file=file) # upload file

        if upload.upload_success:
          data = core(image_path=upload.imagepath, num_colors=10)

          colors_palette = data[0].tolist() # colors_palette returned from core
          image_url = data[1] # url of the encoded image
          message = data[2] # message returned from core
          status = data[3] # status returned from core

          # delete the used image to free space
          upload.delete_file(upload.imagepath)

          flash(message, status)
          return render_template('index.html', image_url=image_url, colors=colors_palette)
        else:
          flash('There was an error during image uploading --- Please try again', 'warning')
      
    except Exception as e:
      flash(f'Something went wrong: {e}', 'danger')
  return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True)