from PIL import Image
import numpy as np
from k_means_constrained import KMeansConstrained
from sklearn.cluster import KMeans
import base64
from io import BytesIO

class ColorPalette:
  """Color Palette Object"""
  def __init__(self):
    self.get_color_is_success = False

  def load_image_as_numpy(self, image_path, resize=True, size=(150, 150)):
    """
    Loads an image and converts it to a NumPy array.
    image_path(str): path of the image to laod
    """
    img = Image.open(image_path)
    if resize:
      img = img.resize(size)  # resize to speed up clustering

    img_array = np.array(img)
    return img_array
  
  def get_color_palette(self, img_array, num_colors=10, sample_size=10000):
    """
    Extracts a color palette from an image using KMeans clustering.
    img_array(array): Numpy array variable
    num_colors(int): Number of most colors to be retrieved
    """
    # Reshape the image array to a list of pixels (R, G, B)
    pixels = img_array.reshape(-1, 3)

    # Randomly sample pixels if too many
    if len(pixels) > sample_size:
        idx = np.random.choice(len(pixels), sample_size, replace=False)
        pixels = pixels[idx]

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=num_colors, random_state=0, n_init=10)
    kmeans.fit(pixels)

    # The cluster centers are the prominent colors
    palette = kmeans.cluster_centers_.astype(int)
    self.get_color_is_success = True # set get_color_is_success true in object
    return palette
  
  def get_base64_image(self, image_path):
    """
    Returns base64 encoded of an image
    image_path(str): Path of the image to be encoded
    """
    with Image.open(image_path) as img:
        buffer = BytesIO()
        img.save(buffer, format="PNG")  # or JPG depending on your needs
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"