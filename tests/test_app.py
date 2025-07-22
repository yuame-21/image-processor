import io
import pytest
from app import app, calc_avg_intensity
from PIL import Image

# Create test images
@pytest.fixture
def black_img():
    return Image.new('RGB', (10, 10), (0, 0, 0))

@pytest.fixture
def white_img():
    return Image.new('RGB', (10, 10), (255, 255, 255)) 

@pytest.fixture
def gray_img():
    return Image.new('RGB', (10, 10), (128, 128, 128))

# Create test client for the Flask app
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Helper function to create a test image - different that previous fixtures as it saves as a file
def create_test_image(color, size=(10, 10)):
    img = Image.new('RGB', size, color)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

def test_calc_avg_intensity_black(black_img):
    image = black_img
    intensity = calc_avg_intensity(image)
    assert intensity == 0.0

def test_calc_avg_intensity_white(white_img):
    image = white_img
    intensity = calc_avg_intensity(image)
    assert intensity == 255.0

def test_calc_avg_intensity_gray(gray_img):
    image = gray_img
    intensity = calc_avg_intensity(image)
    assert intensity == 128.0

def test_root_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, World!" in response.data

def test_calculate_intensity_endpoint(client):
    # Create a test image
    test_image = create_test_image((100, 150, 200))
    
    # Send POST request
    response = client.post('/calculate-intensity', 
                          data={'image': (test_image, 'test.png')},
                          content_type='multipart/form-data')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'avg_intensity' in data
    assert isinstance(data['avg_intensity'], float)
    assert 140 < data['avg_intensity'] < 160

def test_no_image_provided(client):
    response = client.post('/calculate-intensity')
    # Bad request if no image is provided
    assert response.status_code == 400

def test_calculate_intensity_edge_cases():
    # Single pixel image
    single_pixel = Image.new('RGB', (1, 1), (100, 100, 100))
    intensity = calc_avg_intensity(single_pixel)
    assert intensity == 100.0
    
    # Large uniform image
    large_img = Image.new('RGB', (100, 100), (50, 50, 50))
    intensity = calc_avg_intensity(large_img)
    assert intensity == 50.0