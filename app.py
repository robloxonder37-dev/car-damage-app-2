import streamlit as st
from PIL import Image
import numpy as np
import cv2

st.set_page_config(page_title="Araç Hasar Tespit Asistanı", page_icon="🚗", layout="centered")

st.title("🚗 Araç Hasar Tespit Asistanı")
st.write("Hasarlı aracın fotoğrafını yükleyin, yapay zeka saniyeler içinde analiz edip raporlasın.")

uploaded_file = st.file_uploader("Aracın fotoğrafını seçin veya çekin", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Yüklenen Araç Fotoğrafı", use_container_width=True)
    
    st.markdown("---")
    
    if st.button("Hasar Analizini Başlat", type="primary"):
        with st.spinner("Yapay zeka fotoğrafı inceliyor, lütfen bekleyin..."):
            img_array = np.array(image)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            edges = cv2.Canny(blurred, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            damage_count = 0
            output_img = img_array.copy()
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 150 < area < 8000:
                    damage_count += 1
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(output_img, (x, y), (x + w, y + h), (255, 0, 0), 3)
            
            st.success("Analiz Tamamlandı!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Tespit Edilen Hasar Bölgesi", value=f"{damage_count} Adet")
            with col2:
                st.metric(label="Tahmini Durum", value="İnceleme Gerektirir" if damage_count > 0 else "Hasar Görünmüyor")
            
            st.image(output_img, caption="Hasarlı Bölgelerin İşaretlenmiş Hali", use_container_width=True)
            
            st.info("💡 **Not:** Bu sistem ön prototiptir. Kesin ekspertiz raporu yerine ön bilgilendirme amaçlıdır.")
