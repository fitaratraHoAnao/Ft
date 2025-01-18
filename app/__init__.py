from flask import Flask

def startapp(restartbot):
  app = Flask(__name__)
  
  from .views import view
  from .api import api, ogag
  
  ogag(restartbot)
  app.register_blueprint(view)
  app.register_blueprint(api, url_prefix='/api')
  
  return app