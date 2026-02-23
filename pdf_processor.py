import os
import fitz
import pymupdf4llm

def extract_markdown(pdf_path: str) -> str:
    """
    Extract text from PDF as Markdown using pymupdf4llm.
    """
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return md_text

def extract_images(pdf_path: str, output_dir: str) -> list[str]:
    """
    Extract images from PDF that are at least 100x100 pixels.
    Returns a list of saved image file paths.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    doc = fitz.open(pdf_path)
    extracted_images = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        # get_image_info(xrefs=True) returns a list of dicts with rendered bbox and xref
        image_list = page.get_image_info(xrefs=True)
        
        for img_index, img_info in enumerate(image_list):
            xref = img_info.get("xref")
            bbox = img_info.get("bbox")
            if not bbox:
                continue
                
            rect = fitz.Rect(bbox)
            
            # Filter mechanism: ignore small decorative images (icons, color blocks)
            # Use rendered size for filtering
            if rect.width < 100 or rect.height < 100:
                continue
                
            image_saved = False
            image_path = ""
            
            # Attempt native extraction if xref > 0
            if xref and xref > 0:
                try:
                    base_image = doc.extract_image(xref)
                    if base_image and "image" in base_image:
                        image_ext = base_image["ext"]
                        image_bytes = base_image["image"]
                        
                        image_filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
                        image_path = os.path.join(output_dir, image_filename)
                        
                        with open(image_path, "wb") as f:
                            f.write(image_bytes)
                        image_saved = True
                except Exception:
                    pass
            
            # Fallback to precise pixmap screenshot if extraction failed or no real xref
            if not image_saved:
                try:
                    # High resolution screenshot of the image bounding box
                    zoom = 3.0 # Increase DPI for high-quality fallback (approx 216 DPI)
                    mat = fitz.Matrix(zoom, zoom)
                    # Use the image's exact bounding box for clipping out the image perfectly without margins
                    pix = page.get_pixmap(matrix=mat, clip=rect)
                    
                    image_filename = f"page{page_num + 1}_img{img_index + 1}_fallback.png"
                    image_path = os.path.join(output_dir, image_filename)
                    pix.save(image_path)
                    image_saved = True
                except Exception as e:
                    print(f"Fallback extraction failed for page {page_num+1} img {img_index+1}: {e}")
                    continue
            
            if image_saved:
                extracted_images.append(image_path)
            
    doc.close()
    return extracted_images
