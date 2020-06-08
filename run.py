from app import app


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)  # Produção
    # app.run(host="192.168.0.6", port=5000, debug=True)  # Local
