import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project import create_app

# Allow selecting config via environment variable APP_ENV or FLASK_ENV
env = os.environ.get('APP_ENV') or os.environ.get('FLASK_ENV')
app = create_app(config_name=env)

if __name__ == "__main__":
    # Use app.debug from config to control debug server
    app.run(debug=app.config.get('DEBUG', False))
