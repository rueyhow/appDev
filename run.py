from __init__ import app , os , db

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    db.create_all()
    app.run(debug = True)