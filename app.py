from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from dotenv import load_dotenv
from models import db
from controllers import ingredient_blueprint
from controllers.recipe_controller import recipe_controller

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
db.init_app(app)

app.register_blueprint(ingredient_blueprint, url_prefix="/ingredients")
app.register_blueprint(recipe_controller, url_prefix='/recipes')

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def home():
    return "Hello, World! From COGNIFYQ"


if __name__ == "__main__":
    app.run(debug=True)
