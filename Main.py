import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
from pylibdmtx.pylibdmtx import decode
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
    img_file = st.file_uploader(label='Upload a file', type=['png', 'jpg'])
    realtime_update = st.checkbox(label="Update in Real Time", value=True)

    if img_file:
        img = Image.open(img_file)
        if not realtime_update:
            st.write("Double click to save crop")
        cropped_img = st_cropper(img, realtime_update=realtime_update, box_color="#10D604", aspect_ratio=(1, 1))
        
        _ = cropped_img.thumbnail((300,300))
        

        cropped_img = process_image(cropped_img)
        st.image(cropped_img)
        processed_img_pil = Image.fromarray(cropped_img)
        dmtx_object = decode(processed_img_pil)[0]
        serial_number = dmtx_object[0]
        st.write(serial_number)


if __name__ == "__main__":
    main()
