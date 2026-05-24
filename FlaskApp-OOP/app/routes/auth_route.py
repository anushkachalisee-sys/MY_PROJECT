from flask import Blueprint
from app.controllers.auth_controller import AuthController
class AuthRoutes:
    def __init__(self):
        self.bp = Blueprint("auth", __name__)
        self.controller = AuthController()
    def register_routes(self):
        self.bp.route("/login", methods=["GET", "POST"])(self.controller.login)
        self.bp.route("/register", methods=["GET", "POST"])(self.controller.register)
        self.bp.route("/home", methods=["GET", "POST"])(self.controller.home)
        return self.bp