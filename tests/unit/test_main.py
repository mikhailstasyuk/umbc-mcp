from src.app.main import root

def test_root():
    response = root()
    assert response == {"message": "Hello, Kitty!"}
