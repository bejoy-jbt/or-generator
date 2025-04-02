from flask import Flask, request, send_file, render_template
import qrcode
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.form.get("url")
    color = request.form.get("color", "black")  # Default: black
    bg_color = request.form.get("bg_color", "white")  # Default: white
    size = int(request.form.get("size", 10))  # Default: 10
    border = int(request.form.get("border", 2))  # Default: 4

    if not data:
        return "No URL provided", 400
    
    # Create QR code with custom settings
    qr = qrcode.QRCode(
        version=1,  # Version (size)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=size,  # Size of each box
        border=border  # Border thickness
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create QR image with custom colors
    img = qr.make_image(fill_color=color, back_color=bg_color)

    # Save QR code in memory
    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run()
