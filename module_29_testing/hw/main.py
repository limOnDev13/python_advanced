from main import create_app, db_create_all


if __name__ == '__main__':
    app = create_app()
    db_create_all(app)
    app.run()
