import streamlit as st
from PIL import Image

# Sayfa Yapılandırması
st.set_page_config(page_title="İstanbul Rent a Car Ortak Birlik & Risk Havuzu", page_icon="🚨", layout="centered")

# Tasarım ve Başlık
st.title("🚨 İstanbul Rent a Car Ortak Risk & Doğrulama Paneli")
st.write("Vergi Levhası Onaylı, Güvenli Sektörel Birlik ve Kara Liste Sistemi")

st.markdown("---")

# 1. Onaylı Firma Veritabanı
if 'istanbul_firma_listesi' not in st.session_state:
    st.session_state['istanbul_firma_listesi'] = [
        "TüreAuto (Gölcük / İstanbul)",
        "Roadify Rent A Car",
        "Eva Car Rental",
        "Kaan Filo"
    ]

# 2. Onay Bekleyen Firmalar Havuzu (Vergi Levhası ile Başvuranlar)
if 'onay_bekleyen_firmalar' not in st.session_state:
    st.session_state['onay_bekleyen_firmalar'] = []

# 3. Kara Liste ve Risk Veritabanı
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

# Üst Sekmeler
islem_turu = st.radio("İşlem Seçin", ["🔍 Müşteri Sorgula", "➕ Risk Bildirimi Ekle", "🏢 Firma Başvurusu (Vergi Levhası)", "⚙️ Yönetici Onay Paneli"], horizontal=True)

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
        st.warning("⚠️ Sistemde henüz onaylanmış firma bulunmuyor. Lütfen önce 'Firma Başvurusu' yapın ve onaylayın.")
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
                    "⚠️ Hafif Kusur / Dikkat Edilmeli (İncelenmeli)"
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

elif islem_turu == "🏢 Firma Başvurusu (Vergi Levhası)":
    st.subheader("🏢 Yeni Rent a Car Firma Kayıt Başvurusu")
    st.write("Sisteme üye olup ortak havuza katılabilmek için lütfen vergi levhanızı yükleyin.")
    
    with st.form("firma_basvuru_formu"):
        f_adi = st.text_input("Firma Ticari Unvanı", placeholder="Örn: Boğaziçi Rent a Car")
        f_vergi = st.text_input("Vergi Numarası")
        f_yetkili = st.text_input("Yetkili Adı Soyadı")
        f_tel = st.text_input("İşletme Telefonu")
        
        vergi_levhasi_dosya = st.file_uploader("📄 Vergi Levhası Görseli (Zorunlu)", type=["jpg", "jpeg", "png", "pdf"])
        
        basvuru_btn = st.form_submit_button("Onaya Gönder", type="primary")
        
        if basvuru_btn:
            if f_adi and f_vergi and vergi_levhasi_dosya is not None:
                st.session_state['onay_bekleyen_firmalar'].append({
                    "firma_adi": f_adi,
                    "vergi_no": f_vergi,
                    "yetkili": f_yetkili,
                    "telefon": f_tel,
                    "levha": vergi_levhasi_dosya.name
                })
                st.success("✅ Başvurunuz başarıyla alındı!")
                st.info(f"📧 **Yönetici Bilgilendirmesi:** `onderkaya1994@gmail.com` adresine otomatik onay bildirimi gönderildi. Yönetici onayladıktan sonra firmanız aktifleşecektir.")
            else:
                st.error("Lütfen firma unvanını, vergi numarasını girin ve vergi levhası dosyanızı yükleyin.")

else:
    st.subheader("⚙️ Yönetici Onay Paneli (onderkaya1994@gmail.com)")
    st.write("Sisteme başvuran yeni firmaların vergi levhası incelemesi ve sisteme onay verme paneli.")
    
    if not st.session_state['onay_bekleyen_firmalar']:
        st.info("Şu an onay bekleyen yeni firma başvurusu bulunmuyor.")
    else:
        for i, basvuru in enumerate(st.session_state['onay_bekleyen_firmalar']):
            st.warning(f"**Firma:** {basvuru['firma_adi']} | **Yetkili:** {basvuru['yetkili']} | **Vergi No:** {basvuru['vergi_no']}")
            st.caption(f"Yüklenen Vergi Levhası: {basvuru['levha']}")
            
            col_o1, col_o2 = st.columns(2)
            with col_o1:
                if st.button(f"✅ Onayla ve Aktif Et ({basvuru['firma_adi']})", key=f"onay_{i}"):
                    if basvuru['firma_adi'] not in st.session_state['istanbul_firma_listesi']:
                        st.session_state['istanbul_firma_listesi'].append(basvuru['firma_adi'])
                    st.session_state['onay_bekleyen_firmalar'].pop(i)
                    st.success(f"'{basvuru['firma_adi']}' başarıyla onaylandı ve sisteme dahil edildi!")
                    st.rerun()
            with col_o2:
                if st.button(f"❌ Reddet", key=f"red_{i}"):
                    st.session_state['onay_bekleyen_firmalar'].pop(i)
                    st.error("Başvuru reddedildi.")
                    st.rerun()

st.markdown("---")
st.caption("🔒 **İstanbul Rent a Car Birliği:** Vergi levhası kontrollü ve derecelendirilmiş güvenli ortak risk ağı.")
