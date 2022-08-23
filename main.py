from config import create_app
from db import db
from flask_swagger_ui import get_swaggerui_blueprint

app = create_app()

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
)

app.register_blueprint(swagger_blueprint)


@app.after_request
def return_response(resp):
    db.session.commit()
    return resp


if __name__ == "__main__":
    app.run()
