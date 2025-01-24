from flask import Flask, session
from controllers import inventory_controller

def create_app():
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Ganti dengan secret key yang lebih aman

    # Register blueprints
    app.register_blueprint(inventory_controller)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
