import streamlit as st
import time
import pandas as pd
import os
import json
import csv
import datetime
import random

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Barışalım mı?",
    layout="centered"
)

# --- CSS İLE GÖRSELLİK ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        background-color: #ffdee9;
        background-image: linear-gradient(0deg, #ffdee9 0%, #b5fffc 100%);
    }
    h1 {
        color: #ff6b6b;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    /* Evet butonlarını yeşil yapalım */
    div[data-testid="column"]:nth-of-type(1) button {
        background-color: #2ecc71;
        color: white;
    }
    div[data-testid="column"]:nth-of-type(2) button {
        background-color: #2ecc71;
        color: white;
    }
    /* Hayır butonunu kırmızı yapalım */
    div[data-testid="column"]:nth-of-type(3) button {
        background-color: #e74c3c;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- SESSION STATE ---
if 'page_state' not in st.session_state:
    st.session_state.page_state = 'soru'
if 'hayir_sayaci' not in st.session_state:
    st.session_state.hayir_sayaci = 0

# --- LOGLAMA FONKSİYONU ---
def barismayi_kaydet():
    """Barışma anını CSV ve JSON olarak kaydeder."""
    zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    veri = {"tarih": zaman, "durum": "Barisildi", "mesaj": "Seni Seviyorum"}
    
    # 1. CSV'ye Kayıt
    df = pd.DataFrame([veri])
    dosya_adi = "barisma_kayitlari.csv"
    
    if not os.path.exists(dosya_adi):
        df.to_csv(dosya_adi, index=False)
    else:
        df.to_csv(dosya_adi, mode='a', header=False, index=False)
        
    # 2. JSON'a Kayıt
    with open("barisma_log.json", "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False)

# --- SAYFA AKIŞI ---

if st.session_state.page_state == 'soru':
    # --- SORU EKRANI ---
    
    try:
        st.image("roblox_ani.png", caption="O güzel günlerin hatırına...", use_container_width=True)
    except:
        st.write("*(roblox_ani.png dosyası bulunamadı, ama hayal et)*")

    st.markdown("<h1>Barışalım mı artık?</h1>", unsafe_allow_html=True)
    
    st.write("") 
    st.write("") 

    # GÜNCELLENEN BUTONLAR (Mobil uyumlu ve emojisiz)
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Evet", key="btn_evet", use_container_width=True):
            st.session_state.page_state = 'baristik'
            st.rerun()

    with col2:
        if st.button("Kesinlikle", key="btn_kesinlikle", use_container_width=True):
            st.session_state.page_state = 'baristik'
            st.rerun()

    with col3:
        if st.button("Hayır", key=f"btn_hayir_{st.session_state.hayir_sayaci}", use_container_width=True):
            st.session_state.hayir_sayaci += 1
            st.toast("Bu buton bozuk! Basamazsın ki!", icon=None)
            time.sleep(0.5)
            st.rerun()

    if st.session_state.hayir_sayaci > 0:
        st.info(f"{st.session_state.hayir_sayaci} kere denedin ama 'Hayır' diyemezsin")

else:
    # --- SONUÇ EKRANI (BARIŞTIK) ---
    
    st.balloons()
    
    st.markdown("<h1 style='font-size: 3rem;'>oh beeeeeeee!</h1>", unsafe_allow_html=True)
    
    try:
        st.image("tavsan.png", use_container_width=True)
    except:
        st.error("Tavşan resmi (tavsan.png) klasörde yok!")

    st.success("Barışma anlaşması imzalandı ve veritabanına kaydedildi!")
    
    barismayi_kaydet()
    
    if st.button("Başa Dön"):
        st.session_state.page_state = 'soru'
        st.session_state.hayir_sayaci = 0
        st.rerun()