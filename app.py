import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="TüreAuto Profesyonel Değerleme", page_icon="🚗", layout="centered")

# Tasarım ve Başlık
st.title("🚗 TüreAuto Akıllı Araç Değerleme")
st.write("Genişletilmiş piyasa matrisi ile aracınızın gerçekçi alım-satım değerini hemen hesaplayın.")

st.markdown("---")

# 1. Bölüm: Araç ve Donanım Seçimi
st.subheader("📋 1. Araç Bilgileri")

col1, col2 = st.columns(2)
with col1:
    marka = st.selectbox(
        "Marka", 
        ["Volkswagen", "Renault", "Fiat", "Ford", "BMW", "Mercedes-Benz", "Toyota", "Hyundai", "Honda", "Audi", "Skoda", "Peugeot"]
    )
with col2:
    yil = st.slider("Model Yılı", 2012, 2026, 2021)

col3, col4 = st.columns(2)
with col3:
    yakit = st.selectbox("Yakıt Türü", ["Benzin", "Dizel", "Benzin & LPG", "Hibrit", "Elektrik"])
with col4:
    vites = st.selectbox("Vites Türü", ["Manuel", "Yarı Otomatik", "Otomatik"])

kilometre = st.number_input("Kilometre (KM)", min_value=0, max_value=600000, value=65000, step=5000)

st.markdown("---")

# 2. Bölüm: Kaporta ve Boya Durumu
st.subheader("🛠️ 2. Ekspertiz Durumu (Boya / Değişen)")
st.write("Aracın kusurlu veya boyalı/değişen parçalarını seçin:")

col_b1, col_b2 = st.columns(2)
with col_b1:
    boyali_parca = st.multiselect(
        "Boyalı Parçalar",
        ["Ön Tampon", "Arka Tampon", "Motor Kaputu", "Sol Ön Çamurluk", "Sol Ön Kapı", "Sol Arka Kapı", "Sol Arka Çamurluk", "Sağ Ön Çamurluk", "Sağ Ön Kapı", "Sağ Arka Kapı", "Sağ Arka Çamurluk", "Bagaj Kapağı", "Tavan"]
    )
with col_b2:
    degisen_parca = st.multiselect(
        "Değişen Parçalar",
        ["Motor Kaputu", "Sol Ön Çamurluk", "Sol Ön Kapı", "Sol Arka Kapı", "Sol Arka Çamurluk", "Sağ Ön Çamurluk", "Sağ Ön Kapı", "Sağ Arka Kapı", "Sağ Arka Çamurluk", "Bagaj Kapağı", "Tavan (Ağır Hasar)"]
    )

col_t1, col_t2 = st.columns(2)
with col_t1:
    tramer = st.number_input("Tramer / Hasar Kaydı (TL)", min_value=0, value=0, step=2500)
with col_t2:
    kasa_tipi = st.selectbox("Kasa / Donanım Tipi", ["Standart / Hatchback", "Sedan", "SUV / Arazi", "Ticari / Van"])

st.markdown("---")

# 3. Hesaplama ve Piyasa Analizi
if st.button("🚀 Detaylı Piyasa Analizini Başlat", type="primary", use_container_width=True):
    with st.spinner("Güncel piyasa matrisi hesaplanıyor..."):
        
        # Kapsamlı Marka Bazlı Taban Fiyatlar (2026 Piyasa Simülasyonu)
        piyasa_matrisi = {
            "Volkswagen": 1150000, "Renault": 850000, "Fiat": 720000, 
            "Ford": 900000, "BMW": 1950000, "Mercedes-Benz": 2100000, 
            "Toyota": 1050000, "Hyundai": 880000, "Honda": 960000,
            "Audi": 1800000, "Skoda": 1000000, "Peugeot": 920000
        }
        
        taban = piyasa_matrisi.get(marka, 900000)
        
        # Kasa tipi çarpanı
        kasa_carpani = {"Standart / Hatchback": 1.0, "Sedan": 1.05, "SUV / Arazi": 1.25, "Ticari / Van": 0.9}
        taban = taban * kasa_carpani.get(kasa_tipi, 1.0)
        
        # Yıl ve Yaş Eskimesi
        yas_farki = (2026 - yil) * 45000
        
        # Kilometre Cezası (Yılda ortalama 20.000 km baz alınır)
        ideal_km = (2026 - yil) * 18000
        km_farki = kilometre - ideal_km
        km_cezasi = 0
        if km_farki > 0:
            km_cezasi = (km_farki / 1000) * 1200 # Fazla km başına düşüş
        else:
            km_cezasi = (km_farki / 1000) * 800  # Düşük km primi
            
        # Boya ve Değişen Değer Kayıpları
        boya_kaybi = len(boyali_parca) * 12000
        degisen_kaybi = len(degisen_parca) * 32000
        
        # Tramer Etkisi (Ağır hasar veya normal tramer oranı)
        tramer_kaybi = tramer * 0.65
        
        # Net Fiyat Hesaplama
        hesaplanan_deger = taban - yas_farki - km_cezasi - boya_kaybi - degisen_kaybi - tramer_kaybi
        
        if hesaplanan_deger < 300000:
            hesaplanan_deger = 300000
            
        # Alış (Galeri maliyet/takas) ve Satış (Perakende) aralığı
        alis_fiyati = int(hesaplanan_deger * 0.92)
        piyasa_ortalamasi = int(hesaplanan_deger)
        satis_fiyati = int(hesaplanan_deger * 1.07)

    # Sonuç Ekranı Gösterimi
    st.success("📊 Analiz Tamamlandı - Piyasa Raporu Hazır!")
    
    st.metric(label="Önerilen Perakende Piyasa Değeri", value=f"{satis_fiyati:,} TL".replace(",", "."))
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.info(f"🛡️ **Galeri Alış / Takas:**\n\n{alis_fiyati:,} TL".replace(",", "."))
    with col_s2:
        st.warning(f"⚖️ **Reel Piyasa Ortalaması:**\n\n{piyasa_ortalamasi:,} TL".replace(",", "."))
    with col_s3:
        st.error(f"🏷️ **Hızlı Satış (Acil):**\n\n{int(alis_fiyati * 0.95):,} TL".replace(",", "."))
        
    st.write("---")
    st.markdown("### 💡 Galeri Operasyon Notu")
    st.write("Bu rapor; seçilen kilometre sapması, parça bazlı boya/değişen kayıpları ve güncel piyasa sirkülasyonu baz alınarak otomatik oluşturulmuştur.")
    
