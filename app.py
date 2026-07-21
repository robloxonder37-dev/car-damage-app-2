import streamlit as st
import urllib.parse

# Sayfa Yapılandırması
st.set_page_config(page_title="TüreAuto Profesyonel Değerleme", page_icon="🚗", layout="centered")

# Tasarım ve Başlık
st.title("🚗 TüreAuto Canlı Piyasa & Değerleme Paneli")
st.write("Genişletilmiş model ve donanım matrisi ile güncel ekspertiz ve piyasa analizi.")

st.markdown("---")

# 1. Bölüm: Marka, Model ve Donanım Seçimi
st.subheader("📋 1. Araç ve Paket Bilgileri")

marka = st.selectbox(
    "Marka", 
    ["Renault", "Volkswagen", "Fiat", "Ford", "BMW", "Mercedes-Benz", "Toyota", "Hyundai", "Honda", "Audi", "Skoda", "Peugeot", "Opel", "Dacia"]
)

# Kapsamlı Model ve Donanım Matrisi
model_veri_tabani = {
    "Renault": {
        "Clio": ["Joy", "Touch", "Icon", "Evolution", "Techno"],
        "Megane": ["Joy", "Touch", "Icon", "Limited", "Line"],
        "Megane Sedan": ["Joy", "Touch", "Icon"],
        "Captur": ["Touch", "Icon", "R.S. Line"],
        "Austral": ["Techno", "Techno Esprit Alpine", "Iconic"]
    },
    "Volkswagen": {
        "Golf": ["Impression", "Life", "Style", "R-Line"],
        "Polo": ["Impression", "Life", "Style"],
        "Passat": ["Business", "Elegance", "R-Line"],
        "T-Roc": ["Life", "Style", "R-Line"],
        "Tiguan": ["Life", "Elegance", "R-Line"]
    },
    "Fiat": {
        "Egea": ["Easy", "Urban", "Lounge", "Cross"],
        "Egea Cross": ["Street", "Urban", "Lounge"],
        "Fiorino": ["Pop", "Premio", "Combi"],
        "Doblo": ["Safety", "Premio", "Ecoline"]
    },
    "Ford": {
        "Focus": ["Trend X", "Titanium", "Active", "ST-Line"],
        "Fiesta": ["Trend", "Titanium"],
        "Kuga": ["Style", "Titanium", "ST-Line"],
        "Puma": ["Style", "ST-Line"]
    },
    "BMW": {
        "1 Serisi": ["Sport Line", "M Sport"],
        "3 Serisi": ["First Edition Luxury", "First Edition M Sport"],
        "5 Serisi": ["Luxury Line", "M Sport"],
        "X1": ["sDrive16d M Sport", "xDrive20d"]
    },
    "Mercedes-Benz": {
        "A Serisi": ["AMG", "Progressive"],
        "C Serisi": ["AMG", "Exclusive", "Prime"],
        "E Serisi": ["AMG", "Exclusive"],
        "GLA": ["AMG", "Progressive"]
    },
    "Toyota": {
        "Corolla": ["Vision", "Dream", "Flame", "Passion"],
        "CH-R": ["Flame", "Passion"],
        "Yaris": ["Dream", "Flame", "Style"]
    },
    "Hyundai": {
        "i20": ["Jump", "Style", "Elite"],
        "i30": ["Style", "Elite"],
        "Bayon": ["Jump", "Style", "Elite"],
        "Tucson": ["Prime", "Plus", "Elite", "H-Line"]
    },
    "Honda": {
        "Civic": ["Dream", "Premium", "Elegance", "Executive+"],
        "HR-V": ["Executive"],
        "CR-V": ["Elegance", "Executive"]
    },
    "Audi": {
        "A3": ["Advanced", "S Line"],
        "A4": ["Advanced", "Design", "S Line"],
        "Q2": ["Advanced", "S Line"],
        "Q3": ["Advanced", "S Line"]
    },
    "Skoda": {
        "Octavia": ["Elite", "Ambition", "Style", "Premium"],
        "Superb": ["Ambition", "Style", "Elite", "L&K"]
    },
    "Peugeot": {
        "208": ["Active", "Allure", "GT"],
        "308": ["Active Prime", "Allure", "GT"],
        "2008": ["Active", "Allure", "GT"],
        "3008": ["Active Prime", "Allure", "GT"]
    },
    "Opel": {
        "Corsa": ["Edition", "GS", "Ultimate"],
        "Astra": ["Edition", "GS", "Ultimate"],
        "Mokka": ["Edition", "GS"]
    },
    "Dacia": {
        "Sandero": ["Comfort", "Prestige"],
        "Duster": ["Expression", "Journey", "Extreme"]
    }
}

mevcut_modeller = list(model_veri_tabani.get(marka, {"Standart": ["Standart"]}).keys())

col_m1, col_m2 = st.columns(2)
with col_m1:
    secilen_model = st.selectbox("Model", mevcut_modeller)
with col_m2:
    mevcut_paketler = model_veri_tabani.get(marka, {}).get(secilen_model, ["Standart Paket"])
    donanim = st.selectbox("Donanım / Paket", mevcut_paketler)

col1, col2 = st.columns(2)
with col1:
    yil = st.slider("Model Yılı", 2014, 2026, 2023)
with col2:
    yakit = st.selectbox("Yakıt Türü", ["Benzin", "Dizel", "Benzin & LPG", "Hibrit", "Elektrik"])

col3, col4 = st.columns(2)
with col3:
    vites = st.selectbox("Vites Türü", ["Manuel", "Yarı Otomatik", "Otomatik"])
with col4:
    kilometre = st.number_input("Kilometre (KM)", min_value=0, max_value=500000, value=45000, step=5000)

st.markdown("---")

# 2. Bölüm: Ekspertiz (Boya / Değişen / Tramer)
st.subheader("🛠️ 2. Ekspertiz Detayları")

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

# 3. Hesaplama ve Canlı İlan Yönlendirmesi
if st.button("🚀 Piyasa Analizini ve Değeri Hesapla", type="primary", use_container_width=True):
    with st.spinner("Güncel matris analiz ediliyor..."):
        
        # Baz Fiyat Belirleme Matrisi
        taban_fiyatlar = {
            "Clio": 950000, "Megane": 1250000, "Megane Sedan": 1200000, "Captur": 1300000, "Austral": 1750000,
            "Golf": 1450000, "Polo": 1050000, "Passat": 1850000, "T-Roc": 1600000, "Tiguan": 1950000,
            "Egea": 850000, "Egea Cross": 950000, "Fiorino": 700000, "Doblo": 780000,
            "Focus": 1150000, "Fiesta": 850000, "Kuga": 1650000, "Puma": 1350000,
            "1 Serisi": 1700000, "3 Serisi": 2400000, "5 Serisi": 3200000, "X1": 2300000,
            "A Serisi": 1900000, "C Serisi": 2600000, "E Serisi": 3500000, "GLA": 2200000,
            "Corolla": 1200000, "CH-R": 1450000, "Yaris": 1050000,
            "i20": 880000, "i30": 1050000, "Bayon": 980000, "Tucson": 1700000,
            "Civic": 1400000, "HR-V": 1550000, "CR-V": 1900000,
            "A3": 1800000, "A4": 2200000, "Q2": 1750000, "Q3": 2300000,
            "Octavia": 1350000, "Superb": 1800000,
            "208": 950000, "308": 1250000, "2008": 1350000, "3008": 1750000,
            "Corsa": 920000, "Astra": 1200000, "Mokka": 1350000,
            "Sandero": 820000, "Duster": 1100000
        }
        
        taban = taban_fiyatlar.get(secilen_model, 1000000)
        
        # Yaş ve Kilometre Faktörleri
        yas_farki = (2026 - yil) * 50000
        ideal_km = (2026 - yil) * 17000
        km_farki = kilometre - ideal_km
        km_cezasi = (km_farki / 1000) * 1200 if km_farki > 0 else (km_farki / 1000) * 800
        
        # Parça ve Tramer Kayıpları
        boya_kaybi = len(boyali_parca) * 12000
        degisen_kaybi = len(degisen_parca) * 30000
        tramer_kaybi = tramer * 0.65
        
        hesaplanan_deger = taban - yas_farki - km_cezasi - boya_kaybi - degisen_kaybi - tramer_kaybi
        if hesaplanan_deger < 350000:
            hesaplanan_deger = 350000
            
        alis_fiyati = int(hesaplanan_deger * 0.92)
        piyasa_ortalamasi = int(hesaplanan_deger)
        satis_fiyati = int(hesaplanan_deger * 1.06)

    # Sonuç Ekranı
    st.success("📊 TüreAuto Analiz Raporu Hazır!")
    
    st.metric(label=f"{marka} {secilen_model} ({donanim}) Piyasa Değeri", value=f"{satis_fiyati:,} TL".replace(",", "."))
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.info(f"🛡️ **Galeri Alış / Takas:**\n\n{alis_fiyati:,} TL".replace(",", "."))
    with col_s2:
        st.warning(f"⚖️ **Reel Piyasa Ortalaması:**\n\n{piyasa_ortalamasi:,} TL".replace(",", "."))
    with col_s3:
        st.error(f"🏷️ **Hızlı Satış Alt Sınır:**\n\n{int(alis_fiyati * 0.93):,} TL".replace(",", "."))
        
    st.write("---")
    st.markdown("### 🌐 Canlı Piyasayı Kontrol Et (Tek Tık)")
    st.write("Seçtiğiniz araca ait güncel ilanları doğrudan incelemek için aşağıdaki bağlantıları kullanın:")
    
    # Canlı Arama Linkleri
    arama_sorgusu = f"{marka} {secilen_model} {donanim}"
    encoded_query = urllib.parse.quote(arama_sorgusu)
    
    sahibinden_url = f"https://www.sahibinden.com/{marka.lower()}-{secilen_model.lower().replace(' ', '-')}/vasita?query_text={encoded_query}"
    arabam_url = f"https://www.arabam.com/ikinci-el?q={encoded_query}"
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown(f"👉 **[Sahibinden.com İlanları]({sahibinden_url})**")
    with col_l2:
        st.markdown(f"👉 **[Arabam.com İlanları]({arabam_url})**")
        
    st.write("---")
    st.caption("💡 **TüreAuto Bilgi:** Günlük kontrolleriniz için bu panel her an cebinizde hazır!")
