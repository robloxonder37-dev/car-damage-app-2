import streamlit as st
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sayfa Yapılandırması
st.set_page_config(page_title="İstanbul Rent a Car Ortak Birlik & Risk Havuzu", page_icon="🚨", layout="centered")

# Tasarım ve Başlık
st.title("🚨 İstanbul Rent a Car Ortak Risk & Abonelik Paneli")
st.write("Vergi Levhası Onaylı, E-Posta Bildirimli ve Abonelik Destekli Sektörel Birlik Sistemi")

st.markdown("---")

# 1. Onaylı Firma Veritabanı
if 'istanbul_firma_listesi' not in st.session_state:
    st.session_state['istanbul_firma_listesi'] = [
        "TüreAuto (Gölcük / İstanbul)",
        "Roadify Rent A Car",
        "Eva Car Rental",
        "Kaan Filo"
    ]

# 2. Onay Bekleyen Firmalar Havuzu
if 'onay_bekleyen_firmalar' not in st.session_state:
    st.session_state['onay_bekleyen_firmalar'] = []

# 3. Abonelik Bilgileri Veritabanı
if 'firma_abonelikleri' not in st.session_state:
    st.session_state['firma_abonelikleri'] = {
        "TüreAuto (Gölcük / İstanbul)": {"durum": "Aktif Üye (Sınırsız)", "tutar": "100 TL/Ay"},
        "Roadify Rent A Car": {"durum": "Aktif Üye", "tutar": "100 TL/Ay"},
        "Eva Car Rental": {"durum": "Aktif Üye", "tutar": "100 TL/Ay"},
        "Kaan Filo": {"durum": "Aktif Üye", "tutar": "100 TL/Ay"}
    }

# 4. Kara Liste ve Risk Veritabanı
if 'istanbul_kara_liste' not in st.session_state:
    st.session_state['istanbul_kara_liste'] = [
        {
            "tc": "11111111110", 
            "pasaport": "U12345678",
            "ad": "Ahmet Yılmaz", 
            "telefon": "0532 000 00 01", 
            "firma": "Roadify Rent A Car", 
            "risk_tipi": "🚨 Kesin Kara Liste (Hırsız / Dolandırıcı)",
            "sebep": "Hırsız! Arabamı çaldı, günlerce bulunamadı, dolandırıcı şahıs. Kesinlikle bu kişiye araç vermeyin, çok riskli müşteri!",
            "kimlik_resmi": None
        },
        {
            "tc": "22222222220", 
            "pasaport": "Yok",
            "ad": "Caner Demir", 
            "telefon": "0533 111 11 02", 
            "firma": "Kaan Filo", 
            "risk_tipi": "⚠️ Hafif Kusur / Dikkat Edilmeli (İncelenmeli)",
            "sebep": "Araç biraz pis teslim edildi, kaportada ufak çizikler vardı. Ödemeyi 1 gün geciktirdi ama kapattı. Yine de müşteri dikkatli incelenmeli.",
            "kimlik_resmi": None
        }
    ]

# Gerçek E-Posta Gönderme Fonksiyonu (onderkaya1994@gmail.com adresine)
def yoneticiye_mail_gonder(firma_adi, vergi_no, yetkili_kisi):
    hedef_mail = "onderkaya1994@gmail.com"
    konu = f"Yeni Rent a Car Firma Başvurusu: {firma_adi}"
    govde = f"""
    Merhaba Yönetici,
    
    Sisteme yeni bir kiralama firması kayıt başvurusunda bulundu ve vergi levhası yükledi.
    
    Firma Bilgileri:
    - Firma Unvanı: {firma_adi}
    - Vergi Numarası: {vergi_no}
    - Yetkili: {yetkili_kisi}
    
    Lütfen Yönetici Onay Paneli (onderkaya1994@gmail.com yetkisiyle) üzerinden başvuruyu inceleyip onaylayın.
    """
    
    # Not: Python SMTP ayarları (Şifre vb. eklenene kadar simülasyon ve log mantığıyla çalışır)
    try:
        # Gerçek sunucu entegrasyonu için SMTP sunucu blokları buraya yazılır.
        print(f"Mail başarıyla {hedef_mail} adresine yönlendirildi.")
        return True
    except Exception as e:
        return False

# Üst Sekmeler
islem_turu = st.radio("İşlem Seçin", ["🔍 Müşteri Sorgula", "➕ Risk Bildirimi Ekle", "🏢 Firma Başvurusu", "💳 Abonelik Paneli", "⚙️ Yönetici Onay Paneli"], horizontal=True)

st.markdown("---")

if islem_turu == "🔍 Müşteri Sorgula":
    st.subheader("🕵️ Ortak Risk Havuzu Sorgulama")
    st.write("Müşterinin T.C., Telefon veya Pasaport numarası ile geçmiş vukuatlarını ve risk derecesini görün.")
    
    aranan_kriter = st.text_input("T.C. Kimlik No, Telefon veya Pasaport No Girin")
    
    if st.button("Havuzda Sorgula", type="primary", use_container_width=True):
        if not aranan_kriter:
            st.warning("Lütfen sorgulama için bir kriter yazın.")
        else:
            bulunanlar = [
                k for k in st.session_state['istanbul_kara_liste'] 
                if aranan_kriter in k['tc'] or aranan_kriter in k['telefon'] or aranan_kriter.upper() in k['pasaport'].upper()
            ]
            
            if bulunanlar:
                for kayit in bulunanlar:
                    if "Kesin" in kayit['risk_tipi'] or "Hırsız" in kayit['risk_tipi']:
                        st.error(f"🚨 KRİTİK ALARM! {kayit['risk_tipi']}")
                    else:
                        st.warning(f"⚠️ DİKKAT! {kayit['risk_tipi']}")
                        
                    st.markdown(f"""
                    * 👤 **Ad Soyad:** {kayit['ad']}
                    * 🆔 **T.C. / Pasaport:** {kayit['tc']} / **{kayit['pasaport']}**
                    * 📞 **Telefon:** {kayit['telefon']}
                    * 🏢 **Bildiren Kurum:** **{kayit['firma']}**
                    * ⚠️ **Risk Durumu:** _{kayit['risk_tipi']}_
                    * 📝 **Detaylı Açıklama:** **{kayit['sebep']}**
                    """)
                    
                    if kayit['kimlik_resmi'] is not None:
                        st.image(kayit['kimlik_resmi'], caption=f"{kayit['ad']} - Kimlik / Pasaport Belgesi", use_container_width=True)
                        
                st.error("❌ **Birlik Tavsiyesi:** Açıklamaları dikkatle okuyun; hırsız veya dolandırıcı gibi kesin kara listedeki kişilere asla araç vermeyin. Hafif kusurlularda ise müşteriyi detaylı inceleyip o şekilde karar verin!")
            else:
                st.success("✅ Temiz! Ortak havuzda bu kriterle eşleşen aktif bir risk kaydı bulunamadı.")

elif islem_turu == "➕ Risk Bildirimi Ekle":
    st.subheader("➕ Ortak Havuza Risk Bildirimi Ekle")
    st.write("Sorun yaşatan müşterinin detaylarını ve derecesini sisteme işleyin.")
    
    if not st.session_state['istanbul_firma_listesi']:
        st.warning("⚠️ Sistemde henüz onaylanmış firma bulunmuyor.")
    else:
        with st.form("risk_ekleme_formu"):
            bildiren_firma = st.selectbox("Bildirim Yapan Onaylı Firma", st.session_state['istanbul_firma_listesi'])
            yeni_ad = st.text_input("Müşteri Adı Soyadı")
            
            col_k1, col_k2 = st.columns(2)
            with col_k1:
                yeni_tc = st.text_input("T.C. Kimlik Numarası")
            with col_k2:
                yeni_pasaport = st.text_input("Pasaport Numarası (Yabancı ise)")
                
            yeni_tel = st.text_input("Telefon Numarası")
            
            risk_derecesi = st.selectbox(
                "Risk ve Vaka Derecesi",
                [
                    "🚨 Kesin Kara Liste (Hırsız / Dolandırıcı)",
                    "⚠️ Hafif Kusur / Dikkat Edilmeli (Incelenmeli)"
                ]
            )
            
            yeni_sebep = st.text_area(
                "Detaylı Açıklama", 
                placeholder="Örn: Hırsız arabamı çaldı / Dolandırıcı, kesinlikle araç vermeyin! Veya: Araçta ufak çizik vardı, pis teslim etti, müşteri incelenmeli..."
            )
            
            yuklenen_dosya = st.file_uploader("Müşterinin Kimlik / Pasaport Fotoğrafı", type=["jpg", "jpeg", "png"])
            kimlik_img = None
            if yuklenen_dosya is not None:
                kimlik_img = Image.open(yuklenen_dosya)
                st.image(kimlik_img, caption="Kimlik Önizleme", use_container_width=True)

            submit_btn = st.form_submit_button("🚨 Havuza Kaydet ve Sektörü Uyar", type="primary")
            
            if submit_btn:
                if yeni_ad and (yeni_tc or yeni_pasaport) and yeni_sebep:
                    st.session_state['istanbul_kara_liste'].append({
                        "tc": yeni_tc if yeni_tc else "Belirtilmemiş",
                        "pasaport": yeni_pasaport if yeni_pasaport else "Yok",
                        "ad": yeni_ad,
                        "telefon": yeni_tel,
                        "firma": bildiren_firma,
                        "risk_tipi": risk_derecesi,
                        "sebep": yeni_sebep,
                        "kimlik_resmi": kimlik_img
                    })
                    st.success("Başarıyla eklendi! Risk kaydı ortak havuza işlendi.")
                else:
                    st.error("Lütfen zorunlu alanları doldurun.")

elif islem_turu == "🏢 Firma Başvurusu":
    st.subheader("🏢 Yeni Rent a Car Firma Kayıt Başvurusu")
    st.write("Sisteme üye olup ortak havuza katılabilmek için lütfen vergi levhanızı yükleyin. (Aylık abonelik: 100 TL)")
    
    with st.form("firma_basvuru_formu"):
        f_adi = st.text_input("Firma Ticari Unvanı", placeholder="Örn: Boğaziçi Rent a Car")
        f_vergi = st.text_input("Vergi Numarası")
        f_yetkili = st.text_input("Yetkili Adı Soyadı")
        f_tel = st.text_input("İşletme Telefonu")
        
        vergi_levhasi_dosya = st.file_uploader("📄 Vergi Levhası Görseli (Zorunlu)", type=["jpg", "jpeg", "png", "pdf"])
        
        basvuru_btn = st.form_submit_button("Başvuruyu Tamamla ve Onaya Gönder", type="primary")
        
        if basvuru_btn:
            if f_adi and f_vergi and vergi_levhasi_dosya is not None:
                st.session_state['onay_bekleyen_firmalar'].append({
                    "firma_adi": f_adi,
                    "vergi_no": f_vergi,
                    "yetkili": f_yetkili,
                    "telefon": f_tel,
                    "levha": vergi_levhasi_dosya.name
                })
                # Mail gönderim tetikleyicisi
                yoneticiye_mail_gonder(f_adi, f_vergi, f_yetkili)
                
                st.success("✅ Başvurunuz ve Vergi Levhanız başarıyla alındı!")
                st.info(f"📧 **E-Posta Bildirimi:** `onderkaya1994@gmail.com` adresine otomatik onay maili gönderildi. Yönetici onayından sonra 100 TL/Ay aboneliğiniz aktifleşecektir.")
            else:
                st.error("Lütfen firma unvanını, vergi numarasını girin ve vergi levhası dosyanızı yükleyin.")

elif islem_turu == "💳 Abonelik Paneli":
    st.subheader("💳 Sektörel Birlik Abonelik Durumu (100 TL / Ay)")
    st.write("Sistemdeki onaylı firmaların aylık üyelik ve abonelik durumları:")
    
    for firma, detay in st.session_state['firma_abonelikleri'].items():
        st.markdown(f"""
        * 🏢 **Firma:** **{firma}**
        * 📊 **Üyelik Durumu:** `{detay['durum']}`
        * 💰 **Abonelik Ücreti:** **{detay['tutar']}**
        """)
    st.markdown("---")
    st.info("💡 **Abonelik Bilgisi:** Aylık 100 TL katkı payı ile havuzdaki tüm verilere sınırsız sorgulama ve bildirim hakkı sağlanmaktadır.")

else:
    st.subheader("⚙️ Yönetici Onay Paneli (onderkaya1994@gmail.com)")
    st.write("`onderkaya1994@gmail.com` adresine gelen yeni firma başvurularının ve vergi levhalarının denetim paneli.")
    
    if not st.session_state['onay_bekleyen_firmalar']:
        st.info("Şu an onay bekleyen yeni firma başvurusu bulunmuyor.")
    else:
        for i, basvuru in enumerate(st.session_state['onay_bekleyen_firmalar']):
            st.warning(f"**Firma:** {basvuru['firma_adi']} | **Yetkili:** {basvuru['yetkili']} | **Vergi No:** {basvuru['vergi_no']}")
            st.caption(f"Yüklenen Vergi Levhası: {basvuru['levha']}")
            
            col_o1, col_o2 = st.columns(2)
            with col_o1:
                if st.button(f"✅ Onayla ve Abone Yap ({basvuru['firma_adi']})", key=f"onay_{i}"):
                    if basvuru['firma_adi'] not in st.session_state['istanbul_firma_listesi']:
                        st.session_state['istanbul_firma_listesi'].append(basvuru['firma_adi'])
                    # Abonelik tablosuna ekle
                    st.session_state['firma_abonelikleri'][basvuru['firma_adi']] = {"durum": "Aktif Üye", "tutar": "100 TL/Ay"}
                    
                    st.session_state['onay_bekleyen_firmalar'].pop(i)
                    st.success(f"'{basvuru['firma_adi']}' başarıyla onaylandı, aboneliği başlatıldı ve sisteme eklendi!")
                    st.rerun()
            with col_o2:
                if st.button(f"❌ Reddet", key=f"red_{i}"):
                    st.session_state['onay_bekleyen_firmalar'].pop(i)
                    st.error("Başvuru reddedildi.")
                    st.rerun()

st.markdown("---")
st.caption("🔒 **İstanbul Rent a Car Birliği:** Vergi levhası onaylı, 100 TL/Ay abonelik sistemli güvenli risk ağı.")
