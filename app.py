from flask import Flask, render_template, request, Markup
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        fg_color = request.form.get('fgcolor', '#000000')
        bg_color = request.form.get('bgcolor', '#ffffff')
        
        # Validate the URL
        if not url:
            return render_template('index.html', qr_image=None, error_message='Please enter a valid URL.')

        try:
            qr_size = int(request.form.get('qrsize', 200))  # Default QR code size is 200px
        except ValueError:
            return render_template('index.html', qr_image=None, error_message='Invalid QR code size.')

        qr_data_url, error_message = generate_qr_code(url, fg_color, bg_color, qr_size)

        if qr_data_url:
            return render_template('index.html', qr_image=Markup(qr_data_url), error_message=None)
        else:
            return render_template('index.html', qr_image=None, error_message=error_message)

    return render_template('index.html', qr_image=None, error_message=None)

def generate_qr_code(url, fg_color, bg_color, size):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        qr_img = qr.make_image(fill=fg_color, back_color=bg_color)

        # Resize the QR code image
        qr_img = qr_img.resize((size, size))

        qr_io = BytesIO()
        qr_img.save(qr_io, 'PNG')
        qr_io.seek(0)

        qr_data_url = "data:image/png;base64," + base64.b64encode(qr_io.read()).decode()

        return qr_data_url, None
    except Exception as e:
        return None, str(e)

# Existing generate_qr_code function...

if __name__ == '__main__':
    app.run(debug=True)

# Existing generate_qr_code function...


if __name__ == '__main__':
    app.run(debug=True)
