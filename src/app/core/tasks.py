from app import app


@app.task
def test():
    print('This is a test!')
