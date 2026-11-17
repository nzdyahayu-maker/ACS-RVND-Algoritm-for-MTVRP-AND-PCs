import streamlit as st
import pandas as pd
import numpy as np
import base64
import random
import decimal
import math
import plotly.graph_objects as go

# Fungsi kustom pembulatan standar (Round Half Up seperti Excel)
def excel_round(val):
    return int(decimal.Decimal(str(val)).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP))

# --- 1. KONFIGURASI HALAMAN & STATE ---
st.set_page_config(
    page_title="Algoritma ACS-RVND pada MTVRP AND-PCs oleh Dyah Ayu",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "page_state" not in st.session_state:
    st.session_state["page_state"] = "cover"

# --- 2. FUNGSI LOGO & CUSTOM CSS DENGAN FONTAWESOME & GRADASI BIRU CERAH ---
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

logo_um_base64 = get_image_base64("logo_um.png")
logo_html = f'<img src="data:image/png;base64,{logo_um_base64}" class="univ-logo">' if logo_um_base64 else ""

st.markdown(f"""
    <!-- CDN FontAwesome 6.4.0 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
    html, body, [class*="css"], .stApp {{
        font-family: 'Times New Roman', Times, serif !important;
        background: linear-gradient(135deg, #e6f2ff 0%, #cce5ff 50%, #e8f4ff 100%) !important;
        background-attachment: fixed !important;
    }}
    
    .univ-logo {{
        position: fixed;
        top: 20px;
        right: 40px;
        width: 140px;
        z-index: 9999;
    }}
    .login-card {{
        background: rgba(255, 255, 255, 0.95);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 102, 204, 0.12);
        border-top: 6px solid #007bff;
        margin-top: 30px;
        backdrop-filter: blur(5px);
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%) !important;
        color: white !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }}
    .stButton>button:hover {{
        background: linear-gradient(135deg, #0056b3 0%, #003366 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 123, 255, 0.4) !important;
    }}
    .route-card {{
        background: #ffffff;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(0, 102, 204, 0.08);
        margin-bottom: 14px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #e1effe;
        min-height: 165px;
    }}
    .route-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 102, 204, 0.15);
    }}
    .metric-box {{
        background: linear-gradient(135deg, #ffffff 0%, #e6f0fa 100%);
        padding: 16px;
        border-radius: 12px;
        border-left: 5px solid #007bff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(90deg, #004085 0%, #002752 100%);
        color: white;
        text-align: center;
        padding: 8px;
        font-size: 13px;
        z-index: 999;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }}
    </style>
    {logo_html}
""", unsafe_allow_html=True)

# ==========================================
# HALAMAN 1: COVER PAGE
# ==========================================
if st.session_state["page_state"] == "cover":
    st.title("🚚 Sistem Optimasi Rute Kendaraan (VRP)")
    st.subheader("Multi Trip Vehicle Routing Problem with Precedence Constraint (MTVRP AND-PCs)")
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="login-card">
                <h2 style="text-align: center; color: #0056b3;"><i class="fa-solid fa-truck-ramp-box"></i> Selamat Datang</h2>
                <p style="text-align: center; font-size: 16px; color: #444;">
                    Sistem Penjadwalan Rute Kendaraan Berbasis Metaheuristik (ACS) <br>
                    dan Perbaikan Solusi Local Search (RVND).
                </p>
                <hr style="border: 0.5px solid #d0e2ff; margin: 25px 0;">
                <p style="text-align: center; font-size: 14px; color: #666;">
                    Silakan klik tombol di bawah untuk masuk ke dashboard utama.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        if st.button("🚀 Masuk ke Dashboard Aplikasi", type="primary", use_container_width=True):
            st.session_state["page_state"] = "dashboard"
            st.rerun()

# ==========================================
# HALAMAN 2: DASHBOARD UTAMA
# ==========================================
else:
    with st.sidebar:
        st.markdown("### <i class='fa-solid fa-sliders'></i> Kontrol Aplikasi", unsafe_allow_html=True)
        st.info("**Developer:**\nDyah Ayu Nur Zubaidah\n\n**NIM:**\n230312608130\n\n**Pembimbing:**\nDra. Sapti Wahyuningsih, M.Si")
        st.divider()
        if st.button("🏠 Kembali ke Cover Page", use_container_width=True):
            st.session_state["page_state"] = "cover"
            st.rerun()

    st.title("Dashboard Optimalisasi Rute Kendaraan")
    st.caption("Multi Trip Vehicle Routing Problem with AND Type-Precedence Constraint with ACS-RVND Algorithm")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Input & Preview Data", 
        "📍 Inisialisasi Pheromone Awal (NN)", 
        "🐜 Proses ACS", 
        "🔄 Perbaikan RVND", 
        "📊 Hasil Efisiensi"
    ])

    # --- TAB 1: INPUT DATA ---
    with tab1:
        st.markdown("### <i class='fa-solid fa-truck'></i> Data Kendaraan", unsafe_allow_html=True)
        if "max_rute_p" not in st.session_state:
            st.session_state["max_rute_p"] = 10

        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        with col_k1:
            jenis_kendaraan = st.text_input("Jenis Kendaraan", value="PICK UP (BOX)")
        with col_k2:
            kapasitas_kendaraan = st.number_input("Kapasitas Kendaraan (Unit)", min_value=1, value=100)
            st.session_state["kapasitas_kendaraan"] = kapasitas_kendaraan
        with col_k3:
            biaya_operasional = st.number_input("Biaya Operasional (Rp/km)", min_value=0, value=10000)
            st.session_state["biaya_operasional"] = biaya_operasional
        with col_k4:
            max_rute_p_tab1 = st.number_input(
                "Batas Maks. Rute/Kendaraan (p)",
                min_value=1,
                max_value=10,
                value=min(10, int(st.session_state["max_rute_p"])),
                step=1,
                key="input_max_rute_p_tab1",
                help="Batas maksimal jumlah rute (trip) untuk 1 kendaraan (maksimal 10 rute). Jika total rute melebihi p, akan mengambil kendaraan lain."
            )
            st.session_state["max_rute_p"] = int(max_rute_p_tab1)
        
        st.divider()
        st.markdown("### <i class='fa-solid fa-users'></i> Data Pelanggan & Depot", unsafe_allow_html=True)
        st.info("💡 **Catatan:** Baris pertama pada tabel otomatis ditetapkan sebagai **Depot** (indeks internal `0`, Demand = `0`).")
        
        with st.expander("📁 Unggah File Dataset Pelanggan (CSV / Excel)", expanded=True):
            uploaded_file = st.file_uploader("Pilih file dataset (Format .csv, .xlsx, .xls)", type=["csv", "xlsx", "xls"])
            if uploaded_file is not None:
                file_sig = f"{uploaded_file.name}_{uploaded_file.size}"
                if st.session_state.get("last_uploaded_file") != file_sig:
                    try:
                        if uploaded_file.name.endswith('.csv'):
                            df_upload = pd.read_csv(uploaded_file)
                        else:
                            df_upload = pd.read_excel(uploaded_file)
                        
                        col_map = {}
                        for col in df_upload.columns:
                            c_lower = str(col).lower().strip()
                            if 'no' in c_lower or 'id' in c_lower: col_map[col] = "No"
                            elif 'nama' in c_lower or 'name' in c_lower or 'pelanggan' in c_lower or 'titik' in c_lower or 'simpul' in c_lower: col_map[col] = "Nama Pelanggan"
                            elif 'demand' in c_lower or 'minta' in c_lower or 'permintaan' in c_lower: col_map[col] = "Permintaan (Demand)"
                            elif 'x' in c_lower: col_map[col] = "Koordinat X"
                            elif 'y' in c_lower: col_map[col] = "Koordinat Y"
                        df_renamed = df_upload.rename(columns=col_map)

                        if "No" not in df_renamed.columns:
                            df_renamed.insert(0, "No", range(len(df_renamed)))

                        required_cols = ["No", "Nama Pelanggan", "Permintaan (Demand)", "Koordinat X", "Koordinat Y"]
                        
                        if all(col in df_renamed.columns for col in required_cols):
                            df_renamed = df_renamed[required_cols].dropna(subset=["Nama Pelanggan", "Koordinat X", "Koordinat Y"]).reset_index(drop=True)
                            df_renamed["No"] = range(len(df_renamed))
                            df_renamed.loc[0, "Permintaan (Demand)"] = 0
                            df_renamed["Nama Pelanggan"] = df_renamed["Nama Pelanggan"].astype(str).str.strip()

                            st.session_state["uploaded_custom_data"] = df_renamed
                            st.session_state["last_uploaded_file"] = file_sig
                            for key_reset in ["dist_matrix", "predecessor_dict", "solution_clusters", "acs_results", "rvnd_results"]:
                                if key_reset in st.session_state:
                                    del st.session_state[key_reset]
                            st.success(f"Dataset '{uploaded_file.name}' berhasil diunggah! Baris pertama ({df_renamed.loc[0, 'Nama Pelanggan']}) ditetapkan sebagai Depot.")
                        else:
                            st.error("Format file tidak sesuai. Pastikan file memiliki kolom: Nama Pelanggan, Permintaan (Demand), Koordinat X, Koordinat Y.")
                    except Exception as e:
                        st.error(f"Gagal membaca file: {e}")
            else:
                if "last_uploaded_file" in st.session_state:
                    del st.session_state["last_uploaded_file"]
                    if "uploaded_custom_data" in st.session_state:
                        del st.session_state["uploaded_custom_data"]

        if "uploaded_custom_data" in st.session_state:
            default_data = st.session_state["uploaded_custom_data"]
        else:
            default_data = pd.DataFrame({
                "No": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "Nama Pelanggan": [
                    "PT SO GOOD FOOD MANUFACTURING",
                    "HOSHINO COFFEE SENAYAN CITY",
                    "SHABU - SHABU HOUSE ITC PERMATA HIJAU",
                    "RS MITRA KELUARGA GADING SERPONG",
                    "OOTOYA SENAYAN CITY",
                    "HOLYCOW ! STEAKHOUSE BY CHEF AFIT - BINTARO",
                    "RSU MUHAMMADIYAH TAMAN PURING",
                    "FARMERS MARKET 99 KELAPA GADING",
                    "LOTTE SHOPPING MERUYA",
                    "DAILY FOOD HALL - MILLENIUM MALL SENEN",
                    "HERO PERMATA HIJAU"
                ],
                "Permintaan (Demand)": [0, 20, 49, 25, 30, 10, 37, 30, 35, 46, 32],
                "Koordinat X": [0, 35, 38, 14, 35, 27, 34, 47, 28, 40, 34],
                "Koordinat Y": [0, 50, 12, 30, 38, 8, 60, 22, 36, 2, 28]
            })
            default_data = default_data[["No", "Nama Pelanggan", "Permintaan (Demand)", "Koordinat X", "Koordinat Y"]]
        
        edited_df = st.data_editor(
            default_data, 
            num_rows="dynamic", 
            use_container_width=True, 
            key="input_table_editor",
            hide_index=True
        )
        
        if st.button("⚡ Olah Data & Hitung Matriks Jarak", type="primary"):
            cleaned_df = edited_df.dropna(subset=["Nama Pelanggan", "Koordinat X", "Koordinat Y"]).reset_index(drop=True)
            cleaned_df["No"] = range(len(cleaned_df))
            cleaned_df.loc[0, "Permintaan (Demand)"] = 0
            cleaned_df["Nama Pelanggan"] = cleaned_df["Nama Pelanggan"].astype(str).str.strip()

            st.session_state["df_data"] = cleaned_df
            coords = cleaned_df[["Koordinat X", "Koordinat Y"]].values
            n = len(coords)
            dist_matrix = np.zeros((n, n), dtype=int)
            for i in range(n):
                for j in range(n):
                    if i != j:
                        raw_dist = np.sqrt((coords[i][0] - coords[j][0])**2 + (coords[i][1] - coords[j][1])**2)
                        dist_matrix[i, j] = excel_round(raw_dist)
                    else:
                        dist_matrix[i, j] = 0
            
            labels = [str(row["Nama Pelanggan"]) for _, row in cleaned_df.iterrows()]
            matrix_df = pd.DataFrame(dist_matrix, index=labels, columns=labels)
            st.session_state["dist_matrix"] = matrix_df
            st.success("Data berhasil diolah dan Matriks Jarak berhasil dihitung.")

        if "dist_matrix" in st.session_state:
            st.divider()
            
            st.markdown("### <i class='fa-solid fa-diagram-project'></i> Daftar Pelanggan Prioritas (Predecessor)", unsafe_allow_html=True)
            
            df_curr_inputs = st.session_state["df_data"]
            pelanggan_only = df_curr_inputs[df_curr_inputs["No"] != 0].reset_index(drop=True)
            num_pel = len(pelanggan_only)
            
            default_predecessors = {
                1: "{3,6}", 2: "{}", 3: "{}", 4: "{}", 5: "{}",
                6: "{}", 7: "{2,8,9}", 8: "{}", 9: "{}", 10: "{4}"
            }
            if "predecessor_dict" not in st.session_state or len(st.session_state["predecessor_dict"]) != num_pel:
                st.session_state["predecessor_dict"] = {
                    int(row["No"]): default_predecessors.get(int(row["No"]), "{}") 
                    for _, row in pelanggan_only.iterrows()
                }

            col_tau, col_rand1, col_info_tau = st.columns([1.5, 1.5, 3])
            with col_tau:
                tau_pc = st.number_input(
                    "Faktor Kepadatan PCs (τ)",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.70,
                    step=0.05,
                    format="%.2f",
                    help="Berdasarkan Driessel & Mönch (2011): Simpul dikatakan bebas pendahulu jika bilangan acak U[0,1] < τ. ( Misal : τ = 0: paling padat, τ = 0.40: sedang, τ = 0.80: paling longgar)."
                )
            with col_rand1:
                st.write("")
                st.write("")
                btn_random_pc = st.button("🎲 Acak Pendahulu", use_container_width=True)
            with col_info_tau:
                st.write("")
                pct_free = tau_pc * 100
                pct_constrained = (1.0 - tau_pc) * 100
                if tau_pc == 0.0:
                    st.info("**τ = 0,00 (PCs Paling Padat):** Peluang bebas pendahulu **0%** (seluruh pelanggan selain simpul pertama dalam urutan acak diberi pendahulu).")
                elif tau_pc == 1.0:
                    st.info("**τ = 1,00 (Tanpa PCs):** Peluang bebas pendahulu **100%** (`{}` untuk semua pelanggan).")
                else:
                    st.info(f"**τ = {tau_pc:.2f}:** Peluang simpul **bebas pendahulu {pct_free:.0f}%** ($U[0,1] < {tau_pc:.2f}$) dan peluang **memiliki pendahulu {pct_constrained:.0f}%** (bebas siklus).")

            if btn_random_pc:
                p_ids = [int(row["No"]) for _, row in pelanggan_only.iterrows()]
                new_pred_sets = {pid: set() for pid in p_ids}
                
                if tau_pc < 1.0 and num_pel >= 2:
                    ordered_nodes = p_ids.copy()
                    random.shuffle(ordered_nodes)
                    
                    for col_idx in range(1, num_pel):
                        if random.random() >= tau_pc:
                            target_node = ordered_nodes[col_idx]
                            earlier_nodes = ordered_nodes[:col_idx]
                            max_preds = min(3, len(earlier_nodes))
                            k_preds = random.randint(1, max_preds)
                            chosen_preds = random.sample(earlier_nodes, k_preds)
                            new_pred_sets[target_node] = set(chosen_preds)

                st.session_state["predecessor_dict"] = {
                    pid: "{" + ", ".join(map(str, sorted(list(p_set)))) + "}"
                    for pid, p_set in new_pred_sets.items()
                }
                st.rerun()

            pred_data = []
            for _, row in pelanggan_only.iterrows():
                pel_id = int(row["No"])
                pred_val = st.session_state["predecessor_dict"].get(pel_id, "{}")
                pred_data.append({
                    "Pelanggan": pel_id,
                    "Nama Pelanggan": row["Nama Pelanggan"],
                    "Pendahulu/Predecessor": pred_val,
                    "Simpul AND-PCs": f"AND_{pel_id} = {pred_val}"
                })
            df_pred_display = pd.DataFrame(pred_data)
            edited_pred_df = st.data_editor(
                df_pred_display,
                column_config={
                    "Pelanggan": st.column_config.NumberColumn("No", disabled=True),
                    "Nama Pelanggan": st.column_config.TextColumn("Nama Pelanggan", disabled=True),
                    "Pendahulu/Predecessor": st.column_config.TextColumn("Pendahulu/Predecessor", help="Ketik himpunan pendahulu, misal: {3,6} atau {}"),
                    "Simpul AND-PCs": st.column_config.TextColumn("Simpul AND-PC", disabled=True)
                },
                hide_index=True,
                use_container_width=True,
                key="pred_table_editor"
            )
            updated_dict = {}
            for idx, row in edited_pred_df.iterrows():
                p_id = int(row["Pelanggan"])
                p_val = str(row["Pendahulu/Predecessor"]).strip()
                if not (p_val.startswith("{") and p_val.endswith("}")):
                    p_val = "{" + p_val.replace("{", "").replace("}", "") + "}"
                updated_dict[p_id] = p_val
            st.session_state["predecessor_dict"] = updated_dict

            st.divider()

            st.markdown("### <i class='fa-solid fa-table-cells'></i> Matriks Jarak Euclidean", unsafe_allow_html=True)
            st.dataframe(st.session_state["dist_matrix"], use_container_width=True)
            st.divider()

            st.markdown("### <i class='fa-solid fa-map-location-dot'></i> Plot Titik Geografis & Graf Komplit", unsafe_allow_html=True)
            st.caption("Label titik menampilkan nama pelanggan dan depot sesuai dataset. Arahkan kursor ke titik untuk detail permintaan dan jarak ke depot.")
            df_curr = st.session_state["df_data"].reset_index(drop=True)
            coords = df_curr[["Koordinat X", "Koordinat Y"]].values
            n = len(coords)
            dist_matrix = st.session_state["dist_matrix"].values
            fig = go.Figure()

            edge_x, edge_y = [], []
            for i in range(n):
                for j in range(i + 1, n):
                    edge_x.extend([coords[i][0], coords[j][0], None])
                    edge_y.extend([coords[i][1], coords[j][1], None])

            fig.add_trace(go.Scatter(
                x=edge_x,
                y=edge_y,
                mode='lines',
                line=dict(color='rgba(51, 51, 51, 0.3)', width=0.8),
                hoverinfo='skip',
                showlegend=False
            ))

            pel_df = df_curr[df_curr["No"] != 0]
            pel_hover_texts = []
            for idx, row in pel_df.iterrows():
                dist_to_depot = dist_matrix[0, idx]
                text_info = (
                    f"<b>{row['Nama Pelanggan']}</b> (P{row['No']})<br>"
                    f"Koordinat: ({row['Koordinat X']}, {row['Koordinat Y']})<br>"
                    f"Permintaan: {row['Permintaan (Demand)']} unit<br>"
                    f"<b>Jarak ke Depot: {int(dist_to_depot)} km</b>"
                )
                pel_hover_texts.append(text_info)

            fig.add_trace(go.Scatter(
                x=pel_df["Koordinat X"],
                y=pel_df["Koordinat Y"],
                mode='markers+text',
                marker=dict(color='#0056b3', size=12),
                text=[str(row['Nama Pelanggan']) for _, row in pel_df.iterrows()],
                textposition="top center",
                textfont=dict(size=9 if n > 25 else 10, color='#1a1a1a'),
                name="Pelanggan",
                hoverinfo='text',
                hovertext=pel_hover_texts
            ))

            depot_x, depot_y = coords[0][0], coords[0][1]
            depot_name = str(df_curr.iloc[0]['Nama Pelanggan'])
            fig.add_trace(go.Scatter(
                x=[depot_x],
                y=[depot_y],
                mode='markers+text',
                marker=dict(color='#dc3545', size=16, symbol='square'),
                text=[depot_name],
                textposition="bottom center",
                textfont=dict(size=10, color='#dc3545'),
                name=f"Depot ({depot_name})",
                hoverinfo='text',
                hovertext=f"<b>Depot: {depot_name}</b><br>Koordinat: ({depot_x}, {depot_y})"
            ))

            min_x, max_x = coords[:, 0].min(), coords[:, 0].max()
            min_y, max_y = coords[:, 1].min(), coords[:, 1].max()
            fig.update_layout(
                width=850, height=520,
                margin=dict(l=40, r=40, t=30, b=40),
                xaxis=dict(title="Koordinat X", range=[min_x - 8, max_x + 8], showgrid=True, gridcolor='#e1effe'),
                yaxis=dict(title="Koordinat Y", range=[min_y - 8, max_y + 8], showgrid=True, gridcolor='#e1effe'),
                template="plotly_white",
                legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)")
            )
            st.plotly_chart(fig, use_container_width=True, key="plot_tab1_graph")

    # --- TAB 2: INISIALISASI PHEROMONE AWAL (NEAREST NEIGHBORHOOD) ---
    with tab2:
        st.subheader("Inisialisasi Pheromone Awal (Nearest Neighborhood)")
        st.caption("Pembentukan rute awal berbasis Nearest Neighborhood (NN) untuk menghitung total jarak awal (L₀) dan intensitas pheromone awal (τ₀ = 1 / (n × L₀)) dengan memenuhi kapasitas kendaraan, Precedence Constraints (AND-PCs), serta batas maksimum rute per kendaraan (p).")
        
        if "df_data" not in st.session_state or "dist_matrix" not in st.session_state:
            st.warning("Silakan olah dan simpan data terlebih dahulu di Tab 'Input & Preview Data'.")
        else:
            df_curr = st.session_state["df_data"].reset_index(drop=True)
            dist_arr = st.session_state["dist_matrix"].values.tolist()
            capacity = st.session_state.get("kapasitas_kendaraan", 100)
            bo = st.session_state.get("biaya_operasional", 10000)
            p_limit_curr = int(st.session_state.get("max_rute_p", 10))
            no_to_idx = {int(row["No"]): idx for idx, row in df_curr.iterrows()}
            demand_dict = {int(row["No"]): float(row["Permintaan (Demand)"]) for _, row in df_curr.iterrows()}
            n_cust_total = len(df_curr[df_curr["No"] != 0])
            
            predecessors_parsed = {}
            pred_dict_str = st.session_state.get("predecessor_dict", {})
            for p_id_str, p_set_str in pred_dict_str.items():
                p_id = int(p_id_str)
                cleaned = p_set_str.replace("{", "").replace("}", "").strip()
                if cleaned:
                    predecessors_parsed[p_id] = [int(x.strip()) for x in cleaned.split(",") if x.strip().isdigit()]
                else:
                    predecessors_parsed[p_id] = []

            if st.button("▶️ Jalankan Inisialisasi Solusi & Pheromone Awal (NN)", type="primary"):
                with st.spinner("Menghitung rute awal Nearest Neighborhood..."):
                    unserved = [int(row["No"]) for _, row in df_curr[df_curr["No"] != 0].iterrows()]
                    served = set()
                    clusters_info = []
                    route_counter = 1
                    is_feasible = True

                    while unserved:
                        cluster_history = []
                        current_route = []
                        current_load = 0
                        current_node = 0
                        
                        valid_candidates_from_depot = []
                        idx0 = no_to_idx[0]
                        for cand in unserved:
                            preds = predecessors_parsed.get(cand, [])
                            demand_cand = demand_dict[cand]
                            if all(p in served for p in preds) and demand_cand <= capacity:
                                dist_d = dist_arr[idx0][no_to_idx[cand]]
                                valid_candidates_from_depot.append((cand, dist_d))
                        
                        if not valid_candidates_from_depot:
                            st.error("Terjadi Deadlock / Infeasible: Tidak ada pelanggan tersisa yang memenuhi aturan Precedence Constraint maupun batas kapasitas kendaraan.")
                            is_feasible = False
                            break

                        valid_candidates_from_depot.sort(key=lambda x: x[1])
                        min_dist_depot = valid_candidates_from_depot[0][1]
                        nearest_depot_candidates = [cand for cand, dist in valid_candidates_from_depot if dist == min_dist_depot]
                        
                        first_node = random.choice(nearest_depot_candidates)
                        cluster_history.append({
                            "Urutan": "Start (0)", "Jarak": "-", "Kapasitas": "0", "Aturan PCs": "-", "Ket": "-"
                        })
                        demand_first = demand_dict[first_node]
                        current_route.append(first_node)
                        current_load += demand_first
                        served.add(first_node)
                        unserved.remove(first_node)
                        cluster_history.append({
                            "Urutan": f"0 ➔ P{first_node}", "Jarak": f"{min_dist_depot} km",
                            "Kapasitas": f"{int(current_load)} unit", "Aturan PCs": "Pendahulu Terpenuhi", "Ket": "M"
                        })
                        current_node = first_node

                        while True:
                            idx_curr = no_to_idx[current_node]
                            candidates = [(cand, dist_arr[idx_curr][no_to_idx[cand]]) for cand in unserved]
                            candidates.sort(key=lambda x: x[1])
                            found_next = False
                            for cand, dist_c in candidates:
                                demand_c = demand_dict[cand]
                                preds = predecessors_parsed.get(cand, [])
                                missing_preds = [p for p in preds if p not in served]
                                pcs_ok = len(missing_preds) == 0
                                cap_ok = (current_load + demand_c <= capacity)
                                if pcs_ok and cap_ok:
                                    current_route.append(cand)
                                    current_load += demand_c
                                    served.add(cand)
                                    unserved.remove(cand)
                                    cluster_history.append({
                                        "Urutan": f"P{current_node} ➔ P{cand}", "Jarak": f"{dist_c} km",
                                        "Kapasitas": f"{int(current_load)} unit", "Aturan PCs": "Pendahulu Terpenuhi", "Ket": "M"
                                    })
                                    current_node = cand
                                    found_next = True
                                    break
                                else:
                                    reason_list = []
                                    if not pcs_ok: reason_list.append(f"Pendahulu P{missing_preds} Belum Dilayani")
                                    if not cap_ok: reason_list.append(f"Kapasitas Over ({int(current_load + demand_c)} > {capacity})")
                                    cluster_history.append({
                                        "Urutan": f"P{current_node} ➔ P{cand}", "Jarak": f"{dist_c} km",
                                        "Kapasitas": f"{int(current_load + demand_c)} unit", "Aturan PCs": " & ".join(reason_list), "Ket": "TM"
                                    })
                            if not found_next:
                                dist_back = dist_arr[no_to_idx[current_node]][idx0]
                                cluster_history.append({
                                    "Urutan": f"P{current_node} ➔ Depot (0)", "Jarak": f"{dist_back} km",
                                    "Kapasitas": f"{int(current_load)} unit", "Aturan PCs": "Kembali ke Depot", "Ket": "M"
                                })
                                break
                        full_r = [0] + current_route + [0]
                        total_dist_cl = sum(dist_arr[no_to_idx[full_r[k]]][no_to_idx[full_r[k+1]]] for k in range(len(full_r) - 1))
                        clusters_info.append({
                            "route_id": route_counter,
                            "route": current_route,
                            "load": int(current_load),
                            "distance": total_dist_cl,
                            "cost": total_dist_cl * bo,
                            "history": pd.DataFrame(cluster_history)
                        })
                        route_counter += 1

                    if is_feasible and clusters_info:
                        L0_init = sum(c["distance"] for c in clusters_info)
                        tau0_init = 1.0 / (n_cust_total * L0_init) if (n_cust_total * L0_init) > 0 else 0.0001
                        st.session_state["solution_clusters"] = clusters_info
                        st.session_state["nn_L0"] = L0_init
                        st.session_state["nn_tau0"] = tau0_init
                        for key_reset in ["acs_results", "rvnd_results"]:
                            if key_reset in st.session_state:
                                del st.session_state[key_reset]
                        st.success(f"Inisialisasi Solusi Awal NN Berhasil! Diperoleh L₀ = {L0_init} km dan Pheromone Awal τ₀ = {tau0_init:.8f}.")

            if "solution_clusters" in st.session_state:
                clusters_info = st.session_state["solution_clusters"]
                tot_all_load = sum(c["load"] for c in clusters_info)
                tot_all_dist = sum(c["distance"] for c in clusters_info)
                tot_all_cost = sum(c["cost"] for c in clusters_info)
                num_vehicles_nn = math.ceil(len(clusters_info) / p_limit_curr)
                tau0_disp = st.session_state.get(
                    "nn_tau0",
                    1.0 / (n_cust_total * tot_all_dist) if (n_cust_total * tot_all_dist) > 0 else 0.0001
                )

                st.divider()
                st.markdown("### <i class='fa-solid fa-flask'></i> Parameter Pheromone Awal Hasil Nearest Neighborhood", unsafe_allow_html=True)
                col_nn1, col_nn2, col_nn3, col_nn4, col_nn5 = st.columns(5)
                col_nn1.metric("Jumlah Pelanggan (n)", f"{n_cust_total} titik")
                col_nn2.metric("Jumlah Rute Awal", f"{len(clusters_info)} rute")
                col_nn3.metric(f"Kendaraan (p={p_limit_curr})", f"{num_vehicles_nn} unit")
                col_nn4.metric("Panjang Tur Awal (L₀)", f"{tot_all_dist} km")
                col_nn5.metric("Pheromone Awal (τ₀)", f"{tau0_disp:.8f}")
                st.caption(f"Rumus Inisialisasi: $\\tau_0 = \\frac{{1}}{{n \\times L_0}} = \\frac{{1}}{{{n_cust_total} \\times {tot_all_dist}}} = {tau0_disp:.8f}$")

                st.divider()
                with st.expander("🔍 Lihat Detail Langkah-Langkah Pembentukan Rute (Perhitungan NN)", expanded=False):
                    for cl in clusters_info:
                        r_idx_nn = cl['route_id'] - 1
                        veh_id_nn = (r_idx_nn // p_limit_curr) + 1
                        trip_in_veh_nn = (r_idx_nn % p_limit_curr) + 1
                        st.markdown(f"#### **Kendaraan {veh_id_nn} — Trip {trip_in_veh_nn}/{p_limit_curr} (Rute {cl['route_id']})**")
                        st.dataframe(cl["history"], use_container_width=True, hide_index=True)

                st.divider()
                st.subheader("Hasil Akhir Rute Kendaraan (Solusi Awal NN)")
                colors = ['#007bff', '#28a745', '#fd7e14', '#dc3545', '#6f42c1', '#17a2b8']

                cols_per_row = 3
                for idx_step in range(0, len(clusters_info), cols_per_row):
                    grid_cols = st.columns(cols_per_row)
                    for i in range(cols_per_row):
                        if idx_step + i < len(clusters_info):
                            route_idx = idx_step + i
                            cl = clusters_info[route_idx]
                            veh_id = (route_idx // p_limit_curr) + 1
                            trip_in_veh = (route_idx % p_limit_curr) + 1
                            route_names = ["0"] + [f"P{node}" for node in cl["route"]] + ["0"]
                            route_str = " ➔ ".join(route_names)
                            with grid_cols[i]:
                                st.markdown(f"""
                                    <div class="route-card" style="border-left: 5px solid {colors[(veh_id - 1) % len(colors)]};">
                                        <h4 style="margin:0; color: #004085; font-size: 15px;"><i class="fa-solid fa-truck"></i> Kendaraan {veh_id} — Trip {trip_in_veh}/{p_limit_curr} (Rute {cl['route_id']})</h4>
                                        <p style="margin: 6px 0 0 0; font-size: 13px;"><b>Rute:</b> {route_str}</p>
                                        <p style="margin: 3px 0 0 0; font-size: 12px; color: #555;"><i class="fa-solid fa-boxes-packing"></i> <b>Muatan:</b> {cl['load']}/{capacity} unit</p>
                                        <p style="margin: 3px 0 0 0; font-size: 12px; color: #555;"><i class="fa-solid fa-ruler-horizontal"></i> <b>Jarak:</b> {cl['distance']} km</p>
                                        <p style="margin: 3px 0 0 0; font-size: 12px; color: #0056b3;"><i class="fa-solid fa-money-bill-wave"></i> <b>Biaya:</b> Rp {cl['cost']:,.0f}</p>
                                    </div>
                                """, unsafe_allow_html=True)

                st.markdown(f"""
                    <div style="background: #ffffff; padding: 16px; border-radius: 12px; border: 1px solid #b8daff; box-shadow: 0 4px 10px rgba(0,123,255,0.08); margin-top: 8px; margin-bottom: 16px;">
                        <h4 style="margin:0; color: #004085; font-size: 16px;"><i class="fa-solid fa-clipboard-check"></i> Ringkasan Total Seluruh Rute Awal (NN)</h4>
                        <p style="margin: 6px 0 0 0; font-size: 14px; color: #004085;">
                            <b>Jumlah Kendaraan Terbentuk:</b> {num_vehicles_nn} unit &nbsp;|&nbsp;
                            <b>Jumlah Rute:</b> {len(clusters_info)} rute &nbsp;|&nbsp; 
                            <b>Total Permintaan:</b> {tot_all_load} unit &nbsp;|&nbsp; 
                            <b>Total Jarak (L₀):</b> {tot_all_dist} km &nbsp;|&nbsp; 
                            <b>Total Biaya Keseluruhan:</b> Rp {tot_all_cost:,.0f} &nbsp;|&nbsp; 
                            <b>τ₀:</b> {tau0_disp:.8f}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                st.divider()
                st.subheader("Visualisasi Rute Awal NN")
                fig_cl = go.Figure()
                coords = df_curr[["Koordinat X", "Koordinat Y"]].values
                depot_x, depot_y = coords[0][0], coords[0][1]
                fig_cl.add_trace(go.Scatter(
                    x=[depot_x], y=[depot_y],
                    mode='markers+text', marker=dict(color='#dc3545', size=18, symbol='square'),
                    text=["0"], textposition="bottom center", name="Depot (0)"
                ))
                for idx, cl in enumerate(clusters_info):
                    veh_id = (idx // p_limit_curr) + 1
                    trip_in_veh = (idx % p_limit_curr) + 1
                    color_code = colors[idx % len(colors)]
                    route_nodes = [0] + cl["route"] + [0]
                    rx = [coords[no_to_idx[node]][0] for node in route_nodes]
                    ry = [coords[no_to_idx[node]][1] for node in route_nodes]
                    fig_cl.add_trace(go.Scatter(
                        x=rx, y=ry, mode='lines+markers+text',
                        line=dict(color=color_code, width=2.5),
                        marker=dict(size=12, color=color_code),
                        text=[str(node) if node != 0 else "" for node in route_nodes],
                        textposition="top center", name=f"K{veh_id}-Trip {trip_in_veh} (Rute {cl['route_id']})",
                        hoverinfo='text', hovertext=[f"Kendaraan {veh_id} - Rute {cl['route_id']}: {df_curr.iloc[no_to_idx[node]]['Nama Pelanggan']}" for node in route_nodes]
                    ))
                    for k in range(len(route_nodes) - 1):
                        x_start, y_start = rx[k], ry[k]
                        x_end, y_end = rx[k+1], ry[k+1]
                        fig_cl.add_annotation(
                            x=(x_start + x_end) / 2, y=(y_start + y_end) / 2,
                            ax=x_start, ay=y_start, xref="x", yref="y", axref="x", ayref="y",
                            showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2, arrowcolor=color_code
                        )
                and_text_lines = []
                for p_id in sorted(predecessors_parsed.keys()):
                    preds = predecessors_parsed[p_id]
                    if preds:
                        preds_str = "{" + ",".join(map(str, preds)) + "}"
                        and_text_lines.append(f"<b>AND<sub>{p_id}</sub></b> = {preds_str}")
                
                if and_text_lines and len(and_text_lines) <= 15:
                    fig_cl.add_annotation(
                        xref="paper", yref="paper", x=0.98, y=0.98,
                        text=f"<b>Aturan Precedence (AND-PCs):</b><br>{'<br>'.join(and_text_lines)}",
                        showarrow=False, bordercolor="#0056b3", borderwidth=1, borderpad=8, bgcolor="#ffffff", opacity=0.9, align="left"
                    )
                min_x, max_x = coords[:, 0].min(), coords[:, 0].max()
                min_y, max_y = coords[:, 1].min(), coords[:, 1].max()
                fig_cl.update_layout(
                    width=850, height=550, margin=dict(l=40, r=40, t=30, b=40),
                    xaxis=dict(title="Koordinat X", range=[min_x - 8, max_x + 8], showgrid=True, gridcolor='#e1effe'),
                    yaxis=dict(title="Koordinat Y", range=[min_y - 8, max_y + 8], showgrid=True, gridcolor='#e1effe'),
                    template="plotly_white", legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)")
                )
                st.plotly_chart(fig_cl, use_container_width=True, key="plot_tab2_nn")

    # --- TAB 3: PROSES ACS ---
    with tab3:
        st.subheader("Parameter & Proses Ant Colony System (ACS)")
        p_limit_curr = int(st.session_state.get("max_rute_p", 10))
        
        if "acs_m" not in st.session_state: st.session_state["acs_m"] = 2
        if "acs_q0" not in st.session_state: st.session_state["acs_q0"] = 0.85
        if "acs_rho" not in st.session_state: st.session_state["acs_rho"] = 0.10
        if "acs_alpha" not in st.session_state: st.session_state["acs_alpha"] = 0.10
        if "acs_beta" not in st.session_state: st.session_state["acs_beta"] = 2.0
        if "acs_iter" not in st.session_state: st.session_state["acs_iter"] = 2

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("#### <i class='fa-solid fa-bug'></i> Parameter Algoritma Semut", unsafe_allow_html=True)
            acs_m = st.number_input("Jumlah Semut (m)", min_value=1, value=st.session_state["acs_m"], step=1)
            acs_q0 = st.number_input("Parameter Pembanding (q₀)", min_value=0.0, max_value=1.0, value=float(st.session_state["acs_q0"]), step=0.05, format="%.2f")
            acs_rho = st.number_input("Parameter Pheromone Lokal (ρ / rho)", min_value=0.0, max_value=1.0, value=float(st.session_state["acs_rho"]), step=0.05, format="%.2f")
        with col_p2:
            st.markdown("#### <i class='fa-solid fa-rotate'></i> Parameter Pembobot & Iterasi", unsafe_allow_html=True)
            acs_alpha = st.number_input("Parameter Evaporasi Global (α / alpha)", min_value=0.0, max_value=1.0, value=float(st.session_state["acs_alpha"]), step=0.05, format="%.2f")
            acs_beta = st.number_input("Parameter Visibilitas (β / beta)", min_value=0.0, value=float(st.session_state["acs_beta"]), step=0.5, format="%.1f")
            acs_iter = st.number_input("Jumlah Iterasi Maksimum (N_max)", min_value=1, value=st.session_state["acs_iter"], step=1)

        st.session_state["acs_m"] = acs_m
        st.session_state["acs_q0"] = acs_q0
        st.session_state["acs_rho"] = acs_rho
        st.session_state["acs_alpha"] = acs_alpha
        st.session_state["acs_beta"] = acs_beta
        st.session_state["acs_iter"] = acs_iter

        st.divider()
        if "df_data" not in st.session_state or "dist_matrix" not in st.session_state:
            st.warning("Silakan olah data terlebih dahulu di Tab 'Input & Preview Data'.")
        elif "solution_clusters" not in st.session_state:
            st.warning("Silakan jalankan inisialisasi pheromone awal terlebih dahulu di Tab 'Inisialisasi Pheromone Awal (NN)'.")
        else:
            if st.button("🐜 Jalankan Perhitungan ACS", type="primary"):
                with st.spinner("Menjalankan iterasi Ant Colony System (ACS)..."):
                    df_curr = st.session_state["df_data"].reset_index(drop=True)
                    dist_arr = st.session_state["dist_matrix"].values.tolist()
                    capacity = st.session_state.get("kapasitas_kendaraan", 100)
                    bo = st.session_state.get("biaya_operasional", 10000)
                    p_limit = int(st.session_state.get("max_rute_p", 10))
                    no_to_idx = {int(row["No"]): idx for idx, row in df_curr.iterrows()}
                    demand_dict = {int(row["No"]): float(row["Permintaan (Demand)"]) for _, row in df_curr.iterrows()}
                    all_cust_nodes = [int(row["No"]) for _, row in df_curr[df_curr["No"] != 0].iterrows()]
                    n_cust = len(all_cust_nodes)

                    predecessors_parsed = {}
                    pred_dict_str = st.session_state.get("predecessor_dict", {})
                    for p_id_str, p_set_str in pred_dict_str.items():
                        p_id = int(p_id_str)
                        cleaned = p_set_str.replace("{", "").replace("}", "").strip()
                        if cleaned:
                            predecessors_parsed[p_id] = tuple(int(x.strip()) for x in cleaned.split(",") if x.strip().isdigit())
                        else:
                            predecessors_parsed[p_id] = ()

                    initial_clusters = st.session_state["solution_clusters"]
                    L0 = sum(c["distance"] for c in initial_clusters)
                    tau_0 = st.session_state.get("nn_tau0", 1.0 / (n_cust * L0) if (n_cust * L0) > 0 else 0.0001)
                    
                    n_nodes = len(df_curr)
                    eta_pow_matrix = [[0.0] * n_nodes for _ in range(n_nodes)]
                    for i in range(n_nodes):
                        for j in range(n_nodes):
                            if i != j and dist_arr[i][j] > 0:
                                eta_pow_matrix[i][j] = (1.0 / dist_arr[i][j]) ** acs_beta

                    def build_ant_tour(tau_mat):
                        unserved = set(all_cust_nodes)
                        served = set()
                        ant_routes = []
                        idx_depot = no_to_idx[0]

                        while unserved:
                            curr_route = []
                            curr_load = 0.0

                            valid_start_cands = [
                                c for c in unserved
                                if demand_dict[c] <= capacity
                                and all(p in served for p in predecessors_parsed.get(c, ()))
                            ]
                            if not valid_start_cands:
                                return None

                            first_node = random.choice(valid_start_cands)

                            curr_route.append(first_node)
                            curr_load += demand_dict[first_node]
                            served.add(first_node)
                            unserved.remove(first_node)

                            idx_j = no_to_idx[first_node]
                            val_tau = (1 - acs_rho) * tau_mat[idx_depot][idx_j] + acs_rho * tau_0
                            tau_mat[idx_depot][idx_j] = val_tau
                            tau_mat[idx_j][idx_depot] = val_tau
                            curr_node = first_node

                            while True:
                                rem_cap = capacity - curr_load
                                valid_next = [
                                    cand for cand in unserved
                                    if demand_dict[cand] <= rem_cap
                                    and all(p in served for p in predecessors_parsed.get(cand, ()))
                                ]
                                if not valid_next:
                                    idx_curr = no_to_idx[curr_node]
                                    val_tau = (1 - acs_rho) * tau_mat[idx_curr][idx_depot] + acs_rho * tau_0
                                    tau_mat[idx_curr][idx_depot] = val_tau
                                    tau_mat[idx_depot][idx_curr] = val_tau
                                    break

                                idx_curr = no_to_idx[curr_node]
                                tau_row = tau_mat[idx_curr]
                                eta_row = eta_pow_matrix[idx_curr]
                                q = random.random()

                                if q <= acs_q0:
                                    next_node = max(valid_next, key=lambda c: tau_row[no_to_idx[c]] * eta_row[no_to_idx[c]])
                                else:
                                    scores = [tau_row[no_to_idx[c]] * eta_row[no_to_idx[c]] for c in valid_next]
                                    tot_s = sum(scores)
                                    next_node = random.choices(valid_next, weights=scores, k=1)[0] if tot_s > 0 else random.choice(valid_next)

                                curr_route.append(next_node)
                                curr_load += demand_dict[next_node]
                                served.add(next_node)
                                unserved.remove(next_node)

                                idx_next = no_to_idx[next_node]
                                val_tau = (1 - acs_rho) * tau_mat[idx_curr][idx_next] + acs_rho * tau_0
                                tau_mat[idx_curr][idx_next] = val_tau
                                tau_mat[idx_next][idx_curr] = val_tau
                                curr_node = next_node

                            ant_routes.append(curr_route)

                        return ant_routes

                    def calc_tour_dist(routes):
                        idx_depot = no_to_idx[0]
                        tot = 0
                        for r in routes:
                            prev = idx_depot
                            for node in r:
                                curr = no_to_idx[node]
                                tot += dist_arr[prev][curr]
                                prev = curr
                            tot += dist_arr[prev][idx_depot]
                        return tot

                    global_best_routes = None
                    global_best_dist = float('inf')
                    best_ant_id = 1
                    best_iter_id = 1
                    iteration_logs = []
                    idx_depot = no_to_idx[0]

                    for k_ant in range(1, acs_m + 1):
                        tau_matrix = [[tau_0] * n_nodes for _ in range(n_nodes)]
                        ant_best_routes = None
                        ant_best_dist = float('inf')

                        for it in range(1, acs_iter + 1):
                            n_trials = 1 if it == 1 else max(5, n_cust)
                            trial_best_routes = None
                            trial_best_dist = float('inf')

                            for _ in range(n_trials):
                                tau_copy = [row[:] for row in tau_matrix]
                                cand_routes = build_ant_tour(tau_copy)
                                if cand_routes is not None:
                                    cand_dist = calc_tour_dist(cand_routes)
                                    if cand_dist < trial_best_dist:
                                        trial_best_dist = cand_dist
                                        trial_best_routes = cand_routes
                                        best_tau_after_local = tau_copy

                            if trial_best_routes is not None:
                                tau_matrix = best_tau_after_local
                                if trial_best_dist <= ant_best_dist:
                                    ant_best_dist = trial_best_dist
                                    ant_best_routes = [r[:] for r in trial_best_routes]

                                if ant_best_dist > 0:
                                    delta_tau = 1.0 / ant_best_dist
                                    for r in ant_best_routes:
                                        prev = idx_depot
                                        for node in r:
                                            curr = no_to_idx[node]
                                            val_tau = (1 - acs_alpha) * tau_matrix[prev][curr] + acs_alpha * delta_tau
                                            tau_matrix[prev][curr] = val_tau
                                            tau_matrix[curr][prev] = val_tau
                                            prev = curr
                                        val_tau = (1 - acs_alpha) * tau_matrix[prev][idx_depot] + acs_alpha * delta_tau
                                        tau_matrix[prev][idx_depot] = val_tau
                                        tau_matrix[idx_depot][prev] = val_tau

                                if ant_best_dist < global_best_dist:
                                    global_best_dist = ant_best_dist
                                    global_best_routes = [r[:] for r in ant_best_routes]
                                    best_ant_id = k_ant
                                    best_iter_id = it

                                num_veh_iter = math.ceil(len(ant_best_routes) / p_limit)
                                iteration_logs.append({
                                    "Semut ke-": k_ant,
                                    "Iterasi ke-": it,
                                    "Jumlah Rute": len(ant_best_routes),
                                    "Jumlah Kendaraan": num_veh_iter,
                                    "Total Jarak (km)": ant_best_dist,
                                    "Total Biaya (Rp)": ant_best_dist * bo
                                })

                if global_best_routes is not None:
                    num_vehicles_acs = math.ceil(len(global_best_routes) / p_limit)
                    st.session_state["acs_results"] = {
                        "tau_0": tau_0,
                        "global_best_dist": global_best_dist,
                        "global_best_cost": global_best_dist * bo,
                        "global_best_routes": global_best_routes,
                        "num_vehicles": num_vehicles_acs,
                        "max_rute_p": p_limit,
                        "best_ant_id": best_ant_id,
                        "best_iter_id": best_iter_id,
                        "iteration_logs": pd.DataFrame(iteration_logs)
                    }
                    if "rvnd_results" in st.session_state:
                        del st.session_state["rvnd_results"]
                    st.success(f"Perhitungan ACS Berhasil! Terbentuk {len(global_best_routes)} rute dengan {num_vehicles_acs} kendaraan, Total Jarak = {global_best_dist} km.")
                else:
                    st.error("Tidak ditemukan solusi layak (feasible) pada proses ACS. Periksa aturan Precedence Constraints atau kapasitas kendaraan.")

            if "acs_results" in st.session_state:
                res = st.session_state["acs_results"]
                df_curr = st.session_state["df_data"].reset_index(drop=True)
                bo = st.session_state.get("biaya_operasional", 10000)
                capacity = st.session_state.get("kapasitas_kendaraan", 100)
                p_limit_curr = int(st.session_state.get("max_rute_p", 10))
                no_to_idx = {int(row["No"]): idx for idx, row in df_curr.iterrows()}
                demand_dict = {int(row["No"]): float(row["Permintaan (Demand)"]) for _, row in df_curr.iterrows()}
                dist_arr = st.session_state["dist_matrix"].values.tolist()
                predecessors_parsed = {}
                pred_dict_str = st.session_state.get("predecessor_dict", {})
                for p_id_str, p_set_str in pred_dict_str.items():
                    p_id = int(p_id_str)
                    cleaned = p_set_str.replace("{", "").replace("}", "").strip()
                    if cleaned:
                        predecessors_parsed[p_id] = [int(x.strip()) for x in cleaned.split(",") if x.strip().isdigit()]
                    else:
                        predecessors_parsed[p_id] = []

                best_routes = res["global_best_routes"]
                num_vehicles_acs = math.ceil(len(best_routes) / p_limit_curr)

                st.divider()
                st.subheader("Hasil Perhitungan Ant Colony System (ACS)")
                st.caption(f"Intensitas Pheromone Awal (τ₀): **{res['tau_0']:.8f}**")
                
                with st.expander("🔍 Lihat Tabel Hasil Penentuan Rute Terbaik (Per Semut & Iterasi)", expanded=False):
                    st.dataframe(res["iteration_logs"], use_container_width=True, hide_index=True)

                st.divider()
                st.subheader("Solusi Rute Terbaik ACS & Alokasi Kendaraan (Global Best Tour)")
                colors = ['#007bff', '#28a745', '#fd7e14', '#dc3545', '#6f42c1', '#17a2b8']
                tot_load_all = 0

                cols_per_row = 3
                for idx_step in range(0, len(best_routes), cols_per_row):
                    grid_cols = st.columns(cols_per_row)
                    for i in range(cols_per_row):
                        if idx_step + i < len(best_routes):
                            route_idx = idx_step + i
                            r = best_routes[route_idx]
                            veh_id = (route_idx // p_limit_curr) + 1
                            trip_in_veh = (route_idx % p_limit_curr) + 1
                            route_names = ["0"] + [f"P{node}" for node in r] + ["0"]
                            route_str = " ➔ ".join(route_names)
                            r_load = sum(demand_dict[node] for node in r)
                            tot_load_all += r_load
                            full_r = [0] + r + [0]
                            r_dist = sum(dist_arr[no_to_idx[full_r[k]]][no_to_idx[full_r[k+1]]] for k in range(len(full_r)-1))
                            r_cost = r_dist * bo
                            with grid_cols[i]:
                                st.markdown(f"""
                                    <div class="route-card" style="border-left: 5px solid {colors[(veh_id - 1) % len(colors)]};">
                                        <h4 style="margin:0; color: #004085; font-size: 15px;"><i class="fa-solid fa-truck"></i> Kendaraan {veh_id} — Trip {trip_in_veh}/{p_limit_curr} (Rute {route_idx + 1})</h4>
                                        <p style="margin: 6px 0 0 0; font-size: 13px;"><b>Rute:</b> {route_str}</p>
                                        <p style="margin: 3px 0 0 0; font-size: 12px; color: #555;"><i class="fa-solid fa-boxes-packing"></i> <b>Muatan:</b> {int(r_load)}/{capacity} unit</p>
                                        <p style="margin: 3px 0 0 0; font-size: 12px; color: #555;"><i class="fa-solid fa-ruler-horizontal"></i> <b>Jarak:</b> {r_dist} km</p>
                                        <p style="margin: 3px 0 0 0; font-size: 12px; color: #0056b3;"><i class="fa-solid fa-money-bill-wave"></i> <b>Biaya:</b> Rp {r_cost:,.0f}</p>
                                    </div>
                                """, unsafe_allow_html=True)

                st.markdown(f"""
                    <div style="background: #ffffff; padding: 16px; border-radius: 12px; border: 1px solid #b8daff; box-shadow: 0 4px 10px rgba(0,123,255,0.08); margin-top: 8px; margin-bottom: 16px;">
                        <h4 style="margin:0; color: #004085; font-size: 16px;"><i class="fa-solid fa-clipboard-check"></i> Ringkasan Total Seluruh Rute & Kendaraan ACS</h4>
                        <p style="margin: 6px 0 0 0; font-size: 14px; color: #004085;">
                            <b>Jumlah Kendaraan Terbentuk:</b> {num_vehicles_acs} unit &nbsp;|&nbsp;
                            <b>Jumlah Rute:</b> {len(best_routes)} rute &nbsp;|&nbsp; 
                            <b>Total Permintaan:</b> {int(tot_load_all)} unit &nbsp;|&nbsp; 
                            <b>Total Jarak:</b> {res['global_best_dist']} km &nbsp;|&nbsp; 
                            <b>Total Biaya Keseluruhan:</b> Rp {res['global_best_cost']:,.0f}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                st.divider()
                st.subheader("Visualisasi Rute Terbaik ACS")
                fig_acs = go.Figure()
                coords = df_curr[["Koordinat X", "Koordinat Y"]].values
                depot_x, depot_y = coords[0][0], coords[0][1]
                fig_acs.add_trace(go.Scatter(
                    x=[depot_x], y=[depot_y],
                    mode='markers+text', marker=dict(color='#dc3545', size=18, symbol='square'),
                    text=["0"], textposition="bottom center", name="Depot (0)"
                ))
                for idx, r in enumerate(best_routes):
                    veh_id = (idx // p_limit_curr) + 1
                    trip_in_veh = (idx % p_limit_curr) + 1
                    color_code = colors[idx % len(colors)]
                    route_nodes = [0] + r + [0]
                    rx = [coords[no_to_idx[node]][0] for node in route_nodes]
                    ry = [coords[no_to_idx[node]][1] for node in route_nodes]
                    fig_acs.add_trace(go.Scatter(
                        x=rx, y=ry, mode='lines+markers+text',
                        line=dict(color=color_code, width=2.5),
                        marker=dict(size=12, color=color_code),
                        text=[str(node) if node != 0 else "" for node in route_nodes],
                        textposition="top center", name=f"K{veh_id}-Trip {trip_in_veh} (Rute {idx+1})",
                        hoverinfo='text', hovertext=[f"Kendaraan {veh_id} - Rute {idx+1}: {df_curr.iloc[no_to_idx[node]]['Nama Pelanggan']}" for node in route_nodes]
                    ))
                    for k in range(len(route_nodes) - 1):
                        x_start, y_start = rx[k], ry[k]
                        x_end, y_end = rx[k+1], ry[k+1]
                        fig_acs.add_annotation(
                            x=(x_start + x_end) / 2, y=(y_start + y_end) / 2,
                            ax=x_start, ay=y_start, xref="x", yref="y", axref="x", ayref="y",
                            showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2, arrowcolor=color_code
                        )
                and_text_lines = []
                for p_id in sorted(predecessors_parsed.keys()):
                    preds = predecessors_parsed[p_id]
                    if preds:
                        preds_str = "{" + ",".join(map(str, preds)) + "}"
                        and_text_lines.append(f"<b>AND<sub>{p_id}</sub></b> = {preds_str}")
                
                if and_text_lines and len(and_text_lines) <= 15:
                    fig_acs.add_annotation(
                        xref="paper", yref="paper", x=0.98, y=0.98,
                        text=f"<b>Aturan Precedence (AND-PC):</b><br>{'<br>'.join(and_text_lines)}",
                        showarrow=False, bordercolor="#0056b3", borderwidth=1, borderpad=8, bgcolor="#ffffff", opacity=0.9, align="left"
                    )
                min_x, max_x = coords[:, 0].min(), coords[:, 0].max()
                min_y, max_y = coords[:, 1].min(), coords[:, 1].max()
                fig_acs.update_layout(
                    width=850, height=550, margin=dict(l=40, r=40, t=30, b=40),
                    xaxis=dict(title="Koordinat X", range=[min_x - 8, max_x + 8], showgrid=True, gridcolor='#e1effe'),
                    yaxis=dict(title="Koordinat Y", range=[min_y - 8, max_y + 8], showgrid=True, gridcolor='#e1effe'),
                    template="plotly_white", legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)")
                )
                st.plotly_chart(fig_acs, use_container_width=True, key="plot_tab3_acs")

    # --- TAB 4: PERBAIKAN RVND ---
    with tab4:
        st.subheader("Perbaikan Solusi dengan Randomized Variable Neighborhood Descent (RVND)")
        p_limit_curr = int(st.session_state.get("max_rute_p", 10))
        st.caption(f"Proses perbaikan rute hasil ACS menggunakan lingkungan pencarian lokal (Neighborhood Structures) RVND dengan tetap memperhatikan kapasitas kendaraan, aturan AND-PCs, serta batas maksimum rute kendaraan.")
        if "acs_results" not in st.session_state:
            st.warning("Silakan jalankan perhitungan ACS terlebih dahulu pada Tab 'Proses ACS'.")
        else:
            df_curr = st.session_state["df_data"].reset_index(drop=True)
            dist_arr = st.session_state["dist_matrix"].values.tolist()
            capacity = st.session_state.get("kapasitas_kendaraan", 100)
            bo = st.session_state.get("biaya_operasional", 10000)

            no_to_idx = {int(row["No"]): idx for idx, row in df_curr.iterrows()}
            demand_dict = {int(row["No"]): float(row["Permintaan (Demand)"]) for _, row in df_curr.iterrows()}

            predecessors_parsed = {}
            pred_dict_str = st.session_state.get("predecessor_dict", {})
            for p_id_str, p_set_str in pred_dict_str.items():
                p_id = int(p_id_str)
                cleaned = p_set_str.replace("{", "").replace("}", "").strip()
                if cleaned:
                    predecessors_parsed[p_id] = tuple(int(x.strip()) for x in cleaned.split(",") if x.strip().isdigit())
                else:
                    predecessors_parsed[p_id] = ()

            def check_rvnd_validity(routes):
                served_set = set()
                for r in routes:
                    if not r:
                        continue
                    r_load = 0.0
                    for node in r:
                        r_load += demand_dict[node]
                        if r_load > capacity:
                            return False
                        for p in predecessors_parsed.get(node, ()):
                            if p not in served_set:
                                return False
                        served_set.add(node)
                return True

            def get_total_distance(routes):
                tot = 0
                idx0 = no_to_idx[0]
                for r in routes:
                    if not r:
                        continue
                    prev = idx0
                    for node in r:
                        curr = no_to_idx[node]
                        tot += dist_arr[prev][curr]
                        prev = curr
                    tot += dist_arr[prev][idx0]
                return tot

            def clone_routes(routes):
                return [r[:] for r in routes]

            def op_swap_1_1(routes):
                best_r = routes
                best_d = get_total_distance(routes)
                improved = False
                n_r = len(routes)
                for r1 in range(n_r):
                    for r2 in range(r1 + 1, n_r):
                        for i in range(len(routes[r1])):
                            for j in range(len(routes[r2])):
                                cand = clone_routes(routes)
                                cand[r1][i], cand[r2][j] = cand[r2][j], cand[r1][i]
                                if check_rvnd_validity(cand):
                                    d = get_total_distance(cand)
                                    if d < best_d:
                                        best_d = d
                                        best_r = cand
                                        improved = True
                return best_r, best_d, improved

            def op_swap_2_2(routes):
                best_r = routes
                best_d = get_total_distance(routes)
                improved = False
                n_r = len(routes)
                for r1 in range(n_r):
                    if len(routes[r1]) < 2: continue
                    for r2 in range(r1 + 1, n_r):
                        if len(routes[r2]) < 2: continue
                        for i in range(len(routes[r1]) - 1):
                            for j in range(len(routes[r2]) - 1):
                                cand = clone_routes(routes)
                                cand[r1][i:i+2], cand[r2][j:j+2] = cand[r2][j:j+2], cand[r1][i:i+2]
                                if check_rvnd_validity(cand):
                                    d = get_total_distance(cand)
                                    if d < best_d:
                                        best_d = d
                                        best_r = cand
                                        improved = True
                return best_r, best_d, improved

            def op_swap_2_1(routes):
                best_r = routes
                best_d = get_total_distance(routes)
                improved = False
                n_r = len(routes)
                for r1 in range(n_r):
                    if len(routes[r1]) < 2: continue
                    for r2 in range(n_r):
                        if r1 == r2 or len(routes[r2]) < 1: continue
                        for i in range(len(routes[r1]) - 1):
                            for j in range(len(routes[r2])):
                                cand = clone_routes(routes)
                                seg2 = cand[r1][i:i+2]
                                node1 = cand[r2][j]
                                cand[r1] = cand[r1][:i] + [node1] + cand[r1][i+2:]
                                cand[r2] = cand[r2][:j] + seg2 + cand[r2][j+1:]
                                if check_rvnd_validity(cand):
                                    d = get_total_distance(cand)
                                    if d < best_d:
                                        best_d = d
                                        best_r = cand
                                        improved = True
                return best_r, best_d, improved

            def op_shift_1_0(routes):
                best_r = routes
                best_d = get_total_distance(routes)
                improved = False
                n_r = len(routes)
                for r1 in range(n_r):
                    if not routes[r1]: continue
                    for r2 in range(n_r):
                        if r1 == r2: continue
                        for i in range(len(routes[r1])):
                            node = routes[r1][i]
                            for j in range(len(routes[r2]) + 1):
                                cand = clone_routes(routes)
                                cand[r1].pop(i)
                                cand[r2].insert(j, node)
                                cand_clean = [r for r in cand if r]
                                if check_rvnd_validity(cand_clean):
                                    d = get_total_distance(cand_clean)
                                    if d < best_d:
                                        best_d = d
                                        best_r = cand_clean
                                        improved = True
                return best_r, best_d, improved

            def op_shift_2_0(routes):
                best_r = routes
                best_d = get_total_distance(routes)
                improved = False
                n_r = len(routes)
                for r1 in range(n_r):
                    if len(routes[r1]) < 2: continue
                    for r2 in range(n_r):
                        if r1 == r2: continue
                        for i in range(len(routes[r1]) - 1):
                            seg = routes[r1][i:i+2]
                            for j in range(len(routes[r2]) + 1):
                                cand = clone_routes(routes)
                                del cand[r1][i:i+2]
                                cand[r2] = cand[r2][:j] + seg + cand[r2][j:]
                                cand_clean = [r for r in cand if r]
                                if check_rvnd_validity(cand_clean):
                                    d = get_total_distance(cand_clean)
                                    if d < best_d:
                                        best_d = d
                                        best_r = cand_clean
                                        improved = True
                return best_r, best_d, improved

            def op_cross(routes):
                best_r = routes
                best_d = get_total_distance(routes)
                improved = False
                n_r = len(routes)
                for r1 in range(n_r):
                    for r2 in range(r1 + 1, n_r):
                        for i in range(1, len(routes[r1])):
                            for j in range(1, len(routes[r2])):
                                cand = clone_routes(routes)
                                cand[r1], cand[r2] = cand[r1][:i] + cand[r2][j:], cand[r2][:j] + cand[r1][i:]
                                cand_clean = [r for r in cand if r]
                                if check_rvnd_validity(cand_clean):
                                    d = get_total_distance(cand_clean)
                                    if d < best_d:
                                        best_d = d
                                        best_r = cand_clean
                                        improved = True
                return best_r, best_d, improved

            def op_or_opt(routes):
                best_r = routes
                best_d = get_total_distance(routes)
                improved = False
                for r_idx, r in enumerate(routes):
                    if len(r) < 3: continue
                    for seg_len in (2, 3):
                        if len(r) < seg_len: continue
                        for i in range(len(r) - seg_len + 1):
                            seg = r[i:i+seg_len]
                            rem = r[:i] + r[i+seg_len:]
                            for j in range(len(rem) + 1):
                                if j == i: continue
                                cand = clone_routes(routes)
                                cand[r_idx] = rem[:j] + seg + rem[j:]
                                if check_rvnd_validity(cand):
                                    d = get_total_distance(cand)
                                    if d < best_d:
                                        best_d = d
                                        best_r = cand
                                        improved = True
                return best_r, best_d, improved

            def op_2opt_intra(routes):
                best_r = routes
                best_d = get_total_distance(routes)
                improved = False
                for r_idx, r in enumerate(routes):
                    if len(r) < 3: continue
                    for i in range(len(r) - 1):
                        for j in range(i + 2, len(r) + 1):
                            cand = clone_routes(routes)
                            cand[r_idx] = r[:i] + list(reversed(r[i:j])) + r[j:]
                            if check_rvnd_validity(cand):
                                d = get_total_distance(cand)
                                if d < best_d:
                                    best_d = d
                                    best_r = cand
                                    improved = True
                return best_r, best_d, improved

            def op_reinsertion_intra(routes):
                best_r = routes
                best_d = get_total_distance(routes)
                improved = False
                for r_idx, r in enumerate(routes):
                    if len(r) < 2: continue
                    for i in range(len(r)):
                        node = r[i]
                        rem = r[:i] + r[i+1:]
                        for j in range(len(rem) + 1):
                            if j == i: continue
                            cand = clone_routes(routes)
                            cand[r_idx] = rem[:j] + [node] + rem[j:]
                            if check_rvnd_validity(cand):
                                d = get_total_distance(cand)
                                if d < best_d:
                                    best_d = d
                                    best_r = cand
                                    improved = True
                return best_r, best_d, improved

            def op_exchange_intra(routes):
                best_r = routes
                best_d = get_total_distance(routes)
                improved = False
                for r_idx, r in enumerate(routes):
                    if len(r) < 2: continue
                    for i in range(len(r)):
                        for j in range(i + 1, len(r)):
                            cand = clone_routes(routes)
                            cand[r_idx][i], cand[r_idx][j] = cand[r_idx][j], cand[r_idx][i]
                            if check_rvnd_validity(cand):
                                d = get_total_distance(cand)
                                if d < best_d:
                                    best_d = d
                                    best_r = cand
                                    improved = True
                return best_r, best_d, improved

            operator_funcs = {
                "Swap (1,1)": op_swap_1_1, "Swap (2,2)": op_swap_2_2, "Swap (2,1)": op_swap_2_1,
                "Shift (1,0)": op_shift_1_0, "Shift (2,0)": op_shift_2_0, "Cross": op_cross,
                "Or-Opt": op_or_opt, "2-Opt": op_2opt_intra, "Reinsertion": op_reinsertion_intra, "Exchange": op_exchange_intra
            }

            if st.button("🔄 Jalankan Perbaikan RVND", type="primary"):
                with st.spinner("Sedang menjalankan pencarian lokal RVND..."):
                    p_limit_rvnd = int(st.session_state.get("max_rute_p", 10))
                    initial_routes = clone_routes(st.session_state["acs_results"]["global_best_routes"])
                    current_routes = clone_routes(initial_routes)
                    current_dist = get_total_distance(current_routes)
                    NL_master = ["Swap (1,1)", "Swap (2,2)", "Swap (2,1)", "Shift (1,0)", "Shift (2,0)", "Cross"]
                    NL_prime_master = ["Or-Opt", "2-Opt", "Reinsertion", "Exchange"]
                    NL = NL_master[:]
                    rvnd_logs = []
                    step_counter = 1
                    max_improvements = 100

                    while len(NL) > 0 and step_counter <= max_improvements:
                        op_inter_name = random.choice(NL)
                        best_inter_routes, best_inter_dist, improved_inter = operator_funcs[op_inter_name](current_routes)
                        if improved_inter:
                            saved_dist = current_dist - best_inter_dist
                            current_routes = clone_routes(best_inter_routes)
                            current_dist = best_inter_dist
                            
                            rvnd_logs.append({
                                "Langkah": step_counter, "Tipe": "Inter-Route", "Operator Tetangga": op_inter_name,
                                "Status Perbaikan": "Lebih Baik", "Total Jarak (km)": current_dist, "Hemat Biaya (Rp)": saved_dist * bo
                            })
                            step_counter += 1
                            NL = NL_master[:]
                            NL_prime = NL_prime_master[:]
                            while len(NL_prime) > 0 and step_counter <= max_improvements:
                                op_intra_name = random.choice(NL_prime)
                                best_intra_routes, best_intra_dist, improved_intra = operator_funcs[op_intra_name](current_routes)
                                if improved_intra:
                                    saved_intra_dist = current_dist - best_intra_dist
                                    current_routes = clone_routes(best_intra_routes)
                                    current_dist = best_intra_dist
                                    rvnd_logs.append({
                                        "Langkah": step_counter, "Tipe": "Intra-Route", "Operator Tetangga": op_intra_name,
                                        "Status Perbaikan": "Lebih Baik", "Total Jarak (km)": current_dist, "Hemat Biaya (Rp)": saved_intra_dist * bo
                                    })
                                    step_counter += 1
                                    NL_prime = NL_prime_master[:]
                                else:
                                    NL_prime.remove(op_intra_name)
                        else:
                            NL.remove(op_inter_name)

                    final_routes = [r for r in current_routes if len(r) > 0]
                    final_dist = get_total_distance(final_routes)
                    num_vehicles_rvnd = math.ceil(len(final_routes) / p_limit_rvnd)
                    st.session_state["rvnd_results"] = {
                        "final_routes": final_routes,
                        "final_dist": final_dist,
                        "final_cost": final_dist * bo,
                        "num_vehicles": num_vehicles_rvnd,
                        "max_rute_p": p_limit_rvnd,
                        "rvnd_logs": pd.DataFrame(rvnd_logs) if rvnd_logs else pd.DataFrame([{
                            "Langkah": 1, "Tipe": "Konvergen", "Operator Tetangga": "-", 
                            "Status Perbaikan": "Optimal (ACS)", "Total Jarak (km)": final_dist, "Hemat Biaya (Rp)": 0
                        }])
                    }
                st.success(f"Perbaikan RVND Selesai! Terbentuk {len(final_routes)} rute dengan {num_vehicles_rvnd} kendaraan, Total Jarak = {final_dist} km.")

            if "rvnd_results" in st.session_state:
                res_rvnd = st.session_state["rvnd_results"]
                p_limit_curr = int(st.session_state.get("max_rute_p", 10))
                final_routes = res_rvnd["final_routes"]
                num_vehicles_rvnd = math.ceil(len(final_routes) / p_limit_curr)
                
                st.divider()
                with st.expander("🔍 Lihat Log Perbaikan Iterasi RVND (Langkah demi Langkah)", expanded=False):
                    st.dataframe(res_rvnd["rvnd_logs"], use_container_width=True, hide_index=True)

                st.divider()
                st.subheader("Hasil Akhir Rute & Alokasi Kendaraan Perbaikan RVND")
                colors = ['#007bff', '#28a745', '#fd7e14', '#dc3545', '#6f42c1', '#17a2b8']
                tot_load_all = 0

                cols_per_row = 3
                for idx_step in range(0, len(final_routes), cols_per_row):
                    grid_cols = st.columns(cols_per_row)
                    for i in range(cols_per_row):
                        if idx_step + i < len(final_routes):
                            route_idx = idx_step + i
                            r = final_routes[route_idx]
                            veh_id = (route_idx // p_limit_curr) + 1
                            trip_in_veh = (route_idx % p_limit_curr) + 1
                            route_names = ["0"] + [f"P{node}" for node in r] + ["0"]
                            route_str = " ➔ ".join(route_names)
                            r_load = sum(demand_dict[node] for node in r)
                            tot_load_all += r_load
                            full_r = [0] + r + [0]
                            r_dist = sum(dist_arr[no_to_idx[full_r[k]]][no_to_idx[full_r[k+1]]] for k in range(len(full_r)-1))
                            r_cost = r_dist * bo
                            with grid_cols[i]:
                                st.markdown(f"""
                                    <div class="route-card" style="border-left: 5px solid {colors[(veh_id - 1) % len(colors)]};">
                                        <h4 style="margin:0; color: #004085; font-size: 15px;"><i class="fa-solid fa-truck"></i> Kendaraan {veh_id} — Trip {trip_in_veh}/{p_limit_curr} (Rute {route_idx + 1})</h4>
                                        <p style="margin: 6px 0 0 0; font-size: 13px;"><b>Rute:</b> {route_str}</p>
                                        <p style="margin: 3px 0 0 0; font-size: 12px; color: #555;"><i class="fa-solid fa-boxes-packing"></i> <b>Muatan:</b> {int(r_load)}/{capacity} unit</p>
                                        <p style="margin: 3px 0 0 0; font-size: 12px; color: #555;"><i class="fa-solid fa-ruler-horizontal"></i> <b>Jarak:</b> {r_dist} km</p>
                                        <p style="margin: 3px 0 0 0; font-size: 12px; color: #0056b3;"><i class="fa-solid fa-money-bill-wave"></i> <b>Biaya:</b> Rp {r_cost:,.0f}</p>
                                    </div>
                                """, unsafe_allow_html=True)

                st.markdown(f"""
                    <div style="background: #ffffff; padding: 16px; border-radius: 12px; border: 1px solid #b8daff; box-shadow: 0 4px 10px rgba(0,123,255,0.08); margin-top: 8px; margin-bottom: 16px;">
                        <h4 style="margin:0; color: #004085; font-size: 16px;"><i class="fa-solid fa-clipboard-check"></i> Ringkasan Total Seluruh Rute & Kendaraan RVND</h4>
                        <p style="margin: 6px 0 0 0; font-size: 14px; color: #004085;">
                            <b>Jumlah Kendaraan Terbentuk:</b> {num_vehicles_rvnd} unit &nbsp;|&nbsp;
                            <b>Jumlah Rute:</b> {len(final_routes)} rute &nbsp;|&nbsp; 
                            <b>Total Permintaan:</b> {int(tot_load_all)} unit &nbsp;|&nbsp; 
                            <b>Total Jarak:</b> {res_rvnd['final_dist']} km &nbsp;|&nbsp; 
                            <b>Total Biaya Keseluruhan:</b> Rp {res_rvnd['final_cost']:,.0f}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                st.divider()
                st.subheader("Visualisasi Rute Perbaikan RVND")
                fig_rvnd = go.Figure()
                coords = df_curr[["Koordinat X", "Koordinat Y"]].values
                depot_x, depot_y = coords[0][0], coords[0][1]
                fig_rvnd.add_trace(go.Scatter(
                    x=[depot_x], y=[depot_y],
                    mode='markers+text', marker=dict(color='#dc3545', size=18, symbol='square'),
                    text=["0"], textposition="bottom center", name="Depot (0)"
                ))
                for idx, r in enumerate(final_routes):
                    veh_id = (idx // p_limit_curr) + 1
                    trip_in_veh = (idx % p_limit_curr) + 1
                    color_code = colors[idx % len(colors)]
                    route_nodes = [0] + r + [0]
                    rx = [coords[no_to_idx[node]][0] for node in route_nodes]
                    ry = [coords[no_to_idx[node]][1] for node in route_nodes]
                    fig_rvnd.add_trace(go.Scatter(
                        x=rx, y=ry, mode='lines+markers+text',
                        line=dict(color=color_code, width=2.5),
                        marker=dict(size=12, color=color_code),
                        text=[str(node) if node != 0 else "" for node in route_nodes],
                        textposition="top center", name=f"K{veh_id}-Trip {trip_in_veh} (Rute {idx+1})",
                        hoverinfo='text', hovertext=[f"Kendaraan {veh_id} - Rute RVND {idx+1}: {df_curr.iloc[no_to_idx[node]]['Nama Pelanggan']}" for node in route_nodes]
                    ))
                    for k in range(len(route_nodes) - 1):
                        x_start, y_start = rx[k], ry[k]
                        x_end, y_end = rx[k+1], ry[k+1]
                        fig_rvnd.add_annotation(
                            x=(x_start + x_end) / 2, y=(y_start + y_end) / 2,
                            ax=x_start, ay=y_start, xref="x", yref="y", axref="x", ayref="y",
                            showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2, arrowcolor=color_code
                        )
                and_text_lines = []
                for p_id in sorted(predecessors_parsed.keys()):
                    preds = predecessors_parsed[p_id]
                    if preds:
                        preds_str = "{" + ",".join(map(str, preds)) + "}"
                        and_text_lines.append(f"<b>AND<sub>{p_id}</sub></b> = {preds_str}")
                
                if and_text_lines and len(and_text_lines) <= 15:
                    fig_rvnd.add_annotation(
                        xref="paper", yref="paper", x=0.98, y=0.98,
                        text=f"<b>Aturan Precedence (AND-PCs):</b><br>{'<br>'.join(and_text_lines)}",
                        showarrow=False, bordercolor="#0056b3", borderwidth=1, borderpad=8, bgcolor="#ffffff", opacity=0.9, align="left"
                    )
                min_x, max_x = coords[:, 0].min(), coords[:, 0].max()
                min_y, max_y = coords[:, 1].min(), coords[:, 1].max()
                fig_rvnd.update_layout(
                    width=850, height=550, margin=dict(l=40, r=40, t=30, b=40),
                    xaxis=dict(title="Koordinat X", range=[min_x - 8, max_x + 8], showgrid=True, gridcolor='#e1effe'),
                    yaxis=dict(title="Koordinat Y", range=[min_y - 8, max_y + 8], showgrid=True, gridcolor='#e1effe'),
                    template="plotly_white", legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)")
                )
                st.plotly_chart(fig_rvnd, use_container_width=True, key="plot_tab4_rvnd")

    # --- TAB 5: HASIL EFISIENSI ---
    with tab5:
        st.subheader("Analisis Hasil Efisiensi (ACS vs ACS-RVND)")
        st.caption("Perbandingan efisiensi jarak tempuh, biaya operasional, serta jumlah kendaraan yang terbentuk sebelum dan setelah perbaikan RVND.")
        if "acs_results" not in st.session_state or "rvnd_results" not in st.session_state:
            st.warning("Silakan selesaikan perhitungan pada Tab 'Proses ACS' dan Tab 'Perbaikan RVND' terlebih dahulu.")
        else:
            p_limit_curr = int(st.session_state.get("max_rute_p", 10))
            acs_routes = st.session_state["acs_results"]["global_best_routes"]
            rvnd_routes = st.session_state["rvnd_results"]["final_routes"]
            acs_veh = math.ceil(len(acs_routes) / p_limit_curr)
            rvnd_veh = math.ceil(len(rvnd_routes) / p_limit_curr)

            acs_dist = st.session_state["acs_results"]["global_best_dist"]
            acs_cost = st.session_state["acs_results"]["global_best_cost"]
            
            rvnd_dist = st.session_state["rvnd_results"]["final_dist"]
            rvnd_cost = st.session_state["rvnd_results"]["final_cost"]
            dist_saved = acs_dist - rvnd_dist
            cost_saved = acs_cost - rvnd_cost
            efficiency_pct = (dist_saved / acs_dist * 100) if acs_dist > 0 else 0.0
            st.markdown("---")
            st.markdown("### <i class='fa-solid fa-chart-line'></i> Ringkasan Efisiensi Penghematan", unsafe_allow_html=True)
            col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
            col_m1.metric("Total Jarak ACS", f"{acs_dist} km", f"{len(acs_routes)} rute / {acs_veh} kend.")
            col_m2.metric("Total Jarak ACS-RVND", f"{rvnd_dist} km", f"-{dist_saved} km")
            col_m3.metric("Kendaraan Terbentuk", f"{rvnd_veh} unit", f"{len(rvnd_routes)} rute")
            col_m4.metric("Persentase Efisiensi", f"{efficiency_pct:.2f} %")
            col_m5.metric("Penghematan Biaya", f"Rp {cost_saved:,.0f}")
            st.markdown("---")
            st.markdown("### <i class='fa-solid fa-chart-column'></i> Grafik Perbandingan Hasil Solusi Menggunakan Algoritma ACS dan ACS-RVND", unsafe_allow_html=True)
            col_bar1, col_bar2 = st.columns(2)
            with col_bar1:
                fig_bar_dist = go.Figure()
                fig_bar_dist.add_trace(go.Bar(
                    x=["ACS", "ACS-RVND"],
                    y=[acs_dist, rvnd_dist],
                    text=[f"{acs_dist} km", f"{rvnd_dist} km"],
                    textposition='auto',
                    marker_color=['#fd7e14', '#007bff'],
                    width=0.4
                ))
                fig_bar_dist.update_layout(
                    title="<b>Perbandingan Total Jarak (km)</b>",
                    xaxis_title="Metode", yaxis_title="Jarak (km)",
                    template="plotly_white", height=380
                )
                st.plotly_chart(fig_bar_dist, use_container_width=True, key="plot_tab5_dist")
            with col_bar2:
                fig_bar_cost = go.Figure()
                fig_bar_cost.add_trace(go.Bar(
                    x=["ACS", "ACS-RVND"],
                    y=[acs_cost, rvnd_cost],
                    text=[f"Rp {acs_cost:,.0f}", f"Rp {rvnd_cost:,.0f}"],
                    textposition='auto',
                    marker_color=['#fd7e14', '#28a745'],
                    width=0.4
                ))
                fig_bar_cost.update_layout(
                    title="<b>Perbandingan Total Biaya Operasional (Rp)</b>",
                    xaxis_title="Metode", yaxis_title="Biaya (Rp)",
                    template="plotly_white", height=380
                )
                st.plotly_chart(fig_bar_cost, use_container_width=True, key="plot_tab5_cost")
            st.markdown("---")
            st.markdown("### <i class='fa-solid fa-draw-polygon'></i> Perbandingan Grafik Rute Kendaraan", unsafe_allow_html=True)
            df_curr = st.session_state["df_data"].reset_index(drop=True)
            coords = df_curr[["Koordinat X", "Koordinat Y"]].values
            depot_x, depot_y = coords[0][0], coords[0][1]
            no_to_idx = {int(row["No"]): idx for idx, row in df_curr.iterrows()}
            colors = ['#007bff', '#28a745', '#fd7e14', '#dc3545', '#6f42c1', '#17a2b8']
            min_x, max_x = coords[:, 0].min(), coords[:, 0].max()
            min_y, max_y = coords[:, 1].min(), coords[:, 1].max()

            # 1. Grafik Rute Solusi Awal ACS (Lebar Penuh)
            st.subheader(f"1. Rute Solusi Awal ACS ({len(acs_routes)} Rute | {acs_veh} Kendaraan)")
            fig_acs_cmp = go.Figure()
            fig_acs_cmp.add_trace(go.Scatter(
                x=[depot_x], y=[depot_y],
                mode='markers+text', marker=dict(color='#dc3545', size=18, symbol='square'),
                text=["0"], textposition="bottom center", name="Depot (0)"
            ))
            for idx, r in enumerate(acs_routes):
                veh_id = (idx // p_limit_curr) + 1
                trip_in_veh = (idx % p_limit_curr) + 1
                color_code = colors[idx % len(colors)]
                route_nodes = [0] + r + [0]
                rx = [coords[no_to_idx[node]][0] for node in route_nodes]
                ry = [coords[no_to_idx[node]][1] for node in route_nodes]
                fig_acs_cmp.add_trace(go.Scatter(
                    x=rx, y=ry, mode='lines+markers+text',
                    line=dict(color=color_code, width=2.5),
                    marker=dict(size=12, color=color_code),
                    text=[str(node) if node != 0 else "" for node in route_nodes],
                    textposition="top center", name=f"K{veh_id}-Trip {trip_in_veh} (Rute ACS {idx+1})",
                    hoverinfo='text', hovertext=[f"Kendaraan {veh_id} - Rute ACS {idx+1}: {df_curr.iloc[no_to_idx[node]]['Nama Pelanggan']}" for node in route_nodes]
                ))
                for k in range(len(route_nodes) - 1):
                    x_start, y_start = rx[k], ry[k]
                    x_end, y_end = rx[k+1], ry[k+1]
                    fig_acs_cmp.add_annotation(
                        x=(x_start + x_end) / 2, y=(y_start + y_end) / 2,
                        ax=x_start, ay=y_start,
                        xref="x", yref="y", axref="x", ayref="y",
                        showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2, arrowcolor=color_code
                    )
            fig_acs_cmp.update_layout(
                width=850, height=550, margin=dict(l=40, r=40, t=30, b=40),
                xaxis=dict(title="Koordinat X", range=[min_x - 8, max_x + 8], showgrid=True, gridcolor='#e1effe'),
                yaxis=dict(title="Koordinat Y", range=[min_y - 8, max_y + 8], showgrid=True, gridcolor='#e1effe'),
                template="plotly_white", legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)")
            )
            st.plotly_chart(fig_acs_cmp, use_container_width=True, key="plot_tab5_acs")

            st.divider()

            # 2. Grafik Rute Akhir ACS-RVND (Lebar Penuh)
            st.subheader(f"2. Rute Akhir ACS-RVND ({len(rvnd_routes)} Rute | {rvnd_veh} Kendaraan)")
            fig_rvnd_cmp = go.Figure()
            fig_rvnd_cmp.add_trace(go.Scatter(
                x=[depot_x], y=[depot_y],
                mode='markers+text', marker=dict(color='#dc3545', size=18, symbol='square'),
                text=["0"], textposition="bottom center", name="Depot (0)"
            ))
            for idx, r in enumerate(rvnd_routes):
                veh_id = (idx // p_limit_curr) + 1
                trip_in_veh = (idx % p_limit_curr) + 1
                color_code = colors[idx % len(colors)]
                route_nodes = [0] + r + [0]
                rx = [coords[no_to_idx[node]][0] for node in route_nodes]
                ry = [coords[no_to_idx[node]][1] for node in route_nodes]
                fig_rvnd_cmp.add_trace(go.Scatter(
                    x=rx, y=ry, mode='lines+markers+text',
                    line=dict(color=color_code, width=2.5),
                    marker=dict(size=12, color=color_code),
                    text=[str(node) if node != 0 else "" for node in route_nodes],
                    textposition="top center", name=f"K{veh_id}-Trip {trip_in_veh} (Rute RVND {idx+1})",
                    hoverinfo='text', hovertext=[f"Kendaraan {veh_id} - Rute RVND {idx+1}: {df_curr.iloc[no_to_idx[node]]['Nama Pelanggan']}" for node in route_nodes]
                ))
                for k in range(len(route_nodes) - 1):
                    x_start, y_start = rx[k], ry[k]
                    x_end, y_end = rx[k+1], ry[k+1]
                    fig_rvnd_cmp.add_annotation(
                        x=(x_start + x_end) / 2, y=(y_start + y_end) / 2,
                        ax=x_start, ay=y_start,
                        xref="x", yref="y", axref="x", ayref="y",
                        showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2, arrowcolor=color_code
                    )
            fig_rvnd_cmp.update_layout(
                width=850, height=550, margin=dict(l=40, r=40, t=30, b=40),
                xaxis=dict(title="Koordinat X", range=[min_x - 8, max_x + 8], showgrid=True, gridcolor='#e1effe'),
                yaxis=dict(title="Koordinat Y", range=[min_y - 8, max_y + 8], showgrid=True, gridcolor='#e1effe'),
                template="plotly_white", legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)")
            )
            st.plotly_chart(fig_rvnd_cmp, use_container_width=True, key="plot_tab5_rvnd")

# --- 3. FOOTER ---
st.markdown("""
    <div class="footer">
        © 2026 | Skripsi | Dyah Ayu Nur Zubaidah (230312608130) | S1 Matematika | Universitas Negeri Malang
    </div>
""", unsafe_allow_html=True)