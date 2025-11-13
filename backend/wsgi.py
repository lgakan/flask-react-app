from .main import app

if __name__ == "__main__":
    # This allows running with `python wsgi.py` for local testing if needed
    app.run()