import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Rent a Car Ortak Kara Liste", page_icon="🚨", layout="centered")

# Tasarım ve Başlık
st.title("🚨 Rent a Car & Galeri Ortak Risk Paneli")
st.write("Sorunlu kiracıları önceden tespit edin, araçlarınızı ve işletmenizi güvenceye alın.")

st.markdown("---")

# Hafızada örnek bir kara liste veritabanı (Gerçek kullanımda bu kısım bulut veritabanına bağlanır)
if 'kara_liste' not in st.session_state:
    st.session_state['kara_liste'] = [
        {"tc": "11111111110", "ad": "Ahmet Yılmaz", "telefon": "0532 000 00 01", "sebep": "Aracı sözleşme dışı kullandı, hasarlı teslim etti ve ödemeden kaçtı."},
        {"tc": "22222222220", "ad": "Mehmet Demir", "telefon": "0533 111 11 02", "sebep": "Kira bedelini ödemedi, araç 3 gün gecikmeli ve icralık olarak teslim alındı."}
    ]

# Sekmeler (Sorgulama ve Ekleme)
islem_turu = st.radio("İşlem Seçin", ["🔍 Müşteri Sorgula (Risk Kontrol)", "➕ Kara Listeye Yeni Kişi Ekle"], horizontal=True)

st.markdown("---")

if islem_turu == "🔍 Müşteri Sorgula (Risk Kontrol)":
    st.subheader("🕵️ Müşteri Risk Sorgulama")
    st.write("Kiralama yapmadan önce müşterinin T.C. Kimlik veya Telefon numarasını kontrol edin.")
    
    aranan_kriter = st.text_input("T.C. Kimlik No veya Telefon Numarası ile Ara")
    
    if st.button("Sorgula", type="primary", use_container_width=True):
        if not aranan_kriter:
            st.warning("Lütfen sorgulamak için bir T.C. veya telefon girin.")
        else:
            bulunanlar = [k for k in st.session_state['kara_liste'] if aranan_kriter in k['tc'] or aranan_kriter in k['telefon']]
            
            if bulunanlar:
                st.error("🚨 DİKKAT! Bu kişi kara listede kayıtlı!")
                for kayit in bulunanlar:
                    st.markdown(f"""
                    * **Ad Soyad:** {kayit['ad']}
                    * **T.C. No:** {kayit['tc']}
                    * **Telefon:** {kayit['telefon']}
                    * **⚠️ Risk Gerekçesi:** **{kayit['sebep']}**
                    """)
                st.error("❌ **Tavsiye:** Bu kişiye araç KİRALAMAYIN!")
            else:
                st.success("✅ Temiz! Bu kriterle eşleşen aktif bir kara liste kaydı bulunamadı. Kiralama yapılabilir.")

else:
    st.subheader("➕ Kara Listeye Ekleme Paneli")
    st.write("Sorun yaratan, ödeme yapmayan veya araca zarar veren kişileri sisteme bildirin.")
    
    with st.form("kara_liste_form"):
        yeni_ad = st.text_input("Müşterinin Adı Soyadı")
        yeni_tc = st.text_input("T.C. Kimlik Numarası (11 Hane)")
        yeni_tel = st.text_input("Telefon Numarası")
        yeni_sebep = st.text_area("Yaşanan Sorun / Kara Liste Gerekçesi", placeholder="Örn: Kirayı ödemedi, telefonları açmıyor...")
        
        submit_button = st.form_submit_button("🚨 Sistemi Uyar ve Kara Listeye Ekle", type="primary")
        
        if submit_button:
            if yen_ad := yeni_ad and yeni_tc and yeni_sebep:
                yeni_kayit = {
                    "tc": yeni_tc,
                    "ad": yeni_ad,
                    "telefon": yeni_tel,
                    "sebep": yeni_sebep
                }
                st.session_state['kara_liste'].append(yeni_kayit)
                st.success(f"başarıyla eklendi! Artık bu kişi sistemde riskli olarak görünecek.")
            else:
                st.error("Lütfen en azından Ad, T.C. ve Gerekçe alanlarını doldurun.")

st.markdown("---")
st.caption("🔒 **TüreAuto Güvenlik Altyapısı:** Sektörel yardımlaşma ve ortak risk minimizasyon paneli.")
