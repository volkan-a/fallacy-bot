import os
import json
import random
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Reddit API Configuration (Anonymous access for public data)
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'FallacyHunterBot/1.0')

# Hugging Face Configuration
HF_TOKEN = os.getenv('HF_TOKEN', '')
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

# Paths
DATA_FILE = 'data/archive.json'
ASSETS_DIR = 'docs/assets'

# Fallacy Types and Tarot-style Descriptions
FALLACY_STYLES = {
    "Ad Hominem": {"name": "The Betrayer", "desc": "Attacking the person instead of the argument.", "color": "#8B0000"},
    "Straw Man": {"name": "The Illusionist", "desc": "Misrepresenting an argument to make it easier to attack.", "color": "#4B0082"},
    "Appeal to Authority": {"name": "The High Priest", "desc": "Claiming truth because an authority says so.", "color": "#DAA520"},
    "False Dilemma": {"name": "The Forked Path", "desc": "Presenting only two options when more exist.", "color": "#2F4F4F"},
    "Slippery Slope": {"name": "The Avalanche", "desc": "Asserting a small step leads to a chain of negative events.", "color": "#708090"},
    "Circular Reasoning": {"name": "The Ouroboros", "desc": "The conclusion is included in the premise.", "color": "#006400"},
    "Hasty Generalization": {"name": "The Blind Seer", "desc": "Drawing a conclusion from insufficient evidence.", "color": "#A0522D"},
    "Red Herring": {"name": "The Distractor", "desc": "Introducing irrelevant information to divert attention.", "color": "#DC143C"},
    "Tu Quoque": {"name": "The Mirror", "desc": "Avoiding criticism by turning it back on the accuser.", "color": "#9370DB"},
    "No True Scotsman": {"name": "The Gatekeeper", "desc": "Dismissing counterexamples by redefining terms.", "color": "#556B2F"}
}

def get_reddit_posts(limit=20):
    """Fetch top posts from Reddit (r/all or specific subreddits)"""
    headers = {'User-Agent': REDDIT_USER_AGENT}
    # Using public endpoint without auth for simplicity if credentials missing
    # If credentials are present, we could use OAuth for higher limits
    url = "https://www.reddit.com/r/all/top.json?limit={}".format(limit)
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        posts = []
        for child in data['data']['children']:
            post = child['data']
            # Filter out non-text posts or very short ones
            if post['selftext'] and len(post['selftext']) > 50:
                posts.append({
                    "id": post['id'],
                    "title": post['title'],
                    "text": post['selftext'],
                    "url": f"https://reddit.com{post['permalink']}",
                    "score": post['score'],
                    "author": post['author'] if post['author'] else "[deleted]",
                    "created_utc": post['created_utc']
                })
            elif post['is_self'] == False and post['title']: 
                # Consider title-only posts if they are substantial
                if len(post['title']) > 30:
                     posts.append({
                        "id": post['id'],
                        "title": post['title'],
                        "text": post['title'], # Use title as text
                        "url": f"https://reddit.com{post['permalink']}",
                        "score": post['score'],
                        "author": post['author'] if post['author'] else "[deleted]",
                        "created_utc": post['created_utc']
                    })
        return posts
    except Exception as e:
        print(f"Error fetching Reddit posts: {e}")
        return []

def analyze_fallacy(text):
    """Use Hugging Face Inference API to detect fallacies"""
    prompt = f"""
    Analyze the following text for logical fallacies. 
    Identify the single most prominent logical fallacy present.
    Choose ONLY from this list: Ad Hominem, Straw Man, Appeal to Authority, False Dilemma, Slippery Slope, Circular Reasoning, Hasty Generalization, Red Herring, Tu Quoque, No True Scotsman.
    If no clear fallacy is found, return 'None'.
    
    Text: "{text[:500]}" 
    
    Output format (JSON):
    {{
        "fallacy": "Name of Fallacy",
        "confidence": 0.0-1.0,
        "explanation": "Brief explanation of why this is a fallacy in this context."
    }}
    """
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200, "return_full_text": False}}
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        result = response.json()
        
        # Parse the output to extract JSON
        # The API returns a list with generated text, we need to clean it
        if isinstance(result, list) and len(result) > 0:
            generated_text = result[0].get('generated_text', '')
            # Try to find JSON block
            start_idx = generated_text.find('{')
            end_idx = generated_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = generated_text[start_idx:end_idx]
                return json.loads(json_str)
        
        return {"fallacy": "Unknown", "confidence": 0.5, "explanation": "Could not parse AI response."}
    except Exception as e:
        print(f"Error analyzing fallacy: {e}")
        return {"fallacy": "Error", "confidence": 0.0, "explanation": str(e)}

def generate_tarot_card(fallacy_name, tweet_text, card_id):
    """Generate a simple Tarot-style card image using Pillow"""
    width, height = 400, 600
    img = Image.new('RGB', (width, height), color='#1a1a1a')
    draw = ImageDraw.Draw(img)
    
    style = FALLACY_STYLES.get(fallacy_name, {"name": "The Unknown", "desc": "An unidentified anomaly.", "color": "#FFFFFF"})
    
    # Border
    border_color = style["color"]
    draw.rectangle([10, 10, width-10, height-10], outline=border_color, width=4)
    
    # Title Area
    draw.rectangle([20, 20, width-20, 100], fill='#000000')
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 24)
        font_text = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 14)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((width//2, 40), style["name"], fill=border_color, font=font_title, anchor="mm")
    draw.text((width//2, 70), fallacy_name, fill='#CCCCCC', font=font_small, anchor="mm")
    
    # Symbolic Representation (Abstract Geometry based on Fallacy)
    # In a real scenario, we might use an AI image gen API, but here we draw abstract shapes
    center_x, center_y = width//2, 250
    draw.ellipse([center_x-50, center_y-50, center_x+50, center_y+50], outline=border_color, width=2)
    draw.line([center_x-30, center_y-30, center_x+30, center_y+30], fill=border_color, width=2)
    draw.line([center_x+30, center_y-30, center_x-30, center_y+30], fill=border_color, width=2)
    
    # Description
    desc_y = 350
    draw.text((width//2, desc_y), style["desc"], fill='#EEEEEE', font=font_text, anchor="mm", align="center")
    
    # Tweet Text Snippet
    text_y = 420
    clean_text = " ".join(tweet_text.split()[:15]) + "..." if len(tweet_text.split()) > 15 else tweet_text
    # Wrap text manually
    max_chars = 35
    lines = []
    for i in range(0, len(clean_text), max_chars):
        lines.append(clean_text[i:i+max_chars])
    
    current_y = text_y
    for line in lines:
        draw.text((width//2, current_y), line, fill='#AAAAAA', font=font_small, anchor="mm", align="center")
        current_y += 15
        
    # Footer
    draw.text((width//2, height-40), f"Generated: {datetime.now().strftime('%Y-%m-%d')}", fill='#555555', font=font_small, anchor="mm")
    draw.text((width//2, height-25), f"ID: {card_id}", fill='#333333', font=font_small, anchor="mm")
    
    filename = f"{ASSETS_DIR}/card_{card_id}.png"
    img.save(filename)
    return filename

def load_archive():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_archive(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    print("Starting Fallacy Hunter Analysis...")
    
    # 1. Fetch Posts
    posts = get_reddit_posts(limit=20) # Limit to avoid rate limits in free tier
    if not posts:
        print("No posts fetched. Exiting.")
        return

    print(f"Fetched {len(posts)} posts.")
    
    # 2. Analyze each post for fallacies
    analyzed_posts = []
    for post in posts:
        content = post['text']
        result = analyze_fallacy(content)
        if result['fallacy'] != 'None' and result['fallacy'] != 'Error':
            analyzed_posts.append({
                **post,
                "fallacy": result['fallacy'],
                "confidence": result.get('confidence', 0.5),
                "explanation": result.get('explanation', '')
            })
    
    if not analyzed_posts:
        print("No fallacies detected in this batch.")
        return

    # 3. Select the "Best" one (Highest Confidence * Score)
    # Simple scoring: confidence * log(score+1)
    import math
    best_post = None
    max_score = -1
    
    for post in analyzed_posts:
        score_val = post['confidence'] * math.log(post['score'] + 1)
        if score_val > max_score:
            max_score = score_val
            best_post = post
            
    if not best_post:
        print("Could not determine a top fallacy.")
        return

    print(f"Top Fallacy Found: {best_post['fallacy']} in post ID {best_post['id']}")
    
    # 4. Generate Tarot Card
    archive = load_archive()
    new_entry_id = len(archive) + 1
    card_path = generate_tarot_card(best_post['fallacy'], best_post['text'], new_entry_id)
    
    # Prepare entry for archive
    entry = {
        "id": new_entry_id,
        "timestamp": datetime.now().isoformat(),
        "post_url": best_post['url'],
        "post_author": best_post['author'],
        "post_score": best_post['score'],
        "content": best_post['text'],
        "fallacy": best_post['fallacy'],
        "confidence": best_post['confidence'],
        "explanation": best_post['explanation'],
        "card_image": card_path.replace('docs/', ''), # Relative path for web
        "votes": {"up": 0, "down": 0} # Initialize voting
    }
    
    archive.insert(0, entry) # Add to top
    save_archive(archive)
    print(f"Archive updated. Total entries: {len(archive)}")

if __name__ == "__main__":
    main()
