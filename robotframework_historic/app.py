import importlib
import pkg_resources
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from robotframework_historic.utils import config
from robotframework_historic.args import parse_options

args = parse_options()
config.store('mysql_config', {
    "host": args.sqlhost,
    "username": args.username,
    "password": args.password,
    "auth_plugin": 'mysql_native_password'
})

app = FastAPI()
app.mount("/static", StaticFiles(directory=pkg_resources.resource_filename(__name__, 'templates')), name="templates")
# import all the routes
routes = importlib.import_module('robotframework_historic.routes')
app.include_router(routes.router)


def main():
    host_address = args.apphost if args.apphost else '127.0.0.1'
    uvicorn.run("robotframework_historic.app:app", host=host_address, port=5000, log_level="debug")
