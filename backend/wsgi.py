from .main import app

if __name__ == "__main__":
    # This allows running the app with `python wsgi.py` for local testing if needed
    app.run()