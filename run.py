from Apps.initApp import app

from Apps.validation.validationViews import validation


app.register_blueprint(validation)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
