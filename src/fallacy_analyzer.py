import os
import json
import requests
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from huggingface_hub import InferenceClient

# Hugging Face API Client
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is not set!")

client = InferenceClient(token=HF_TOKEN)

# Sabitler
OUTPUT_DIR = "docs"
ASSETS_DIR = os.path.join(OUTPUT_DIR, "assets")
DATA_FILE = os.path.join(OUTPUT_DIR, "fallacies.json")

# Mantık Hatası Türleri ve Tarot Temalı Promptları
FALLACY_PROMPTS = {
    "Ad Hominem": "Mystical tarot card illustration of a person attacking another person's character instead of their argument, dark fantasy style, gold borders, arcane symbols, intricate details, mystical atmosphere",
    "Straw Man": "Mystical tarot card illustration of a scarecrow being fought instead of a real warrior, dark fantasy style, gold borders, arcane symbols, intricate details, mystical atmosphere",
    "Appeal to Authority": "Mystical tarot card illustration of a blind follower worshipping a false idol, dark fantasy style, gold borders, arcane symbols, intricate details, mystical atmosphere",
    "False Dilemma": "Mystical tarot card illustration of a fork in the road with only two paths shown while many exist, dark fantasy style, gold borders, arcane symbols, intricate details, mystical atmosphere",
    "Slippery Slope": "Mystical tarot card illustration of a domino effect leading to catastrophe, dark fantasy style, gold borders, arcane symbols, intricate details, mystical atmosphere",
    "Circular Reasoning": "Mystical tarot card illustration of an ouroboros snake eating its own tail, dark fantasy style, gold borders, arcane symbols, intricate details, mystical atmosphere",
    "Hasty Generalization": "Mystical tarot card illustration of judging a whole forest by one tree, dark fantasy style, gold borders, arcane symbols, intricate details, mystical atmosphere",
    "Red Herring": "Mystical tarot card illustration of a fish distracting from the real path, dark fantasy style, gold borders, arcane symbols, intricate details, mystical atmosphere",
    "Tu Quoque": "Mystical tarot card illustration of two people pointing fingers at each other, dark fantasy style, gold borders, arcane symbols, intricate details, mystical atmosphere",
    "Appeal to Emotion": "Mystical tarot card illustration of hearts clouding judgment, dark fantasy style, gold borders, arcane symbols, intricate details, mystical atmosphere"
}

def get_reddit_posts():
    """Reddit'ten popüler gönderileri çek (ücretsiz API)"""
    headers = {'User-Agent': 'FallacyBot/1.0'}
    url = "https://www.reddit.com/r/all/hot.json?limit=25"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for child in data['data']['children']:
            post_data = child['data']
            # Sadece metin içeren veya kısa başlıklı gönderileri al
            if post_data['selftext'] or len(post_data['title']) > 20:
                text = post_data['selftext'] if post_data['selftext'] else post_data['title']
                if len(text) > 50 and len(text) < 500:  # Çok kısa veya çok uzun olmayanlar
                    posts.append({
                        'title': post_data['title'],
                        'text': text,
                        'url': f"https://reddit.com{post_data['permalink']}",
                        'score': post_data['score'],
                        'author': post_data['author'] if post_data['author'] else 'anonymous',
                        'created_utc': post_data['created_utc']
                    })
        return posts
    except Exception as e:
        print(f"Reddit API error: {e}")
        return []

def analyze_fallacy(text):
    """LLM ile mantık hatası analizi"""
    prompt = f"""Analyze the following text for logical fallacies. 
    Return ONLY a JSON object with this exact structure:
    {{
        "fallacy_type": "name of the fallacy or null",
        "confidence": 0.0-1.0,
        "explanation": "brief explanation in Turkish",
        "quote": "the specific part of text containing the fallacy"
    }}
    
    Text to analyze: "{text[:300]}"... 
    
    If no clear fallacy is found, set fallacy_type to null."""

    try:
        response = client.text_generation(
            prompt,
            model="mistralai/Mistral-7B-Instruct-v0.3",
            max_new_tokens=200,
            temperature=0.3
        )
        
        # JSON'u temizle ve parse et
        clean_response = response.strip()
        if clean_response.startswith('```json'):
            clean_response = clean_response[7:]
        if clean_response.endswith('```'):
            clean_response = clean_response[:-3]
        clean_response = clean_response.strip()
        
        result = json.loads(clean_response)
        return result
    except Exception as e:
        print(f"Analysis error: {e}")
        return {"fallacy_type": None, "confidence": 0, "explanation": "Analiz edilemedi", "quote": ""}

def generate_tarot_image(fallacy_type, output_path):
    """Tarot kartı görseli oluştur"""
    if fallacy_type not in FALLACY_PROMPTS:
        fallacy_type = "Ad Hominem"  # Varsayılan
    
    prompt = FALLACY_PROMPTS[fallacy_type]
    
    try:
        image = client.text_to_image(prompt, model="stabilityai/stable-diffusion-xl-base-1.0")
        image.save(output_path)
        print(f"Görsel başarıyla oluşturuldu: {output_path}")
        return True
    except Exception as e:
        print(f"Image generation error: {e}")
        return False

def create_placeholder_image(fallacy_type, output_path):
    """Görsel oluşturamazsa basit bir placeholder"""
    img = Image.new('RGB', (512, 768), color=(26, 10, 46))
    draw = ImageDraw.Draw(img)
    
    # Basit bir çerçeve
    draw.rectangle([10, 10, 502, 758], outline=(212, 175, 55), width=3)
    
    try:
        # Font denemesi
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 28)
    except:
        font = ImageFont.load_default()
    
    # Metni ortala
    text = fallacy_type
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (512 - text_width) // 2
    y = (768 - text_height) // 2
    
    draw.text((x, y), text, fill=(212, 175, 55), font=font)
    img.save(output_path)

def main():
    # Klasörleri oluştur
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    # Reddit'ten veri çek
    print("Reddit'ten gönderiler alınıyor...")
    posts = get_reddit_posts()
    
    if not posts:
        print("Hiç gönderi alınamadı, varsayılan veri kullanılıyor.")
        posts = [{
            'title': "Örnek Gönderi",
            'text': "Herkes bu filmi beğendi, o halde bu film kesinlikle en iyi filmdir.",
            'url': "#",
            'score': 100,
            'author': "example_user",
            'created_utc': datetime.now().timestamp()
        }]
    
    analyzed_posts = []
    
    # Her gönderiyi analiz et
    print(f"{len(posts)} gönderi analiz ediliyor...")
    for i, post in enumerate(posts):
        print(f"Analiz {i+1}/{len(posts)}: {post['title'][:30]}...")
        
        result = analyze_fallacy(post['text'])
        
        if result.get('fallacy_type'):
            # Görsel oluştur
            timestamp = int(datetime.now().timestamp())
            image_filename = f"fallacy_{timestamp}_{i}.png"
            image_path = os.path.join(ASSETS_DIR, image_filename)
            
            success = generate_tarot_image(result['fallacy_type'], image_path)
            if not success:
                # Görsel oluşturulamazsa placeholder SVG kullan
                image_filename = f"fallback_card.svg"
                image_path = os.path.join(ASSETS_DIR, image_filename)
                # Placeholder zaten mevcut, kopyalamaya gerek yok
            
            analyzed_posts.append({
                'id': f"fallacy_{timestamp}_{i}",
                'timestamp': timestamp,
                'date': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M'),
                'original_post': {
                    'title': post['title'],
                    'text': post['text'],
                    'url': post['url'],
                    'author': post['author'],
                    'score': post['score']
                },
                'fallacy': {
                    'type': result['fallacy_type'],
                    'confidence': result.get('confidence', 0.5),
                    'explanation': result.get('explanation', 'Açıklama yok'),
                    'quote': result.get('quote', '')
                },
                'image': f"assets/{image_filename}",
                'votes': {'up': 0, 'down': 0},
                'category': 'new'  # new, hot, best için kullanılacak
            })
    
    # Mevcut verileri yükle (arsiv için)
    existing_data = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except:
            existing_data = []
    
    # Yeni verileri ekle
    all_data = analyzed_posts + existing_data
    
    # Sıralama kategorilerini güncelle
    # Hot: Son 24 saatte çok oy alan
    # Best: Tüm zamanların en çok oy alan
    # Newest: En yeni
    for item in all_data:
        age_hours = (datetime.now().timestamp() - item['timestamp']) / 3600
        score = item['votes']['up'] - item['votes']['down']
        
        if age_hours < 24 and score > 2:
            item['category'] = 'hot'
        elif score > 5:
            item['category'] = 'best'
        else:
            item['category'] = 'new'
    
    # Verileri kaydet
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"Toplam {len(all_data)} mantık hatası kaydedildi.")
    print("Veriler docs/fallacies.json dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
