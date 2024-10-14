"""run"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    host = app.config.get('HOST', '127.0.0.1')
    port = app.config.get('PORT', 5000)
    app.run(host=host, port=port)
