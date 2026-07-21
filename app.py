import streamlit as st
import urllib.parse

# Sayfa Yapılandırması
st.set_page_config(page_title="TüreAuto Profesyonel Değerleme", page_icon="🚗", layout="centered")

# Tasarım ve Başlık
st.title("🚗 TüreAuto Akıllı Araç Değerleme & İlan Asistanı")
st.write("Model, donanım ve ekspertiz analizi ile canlı piyasa takip paneli.")

st.markdown("---")

# 1. Bölüm: Marka ve Model Seçimi
st.subheader("📋 1. Araç ve Model Bilgileri")

marka = st.selectbox(
    "Marka", 
    ["Renault", "Volkswagen", "Fiat", "Ford", "BMW", "Mercedes-Benz", "Toyota", "Hyundai", "Honda", "Audi", "Skoda", "Peugeot"]
)

model_secenekleri = {
    "Renault": ["Clio", "Megane", "Megane Sedan", "Captur", "Austral", "Taliant"],
    "Volkswagen": ["Golf", "Polo", "Passat", "T-Roc", "Tiguan", "Taigo"],
    "Fiat": ["Egea", "Egea Cross", "Fiorino", "Doblo"],
    "Ford": ["Focus", "Fiesta", "Kuga", "Puma"],
    "BMW": ["1 Serisi", "3 Serisi", "5 Serisi", "X1", "X3"],
    "Mercedes-Benz": ["A Serisi", "C Serisi", "E Serisi", "GLA", "GLB"],
    "Toyota": ["Corolla", "CH-R", "Yaris", "RAV4"],
    "Hyundai": ["i20", "i30", "Bayon", "Tucson"],
    "Honda": ["Civic", "HR-V", "CR-V"],
    "Audi": ["A3", "A4", "Q2", "Q3"],
    "Skoda": ["Octavia", "Superb", "Kamiq", "Karoq"],
    "Peugeot": ["208", "308", "2008", "3008", "5008"]
}

col_m1, col_m2 = st.columns(2)
with col_m1:
    secilen_model = st.selectbox("Model", model_secenekleri.get(marka, ["Standart Model"]))
with col_m2:
    donanim = st.selectbox("Donanım Paketi", ["Joy / Basit", "Touch / Standart", "Icon / Prestij", "Full / Premium"])

col1, col2 = st.columns(2)
with col1:
    yil = st.slider("Model Yılı", 2012, 2026, 2022)
with col2:
    yakit = st.selectbox("Yakıt Türü", ["Benzin", "Dizel", "Benzin & LPG", "Hibrit", "Elektrik"])

col3, col4 = st.columns(2)
with col3:
    vites = st.selectbox("Vites Türü", ["Manuel", "Yarı Otomatik", "Otomatik"])
with col4:
    kilometre = st.number_input("Kilometre (KM)", min_value=0, max_value=600000, value=55000, step=5000)

st.markdown("---")

# 2. Bölüm: Kaporta ve Boya Durumu
st.subheader("🛠️ 2. Ekspertiz Durumu (Boya / Değişen)")

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

tramer = st.number_input("Tramer / Hasar Kaydı (TL)", min_value=0, value=0, step=2500)

st.markdown("---")

# 3. Hesaplama ve Canlı İlan Linkleri
if st.button("🚀 Analizi Başlat ve Canlı İlanları Getir", type="primary", use_container_width=True):
    with st.spinner("Piyasa matrisi hesaplanıyor ve ilanlar filtreleniyor..."):
        
        model_taban_fiyatlari = {
            "Clio": 850000, "Megane": 1150000, "Megane Sedan": 1100000, "Captur": 1200000, "Austral": 1650000, "Taliant": 780000,
            "Golf": 1350000, "Polo": 950000, "Passat": 1750000, "T-Roc": 1500000, "Tiguan": 1850000, "Taigo": 1300000,
            "Egea": 750000, "Egea Cross": 850000, "Fiorino": 650000, "Doblo": 720000,
            "Focus": 1050000, "Fiesta": 780000, "Kuga": 1550000, "Puma": 1250000,
            "1 Serisi": 1600000, "3 Serisi": 2300000, "5 Serisi": 3100000, "X1": 2200000, "X3": 3500000,
            "A Serisi": 1800000, "C Serisi": 2500000, "E Serisi": 3400000, "GLA": 2100000, "GLB": 2400000,
            "Corolla": 1100000, "CH-R": 1350000, "Yaris": 950000, "RAV4": 2100000,
            "i20": 800000, "i30": 950000, "Bayon": 900000, "Tucson": 1600000,
            "Civic": 1300000, "HR-V": 1450000, "CR-V": 1800000,
            "A3": 1700000, "A4": 2100000, "Q2": 1650000, "Q3": 2200000,
            "Octavia": 1250000, "Superb": 1700000, "Kamiq": 1150000, "Karoq": 1450000,
            "208": 880000, "308": 1150000, "2008": 1250000, "3008": 1650000, "5008": 1950000
        }
        
        taban = model_taban_fiyatlari.get(secilen_model, 950000)
        donanim_carpani = {"Joy / Basit": 0.92, "Touch / Standart": 1.0, "Icon / Prestij": 1.08, "Full / Premium": 1.16}
        taban = taban * donanim_carpani.get(donanim, 1.0)
        
        yas_farki = (2026 - yil) * 45000
        ideal_km = (2026 - yil) * 18000
        km_farki = kilometre - ideal_km
        km_cezasi = (km_farki / 1000) * 1100 if km_farki > 0 else (km_farki / 1000) * 700
            
        boya_kaybi = len(boyali_parca) * 10000
        degisen_kaybi = len(degisen_parca) * 28000
        tramer_kaybi = tramer * 0.6
        
        hesaplanan_deger = taban - yas_farki - km_cezasi - boya_kaybi - degisen_kaybi - tramer_kaybi
        if hesaplanan_deger < 300000:
            hesaplanan_deger = 300000
            
        alis_fiyati = int(hesaplanan_deger * 0.92)
        piyasa_ortalamasi = int(hesaplanan_deger)
        satis_fiyati = int(hesaplanan_deger * 1.06)

    # Sonuç Ekranı
    st.success("📊 Analiz Tamamlandı - Piyasa Raporu Hazır!")
    
    st.metric(label=f"{marka} {secilen_model} ({donanim}) Değeri", value=f"{satis_fiyati:,} TL".replace(",", "."))
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.info(f"🛡️ **Galeri Alış / Takas:**\n\n{alis_fiyati:,} TL".replace(",", "."))
    with col_s2:
        st.warning(f"⚖️ **Reel Piyasa Ortalaması:**\n\n{piyasa_ortalamasi:,} TL".replace(",", "."))
    with col_s3:
        st.error(f"🏷️ **Hızlı Satış (Acil):**\n\n{int(alis_fiyati * 0.94):,} TL".replace(",", "."))
        
    st.write("---")
    st.markdown("### 🌐 Canlı İlan Piyasası (Tek Tıkla Kontrol Et)")
    st.write("Seçtiğiniz kriterlere en uygun güncel ilanları doğrudan büyük platformlarda inceleyin:")
    
    # Dinamik Arama Linkleri Oluşturma
    Arama_Sorgusu = f"{marka} {secilen_model} {yil}"
    Encoded_Query = urllib.parse.quote(Arama_Sorgusu)
    
    Sahibinden_Url = f"https://www.sahibinden.com/{marka.lower()}-{secilen_model.lower().replace(' ', '-')}/vasita?query_text={Encoded_Query}"
    Arabam_Url = f"https://www.arabam.com/ikinci-el?q={Encoded_Query}"
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown(f"👉 **[Sahibinden.com'da İncele]({Sahibinden_Url})**")
    with col_l2:
        st.markdown(f"👉 **[Arabam.com'da İncele]({Arabam_Url})**")
        
    st.write("---")
    st.caption("💡 **Not:** Linkler, seçtiğiniz marka, model ve yıla göre otomatik filtrelenerek oluşturulmuştur.")
    
