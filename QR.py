import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SolidFillColorMask, SquareGradiantColorMask
from io import BytesIO

def generate_styled_qr_code(data, style='Rounded', color_mask='Solid'):
    # Create a QR code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Select the style for the QR code
    if style == 'Rounded':
        module_drawer = RoundedModuleDrawer()
    elif style == 'Gapped':
        module_drawer = GappedSquareModuleDrawer()
    elif style == 'Circle':
        module_drawer = CircleModuleDrawer()
    else:
        module_drawer = None  # Default

    # Select the color mask for the QR code
    if color_mask == 'Radial':
        color_mask = RadialGradiantColorMask()
    elif color_mask == 'Square':
        color_mask = SquareGradiantColorMask()
    else:  # Default solid fill
        color_mask = SolidFillColorMask(back_color=(255, 255, 255), front_color=(0, 0, 0))

    # Create the QR code image with the specified style
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=module_drawer, color_mask=color_mask)

    # Convert the image to a format that can be displayed in Streamlit
    img_byte_array = BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()

    return img_byte_array

# Streamlit app
st.title("QR Code Generator")

# Input field for the data to encode in the QR code
data = st.text_input("Enter the data for the QR code:")

# Dropdown for style selection
style = st.selectbox("Choose a style for the QR code:", ('Rounded', 'Gapped', 'Circle'))

# Dropdown for color mask selection
color_mask = st.selectbox("Choose a color mask for the QR code:", ('Solid', 'Radial', 'Square'))

if st.button("Generate QR Code"):
    if data:
        # Generate the QR code
        qr_img = generate_styled_qr_code(data, style=style, color_mask=color_mask)
        
        # Display the generated QR code image
        st.image(qr_img, caption="Your QR Code")

        # Add a download button
        st.download_button(
            label="Download QR Code",
            data=qr_img,
            file_name="qrcode.png",
            mime="image/png"
        )
    else:
        st.error("Please enter data to generate the QR code.")
