import os

from flask import Flask, render_template

from config import SECRET_KEY
from exceptions.database.db import initialize_database
from models.routes.employee_routes import employee_routes


def create_app():
	app = Flask(__name__)
	app.config["SECRET_KEY"] = SECRET_KEY
	initialize_database()
	app.register_blueprint(employee_routes)

	@app.get("/")
	def index():
		return render_template("index.html")

	return app


app = create_app()


if __name__ == "__main__":
	host = os.environ.get("HOST", "127.0.0.1")
	port = int(os.environ.get("PORT", "5000"))
	debug = os.environ.get("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}
	app.run(host=host, port=port, debug=debug)
