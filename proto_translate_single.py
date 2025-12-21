import fitz # pymupdf
import re
import os
import difflib

# Configuration
HTML_PATH = 'two-rooms-rules/characters.html'
PDF_INPUT = 'pnp_translation/two-rooms-one-boom/Origin_EN/Cards/PnP01.pdf'
PDF_OUTPUT = 'pnp_translation/two-rooms-one-boom/Translated_ZHTW/PnP01_proto.pdf'

# Font candidates
FONTS = [
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/STHeiti Medium.ttc', 
    '/System/Library/Fonts/Hiragino Sans GB.ttc'
]
FONT_PATH = next((f for f in FONTS if os.path.exists(f)), None)

# Manual dictionary for UI terms
MANUAL_DICT = {
    "YOU ARE THE": "你的身分是",
    "BLUE TEAM": "藍隊",
    "RED TEAM": "紅隊",
    "GREY TEAM": "灰隊",
    "GREEN TEAM": "綠隊",
    "COLOR": "顏色",
    "LEADER": "隊長"
}

def load_mappings(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    mapping = {}
    blocks = content.split('{')
    for block in blocks:
        # Extract English Name
        en_match = re.search(r'en:\s*"([^"]+)"', block)
        zh_match = re.search(r'zh:\s*"([^"]+)"', block)
        desc_match = re.search(r'desc:\s*"([^"]+)"', block)
        
        if en_match and zh_match:
            en_text = en_match.group(1).strip().upper()
            zh_text = zh_match.group(1).strip()
            mapping[normalize_key(en_text)] = zh_text
            
            # Extract Description if available
            # We map Description EN content to Chinese Desc?
            # Wait, the HTML doesn't have EN descriptions, only ZHTW descriptions!
            # The EN descriptions are on the cards!
            # If the HTML only has ZH description, we can't map EN description -> ZH description easily 
            # UNLESS we manually transcribe or finding EN text from the cards and create a map.
            # But the user said: "we have en pnp cards... and characters.html translate all text"
            # It implies we need to find the EN text on the card and replace with `desc` from HTML.
            # So we map `en_name` -> `zh_desc`.
            
            if desc_match:
                 mapping[f"DESC_{en_text}"] = desc_match.group(1).strip()
                 
    return mapping

def normalize_key(text):
    # Remove newlines, extra spaces, non-alphanumeric (keep spaces?)
    # "FORCE A CARD SHARE\nONCE PER ROUND" -> "FORCE A CARD SHARE ONCE PER ROUND"
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip().upper()

def get_text_color(span_color):
    r = ((span_color >> 16) & 0xFF) / 255.0
    g = ((span_color >> 8) & 0xFF) / 255.0
    b = (span_color & 0xFF) / 255.0
    return (r, g, b)

def get_background_color(page_pix, rect):
    x, y = int(rect.x0), int(rect.y0)
    points = [ (x-2, y+2), (x+2, y-2), (int(rect.x1)+2, y+2), (x+2, int(rect.y1)+2) ]
    valid_samples = []
    for px, py in points:
        if 0 <= px < page_pix.width and 0 <= py < page_pix.height:
            try: valid_samples.append(page_pix.pixel(px, py)) 
            except: pass
    if not valid_samples: return (1, 1, 1)
    
    r_sum, g_sum, b_sum = 0, 0, 0
    for r, g, b in valid_samples:
        r_sum += r; g_sum += g; b_sum += b
    count = len(valid_samples)
    return (r_sum/count/255.0, g_sum/count/255.0, b_sum/count/255.0)

def draw_vertical_text(page, rect, text, fontname, fontfile, fontsize, color):
    # Draw characters stacked top-to-bottom, centered in rect
    # Calculate total height
    line_height = fontsize * 1.0
    total_height = len(text) * line_height
    
    # Start Y: Center vertically in rect
    start_y = rect.y0 + (rect.height - total_height) / 2 + fontsize # +fontsize because text point is bottom-left usually? 
    # Actually insert_text point is baseline.
    
    # X Center
    center_x = rect.x0 + rect.width / 2
    
    # Create font object for calculation
    font = fitz.Font(fontfile=fontfile)
    
    curr_y = start_y
    for char in text:
        # Check boundary
        if curr_y > rect.y1: break
        
        # Draw char
        # Need to center char horizontally?
        # calc width of char
        char_width = font.text_length(char, fontsize=fontsize)
        char_x = center_x - (char_width / 2)
        
        page.insert_text((char_x, curr_y), char, fontname=fontname, fontfile=fontfile, fontsize=fontsize, color=color)
        
        curr_y += line_height

def main():
    os.makedirs(os.path.dirname(PDF_OUTPUT), exist_ok=True)
    
    full_map = {**load_mappings(HTML_PATH), **MANUAL_DICT}
    # Add normalized keys for manual dict
    for k, v in MANUAL_DICT.items():
        full_map[normalize_key(k)] = v
        
    print(f"Loaded {len(full_map)} mappings.")
    # Debug: print keys starting with "DESC_"
    # print([k for k in full_map.keys() if k.startswith("DESC_")])

    doc = fitz.open(PDF_INPUT)
    page = doc[0]
    page_pix = page.get_pixmap()
    text_dict = page.get_text("dict")
    
    matches = []
    
    # First pass: Collect all text blocks and try to identify "Name" blocks vs "Desc" blocks.
    # The PDF structure might be:
    # Block 1: "AGENT" (Name)
    # Block 2: "FORCE A CARD..." (Desc)
    
    # We can try to match ANY block text against our keys.
    # Also, we need to match "Description" text on the card to the "Description" in our map.
    # Problem: The map keys are mostly NAMES (e.g. "AGENT").
    # The map has "DESC_AGENT" -> "Chinese Desc".
    # BUT the valid text on the card is "FORCE A CARD SHARE...".
    # We do NOT have the English description in our map to match against!
    # "FORCE A CARD SHARE..." is not in characters.html EN field.
    
    # STRATEGY: 
    # 1. Identify valid extraction of NAME (e.g. "AGENT").
    # 2. Look for text blocks *near* the name block?
    # 3. OR assume the text block that is NOT a name/title is a description?
    # 4. OR (User implied) EN descriptions are standard? 
    # Actually, without the EN description text in the mapping, we can't find and replace it by content match.
    # UNLESS we match by proximity to the Name.
    
    # Let's verify what we have.
    # We found "AGENT" -> replace with "特務".
    # If we find "AGENT", we can look for a nearby text block that looks like a description and replace it with full_map["DESC_AGENT"].
    
    found_names = [] # (rect, name_key)
    
    for block in text_dict["blocks"]:
        if "lines" not in block: continue
        
        # Reconstruct text
        block_text = ""
        first_span_color = (0, 0, 0)
        has_color = False
        b_x0, b_y0, b_x1, b_y1 = block["bbox"]
        
        for line in block["lines"]:
            for span in line["spans"]:
                if not has_color:
                    first_span_color = get_text_color(span["color"])
                    has_color = True
                block_text += span["text"]
            block_text += "\n"
            
        clean_text = normalize_key(block_text)
        
        # Try finding Name match
        target_zh = full_map.get(clean_text)
        
        # If no strict match, fuzzy match for Title?
        # " YOU ARE THE " might have spaces.
        
        rect = fitz.Rect(b_x0, b_y0, b_x1, b_y1)
        bg_color = get_background_color(page_pix, rect)
        
        if target_zh:
            print(f"Match Name: '{clean_text}' -> '{target_zh}'")
            found_names.append((rect, clean_text)) # Store rect and key (e.g. "AGENT")
            
            # Redact & Replace
            page.draw_rect(rect, color=bg_color, fill=bg_color)
            
            is_vertical = (b_y1 - b_y0) > (b_x1 - b_x0) * 1.5
            
            # Draw Text
            if is_vertical:
                # Use custom vertical drawer
                # Calculate fontsize
                avail_w = b_y1 - b_y0
                avail_h = b_x1 - b_x0 # width of strip
                fontsize = min(avail_h * 0.8, avail_w / len(target_zh))
                fontsize = max(min(fontsize, 40), 10)
                
                # Use bold font if possible? STHeiti Medium is medium.
                draw_vertical_text(page, rect, target_zh, "heiti", FONT_PATH, fontsize, first_span_color)
                
            else:
                 # Horizontal
                 avail_w = b_x1 - b_x0
                 avail_h = b_y1 - b_y0
                 fontsize = min(avail_h * 0.8, avail_w / len(target_zh))
                 
                 page.insert_textbox(rect, target_zh, fontsize=fontsize, fontname="heiti", fontfile=FONT_PATH, align=1, color=first_span_color)

        else:
            # Check if this might be a description?
            # It's a block that didn't match a Name.
            # Is it close to a Name we found?
            # We haven't processed all names yet.
            # So store "Unmatched Blocks" and process closer later?
            pass

    # Pass 2: Association for Descriptions
    # For every found Name (e.g. "AGENT"), find the nearest unmatched block?
    # Inspect PDF layout:
    # "AGENT" is vertical on the side.
    # Description "FORCE A CARD SHARE..." is also vertical on the side? Or horizontal?
    # Inspect logs: 
    # (519, 326, 548, 454) "ANARCHIST" (Vertical)
    # (513, 326, 521, 476) "USURP ROOM LEADER..." (Vertical, right next to it?)
    # They are very close.
    
    # We need to re-iterate blocks to find descriptions.
    # But first, let's see if we can identify them by content if we had content?
    # Since we don't, we MUST use proximity.
    
    # For each found_name, look for a block that:
    # 1. Is intersecting or very close? 
    # 2. Contains enough text to be a description?
    
    for name_rect, name_key in found_names:
        desc_key = f"DESC_{name_key}"
        target_desc = full_map.get(desc_key)
        
        if not target_desc: continue
        
        # Search for nearby block
        best_block = None
        min_dist = 9999
        
        center_name = (name_rect.x0 + name_rect.width/2, name_rect.y0 + name_rect.height/2)
        
        for block in text_dict["blocks"]:
             if "lines" not in block: continue
             b_rect = fitz.Rect(block["bbox"])
             
             # Skip if this block was the name itself (overlap?)
             # Skip if this block was the name itself (overlap?)
             # Check intersection
             intersection = b_rect.intersect(name_rect)
             # PyMuPDF intersect returns a rect. check validity.
             if intersection.is_valid:
                 intersect_area = intersection.width * intersection.height
                 b_area = b_rect.width * b_rect.height
                 if b_area > 0 and intersect_area / b_area > 0.8:
                     continue # It's the name block
             
             # Skip if matched other name? (Already redacted? No, we didn't remove from list)
             
             # Calculate distance
             # Vertical layout: Desription usually below or next to?
             # "ANARCHIST" (x=519..548)
             # Desc (x=513..521) -> Left of it.
             
             center_block = (b_rect.x0 + b_rect.width/2, b_rect.y0 + b_rect.height/2)
             dist = ((center_name[0]-center_block[0])**2 + (center_name[1]-center_block[1])**2)**0.5
             
             if dist < 100: # Threshold
                 # Check if it has text?
                 # Assume closest block is the description.
                 # Also avoid matching "GREY TEAM" or "YOU ARE THE".
                 
                 # Re-extract text just to check
                 b_text = ""
                 for line in block["lines"]:
                    for span in line["spans"]:
                        b_text += span["text"]
                 
                 norm_text = normalize_key(b_text)
                 if norm_text in full_map: continue # It's another known key
                 
                 if dist < min_dist:
                     min_dist = dist
                     best_block = block
                     
        if best_block:
            print(f"Found Desc for {name_key}: at dist {min_dist}")
            # Replace Desc
            b_rect = fitz.Rect(best_block["bbox"])
            bg_color = get_background_color(page_pix, b_rect)
            page.draw_rect(b_rect, color=bg_color, fill=bg_color)
            
            is_vertical = (b_rect.height > b_rect.width * 1.5)
            
            # Extract first span color
            color = (0,0,0)
            try:
                color = get_text_color(best_block["lines"][0]["spans"][0]["color"])
            except: pass

            if is_vertical:
                 avail_w = b_rect.height
                 avail_h = b_rect.width
                 # Description text is long.
                 # For vertical description, we might want to wrap?
                 # "FORCE A CARD SHARE" -> 
                 # F
                 # O
                 # R...
                 # But Chinese description is also long.
                 # target_desc: "篡位次數超過..."
                 # We probably need multiple columns or small font.
                 # With simple draw_vertical_text (single column), it might overflow.
                 # Let's try single column first, autosized.
                 fontsize = avail_h * 0.8
                 # Check fit?
                 if len(target_desc) * fontsize > avail_w:
                     fontsize = avail_w / len(target_desc)
                 
                 fontsize = max(min(fontsize, 12), 5) # readable min
                 draw_vertical_text(page, b_rect, target_desc, "heiti", FONT_PATH, fontsize, color)
            else:
                 page.insert_textbox(b_rect, target_desc, fontsize=8, fontname="heiti", fontfile=FONT_PATH, align=1, color=color)

    doc.save(PDF_OUTPUT)
    pix = page.get_pixmap()
    pix.save(PDF_OUTPUT.replace('.pdf', '.png'))
    print(f"Saved preview to {PDF_OUTPUT.replace('.pdf', '.png')}")

if __name__ == "__main__":
    main()
