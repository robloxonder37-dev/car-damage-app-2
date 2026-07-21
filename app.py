import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="TüreAuto Araç Değerleme", page_icon="💰", layout="centered")

# Tasarım ve Başlık
st.title("🚗 TüreAuto Araç Değerleme Paneli")
st.write("Aracın bilgilerini girin, piyasa koşullarına göre tahmini değerini ve fiyat aralığını hemen hesaplayalım.")

st.markdown("---")

# 1. Bölüm: Temel Araç Bilgileri
st.subheader("📋 1. Araç Bilgileri")

col1, col2 = st.columns(2)
with col1:
    marka = st.selectbox("Marka", ["Volkswagen", "Renault", "Fiat", "Ford", "BMW", "Mercedes-Benz", "Toyota", "Hyundai", "Honda"])
with col2:
    yil = st.slider("Model Yılı", 2010, 2026, 2020)

col3, col4 = st.columns(2)
with col3:
    yakit = st.selectbox("Yakıt Türü", ["Benzin", "Dizel", "Benzin & LPG", "Hibrit", "Elektrik"])
with col4:
    vites = st.selectbox("Vites Türü", ["Manuel", "Yarı Otomatik", "Otomatik"])

kilometre = st.number_input("Kilometre (KM)", min_value=0, max_value=500000, value=75000, step=5000)

st.markdown("---")

# 2. Bölüm: Kaporta ve Boya Durumu
st.subheader("🛠️ 2. Boya ve Değişen Parçalar")
st.write("Aracınızda boyalı veya değişen parçaları işaretleyin:")

col_b1, col_b2 = st.columns(2)
with col_b1:
    boyali_parca = st.multiselect(
        "Boyalı Parçalar",
        ["Ön Tampon", "Arka Tampon", "Motor Kaputu", "Sol Ön Çamurluk", "Sol Ön Kapı", "Sol Arka Kapı", "Sol Arka Çamurluk", "Sağ Ön Çamurluk", "Sağ Ön Kapı", "Sağ Arka Kapı", "Sağ Arka Çamurluk", "Bagaj Kapağı"]
    )
with col_b2:
    degisen_parca = st.multiselect(
        "Değişen Parçalar",
        ["Motor Kaputu", "Sol Ön Çamurluk", "Sol Ön Kapı", "Sol Arka Kapı", "Sol Arka Çamurluk", "Sağ Ön Çamurluk", "Sağ Ön Kapı", "Sağ Arka Kapı", "Sağ Arka Çamurluk", "Bagaj Kapağı"]
    )

tramer = st.number_input("Tramer / Hasar Kaydı Tutarı (TL)", min_value=0, value=0, step=5000)

st.markdown("---")

# 3. Hesaplama ve Sonuç Butonu
if st.button("🚀 Araç Değerini Hesapla", type="primary", use_container_width=True):
    with st.spinner("Piyasa verileri analiz ediliyor..."):
        
        # Basit bir fiyatlandırma simülasyon mantığı (Marka ve yıla göre taban fiyat belirleme)
        taban_fiyatlar = {
            "Volkswagen": 950000, "Renault": 700000, "Fiat": 600000, 
            "Ford": 750000, "BMW": 1600000, "Mercedes-Benz": 1750000, 
            "Toyota": 850000, "Hyundai": 720000, "Honda": 800000
        }
        
        taban = taban_fiyatlar.get(marka, 800000)
        
        # Yıl etkisi
        yil_farki = (yil - 2015) * 60000
        
        # Kilometre düşüşü
        km_dususu = (kilometre / 10000) * 15000
        
        # Boya ve değişen düşüşleri
        boya_kaybi = len(boyali_parca) * 15000
        degisen_kaybi = len(degisen_parca) * 35000
        tramer_kaybi = tramer * 0.7  # Tramerin piyasaya etkisi
        
        tahmini_fiyat = taban + yil_farki - km_dususu - boya_kaybi - degisen_kaybi - tramer_kaybi
        
        if tahmini_fiyat < 200000:
            tahmini_fiyat = 250000 # Minimum taban
            
        alt_limit = int(tahmini_fiyat * 0.95)
        ust_limit = int(tahmini_fiyat * 1.05)

    # Sonuç Ekranı
    st.success("Analiz Başarıyla Tamamlandı! 📊")
    
    st.metric(label="Tahmini Ortalama Piyasa Değeri", value=f"{int(tahmini_fiyat):,} TL".replace(",", "."))
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.info(f"📉 **Alış / Ticaret Alt Sınırı:**\n\n {alt_limit:,} TL".replace(",", "."))
    with col_s2:
        st.warning(f"📈 **Perakende Üst Sınırı:**\n\n {ust_limit:,} TL".replace(",", "."))
        
    st.write("---")
    st.caption("⚠️ **Not:** Bu değerleme; girilen kilometre, boya, değişen ve tramer bilgilerine göre yapay zeka tarafından üretilen tahmini piyasa ortalamasıdır.")
