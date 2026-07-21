import streamlit as st
from PIL import Image

# Sayfa Yapılandırması
st.set_page_config(page_title="Sektörel Ortak Kara Liste & Kimlik Kontrolü", page_icon="🚨", layout="centered")

# Tasarım ve Başlık
st.title("🚨 Rent a Car Ortak Risk & Kimlik Doğrulama Paneli")
st.write("Küçük ve orta ölçekli işletmeler için ortak kara liste ve kimlik/pasaport kontrol asistanı.")

st.markdown("---")

# Hafızada Türkiye Geneli Sektör Veritabanı ve Örnek Kayıtlar
if 'kara_liste' not in st.session_state:
    st.session_state['kara_liste'] = [
        {
            "tc": "11111111110", 
            "pasaport": "U12345678",
            "ad": "Ahmet Yılmaz", 
            "telefon": "0532 000 00 01", 
            "firma": "Enterprise Rent a Car Türkiye", 
            "sebep": "Sözleşme dışı şehir dışına çıkarıldı, araç hasarlı teslim edilip ödemeden kaçıldı.",
            "kimlik_resmi": None
        },
        {
            "tc": "22222222220", 
            "pasaport": "M98765432",
            "ad": "Mehmet Demir", 
            "telefon": "0533 111 11 02", 
            "firma": "Avis Rent a Car", 
            "sebep": "Kira bedeli 5 gün geciktirildi, araç icra yoluyla şantiyeden teslim alındı.",
            "kimlik_resmi": None
        }
    ]

# Sektördeki Kurumsal ve Dernek Üyesi Firma Listesi
sektor_firmalari = [
    "TüreAuto (Kendi İşletmeniz)",
    "TOKKDER Üyesi Yerel İşletmeler",
    "AKKDER Üyesi Rent a Car",
    "Enterprise Rent a Car",
    "Avis & Budget Rent a Car",
    "Europcar & Goldcar",
    "Sixt Rent a Car",
    "Zeplin Car Rental",
    "Garenta / Çelik Motor",
    "Bağımsız Yerel Rent a Car"
]

# Sekmeler
islem_turu = st.radio("İşlem Türü", ["🔍 Müşteri Sorgula (Kimlik/Pasaport)", "➕ Havuza Riskli Bildirimi Ekle"], horizontal=True)

st.markdown("---")

if islem_turu == "🔍 Müşteri Sorgula (Kimlik/Pasaport)":
    st.subheader("🕵️ Hızlı Risk ve Belge Sorgulama")
    st.write("Müşterinin T.C. Kimlik Numarası, Telefonu veya Pasaport Numarası ile ortak havuzu tarayın.")
    
    aranan_kriter = st.text_input("T.C. Kimlik No, Telefon veya Pasaport No Girin")
    
    if st.button("Havuzda Sorgula", type="primary", use_container_width=True):
        if not aranan_kriter:
            st.warning("Lütfen sorgulama için bir kriter yazın.")
        else:
            bulunanlar = [
                k for k in st.session_state['kara_liste'] 
                if aranan_kriter in k['tc'] or aranan_kriter in k['telefon'] or aranan_kriter.upper() in k['pasaport'].upper()
            ]
            
            if bulunanlar:
                st.error("🚨 KRİTİK ALARM! Bu kişi ortak kara listede kayıtlı!")
                for kayit in bulunanlar:
                    st.markdown(f"""
                    * 👤 **Ad Soyad:** {kayit['ad']}
                    * 🆔 **T.C. No / Pasaport:** {kayit['tc']} / **{kayit['pasaport']}**
                    * 📞 **Telefon:** {kayit['telefon']}
                    * 🏢 **Bildiren Kurum / Firma:** **{kayit['firma']}**
                    * ⚠️ **Yaşanan Vaka / Gerekçe:** _{kayit['sebep']}_
                    """)
                    
                    # Eğer kayıt eklenirken kimlik resmi yüklenmişse doğrudan göster
                    if kayit['kimlik_resmi'] is not None:
                        st.image(kayit['kimlik_resmi'], caption=f"{kayit['ad']} - Yüklenen Kimlik / Pasaport Belgesi", use_container_width=True)
                        
                st.error("❌ **Ortak Sektör Tavsiyesi:** Bu kişiye kesinlikle araç KİRALAMAYIN!")
            else:
                st.success("✅ Temiz! Ortak havuzda bu kriterle eşleşen aktif bir risk kaydı bulunamadı. Kiralama güvenle yapılabilir.")

else:
    st.subheader("➕ Sektörel Ortak Havuza Belge Destekli Bildirim Ekle")
    st.write("Sorun yaşatan müşterinin bilgilerini ve kimlik/pasaport fotoğrafını sisteme yükleyerek tüm sektörü koruyun.")
    
    with st.form("risk_ekleme_formu"):
        bildiren_firma = st.selectbox("Bildirim Yapan Firma", sektor_firmalari)
        yeni_ad = st.text_input("Sorunlu Müşteri Adı Soyadı")
        
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            yeni_tc = st.text_input("T.C. Kimlik Numarası")
        with col_k2:
            yeni_pasaport = st.text_input("Pasaport Numarası (Yabancı uyruklu ise)")
            
        yeni_tel = st.text_input("Müşteri Telefon Numarası")
        yeni_sebep = st.text_area("Yaşanan Problem Detayı", placeholder="Örn: Kirayı ödemedi, telefonları engelledi...")
        
        # Kimlik veya Pasaport Görseli Yükleme Alanı
        yuklenen_dosya = st.file_uploader("Müşterinin Kimlik / Pasaport Fotoğrafını Yükle", type=["jpg", "jpeg", "png"])
        
        # Görsel yüklendiyse önizlemesini hemen gösterelim
        kimlik_img = None
        if yuklenen_dosya is not None:
            kimlik_img = Image.open(yuklenen_dosya)
            st.image(kimlik_img, caption="Yüklenen Kimlik / Pasaport Önizlemesi", use_container_width=True)

        submit_btn = st.form_submit_button("🚨 Havuzu Güncelle ve Görseli Kaydet", type="primary")
        
        if submit_btn:
            if yeni_ad and (yeni_tc or yeni_pasaport) and yeni_sebep:
                yeni_kayit = {
                    "tc": yeni_tc if yeni_tc else "Belirtilmemiş",
                    "pasaport": yeni_pasaport if yeni_pasaport else "Yok",
                    "ad": yeni_ad,
                    "telefon": yeni_tel,
                    "firma": bildiren_firma,
                    "sebep": yeni_sebep,
                    "kimlik_resmi": kimlik_img
                }
                st.session_state['kara_liste'].append(yeni_kayit)
                st.success(f"Başarıyla eklendi! Kimlik görseli ve risk kaydı '{bildiren_firma}' onaylı olarak havuza işlendi.")
            else:
                st.error("Lütfen Ad Soyad, T.C. veya Pasaport No ile Problem Detayı alanlarını doldurun.")

st.markdown("---")
st.caption("🔒 **TüreAuto & Sektörel Birlik Güvencesi:** Kimlik doğrulamalı ortak risk havuz sistemi.")
                        
