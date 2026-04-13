# import cv2
# import numpy as np
# import threading
# import streamlit as st
# from tensorflow.keras.models import load_model
# from PIL import Image
# from playsound import playsound

# # ====== 1. Load models ======
# # Ensure these files are in the same folder as this script
# eye_model = load_model("eye_model.keras")
# yawn_model = load_model("yawn_model.keras")

# # ====== 2. Load Haar cascade ======
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# # ====== 3. Page setup ======
# st.set_page_config(page_title="Driver Drowsiness Detection", layout="wide")

# # ====== 4. Custom CSS ======
# st.markdown("""
#     <style>
#     .main-title {
#         text-align: center;
#         font-size: 50px;
#         font-weight: bold;
#         color: #FF0000;
#         margin-top: 20px;
#         margin-bottom: 20px;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # ====== 5. HERO / Landing Image ======
# try:
#     hero_image = Image.open(r"C:\Users\bhati\OneDrive\Desktop\DL_mini_project\hero image 1.png")
#     # ✅ FIX: Changed use_container_width=True to width="stretch"
#     st.image(hero_image, width="stretch")
# except:
#     st.warning("Hero image not found!")

# # ====== 6. App title ======
# st.markdown('<h1 class="main-title">🚦 Driver Drowsiness Detection App 🚦</h1>', unsafe_allow_html=True)

# # ====== 7. File uploader ======
# uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# # ====== 8. Play siren function ======
# def play_alarm():
#     # Using a raw string for the path to avoid escape character errors
#     alarm_path = r"C:\Users\bhati\OneDrive\Desktop\DL_mini_project\wefgf-warning-423632.mp3"
#     threading.Thread(target=lambda: playsound(alarm_path), daemon=True).start()

# # ====== 9. Detection logic ======

# if uploaded_file:
#     # Convert uploaded file to OpenCV format
#     file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
#     img = cv2.imdecode(file_bytes, 1)
    
#     # Convert BGR to RGB for display
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
#     # Grayscale for face detection
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.equalizeHist(gray)

#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60,60))

#     if len(faces) == 0:
#         st.warning("❌ No face detected!")
#         st.image(img_rgb, use_container_width=True)
#     else:
#         for (x, y, w, h) in faces:
#             face_section = img_rgb[y:y+h, x:x+w]

#             # 🔷 1. UPGRADED ROI (Calibrated to avoid eyebrows)
#             # Shifting y-coordinates down to catch the eyelids
#             eye_roi = face_section[int(h*0.28):int(h*0.52), int(w*0.20):int(w*0.80)]
#             mouth_roi = face_section[int(h*0.65):int(h*0.95), int(w*0.25):int(w*0.75)]

#             # Resize + Normalize
#             eye_img = cv2.resize(eye_roi, (64,64)).astype("float32") / 255.0
#             mouth_img = cv2.resize(mouth_roi, (64,64)).astype("float32") / 255.0

#             # --- Predictions ---
#             eye_val = float(eye_model.predict(np.expand_dims(eye_img, axis=0), verbose=0)[0][0])
#             yawn_val = float(yawn_model.predict(np.expand_dims(mouth_img, axis=0), verbose=0)[0][0])

#             # 🔥 2. UPGRADED COMBINED LOGIC (Weighted Ensemble)
#             # Higher Score = More Drowsy.
#             eye_danger_score = 1.0 - eye_val 
#             yawn_danger_score = yawn_val

#             # Giving Yawn model 70% weight because it's more accurate (83% vs 50%)
#             fatigue_score = (eye_danger_score * 0.3) + (yawn_danger_score * 0.7)

#             # --- Determine status ---
#             if fatigue_score > 0.40:
#                 status = "🚨 DROWSY"
#                 play_alarm()
#                 box_color = (255, 0, 0) # Red
#                 color_hex = "red"
#             else:
#                 status = "✅ SAFE"
#                 box_color = (0, 255, 0) # Green
#                 color_hex = "green"

#             # --- Display results ---
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.metric("Eye Score (Danger)", f"{eye_danger_score:.2f}")
#             with col2:
#                 st.metric("Yawn Score", f"{yawn_danger_score:.2f}")
#             with col3:
#                 st.metric("Total Fatigue", f"{fatigue_score:.2f}")
            
#             st.markdown(f"<h2 style='text-align:center; color:{color_hex}'>{status}</h2>", unsafe_allow_html=True)

#             # Draw boxes on the image
#             cv2.rectangle(img_rgb, (x, y), (x+w, y+h), box_color, 3)
#             # Draw ROI boxes specifically to show exactly what the model "saw"
#             cv2.rectangle(img_rgb, (x + int(w*0.20), y + int(h*0.28)), (x + int(w*0.80), y + int(h*0.52)), (255, 255, 0), 2)
            
#         st.image(img_rgb, caption="Processed Image", use_container_width=True)
# import cv2
# import numpy as np
# import threading
# import streamlit as st
# from tensorflow.keras.models import load_model
# from PIL import Image
# import io
# import time

# # ─────────────────────────────────────────────
# #  PAGE CONFIG  (must be first Streamlit call)
# # ─────────────────────────────────────────────
# st.set_page_config(
#     page_title="Driver Drowsiness Detection",
#     page_icon="🚗",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# # ─────────────────────────────────────────────
# #  GLOBAL CSS
# # ─────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@500&display=swap');

# /* ── Reset & Base ── */
# html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
# .block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1100px; }

# /* ── Hide default Streamlit chrome ── */
# #MainMenu, footer, header { visibility: hidden; }
# .stDeployButton { display: none; }

# /* ── Top header bar ── */
# .top-bar {
#     display: flex;
#     align-items: center;
#     gap: 16px;
#     padding: 1.2rem 1.6rem;
#     background: #fff;
#     border: 1px solid #E8E5DF;
#     border-radius: 16px;
#     margin-bottom: 1.6rem;
#     box-shadow: 0 1px 4px rgba(0,0,0,0.04);
# }
# .top-bar-icon {
#     width: 48px; height: 48px;
#     background: #FFF3E0;
#     border-radius: 12px;
#     display: flex; align-items: center; justify-content: center;
#     font-size: 24px;
# }
# .top-bar h1 {
#     font-size: 22px; font-weight: 600;
#     color: #1A1A1A; margin: 0; line-height: 1.2;
# }
# .top-bar p { font-size: 13px; color: #6B6B6B; margin: 0; margin-top: 2px; }

# /* ── Cards ── */
# .card {
#     background: #fff;
#     border: 1px solid #E8E5DF;
#     border-radius: 16px;
#     padding: 1.25rem 1.4rem;
#     margin-bottom: 1.2rem;
#     box-shadow: 0 1px 3px rgba(0,0,0,0.03);
# }
# .card-label {
#     font-size: 11px; font-weight: 600;
#     color: #9A9A9A; letter-spacing: 0.07em;
#     text-transform: uppercase; margin-bottom: 0.9rem;
# }

# /* ── Upload zone ── */
# [data-testid="stFileUploader"] {
#     background: #FAFAF8 !important;
#     border: 1.5px dashed #D0CCC4 !important;
#     border-radius: 12px !important;
#     padding: 1.5rem !important;
# }
# [data-testid="stFileUploader"]:hover { border-color: #E8850A !important; }
# [data-testid="stFileUploaderDropzoneInstructions"] { color: #6B6B6B !important; }

# /* ── Analyze button ── */
# .stButton > button {
#     width: 100%;
#     background: #E8850A !important;
#     color: white !important;
#     border: none !important;
#     border-radius: 10px !important;
#     padding: 0.65rem 1.5rem !important;
#     font-size: 15px !important;
#     font-weight: 600 !important;
#     font-family: 'DM Sans', sans-serif !important;
#     cursor: pointer !important;
#     transition: background 0.2s !important;
#     letter-spacing: 0.01em;
# }
# .stButton > button:hover { background: #CF7408 !important; }
# .stButton > button:disabled { background: #D3D1C7 !important; cursor: not-allowed !important; }

# /* ── Status banners ── */
# .status-safe {
#     display: flex; align-items: flex-start; gap: 12px;
#     background: #EAF3DE; border: 1px solid #97C459;
#     border-radius: 12px; padding: 1rem 1.2rem;
# }
# .status-drowsy {
#     display: flex; align-items: flex-start; gap: 12px;
#     background: #FCEBEB; border: 1px solid #F09595;
#     border-radius: 12px; padding: 1rem 1.2rem;
# }
# .status-neutral {
#     display: flex; align-items: flex-start; gap: 12px;
#     background: #F5F4F0; border: 1px solid #E0DDD5;
#     border-radius: 12px; padding: 1rem 1.2rem;
# }
# .status-icon { font-size: 20px; margin-top: 1px; }
# .status-title { font-size: 15px; font-weight: 600; }
# .safe-title { color: #3B6D11; }
# .drowsy-title { color: #A32D2D; }
# .neutral-title { color: #5A5A5A; }
# .status-desc { font-size: 12px; color: #6B6B6B; margin-top: 2px; }

# /* ── Score cards ── */
# .score-row { display: flex; gap: 12px; margin-bottom: 1rem; }
# .score-card {
#     flex: 1;
#     background: #F9F8F5;
#     border-radius: 10px;
#     padding: 0.85rem 1rem;
# }
# .score-card-label { font-size: 11px; color: #9A9A9A; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; }
# .score-card-value { font-size: 26px; font-weight: 600; color: #1A1A1A; font-family: 'DM Mono', monospace; margin: 4px 0 2px; }
# .score-card-sub { font-size: 11px; color: #6B6B6B; }

# /* ── Progress bars ── */
# .bar-wrap { margin-top: 0.5rem; }
# .bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
# .bar-label { font-size: 12px; color: #6B6B6B; width: 80px; flex-shrink: 0; }
# .bar-bg { flex: 1; height: 8px; background: #EDEBE5; border-radius: 4px; overflow: hidden; }
# .bar-val { font-size: 12px; font-weight: 500; color: #1A1A1A; width: 36px; text-align: right; font-family: 'DM Mono', monospace; }

# /* ── History rows ── */
# .hist-row {
#     display: flex; align-items: center; gap: 10px;
#     padding: 0.55rem 0;
#     border-bottom: 1px solid #F0EDE7;
# }
# .hist-row:last-child { border-bottom: none; }
# .hist-badge {
#     font-size: 11px; font-weight: 600;
#     padding: 3px 9px; border-radius: 20px; min-width: 56px; text-align: center;
# }
# .badge-safe { background: #EAF3DE; color: #3B6D11; }
# .badge-drowsy { background: #FCEBEB; color: #A32D2D; }
# .hist-scores { font-size: 12px; color: #6B6B6B; flex: 1; font-family: 'DM Mono', monospace; }
# .hist-time { font-size: 11px; color: #AAAAAA; }

# /* ── Alarm badge ── */
# .alarm-badge {
#     display: inline-flex; align-items: center; gap: 6px;
#     background: #FCEBEB; border: 1px solid #F09595;
#     border-radius: 8px; padding: 5px 12px;
#     font-size: 12px; color: #A32D2D; font-weight: 600;
#     margin-top: 8px;
# }
# </style>
# """, unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# #  SESSION STATE
# # ─────────────────────────────────────────────
# if "history" not in st.session_state:
#     st.session_state.history = []


# # ─────────────────────────────────────────────
# #  LOAD MODELS  (cached so they load once)
# # ─────────────────────────────────────────────
# @st.cache_resource
# def load_models():
#     eye_model  = load_model("eye_model.keras")
#     yawn_model = load_model("yawn_model.keras")
#     face_cascade = cv2.CascadeClassifier(
#         cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
#     )
#     return eye_model, yawn_model, face_cascade

# try:
#     eye_model, yawn_model, face_cascade = load_models()
#     models_loaded = True
# except Exception as e:
#     models_loaded = False
#     model_error = str(e)


# # ─────────────────────────────────────────────
# #  ALARM
# # ─────────────────────────────────────────────
# def play_alarm():
#     try:
#         from playsound import playsound
#         alarm_path = "wefgf-warning-423632.mp3"   # keep in same folder
#         threading.Thread(target=lambda: playsound(alarm_path), daemon=True).start()
#     except Exception:
#         pass   # alarm is optional — UI still works without it


# # ─────────────────────────────────────────────
# #  DETECTION
# # ─────────────────────────────────────────────
# def detect(img_bytes):
#     """Run face + eye + yawn detection on raw image bytes.
#     Returns a dict with keys: faces_found, results, annotated_img"""
#     file_arr = np.asarray(bytearray(img_bytes), dtype=np.uint8)
#     img_bgr  = cv2.imdecode(file_arr, 1)
#     img_rgb  = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
#     gray     = cv2.equalizeHist(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY))

#     faces = face_cascade.detectMultiScale(
#         gray, scaleFactor=1.1, minNeighbors=4, minSize=(50, 50)
#     )

#     if len(faces) == 0:
#         return {"faces_found": False, "results": [], "annotated_img": img_rgb}

#     results = []
#     for (x, y, w, h) in faces:
#         # Eye ROI
#         eye_roi = img_rgb[y + int(h*0.2):y + int(h*0.45),
#                           x + int(w*0.25):x + int(w*0.75)]
#         eye_in  = np.reshape(cv2.resize(eye_roi, (64, 64)) / 255.0, (1, 64, 64, 3))

#         # Mouth ROI
#         mouth_roi = img_rgb[y + int(h*0.65):y + int(h*0.9),
#                             x + int(w*0.3):x + int(w*0.7)]
#         mouth_in  = np.reshape(cv2.resize(mouth_roi, (64, 64)) / 255.0, (1, 64, 64, 3))

#         eye_val  = float(eye_model.predict(eye_in,   verbose=0)[0][0])
#         yawn_val = float(yawn_model.predict(mouth_in, verbose=0)[0][0])
#         drowsy   = eye_val < 0.2 or yawn_val > 0.5
#         color    = (220, 50, 50) if drowsy else (80, 180, 80)

#         # Annotate
#         cv2.rectangle(img_rgb, (x, y), (x+w, y+h), color, 2)
#         cv2.rectangle(img_rgb,
#                       (x+int(w*0.25), y+int(h*0.20)),
#                       (x+int(w*0.75), y+int(h*0.45)), color, 2)
#         cv2.rectangle(img_rgb,
#                       (x+int(w*0.30), y+int(h*0.65)),
#                       (x+int(w*0.70), y+int(h*0.90)), color, 2)
#         label = "DROWSY" if drowsy else "SAFE"
#         cv2.putText(img_rgb, label, (x, y - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

#         results.append({
#             "eye_val":  eye_val,
#             "yawn_val": yawn_val,
#             "drowsy":   drowsy,
#         })

#     return {"faces_found": True, "results": results, "annotated_img": img_rgb}


# # ─────────────────────────────────────────────
# #  UI  —  TOP BAR
# # ─────────────────────────────────────────────
# st.markdown("""
# <div class="top-bar">
#   <div class="top-bar-icon">🚗</div>
#   <div>
#     <h1>Driver Drowsiness Detection</h1>
#     <p>Upload a driver image to analyze alertness using deep learning</p>
#   </div>
# </div>
# """, unsafe_allow_html=True)

# # Model load error notice
# if not models_loaded:
#     st.error(f"⚠️ Could not load models: {model_error}. Make sure `eye_model.keras` and `yawn_model.keras` are in the same folder.")
#     st.stop()


# # ─────────────────────────────────────────────
# #  UI  —  MAIN LAYOUT
# # ─────────────────────────────────────────────
# left_col, right_col = st.columns([1, 1], gap="large")

# # ── LEFT: Upload + Analyze ──
# with left_col:
#     st.markdown('<div class="card"><div class="card-label">Upload image</div>', unsafe_allow_html=True)
#     uploaded = st.file_uploader(
#         label="Upload",
#         type=["jpg", "jpeg", "png"],
#         label_visibility="collapsed"
#     )
#     st.markdown("</div>", unsafe_allow_html=True)

#     analyze_clicked = st.button(
#         "Analyze image",
#         disabled=(uploaded is None),
#         use_container_width=True
#     )

#     # History card
#     st.markdown('<div class="card"><div class="card-label">Recent detections</div>', unsafe_allow_html=True)
#     if not st.session_state.history:
#         st.markdown('<p style="font-size:13px;color:#9A9A9A;padding:0.5rem 0;">No detections yet</p>', unsafe_allow_html=True)
#     else:
#         rows_html = ""
#         for h in st.session_state.history:
#             badge_cls = "badge-drowsy" if h["drowsy"] else "badge-safe"
#             badge_txt = "Drowsy" if h["drowsy"] else "Safe"
#             rows_html += f"""
#             <div class="hist-row">
#               <span class="hist-badge {badge_cls}">{badge_txt}</span>
#               <span class="hist-scores">Eye {h['eye']:.2f} · Yawn {h['yawn']:.2f}</span>
#               <span class="hist-time">{h['time']}</span>
#             </div>"""
#         st.markdown(rows_html, unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

# # ── RIGHT: Preview + Results ──
# with right_col:
#     st.markdown('<div class="card"><div class="card-label">Preview</div>', unsafe_allow_html=True)

#     if uploaded is None:
#         st.markdown("""
#         <div style="background:#F5F4F0;border-radius:12px;aspect-ratio:4/3;
#                     display:flex;align-items:center;justify-content:center;
#                     flex-direction:column;gap:8px;color:#AAAAAA;">
#           <div style="font-size:32px;">🖼️</div>
#           <div style="font-size:13px;">Image will appear here</div>
#         </div>""", unsafe_allow_html=True)

#         st.markdown("""
#         <div class="status-neutral" style="margin-top:1rem;">
#           <div class="status-icon">⏳</div>
#           <div>
#             <div class="status-title neutral-title">Awaiting analysis</div>
#             <div class="status-desc">Upload an image and click Analyze</div>
#           </div>
#         </div>""", unsafe_allow_html=True)

#     else:
#         img_bytes = uploaded.read()
#         pil_img   = Image.open(io.BytesIO(img_bytes))
#         st.image(pil_img, use_container_width=True)

#         if analyze_clicked:
#             with st.spinner("Running detection…"):
#                 result = detect(img_bytes)

#             if not result["faces_found"]:
#                 st.markdown("""
#                 <div class="status-neutral" style="margin-top:1rem;">
#                   <div class="status-icon">🔍</div>
#                   <div>
#                     <div class="status-title neutral-title">No face detected</div>
#                     <div class="status-desc">Try a clearer, front-facing image</div>
#                   </div>
#                 </div>""", unsafe_allow_html=True)
#             else:
#                 # Show annotated image
#                 st.image(result["annotated_img"], use_container_width=True, caption="Annotated result")

#                 for i, r in enumerate(result["results"]):
#                     eye_val  = r["eye_val"]
#                     yawn_val = r["yawn_val"]
#                     drowsy   = r["drowsy"]

#                     eye_pct  = int(eye_val  * 100)
#                     yawn_pct = int(yawn_val * 100)

#                     # Status banner
#                     if drowsy:
#                         play_alarm()
#                         st.markdown(f"""
#                         <div class="status-drowsy" style="margin-top:1rem;">
#                           <div class="status-icon">🚨</div>
#                           <div>
#                             <div class="status-title drowsy-title">Drowsy — Alert!</div>
#                             <div class="status-desc">Low eye openness or yawning detected</div>
#                           </div>
#                         </div>
#                         <div class="alarm-badge">🔔 Alarm triggered</div>
#                         """, unsafe_allow_html=True)
#                     else:
#                         st.markdown(f"""
#                         <div class="status-safe" style="margin-top:1rem;">
#                           <div class="status-icon">✅</div>
#                           <div>
#                             <div class="status-title safe-title">Driver is alert</div>
#                             <div class="status-desc">No signs of drowsiness detected</div>
#                           </div>
#                         </div>""", unsafe_allow_html=True)

#                     # Score cards
#                     eye_sub  = "Eyes closing" if eye_val < 0.2 else "Eyes open"
#                     yawn_sub = "Yawning detected" if yawn_val > 0.5 else "No yawn"
#                     st.markdown(f"""
#                     <div style="margin-top:1rem;">
#                       <div class="score-row">
#                         <div class="score-card">
#                           <div class="score-card-label">Eye openness</div>
#                           <div class="score-card-value">{eye_val:.3f}</div>
#                           <div class="score-card-sub">{eye_sub}</div>
#                         </div>
#                         <div class="score-card">
#                           <div class="score-card-label">Yawn score</div>
#                           <div class="score-card-value">{yawn_val:.3f}</div>
#                           <div class="score-card-sub">{yawn_sub}</div>
#                         </div>
#                       </div>
#                     </div>""", unsafe_allow_html=True)

#                     # Progress bars
#                     eye_bar_color  = "#E24B4A" if eye_val < 0.2 else "#639922"
#                     yawn_bar_color = "#E24B4A" if yawn_val > 0.5 else "#E8850A"
#                     st.markdown(f"""
#                     <div class="bar-wrap">
#                       <div class="bar-row">
#                         <span class="bar-label">Eyes open</span>
#                         <div class="bar-bg">
#                           <div style="width:{eye_pct}%;height:100%;background:{eye_bar_color};border-radius:4px;transition:width 0.6s;"></div>
#                         </div>
#                         <span class="bar-val">{eye_pct}%</span>
#                       </div>
#                       <div class="bar-row">
#                         <span class="bar-label">Yawning</span>
#                         <div class="bar-bg">
#                           <div style="width:{yawn_pct}%;height:100%;background:{yawn_bar_color};border-radius:4px;transition:width 0.6s;"></div>
#                         </div>
#                         <span class="bar-val">{yawn_pct}%</span>
#                       </div>
#                     </div>""", unsafe_allow_html=True)

#                     # Save to history
#                     ts = time.strftime("%H:%M")
#                     st.session_state.history.insert(0, {
#                         "drowsy": drowsy,
#                         "eye":    eye_val,
#                         "yawn":   yawn_val,
#                         "time":   ts,
#                     })
#                     if len(st.session_state.history) > 5:
#                         st.session_state.history.pop()

#                     st.rerun()   # refresh history panel

#         else:
#             st.markdown("""
#             <div class="status-neutral" style="margin-top:1rem;">
#               <div class="status-icon">⏳</div>
#               <div>
#                 <div class="status-title neutral-title">Ready to analyze</div>
#                 <div class="status-desc">Click Analyze image to run detection</div>
#               </div>
#             </div>""", unsafe_allow_html=True)

#     st.markdown("</div>", unsafe_allow_html=True)

import cv2
import numpy as np
import threading
import streamlit as st
from tensorflow.keras.models import load_model
from PIL import Image
import io
import time

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Driver Drowsiness Detection",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1120px; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Top bar ── */
.top-bar {
    display: flex; align-items: center; gap: 16px;
    padding: 1.2rem 1.6rem;
    background: #fff;
    border: 1px solid #E8E5DF;
    border-radius: 16px;
    margin-bottom: 1.6rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.top-bar-icon {
    width: 48px; height: 48px;
    background: #FFF3E0; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; flex-shrink: 0;
}
.top-bar h1 { font-size: 22px; font-weight: 600; color: #1A1A1A; margin: 0; line-height: 1.2; }
.top-bar p  { font-size: 13px; color: #6B6B6B; margin: 0; margin-top: 2px; }

/* ── Cards ── */
.card {
    background: #fff;
    border: 1px solid #E8E5DF;
    border-radius: 16px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}
.card-label {
    font-size: 11px; font-weight: 600;
    color: #9A9A9A; letter-spacing: 0.07em;
    text-transform: uppercase; margin-bottom: 0.9rem;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #FAFAF8 !important;
    border: 1.5px dashed #D0CCC4 !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
}
[data-testid="stFileUploader"]:hover { border-color: #E8850A !important; }

/* ── Analyze button ── */
.stButton > button {
    width: 100%;
    background: #E8850A !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.5rem !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.01em;
    transition: background 0.2s !important;
}
.stButton > button:hover    { background: #CF7408 !important; }
.stButton > button:disabled { background: #D3D1C7 !important; }

/* ── Status banners ── */
.status-safe {
    display: flex; align-items: flex-start; gap: 12px;
    background: #EAF3DE; border: 1px solid #97C459;
    border-radius: 12px; padding: 1rem 1.2rem;
}
.status-drowsy {
    display: flex; align-items: flex-start; gap: 12px;
    background: #FCEBEB; border: 1px solid #F09595;
    border-radius: 12px; padding: 1rem 1.2rem;
}
.status-neutral {
    display: flex; align-items: flex-start; gap: 12px;
    background: #F5F4F0; border: 1px solid #E0DDD5;
    border-radius: 12px; padding: 1rem 1.2rem;
}
.status-icon  { font-size: 20px; margin-top: 1px; }
.status-title { font-size: 15px; font-weight: 600; }
.safe-title   { color: #3B6D11; }
.drowsy-title { color: #A32D2D; }
.neutral-title{ color: #5A5A5A; }
.status-desc  { font-size: 12px; color: #6B6B6B; margin-top: 2px; }

/* ── Three-metric score cards ── */
.score-row { display: flex; gap: 10px; margin-bottom: 1rem; }
.score-card {
    flex: 1; background: #F9F8F5;
    border-radius: 10px; padding: 0.85rem 1rem;
    border-left: 3px solid #E0DDD5;
}
.score-card.danger-eye   { border-left-color: #E8850A; }
.score-card.danger-yawn  { border-left-color: #E24B4A; }
.score-card.fatigue      { border-left-color: #1A1A1A; }
.score-card-label { font-size: 11px; color: #9A9A9A; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; }
.score-card-value { font-size: 26px; font-weight: 600; color: #1A1A1A; font-family: 'DM Mono', monospace; margin: 4px 0 2px; }
.score-card-sub   { font-size: 11px; color: #6B6B6B; }

/* ── Fatigue gauge ── */
.gauge-wrap { margin: 1rem 0 0.5rem; }
.gauge-track {
    width: 100%; height: 14px;
    background: linear-gradient(to right, #EAF3DE 0%, #FAEEDA 45%, #FCEBEB 80%);
    border-radius: 7px; position: relative; overflow: visible;
    border: 1px solid #E0DDD5;
}
.gauge-needle {
    position: absolute; top: -5px;
    width: 4px; height: 24px;
    background: #1A1A1A; border-radius: 2px;
    transform: translateX(-50%);
    transition: left 0.5s cubic-bezier(.4,0,.2,1);
}
.gauge-labels {
    display: flex; justify-content: space-between;
    font-size: 10px; color: #9A9A9A;
    margin-top: 4px; font-family: 'DM Mono', monospace;
}
.gauge-title { font-size: 12px; color: #6B6B6B; margin-bottom: 6px; font-weight: 500; }

/* ── Progress bars ── */
.bar-wrap { margin-top: 0.75rem; }
.bar-row  { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.bar-label{ font-size: 12px; color: #6B6B6B; width: 90px; flex-shrink: 0; }
.bar-bg   { flex: 1; height: 8px; background: #EDEBE5; border-radius: 4px; overflow: hidden; }
.bar-val  { font-size: 12px; font-weight: 500; color: #1A1A1A; width: 36px; text-align: right; font-family: 'DM Mono', monospace; }

/* ── Threshold note ── */
.threshold-note {
    font-size: 11px; color: #9A9A9A; background: #F5F4F0;
    border-radius: 8px; padding: 7px 10px; margin-top: 0.75rem;
    font-family: 'DM Mono', monospace;
}

/* ── History rows ── */
.hist-row {
    display: flex; align-items: center; gap: 10px;
    padding: 0.55rem 0;
    border-bottom: 1px solid #F0EDE7;
}
.hist-row:last-child { border-bottom: none; }
.hist-badge {
    font-size: 11px; font-weight: 600;
    padding: 3px 9px; border-radius: 20px;
    min-width: 56px; text-align: center;
}
.badge-safe   { background: #EAF3DE; color: #3B6D11; }
.badge-drowsy { background: #FCEBEB; color: #A32D2D; }
.hist-scores  { font-size: 12px; color: #6B6B6B; flex: 1; font-family: 'DM Mono', monospace; }
.hist-time    { font-size: 11px; color: #AAAAAA; }

/* ── Alarm badge ── */
.alarm-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #FCEBEB; border: 1px solid #F09595;
    border-radius: 8px; padding: 5px 12px;
    font-size: 12px; color: #A32D2D; font-weight: 600;
    margin-top: 8px;
}

/* ── Weight info pill ── */
.weight-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: #FFF3E0; border: 1px solid #FAC775;
    border-radius: 8px; padding: 5px 12px;
    font-size: 11px; color: #854F0B; font-weight: 500;
    margin-bottom: 0.75rem; font-family: 'DM Mono', monospace;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []


# ─────────────────────────────────────────────
#  LOAD MODELS
# ─────────────────────────────────────────────
@st.cache_resource
def load_models():
    eye_model  = load_model("eye_model.keras")
    yawn_model = load_model("yawn_model.keras")
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    return eye_model, yawn_model, face_cascade

try:
    eye_model, yawn_model, face_cascade = load_models()
    models_loaded = True
except Exception as e:
    models_loaded = False
    model_error   = str(e)


# ─────────────────────────────────────────────
#  ALARM
# ─────────────────────────────────────────────
def play_alarm():
    try:
        from playsound import playsound
        threading.Thread(
            target=lambda: playsound("wefgf-warning-423632.mp3"), daemon=True
        ).start()
    except Exception:
        pass


# ─────────────────────────────────────────────
#  DETECTION  (matches your updated logic exactly)
# ─────────────────────────────────────────────
def detect(img_bytes):
    arr     = np.asarray(bytearray(img_bytes), dtype=np.uint8)
    img_bgr = cv2.imdecode(arr, 1)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    gray    = cv2.equalizeHist(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY))

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
    )

    if len(faces) == 0:
        return {"faces_found": False, "results": [], "annotated_img": img_rgb}

    results = []
    for (x, y, w, h) in faces:
        face_section = img_rgb[y:y+h, x:x+w]

        # Calibrated ROIs (your updated coords)
        eye_roi   = face_section[int(h*0.28):int(h*0.52), int(w*0.20):int(w*0.80)]
        mouth_roi = face_section[int(h*0.65):int(h*0.95), int(w*0.25):int(w*0.75)]

        eye_img   = cv2.resize(eye_roi,   (64, 64)).astype("float32") / 255.0
        mouth_img = cv2.resize(mouth_roi, (64, 64)).astype("float32") / 255.0

        eye_val  = float(eye_model.predict( np.expand_dims(eye_img,   0), verbose=0)[0][0])
        yawn_val = float(yawn_model.predict(np.expand_dims(mouth_img, 0), verbose=0)[0][0])

        # Weighted ensemble (70% yawn, 30% eye)
        eye_danger  = 1.0 - eye_val
        yawn_danger = yawn_val
        fatigue     = (eye_danger * 0.3) + (yawn_danger * 0.7)

        drowsy      = fatigue > 0.40
        box_color   = (220, 50, 50) if drowsy else (80, 180, 80)
        roi_color   = (255, 220, 50)

        # Face box
        cv2.rectangle(img_rgb, (x, y), (x+w, y+h), box_color, 3)
        # Eye ROI box (yellow)
        cv2.rectangle(img_rgb,
                      (x + int(w*0.20), y + int(h*0.28)),
                      (x + int(w*0.80), y + int(h*0.52)), roi_color, 2)
        # Label
        label = "DROWSY" if drowsy else "SAFE"
        cv2.putText(img_rgb, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, box_color, 2)

        results.append({
            "eye_val":    eye_val,
            "yawn_val":   yawn_val,
            "eye_danger": eye_danger,
            "yawn_danger":yawn_danger,
            "fatigue":    fatigue,
            "drowsy":     drowsy,
        })

    return {"faces_found": True, "results": results, "annotated_img": img_rgb}


# ─────────────────────────────────────────────
#  UI — TOP BAR
# ─────────────────────────────────────────────
st.markdown("""
<div class="top-bar">
  <div class="top-bar-icon">🚗</div>
  <div>
    <h1>Driver Drowsiness Detection</h1>
    <p>Weighted ensemble model — Eye danger (30%) + Yawn score (70%) · Threshold 0.40</p>
  </div>
</div>
""", unsafe_allow_html=True)

if not models_loaded:
    st.error(f"⚠️ Could not load models: {model_error}\n\nMake sure `eye_model.keras` and `yawn_model.keras` are in the same folder.")
    st.stop()


# ─────────────────────────────────────────────
#  UI — LAYOUT
# ─────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="large")

# ── LEFT column ──
with left_col:
    st.markdown('<div class="card"><div class="card-label">Upload image</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        label="Upload", type=["jpg", "jpeg", "png"], label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    analyze_clicked = st.button(
        "Analyze image", disabled=(uploaded is None), use_container_width=True
    )

    # History
    st.markdown('<div class="card"><div class="card-label">Recent detections</div>', unsafe_allow_html=True)
    if not st.session_state.history:
        st.markdown('<p style="font-size:13px;color:#9A9A9A;padding:0.5rem 0;text-align:center;">No detections yet</p>', unsafe_allow_html=True)
    else:
        rows = ""
        for h in st.session_state.history:
            bc = "badge-drowsy" if h["drowsy"] else "badge-safe"
            bt = "Drowsy" if h["drowsy"] else "Safe"
            rows += f"""
            <div class="hist-row">
              <span class="hist-badge {bc}">{bt}</span>
              <span class="hist-scores">F:{h['fatigue']:.2f} E:{h['eye_d']:.2f} Y:{h['yawn_d']:.2f}</span>
              <span class="hist-time">{h['time']}</span>
            </div>"""
        st.markdown(rows, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── RIGHT column ──
with right_col:
    st.markdown('<div class="card"><div class="card-label">Preview & Results</div>', unsafe_allow_html=True)

    if uploaded is None:
        st.markdown("""
        <div style="background:#F5F4F0;border-radius:12px;aspect-ratio:4/3;
                    display:flex;align-items:center;justify-content:center;
                    flex-direction:column;gap:8px;color:#AAAAAA;">
          <div style="font-size:32px;">🖼️</div>
          <div style="font-size:13px;">Image will appear here</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class="status-neutral" style="margin-top:1rem;">
          <div class="status-icon">⏳</div>
          <div>
            <div class="status-title neutral-title">Awaiting analysis</div>
            <div class="status-desc">Upload an image and click Analyze</div>
          </div>
        </div>""", unsafe_allow_html=True)

    else:
        img_bytes = uploaded.read()
        st.image(Image.open(io.BytesIO(img_bytes)), use_container_width=True)

        if analyze_clicked:
            with st.spinner("Running weighted ensemble detection…"):
                result = detect(img_bytes)

            if not result["faces_found"]:
                st.markdown("""
                <div class="status-neutral" style="margin-top:1rem;">
                  <div class="status-icon">🔍</div>
                  <div>
                    <div class="status-title neutral-title">No face detected</div>
                    <div class="status-desc">Try a clearer, front-facing image with good lighting</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.image(result["annotated_img"], use_container_width=True, caption="Annotated output")

                for r in result["results"]:
                    eye_d   = r["eye_danger"]
                    yawn_d  = r["yawn_danger"]
                    fatigue = r["fatigue"]
                    drowsy  = r["drowsy"]

                    # Status banner
                    if drowsy:
                        play_alarm()
                        st.markdown("""
                        <div class="status-drowsy" style="margin-top:1rem;">
                          <div class="status-icon">🚨</div>
                          <div>
                            <div class="status-title drowsy-title">Drowsy — Alert!</div>
                            <div class="status-desc">Fatigue score exceeded threshold (> 0.40)</div>
                          </div>
                        </div>
                        <div class="alarm-badge">🔔 Alarm triggered</div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="status-safe" style="margin-top:1rem;">
                          <div class="status-icon">✅</div>
                          <div>
                            <div class="status-title safe-title">Driver is alert</div>
                            <div class="status-desc">Fatigue score is within safe range (≤ 0.40)</div>
                          </div>
                        </div>""", unsafe_allow_html=True)

                    # Weight info pill
                    st.markdown("""
                    <div class="weight-pill" style="margin-top:0.75rem;">
                      ⚖️ Eye danger × 0.30 &nbsp;+&nbsp; Yawn score × 0.70
                    </div>""", unsafe_allow_html=True)

                    # Three score cards
                    eye_sub  = "Eyes closing" if eye_d > 0.8 else ("Partial" if eye_d > 0.5 else "Eyes open")
                    yawn_sub = "Yawning" if yawn_d > 0.5 else "No yawn"
                    fat_sub  = "DROWSY" if fatigue > 0.40 else "Safe"
                    fat_color = "#A32D2D" if fatigue > 0.40 else "#3B6D11"

                    st.markdown(f"""
                    <div class="score-row">
                      <div class="score-card danger-eye">
                        <div class="score-card-label">Eye danger (30%)</div>
                        <div class="score-card-value">{eye_d:.3f}</div>
                        <div class="score-card-sub">{eye_sub}</div>
                      </div>
                      <div class="score-card danger-yawn">
                        <div class="score-card-label">Yawn score (70%)</div>
                        <div class="score-card-value">{yawn_d:.3f}</div>
                        <div class="score-card-sub">{yawn_sub}</div>
                      </div>
                      <div class="score-card fatigue">
                        <div class="score-card-label">Total fatigue</div>
                        <div class="score-card-value" style="color:{fat_color};">{fatigue:.3f}</div>
                        <div class="score-card-sub">{fat_sub}</div>
                      </div>
                    </div>""", unsafe_allow_html=True)

                    # Fatigue gauge
                    needle_pct = min(fatigue * 100, 100)
                    st.markdown(f"""
                    <div class="gauge-wrap">
                      <div class="gauge-title">Fatigue gauge — threshold at 0.40</div>
                      <div class="gauge-track">
                        <div class="gauge-needle" style="left:{needle_pct}%;"></div>
                      </div>
                      <div class="gauge-labels">
                        <span>0.00</span><span>0.20</span>
                        <span style="color:#E24B4A;font-weight:600;">▲ 0.40</span>
                        <span>0.70</span><span>1.00</span>
                      </div>
                    </div>""", unsafe_allow_html=True)

                    # Progress bars
                    eye_pct  = int(eye_d  * 100)
                    yawn_pct = int(yawn_d * 100)
                    fat_pct  = int(fatigue * 100)
                    eye_bar_color  = "#E24B4A" if eye_d > 0.8 else "#E8850A" if eye_d > 0.5 else "#639922"
                    yawn_bar_color = "#E24B4A" if yawn_d > 0.5 else "#E8850A"
                    fat_bar_color  = "#E24B4A" if fatigue > 0.40 else "#639922"

                    st.markdown(f"""
                    <div class="bar-wrap">
                      <div class="bar-row">
                        <span class="bar-label">Eye danger</span>
                        <div class="bar-bg"><div style="width:{eye_pct}%;height:100%;background:{eye_bar_color};border-radius:4px;"></div></div>
                        <span class="bar-val">{eye_pct}%</span>
                      </div>
                      <div class="bar-row">
                        <span class="bar-label">Yawn score</span>
                        <div class="bar-bg"><div style="width:{yawn_pct}%;height:100%;background:{yawn_bar_color};border-radius:4px;"></div></div>
                        <span class="bar-val">{yawn_pct}%</span>
                      </div>
                      <div class="bar-row">
                        <span class="bar-label">Total fatigue</span>
                        <div class="bar-bg"><div style="width:{fat_pct}%;height:100%;background:{fat_bar_color};border-radius:4px;"></div></div>
                        <span class="bar-val">{fat_pct}%</span>
                      </div>
                    </div>
                    <div class="threshold-note">Drowsy if fatigue &gt; 0.40 &nbsp;|&nbsp; fatigue = (1−eye)×0.30 + yawn×0.70</div>
                    """, unsafe_allow_html=True)

                    # Save to history
                    st.session_state.history.insert(0, {
                        "drowsy":  drowsy,
                        "fatigue": fatigue,
                        "eye_d":   eye_d,
                        "yawn_d":  yawn_d,
                        "time":    time.strftime("%H:%M"),
                    })
                    if len(st.session_state.history) > 5:
                        st.session_state.history.pop()

                    st.rerun()

        else:
            st.markdown("""
            <div class="status-neutral" style="margin-top:1rem;">
              <div class="status-icon">⏳</div>
              <div>
                <div class="status-title neutral-title">Ready to analyze</div>
                <div class="status-desc">Click Analyze image to run the ensemble model</div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)