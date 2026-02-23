import streamlit as st
import base64
import os
import zipfile
from pdf_processor import extract_markdown, extract_images

def main():
    st.set_page_config(page_title="PDF Extractor Tool", layout="wide", page_icon="img/jz-icon-32.webp")
    
    def image_to_data_uri(path):
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("ascii")
        return f"data:image/webp;base64,{encoded}"

    logo_white_uri = image_to_data_uri("img/logo-white.webp")
    footer_icon_uri = image_to_data_uri("img/jz-icon-32.webp")

    # Modern Tailwind-like Dark Theme CSS, Custom Headers/Footers, Logo, and Hidden Watermark
    custom_css = """
        <style>
        /* Hide Default Streamlit Elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Modern UI Tweaks (Tailwind Feel - Dark Mode) */
        .stApp {
            background-color: #0f172a; /* slate-900 */
            color: #f8fafc; /* slate-50 */
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }
        
        /* Typography overrides */
        h1, h2, h3, h4, h5, h6, p, span, div {
            color: #f8fafc !important; 
        }
        
        /* Card Styling for main container */
        .main .block-container {
            padding-top: 5rem;
            padding-bottom: 5rem;
            max-width: 64rem;
        }
        
        hr {
            border-color: #334155; /* slate-700 */
            margin-top: 2rem;
            margin-bottom: 2rem;
        }
        
        /* Buttons */
        .stButton button {
            background-color: #1e293b !important; /* slate-800 */
            color: #f8fafc !important;
            border-radius: 0.5rem !important;
            font-weight: 500 !important;
            transition: all 0.2s !important;
            border: 1px solid #475569 !important; /* slate-600 */
        }
        
        .stButton button:hover {
            border-color: #f8fafc !important;
            background-color: #334155 !important; /* slate-700 */
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Primary Button */
        button[data-baseweb="button"]:has(div[data-testid="stMarkdownContainer"]:contains("开始解析")) {
            background-color: #f8fafc !important; /* white-ish */
            color: #0f172a !important; /* dark text */
            border: none !important;
        }
        
        button[data-baseweb="button"]:has(div[data-testid="stMarkdownContainer"]:contains("开始解析")):hover {
            background-color: #cbd5e1 !important; /* slate-300 */
            color: #0f172a !important;
        }
        
        /* File Uploader override */
        [data-testid='stFileUploader'] {
            border-radius: 0.75rem;
            background-color: #1e293b; /* slate-800 */
            color: #f8fafc !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
            padding: 1rem;
            border: 1px dashed #475569; /* slate-600 */
        }
        
        /* Tab Text overrides */
        .stTabs [data-baseweb="tab-list"] button {
            color: #94a3b8 !important; /* slate-400 */
        }
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            color: #f8fafc !important; /* slate-50 */
        }
        
        /* SVG Logo Position */
        .custom-logo {
            position: absolute;
            top: 24px;
            right: 24px;
            width: 64px;
            height: 64px;
            z-index: 9999;
        }
        
        /* Custom Footer */
        .custom-footer {
            position: fixed;
            bottom: 0px;
            left: 0px;
            width: 100%;
            background-color: #0f172a; /* slate-900 */
            border-top: 1px solid #1e293b; /* slate-800 */
            padding: 12px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.875rem;
            color: #94a3b8; /* slate-400 */
            z-index: 9999;
        }
        
        .footer-logo {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 500;
            color: #e2e8f0; /* slate-200 */
        }
        
        /* Hidden Copyright Watermarks */
        .copyright-watermark {
            display: none;
            opacity: 0;
            position: absolute;
            z-index: -1;
            pointer-events: none;
        }
        </style>
    """
    
    custom_html = f"""
        <!-- Hidden DOM Elements for Copyright -->
        <div class="copyright-watermark" data-author="Jiackey" data-studio="DMESTUDIO" data-copyright="© 2026 DMESTUDIO. All rights reserved.">Built by Jiackey @ DMESTUDIO</div>
        
        <!-- Header Logo (DMEStudio img) -->
        <img class="custom-logo" src="{logo_white_uri}" alt="DME Logo"/>
        
        <!-- Custom Footer with Logo -->
        <div class="custom-footer">
            <div class="footer-logo">
                <img width="16" height="16" src="{footer_icon_uri}" alt="DME Logo"/>
                <span>DME Toolchain</span>
            </div>
            <div>PDF Content Extractor v1.0.4</div>
        </div>
    """
    st.markdown(custom_css + custom_html, unsafe_allow_html=True)
    
    st.title("📄 PDF 内容提取工具")
    st.markdown("<p style='color: #94a3b8; font-size: 1.1rem; line-height: 1.6;'>轻松提取 PDF 文档中的<strong style='color:#f8fafc'>纯文本（Markdown）</strong>与<strong style='color:#f8fafc'>高清原始图片（>100px）</strong>。<br/>所有处理均在本地运行。<br/><span style='font-size: 0.9em; opacity: 0.8;'>DMESTUDIO Inc.开发</span></p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("拖拽或点击上传您的 PDF 文件", type=["pdf"])
    
    if uploaded_file is not None:
        # Create a temp directory for this extraction
        temp_dir = "temp_extraction"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)
            
        pdf_path = os.path.join(temp_dir, uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        st.success(f"已成功上传：{uploaded_file.name} (大小: {uploaded_file.size / 1024:.2f} KB)")
        
        if st.button("开始解析", type="primary"):
            with st.spinner("解析中，这可能需要几十秒，请稍候..."):
                images_dir = os.path.join(temp_dir, "images")
                
                try:
                    md_text, is_likely_outlined = extract_markdown(pdf_path)
                    image_paths = extract_images(pdf_path, images_dir)
                    
                    st.toast("解析已完成！", icon="✅")
                    
                    st.session_state["md_text"] = md_text
                    st.session_state["is_likely_outlined"] = is_likely_outlined
                    st.session_state["image_paths"] = image_paths
                    st.session_state["pdf_name"] = uploaded_file.name
                    st.session_state["images_dir"] = images_dir
                    
                except Exception as e:
                    st.error(f"解析过程中发生错误：{str(e)}")
                    return
                    
    # Display results if available in session state
    if "md_text" in st.session_state:
        st.divider()
        st.subheader("解析结果展现")
        
        tab1, tab2 = st.tabs(["📝 Markdown 文本区", f"🖼️ 美术素材区 ({len(st.session_state['image_paths'])}张)"])
        
        # Tab 1: Markdown
        with tab1:
            if st.session_state.get("is_likely_outlined", False):
                st.warning("⚠️ **检测到可能是“已转曲”或“纯图片扫描”的 PDF 文档 系统发现该文档内几乎不包含真实的文本流数据（即便肉眼能看到文字，它们在数据层面上也已经被转换为了矢量线条或图片）。**\n\n"
                          "因此无法常规提取出文本。\n\n"
                          "如果您需要提取此类文档的文字，需要使用包含 OCR功能的工具。")
                          
            col_content, col_actions = st.columns([3, 1])
            with col_content:
                st.markdown(st.session_state["md_text"])
                
            with col_actions:
                st.download_button(
                    label="⬇️ 下载 .md 文件",
                    data=st.session_state["md_text"],
                    file_name=f"{os.path.splitext(st.session_state['pdf_name'])[0]}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
                with st.expander("查看原始 Markdown / 一键复制"):
                    st.code(st.session_state["md_text"], language="markdown")

        # Tab 2: Images
        with tab2:
            image_paths = st.session_state["image_paths"]
            if not image_paths:
                st.info("未从此文档中提取到有效图像（或所有图像均被过滤机制排除）。")
            else:
                zip_path = os.path.join("temp_extraction", "all_images.zip")
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for img_path in image_paths:
                        zipf.write(img_path, os.path.basename(img_path))
                
                with open(zip_path, "rb") as f:
                    zip_data = f.read()
                    
                st.download_button(
                    label="📦 一键打包下载所有图片 (.zip)",
                    data=zip_data,
                    file_name=f"{os.path.splitext(st.session_state['pdf_name'])[0]}_images.zip",
                    mime="application/zip",
                    type="primary"
                )
                st.write("---")
                
                cols = st.columns(3)
                for i, img_path in enumerate(image_paths):
                    col = cols[i % 3]
                    with col:
                        # Displaying image with Streamlit 1.30+ API
                        st.image(img_path, use_container_width=True, caption=os.path.basename(img_path))
                        
                        with open(img_path, "rb") as file:
                            st.download_button(
                                label="下载此图片",
                                data=file,
                                file_name=os.path.basename(img_path),
                                mime="image/png",
                                key=f"dl_btn_{i}",
                                use_container_width=True
                            )

if __name__ == "__main__":
    main()
