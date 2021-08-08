import os

from flask import Flask




def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.logger.debug('app.instance_path = %s', app.instance_path)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE='MyBlog'

    )



    @app.route("/hello")
    def hello():
        return "Hello, World!"



    # apply the blueprints to the app
    from myblog import blog,user,api

    app.register_blueprint(blog.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(api.bp)

    app.add_url_rule("/", endpoint="home")

    return app
