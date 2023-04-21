template = {
    "swagger": "2.0",
    "info": {
        "title": "Bookmarks API",
        "description": "API for Bookmarks. This API consists authentication and bookmarks all curd operations. Here we have GET,PUT,POST,DELETE Methods. you can create a user or login a existing user. This api is a secure api. This api requires access token which makes it more secure. Here are some commonly used operations are present. you can get the source code from the github repository. link of the github repository  https://github.com/Hemu21/bookmarks-api",
        "contact": {
            "email": "gujjalahemanthkumar789@gmail.com"
        },
        "version": "1.0",
        "license":{
          "name": "MIT License",
          "url": "https://mit-license.tiiny.site/"
        }
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "securityDefinitions": {
    "Bearer": {
      "type": "apiKey",
      "name": "Authorization",
      "in": "header",
      "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
    }
  },
  "security": [
    {
      "Bearer": [ ]
    }
  ]
    
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "api",
            "route": "/api/spec",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}