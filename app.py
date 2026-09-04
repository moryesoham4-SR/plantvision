import io
import os
import json
from pathlib import Path
from PIL import Image
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import base64
import config
import database
import auth
from preprocessor import preprocess_image, validate_leaf_image


try:
    from preprocessor import image_to_base64
except Exception:
    def image_to_base64(img: Image.Image, max_dim: int = 400, quality: int = 80) -> str:
        try:
            thumb = img.copy()
            thumb.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
            if thumb.mode != "RGB":
                thumb = thumb.convert("RGB")
            buffered = io.BytesIO()
            thumb.save(buffered, format="JPEG", quality=quality, optimize=True)
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return f"data:image/jpeg;base64,{img_str}"
        except Exception:
            return ""

from report_generator import generate_pdf_report
from data.disease_library import DISEASE_KNOWLEDGE_BASE


from models.potato_model import predict_potato
from models.tomato_model import predict_tomato
from models.apple_model import predict_apple

# 1. Page Configuration
st.set_page_config(
    page_title="PlantVision AI — Plant Pathology System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database & Session
database.init_db()
auth.init_auth_state()

# Session State Variables
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "auth_view" not in st.session_state:
    st.session_state.auth_view = "login"

# 2. Dynamic CSS Loading & Theme Engine
chart_theme = "plotly_dark" if st.session_state.dark_mode else "plotly_white"

css_file = config.STATIC_DIR / "style.css"
if css_file.exists():
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Dynamic Light Theme Override when toggled off
if not st.session_state.dark_mode:
    light_override_css = """
    <style>
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }
    header[data-testid="stHeader"] {
        background-color: #F8FAFC !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #0F172A !important;
    }
    .stMarkdown, .stText, p, span, label, h1, h2, h3, h4, h5, h6 {
        color: #0F172A !important;
    }
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 0.75rem !important;
    }
    div[data-testid="stExpander"] summary {
        color: #0F172A !important;
    }
    div[data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 1rem !important;
        padding: 1.5rem !important;
    }
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #0F172A !important;
    }
    div[data-testid="stFileUploader"] section {
        background-color: #FFFFFF !important;
        border: 1px dashed #CBD5E1 !important;
    }
    div[data-testid="stFileUploader"] span, div[data-testid="stFileUploader"] small {
        color: #64748B !important;
    }
    div[data-testid="stFileUploader"] button {
        background-color: #059669 !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 700 !important;
    }
    div[data-testid="stFileUploader"] button * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
    }
    div[data-testid="stTabs"] button[role="tab"] {
        color: #64748B !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #059669 !important;
        border-bottom-color: #059669 !important;
    }
    div[data-testid="stToggle"] div[role="switch"] {
        background-color: #CBD5E1 !important;
        border: 2px solid #94A3B8 !important;
    }
    div[data-testid="stToggle"] div[role="switch"][aria-checked="true"] {
        background-color: #059669 !important;
        border-color: #047857 !important;
    }
    div[data-testid="stToggle"] div[role="switch"] div {
        background-color: #FFFFFF !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25) !important;
    }
    div[data-testid="stToggle"] label,
    div[data-testid="stToggle"] p,
    div[data-testid="stToggle"] span {
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    .kpi-card {
        background-color: #FFFFFF !important;
        border-color: #E2E8F0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    .kpi-val {
        color: #0F172A !important;
    }
    .kpi-label {
        color: #64748B !important;
    }

    .diagnosis-healthy {
        background-color: #ECFDF5 !important;
        color: #065F46 !important;
        border-left-color: #10B981 !important;
    }
    .diagnosis-moderate {
        background-color: #FFFBEB !important;
        color: #92400E !important;
        border-left-color: #F59E0B !important;
    }
    .diagnosis-severe {
        background-color: #FEF2F2 !important;
        color: #991B1B !important;
        border-left-color: #EF4444 !important;
    }
    </style>
    """
    st.markdown(light_override_css, unsafe_allow_html=True)



# 3. Authentication Routing
if not auth.is_authenticated():
    st.markdown("""
        <div class="main-header">
            <h1>🌿 PlantVision AI</h1>
            <p>Computer Vision-Powered Plant Disease Detection & Treatment System</p>
        </div>
    """, unsafe_allow_html=True)

    # Centered Single-Form Authentication Card
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        # ====== VIEW 1: SIGN IN ======
        if st.session_state.auth_view == "login":
            st.markdown("### 🔐 Sign In to Your Account")
            st.caption("Enter your credentials to access your crop diagnostic scanner and personal scan logs.")
            
            with st.form("login_form"):
                login_username = st.text_input("Username or Email", placeholder="e.g. farmer_john or john@plantvision.ai")
                login_password = st.text_input("Password", type="password", placeholder="••••••••")
                submit_login = st.form_submit_button("🚀 Sign In", type="primary", use_container_width=True)

                if submit_login:
                    if not login_username or not login_password:
                        st.error("Please fill in both username/email and password.")
                    else:
                        success, msg = auth.login(login_username, login_password)
                        if success:
                            st.success("Signed in successfully! Loading dashboard...")
                            st.rerun()
                        else:
                            st.error(msg)

            st.markdown("---")
            st.markdown("<p style='text-align: center; color: #94a3b8;'>Don't have an account yet?</p>", unsafe_allow_html=True)
            if st.button("📝 Create New Account", use_container_width=True):
                st.session_state.auth_view = "register"
                st.rerun()

            # Demo hint
            st.info("💡 **Quick Demo Login:** Username: `farmer_john` | Password: `password123`")

        # ====== VIEW 2: REGISTER (WITH INSTANT AUTO-LOGIN) ======
        else:
            st.markdown("### 📝 Create New Account")
            st.caption("Register now to save scan records, view analytics, and generate treatment reports.")

            with st.form("register_form"):
                reg_name = st.text_input("Full Name", placeholder="e.g. John Doe")
                reg_username = st.text_input("Username", placeholder="e.g. farmer_john")
                reg_email = st.text_input("Email Address", placeholder="john@example.com")
                reg_password = st.text_input("Password", type="password", placeholder="••••••••")
                reg_password_confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••")
                
                submit_reg = st.form_submit_button("🌱 Register & Sign In", type="primary", use_container_width=True)

                if submit_reg:
                    if not reg_name or not reg_username or not reg_email or not reg_password:
                        st.error("All fields are required.")
                    elif reg_password != reg_password_confirm:
                        st.error("Passwords do not match. Please verify your password.")
                    elif len(reg_password) < 6:
                        st.error("Password must be at least 6 characters long.")
                    else:
                        success, uid, msg = database.register_user(reg_username, reg_name, reg_email, reg_password)
                        if success and uid:
                            # Instant Auto-Login on Registration
                            auth.set_user_session({
                                "id": uid,
                                "username": reg_username.strip().lower(),
                                "full_name": reg_name.strip(),
                                "email": reg_email.strip().lower()
                            })
                            st.success(f"🎉 Welcome aboard, {reg_name}! Your account is created in Supabase Cloud and you are logged in.")
                            st.rerun()
                        else:
                            st.error(msg)


            st.markdown("---")
            st.markdown("<p style='text-align: center; color: #94a3b8;'>Already registered?</p>", unsafe_allow_html=True)
            if st.button("⬅️ Back to Sign In", use_container_width=True):
                st.session_state.auth_view = "login"
                st.rerun()

    st.stop()

# 4. Authenticated Sidebar Navigation
user = auth.get_current_user()

with st.sidebar:
    st.markdown(f"### 👤 **{user['full_name']}**")
    st.caption(f"@{user['username']} • {user['email']}")
    st.markdown("---")

    
    selected_page = st.radio(
        "Navigation Menu",
        [
            "🔬 Disease Scanner",
            "📜 Scan History",
            "📊 Analytics Dashboard",
            "📚 Disease Library",
            "⚙️ Settings & Info"
        ],
        index=0
    )
    
    st.markdown("---")
    if config.USE_MOCK:
        st.caption("🟢 **Inference Engine:** Active")
    else:
        st.caption("⚡ **Inference Engine:** Live Weights")
        
    if st.button("🚪 Log Out", use_container_width=True):
        auth.logout()

# 5. Application Pages

# ----------------- PAGE 1: SCANNER -----------------
if selected_page == "🔬 Disease Scanner":
    st.markdown("""
        <div class="main-header">
            <h1>🔬 Plant Disease Scanner</h1>
            <p>Upload or snap a leaf photo for instant deep learning disease diagnosis.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.markdown("#### 1. Select Target Plant *(Compulsory)*")
        plant_options = {
            "none": "⚠️ -- Select Target Plant (Compulsory) --",
            "potato": "🥔 Potato (Solanum tuberosum) - Ready",
            "tomato": "🍅 Tomato (Solanum lycopersicum) - Ready",
            "apple": "🍎 Apple (Malus domestica) - Coming Soon ⏳"
        }
        selected_plant_id = st.selectbox(
            "Target Plant",
            options=list(plant_options.keys()),
            format_func=lambda x: plant_options[x]
        )
        
        uploaded_image = None
        sample_name = ""
        scan_btn = False

        if selected_plant_id == "none":
            st.warning("🌱 **Selecting a target plant is compulsory.** Please choose **Potato** or **Tomato** from the dropdown above to enable the scanner.")
        elif selected_plant_id == "apple":
            st.info("🍎 **Apple Disease Model is Coming Soon ⏳**\n\nOur deep learning neural networks for Apple Scab, Black Rot, and Cedar Apple Rust are currently under active training.\n\nPlease select **🥔 Potato** or **🍅 Tomato** for instant live diagnosis.")
        else:
            st.markdown("#### 2. Input Leaf Image")
            input_mode = st.radio(
                "Choose Input Method:",
                ["📁 Upload Image File", "📷 Live Camera Snap", "⚡ 1-Click Test Samples"],
                horizontal=True
            )
            
            if input_mode == "📁 Upload Image File":
                file_upload = st.file_uploader(
                    "Upload leaf photo (JPG, JPEG, PNG, WEBP, BMP, TIFF, GIF):",
                    type=["jpg", "jpeg", "png", "webp", "bmp", "tiff", "gif", "jfif"],
                    help="Supports all major image formats (JPEG, PNG, WebP, BMP, TIFF). Image will be automatically resized & normalized to 224x224 RGB."
                )
                if file_upload is not None:
                    uploaded_image = file_upload
                    sample_name = file_upload.name
            elif input_mode == "📷 Live Camera Snap":
                cam_upload = st.camera_input("Take a clear photo of the plant leaf:")
                if cam_upload is not None:
                    uploaded_image = cam_upload
                    sample_name = "live_camera_leaf.jpg"
            else:
                # 1-Click Samples
                sample_choices = {
                    "potato": [
                        ("Early Blight", "potato_early_blight.jpg"),
                        ("Late Blight", "potato_late_blight.jpg"),
                        ("Healthy", "potato_healthy.jpg")
                    ],
                    "tomato": [
                        ("Early Blight", "tomato_early_blight.jpg"),
                        ("Late Blight", "tomato_late_blight.jpg"),
                        ("Healthy", "tomato_healthy.jpg")
                    ]
                }
                
                samples = sample_choices.get(selected_plant_id, [])
                sample_label = st.selectbox(
                    "Pick a pre-configured sample condition:",
                    options=[s[0] for s in samples]
                )
                
                selected_sample_file = next((s[1] for s in samples if s[0] == sample_label), None)
                sample_path = config.SAMPLES_DIR / selected_sample_file if selected_sample_file else None
                
                if sample_path and sample_path.exists():
                    uploaded_image = Image.open(sample_path)
                    sample_name = selected_sample_file
                else:
                    # Synthetic sample preview
                    uploaded_image = Image.new("RGB", (300, 300), color=(46, 139, 87))
                    sample_name = selected_sample_file or "sample_leaf.jpg"
                    
            if uploaded_image is not None:
                display_img, resized_img, tensor_input, meta = preprocess_image(uploaded_image)
                st.image(display_img, caption=f"Input Image (Preprocessed to {meta['processed_size'][0]}x{meta['processed_size'][1]} RGB)", use_container_width=True)
                
                # Leaf & Foliage Authenticity Check
                is_leaf, leaf_msg, leaf_meta = validate_leaf_image(display_img)
                if not is_leaf:
                    st.warning(leaf_msg)
                    st.session_state.current_result = None
                    scan_btn = False
                else:
                    st.success("🌿 Plant leaf verified. Ready for pathological diagnosis!")
                    scan_btn = st.button("🚀 Analyze & Diagnose Leaf", type="primary", use_container_width=True)
            else:
                st.info("Please upload an image, snap a photo, or pick a sample leaf to begin scanning.")
                is_leaf = False



    with col_right:
        st.markdown("#### 3. AI Diagnosis & Prescription")
        
        if uploaded_image is not None and scan_btn:
            with st.spinner(f"Running inference with {config.PLANTS[selected_plant_id]['name']} Model..."):
                # Route to plant-specific model
                if selected_plant_id == "potato":
                    result = predict_potato(tensor_input, sample_name)
                elif selected_plant_id == "tomato":
                    result = predict_tomato(tensor_input, sample_name)
                else:
                    result = predict_apple(tensor_input, sample_name)
                
                # Convert leaf image to compact Base64 JPEG Data URL for Supabase storage
                img_b64 = image_to_base64(display_img)
                
                # Also cache locally
                save_filename = f"scan_{user['id']}_{int(meta['processed_size'][0])}_{selected_plant_id}_{sample_name.replace(' ', '_')}.jpg"
                save_path = config.UPLOAD_DIR / save_filename
                try:
                    display_img.save(save_path)
                except Exception:
                    save_path = str(save_path)
                
                # Persist scan (with Base64 image data) to Supabase Cloud & SQLite
                scan_id = database.save_scan(
                    user_id=user["id"],
                    plant=result["plant_name"],
                    disease=result["predicted_disease"],
                    confidence=result["confidence"],
                    severity=result["severity"],
                    is_healthy=result["is_healthy"],
                    image_path=img_b64 if img_b64 else str(save_path),
                    symptoms=result["symptoms"],
                    remedies=result["remedies"]
                )
                
                st.session_state.current_result = result
                st.session_state.current_scan_id = scan_id
                st.session_state.current_img_path = str(save_path)

                
        if st.session_state.get("current_result") is not None:
            res = st.session_state.current_result
            
            # Severity color class
            sev = res["severity"]
            box_class = "diagnosis-healthy" if res["is_healthy"] else ("diagnosis-moderate" if sev == "Moderate" else "diagnosis-severe")
            badge_class = "badge-healthy" if res["is_healthy"] else ("badge-moderate" if sev == "Moderate" else "badge-severe")
            
            st.markdown(f"""
                <div class="diagnosis-box {box_class}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h2 style="margin:0;">{res['predicted_disease']}</h2>
                        <span class="badge {badge_class}">{sev} Severity</span>
                    </div>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
                        <b>Plant:</b> {res['plant_name']} (<i>{res.get('scientific_name', '')}</i>) | 
                        <b>Pathogen:</b> {res.get('pathogen', 'N/A')}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Confidence Progress Bar & Metric
            conf_val = res["confidence"]
            st.markdown(f"**Confidence Score:** {res['confidence_percent']} (Inference Latency: {res.get('inference_time_ms', 45)}ms)")
            st.progress(min(max(float(conf_val), 0.0), 1.0))
            
            # Symptoms List
            st.markdown("##### 📌 Detected Symptoms")
            for sym in res["symptoms"]:
                st.markdown(f"- {sym}")
                
            # Treatment Tabs
            st.markdown("##### 💡 Treatment & Management Plan")
            tab_org, tab_chem, tab_prev = st.tabs(["🌿 Organic Remedies", "🧪 Chemical Fungicides", "🛡️ Prevention"])
            
            with tab_org:
                for o in res["remedies"]["organic"]:
                    st.markdown(f"- {o}")
            with tab_chem:
                for c in res["remedies"]["chemical"]:
                    st.markdown(f"- {c}")
            with tab_prev:
                for p in res["remedies"]["prevention"]:
                    st.markdown(f"- {p}")
                    
            # Class Probabilities Plotly Chart
            if "class_probabilities" in res:
                probs_data = res["class_probabilities"]
                fig = px.bar(
                    x=list(probs_data.values()),
                    y=list(probs_data.keys()),
                    orientation="h",
                    labels={"x": "Probability", "y": "Condition"},
                    title="Model Output Class Distribution",
                    color=list(probs_data.values()),
                    color_continuous_scale="Greens" if res["is_healthy"] else "YlOrRd",
                    template=chart_theme
                )
                fig.update_layout(height=220, margin=dict(l=10, r=10, t=30, b=10))
                st.plotly_chart(fig, use_container_width=True)
                
            # PDF Report Download
            try:
                pdf_bytes = generate_pdf_report(res, st.session_state.get("current_img_path"))
                st.download_button(
                    label="📄 Download Diagnostic PDF Report",
                    data=pdf_bytes,
                    file_name=f"PlantVision_Report_{res['plant_id']}_{res['predicted_disease'].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.caption(f"PDF download temporarily unavailable ({e}).")
        else:
            st.info("Run diagnosis on the left to see the detection results and prescription recommendations.")


# ----------------- PAGE 2: HISTORY -----------------
elif selected_page == "📜 Scan History":
    st.markdown("""
        <div class="main-header">
            <h1>📜 Personal Scan History</h1>
            <p>Review, filter, and export all plant disease diagnoses saved to your account.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Filter controls
    f_col1, f_col2, f_col3 = st.columns([1, 1, 2])
    with f_col1:
        p_filter = st.selectbox("Filter by Plant", ["All", "Potato", "Tomato", "Apple"])
    with f_col2:
        s_filter = st.selectbox("Filter by Status", ["All", "Healthy", "Diseased"])
    with f_col3:
        search_kw = st.text_input("Search disease or plant", placeholder="e.g. Blight or Scab")
        
    scans = database.get_user_scans(user["id"], plant_filter=p_filter, status_filter=s_filter, search_term=search_kw)
    
    if not scans:
        st.warning("No scan records found matching your filters. Try scanning a new leaf!")
    else:
        st.write(f"Found **{len(scans)}** scan records.")
        for scan in scans:
            formatted_date = database.format_timestamp_ist(scan.get("timestamp"))
            with st.expander(f"🗓️ {formatted_date} — {scan['plant']}: **{scan['disease']}** ({scan['confidence']*100:.1f}% Confidence)"):
                h_col1, h_col2 = st.columns([1, 2])

                with h_col1:
                    img_data = scan.get("image_path", "")
                    if img_data:
                        try:
                            if str(img_data).startswith("data:image") or str(img_data).startswith("/9j/"):
                                st.image(img_data, caption=f"{scan['plant']} Leaf (Cloud)", use_container_width=True)
                            elif os.path.exists(str(img_data)):
                                st.image(img_data, caption=f"{scan['plant']} Leaf", use_container_width=True)
                            else:
                                st.caption("Leaf thumbnail saved in cloud.")
                        except Exception:
                            st.caption("Image preview unavailable.")
                    else:
                        st.caption("No image recorded.")

                with h_col2:
                    st.markdown(f"**Severity:** {scan['severity']} | **Status:** {'Healthy' if scan['is_healthy'] else 'Infected'}")
                    st.markdown(f"**Confidence Score:** {scan['confidence']*100:.1f}%")
                    
                    symptoms = json.loads(scan["symptoms_json"]) if scan["symptoms_json"] else []
                    remedies = json.loads(scan["remedies_json"]) if scan["remedies_json"] else {}
                    
                    if symptoms:
                        st.markdown("**Symptoms Recorded:**")
                        for s in symptoms[:2]:
                            st.markdown(f"- {s}")
                            
                    del_btn = st.button("🗑️ Delete Record", key=f"del_{scan['id']}")
                    if del_btn:
                        database.delete_scan(scan["id"], user["id"])
                        st.success("Record deleted.")
                        st.rerun()

# ----------------- PAGE 3: ANALYTICS -----------------
elif selected_page == "📊 Analytics Dashboard":
    st.markdown("""
        <div class="main-header">
            <h1>📊 Crop Health Analytics</h1>
            <p>Visual statistics and trend metrics for all your scans.</p>
        </div>
    """, unsafe_allow_html=True)
    
    stats = database.get_user_analytics(user["id"])
    
    if stats["total_scans"] == 0:
        st.info("No scans recorded yet. Perform some scans in the Disease Scanner to unlock analytics!")
    else:
        # KPI Row
        k_col1, k_col2, k_col3, k_col4 = st.columns(4)
        with k_col1:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-val">{stats['total_scans']}</div>
                    <div class="kpi-label">Total Scans</div>
                </div>
            """, unsafe_allow_html=True)
        with k_col2:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-val" style="color:#10b981;">{stats['healthy_count']}</div>
                    <div class="kpi-label">Healthy Plants</div>
                </div>
            """, unsafe_allow_html=True)
        with k_col3:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-val" style="color:#ef4444;">{stats['diseased_count']}</div>
                    <div class="kpi-label">Diseased / Infected</div>
                </div>
            """, unsafe_allow_html=True)
        with k_col4:
            ratio = (stats['healthy_count'] / stats['total_scans']) * 100 if stats['total_scans'] > 0 else 0
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-val" style="color:#2563eb;">{ratio:.1f}%</div>
                    <div class="kpi-label">Crop Health Ratio</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Charts Row 1
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            st.subheader("🥧 Healthy vs. Diseased Ratio")
            labels = ["Healthy", "Diseased"]
            values = [stats["healthy_count"], stats["diseased_count"]]
            fig_pie = px.pie(
                names=labels,
                values=values,
                color=labels,
                color_discrete_map={"Healthy": "#10B981", "Diseased": "#EF4444"},
                hole=0.4,
                template=chart_theme
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with c_col2:
            st.subheader("📊 Scans by Plant Variety")
            plant_data = stats["plant_counts"]
            if plant_data:
                fig_plant = px.bar(
                    x=list(plant_data.keys()),
                    y=list(plant_data.values()),
                    labels={"x": "Plant", "y": "Scan Count"},
                    color=list(plant_data.keys()),
                    color_discrete_sequence=px.colors.qualitative.Prism,
                    template=chart_theme
                )
                st.plotly_chart(fig_plant, use_container_width=True)
                
        # Charts Row 2
        st.subheader("📈 Disease Frequency Distribution")
        disease_data = stats["disease_counts"]
        if disease_data:
            fig_dis = px.bar(
                x=list(disease_data.keys()),
                y=list(disease_data.values()),
                labels={"x": "Disease Name", "y": "Detections"},
                color=list(disease_data.values()),
                color_continuous_scale="Reds",
                template=chart_theme
            )
            st.plotly_chart(fig_dis, use_container_width=True)
        else:
            st.info("No disease infections detected in your scan records yet.")

# ----------------- PAGE 4: ENCYCLOPEDIA -----------------
elif selected_page == "📚 Disease Library":
    st.markdown("""
        <div class="main-header">
            <h1>📚 Plant Disease Encyclopedia</h1>
            <p>Comprehensive offline guide for Potato, Tomato, and Apple plant pathology.</p>
        </div>
    """, unsafe_allow_html=True)
    
    lib_plant_options = {
        "potato": "🥔 Potato (Solanum tuberosum) - Ready",
        "tomato": "🍅 Tomato (Solanum lycopersicum) - Ready",
        "apple": "🍎 Apple (Malus domestica) - Coming Soon ⏳"
    }
    lib_plant_key = st.selectbox(
        "Select Plant Guide",
        options=list(lib_plant_options.keys()),
        format_func=lambda x: lib_plant_options[x]
    )
    
    if lib_plant_key == "apple":
        st.info("🍎 **Apple Pathology AI Model: Coming Soon ⏳**\n\nThe deep learning classification network for Apple is currently in training. The diagnostic profiles and treatments below are provided for educational reference.")

    diseases = DISEASE_KNOWLEDGE_BASE.get(lib_plant_key, {})

    
    for dis_name, dis_info in diseases.items():
        with st.expander(f"{'🟢' if dis_info['is_healthy'] else '🔴'} **{dis_name}** ({dis_info['scientific_name']}) — Severity: {dis_info['severity']}"):
            st.markdown(f"**Description:** {dis_info['description']}")
            st.markdown(f"**Primary Causes & Factors:** {dis_info['causes']}")
            
            st.markdown("##### 📌 Key Symptoms")
            for s in dis_info["symptoms"]:
                st.markdown(f"- {s}")
                
            st.markdown("##### 🌿 Organic Remedies")
            for o in dis_info["organic_remedies"]:
                st.markdown(f"- {o}")
                
            st.markdown("##### 🧪 Chemical Treatments")
            for c in dis_info["chemical_treatments"]:
                st.markdown(f"- {c}")
                
            st.markdown("##### 🛡️ Preventative Measures")
            for p in dis_info["prevention"]:
                st.markdown(f"- {p}")

# ----------------- PAGE 5: SETTINGS -----------------
elif selected_page == "⚙️ Settings & Info":
    st.markdown("""
        <div class="main-header">
            <h1>⚙️ Settings & Backend Configuration</h1>
            <p>Manage theme preferences, model connections, Google Drive integration, and account profile.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("1. 🎨 Appearance & Display Theme")
    theme_choice = st.radio(
        "Choose Display Mode:",
        ["🌙 Dark Slate Theme (Recommended)", "☀️ Light Clean Theme"],
        index=0 if st.session_state.dark_mode else 1,
        horizontal=True,
        key="settings_theme_radio"
    )
    is_dark = (theme_choice == "🌙 Dark Slate Theme (Recommended)")
    if is_dark != st.session_state.dark_mode:
        st.session_state.dark_mode = is_dark
        st.rerun()

    st.markdown("---")


    st.subheader("2. 🤖 Connect Google Drive Model Weights")
    st.write("Connect trained Deep Learning model weights (`.keras` or `.h5`) directly from your Google Drive folder.")

    with st.expander("🔗 Configure Google Drive File Links / IDs", expanded=True):
        st.markdown(f"**Folder:** [Plant Disease Detection Google Drive](https://drive.google.com/drive/u/0/folders/1ZYQxCLsTL5JiHX2EfX-7FljYZHmL_t-P)")
        
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            potato_input = st.text_input("🥔 Potato Model (Link or File ID)", value=config.PLANTS["potato"].get("drive_file_id", ""), placeholder="e.g. 1ZYQxCLsTL5JiHX2EfX-7FljYZHmL_t-P or https://drive.google.com/file/d/...")
        with c_p2:
            tomato_input = st.text_input("🍅 Tomato Model (Link or File ID)", value=config.PLANTS["tomato"].get("drive_file_id", ""), placeholder="e.g. https://drive.google.com/file/d/...")

        if st.button("⚡ Test & Download Weights from Drive"):
            from models.model_loader import download_from_google_drive, extract_file_id
            
            p_id = extract_file_id(potato_input)
            t_id = extract_file_id(tomato_input)

            if p_id:
                config.PLANTS["potato"]["drive_file_id"] = p_id
                with st.spinner("Downloading Potato model weights..."):
                    p_path = config.MODELS_DIR / config.PLANTS["potato"]["model_file"]
                    if download_from_google_drive(p_id, p_path):
                        st.success("✅ Potato model weights synced and downloaded successfully!")
                    else:
                        st.warning("⚠️ Potato model download attempted. Ensure the Google Drive file is set to 'Anyone with the link can view'.")

            if t_id:
                config.PLANTS["tomato"]["drive_file_id"] = t_id
                with st.spinner("Downloading Tomato model weights..."):
                    t_path = config.MODELS_DIR / config.PLANTS["tomato"]["model_file"]
                    if download_from_google_drive(t_id, t_path):
                        st.success("✅ Tomato model weights synced and downloaded successfully!")
                    else:
                        st.warning("⚠️ Tomato model download attempted. Ensure the Google Drive file is set to 'Anyone with the link can view'.")

    st.markdown("---")

    
    st.subheader("3. Input Preprocessing Configuration")
    st.markdown("""
    - **Resolution:** 224 × 224
    - **Color Channels:** 3 (RGB)
    - **Input Normalization:** [0.0, 1.0] float32
    - **Batch Shape:** (1, 224, 224, 3)
    """)
    
    st.subheader("4. Account Information")
    created_at_ist = database.format_timestamp_ist(user.get('created_at'))
    st.markdown(f"""
    - **User ID:** `{user['id']}`
    - **Full Name:** **{user['full_name']}**
    - **Username:** `@{user['username']}`
    - **Email:** `{user['email']}`
    - **Member Since:** `{created_at_ist}`
    """)




