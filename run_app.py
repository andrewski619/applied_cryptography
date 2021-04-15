from app import app

app.secret_key = "super secret key"
app.run(debug=True)
