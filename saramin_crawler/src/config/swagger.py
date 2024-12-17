from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/swagger_files",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}

apispec = APISpec(
    title="Job Notice API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[MarshmallowPlugin()],
)
