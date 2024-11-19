from app.app import create_app

app = create_app()

# Executar o aplicativo
if __name__ == '__main__':
    app.run(debug=True)