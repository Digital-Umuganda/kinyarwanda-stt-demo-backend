from sanic.websocket import WebSocketProtocol
from sanic_jwt import initialize
from prometheus_fastapi_instrumentator import Instrumentator
from app import create_app
from app.users.auth import authenticate, retrieve_user, extend_payload
from sanic_cors import CORS, cross_origin

app = create_app()
CORS(app)

initialize(app, url_prefix='/token', authenticate=authenticate, retrieve_user=retrieve_user,
           extend_payload=extend_payload)

if __name__ == "__main__":
    HOST, PORT, DEBUG = app.config['HOST'], app.config['PORT'], app.config['DEBUG']
    app.run(host=HOST, port=PORT, debug=DEBUG, protocol=WebSocketProtocol)
#Monitoring
Instrumentator().instrument(app).expose(app)
