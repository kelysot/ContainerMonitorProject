
from database import app
from views.routes import initialize_app


if __name__ == '__main__':
    initialize_app()
    app.run(debug=True, use_reloader=False)


