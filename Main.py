import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
from pylibdmtx.pylibdmtx import decode
from streamlit_back_camera_input import back_camera_input
import cv2
import numpy as np

def increase_contrast(image, alpha):
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=2)
    return adjusted

def increase_brightness(image, beta):
    adjusted = cv2.convertScaleAbs(image, alpha=1.0, beta=beta)
    return adjusted

def deblur_image(image):
    gaussian = cv2.GaussianBlur(image, (9,9), 10.0)
    unsharp_image = cv2.addWeighted(image, 1.5, gaussian, -0.5, 0, image)
    return unsharp_image

def equalize_histogram(image):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_image = cv2.equalizeHist(image_gray)
    return equalized_image

def process_image(image):
    np_image = np.array(image)
    np_image = increase_brightness(np_image, 1.3)
    np_image = increase_contrast(np_image, 1.75)
    # np_image = equalize_histogram(np_image)
    return np_image

def extract_qr_code_area(image):
    qr_detector = cv2.QRCodeDetector()
    return 

def main():
    st.set_option('deprecation.showfileUploaderEncoding', False)

    image_source = st.radio("Bildaufnahme", ('Bildaufnahme über Kamera-App (Empfohlen)', 'Manuell über die Website Bild aufnehmen'))
    img = None

    if image_source=='Bildaufnahme über Kamera-App (Empfohlen)':
        img_file = st.file_uploader(label='Browse Files → Kamera (über Kamera-App) → Bild aufnehmen', type=['png', 'jpg'])
        if img_file:
            img = Image.open(img_file)
    else:
        st.caption("Rückkamera am Smartphone oder Webcam am Laptop")
        img = back_camera_input()
        if img:
            img = Image.open(img)
        st.info('Auf das Video klicken um Bild aufzunehmen')

    st.markdown("""---""")

    if img:
        cropped_img = st_cropper(img, realtime_update=True, box_color="#10D604", aspect_ratio=(1, 1))
        st.write("QR-Code Fokus")
        _ = cropped_img.thumbnail((150,150))
        cropped_img = process_image(cropped_img)
        st.image(cropped_img)

        processed_img_pil = Image.fromarray(cropped_img)
        dmtx_object = decode(processed_img_pil)
        print(dmtx_object)
        if dmtx_object:
            new_dmtx_object = dmtx_object[0]
            if new_dmtx_object:
                serial_number = dmtx_object[0]
                st.write(str(serial_number).split("'")[1])

if __name__ == "__main__":
    main()
