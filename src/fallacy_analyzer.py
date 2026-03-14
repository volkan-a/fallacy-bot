import os
import json
import subprocess
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from huggingface_hub import InferenceClient

# --- Konfigürasyon ---
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is not set!")

# Hugging Face Client - Google Gemma 2B (Hızlı ve Ücretsiz)
client = InferenceClient(token=HF_TOKEN)
ANALYSIS_MODEL = "google/gemma-2b-it"
IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

# Sabitler
OUTPUT_DIR = "docs"
ASSETS_DIR = os.path.join(OUTPUT_DIR, "assets")
DATA_FILE = os.path.join(OUTPUT_DIR, "fallacies.json")
TEMP_JSON_PATH = "/tmp/reddit_data.json"
DATA_DIR = "data"  # GitHub Actions tarafından indirilen verilerin klasörü

# Subreddit listesi - worldnews öncelikli, sırayla denenir
SUBREDDITS = ["worldnews", "fallacy", "philosophy", "funny", "science", "todayilearned", "changemyview"]

# Mantık Hatası Türleri ve Sabit Tarot Promptları
# Tema, aspect ratio ve stil sabittir, sadece konu değişir.
BASE_IMAGE_PROMPT = (
    "Mystical tarot card design, vertical aspect ratio 2:3, intricate gold borders, "
    "dark magical background, esoteric symbolism, high quality digital art, fantasy illustration. "
    "The central image symbolizes the logical fallacy: "
)

FALLACY_KEYWORDS = {
    "Ad Hominem": "a shadowy figure attacking a person instead of their argument",
    "Straw Man": "a scarecrow being fought instead of a real warrior",
    "Appeal to Authority": "a blind follower worshipping a golden idol",
    "False Dilemma": "a fork in the road with only two paths shown while many exist in the fog",
    "Slippery Slope": "dominoes falling off a cliff into an abyss",
    "Circular Reasoning": "an ouroboros snake eating its own tail forming a circle",
    "Hasty Generalization": "judging a whole dark forest by a single twisted tree",
    "Red Herring": "a glowing red fish distracting a traveler from the true path",
    "Tu Quoque": "two figures pointing fingers at each other accusingly",
    "Appeal to Emotion": "glowing hearts and tears clouding a crystal ball of judgment",
    "Bandwagon": "a crowd of faceless people jumping off a cliff together",
    "Begging the Question": "a snake biting its own tail in an infinite loop",
    "No True Scotsman": "a guard denying entry to someone who fits the description",
    "Genetic Fallacy": "judging a gift by the dirty hands holding it",
    "Middle Ground": "two monsters compromising on the fate of a victim in the middle"
}

def download_reddit_json(subreddit):
    """wget ile belirtilen subreddit'in JSON verisini çeker."""
    url = f"https://www.reddit.com/r/{subreddit}/top.json?t=week&limit=25"
    print(f"📡 wget ile çekiliyor: r/{subreddit}...")
    
    try:
        # wget komutu: User-Agent header'ı ile
        result = subprocess.run([
            "wget", "-q", "-O", TEMP_JSON_PATH,
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "--timeout=15",
            url
        ], timeout=20, capture_output=True)
        
        # Dosya boyutunu kontrol et (boş dosya olmamalı)
        if os.path.exists(TEMP_JSON_PATH) and os.path.getsize(TEMP_JSON_PATH) > 100:
            return True
        else:
            print(f"⚠️  İndirilen dosya boş veya çok küçük.")
            if os.path.exists(TEMP_JSON_PATH):
                os.remove(TEMP_JSON_PATH)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  İstek zaman aşımına uğradı (20s).")
        if os.path.exists(TEMP_JSON_PATH):
            os.remove(TEMP_JSON_PATH)
        return False
    except Exception as e:
        print(f"❌ wget hatası: {e}")
        if os.path.exists(TEMP_JSON_PATH):
            os.remove(TEMP_JSON_PATH)
        return False

def parse_reddit_json():
    """İndirilen JSON dosyasından metinleri ayıklar."""
    if not os.path.exists(TEMP_JSON_PATH):
        return []
    
    try:
        with open(TEMP_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        posts = []
        children = data.get('data', {}).get('children', [])
        
        for child in children:
            post_data = child.get('data', {})
            title = post_data.get('title', '')
            selftext = post_data.get('selftext', '')
            
            content = f"{title} {selftext}".strip()
            
            if len(content) > 50 and len(content) < 800:
                posts.append({
                    'title': title,
                    'text': content,
                    'url': f"https://reddit.com{post_data.get('permalink', '#')}",
                    'score': post_data.get('score', 0),
                    'author': post_data.get('author', 'anonymous'),
                    'created_utc': post_data.get('created_utc', 0),
                    'subreddit': 'unknown'
                })
        
        if os.path.exists(TEMP_JSON_PATH):
            os.remove(TEMP_JSON_PATH)
            
        return posts
    except Exception as e:
        print(f"❌ JSON parse hatası: {e}")
        if os.path.exists(TEMP_JSON_PATH):
            os.remove(TEMP_JSON_PATH)
        return []

def load_reddit_from_data_folder():
    """data/ klasöründeki Reddit JSON dosyalarını yükler (GitHub Actions tarafından indirilen)."""
    all_posts = []
    
    print("\n[Reddit Veri Kaynağı - data/ klasörü]")
    
    # data klasörünü kontrol et
    if not os.path.exists(DATA_DIR):
        print(f"⚠️  {DATA_DIR} klasörü bulunamadı.")
        return []
    
    # Tüm JSON dosyalarını tara
    json_files = [f for f in os.listdir(DATA_DIR) if f.startswith('reddit_') and f.endswith('.json')]
    
    if not json_files:
        print("⚠️  data/ klasöründe reddit_*.json dosyası bulunamadı.")
        return []
    
    for json_file in sorted(json_files):
        file_path = os.path.join(DATA_DIR, json_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            children = data.get('data', {}).get('children', [])
            subreddit_name = json_file.replace('reddit_', '').replace('.json', '')
            
            for child in children:
                post_data = child.get('data', {})
                title = post_data.get('title', '')
                selftext = post_data.get('selftext', '')
                
                content = f"{title} {selftext}".strip()
                
                if len(content) > 50 and len(content) < 800:
                    all_posts.append({
                        'title': title,
                        'text': content,
                        'url': f"https://reddit.com{post_data.get('permalink', '#')}",
                        'score': post_data.get('score', 0),
                        'author': post_data.get('author', 'anonymous'),
                        'created_utc': post_data.get('created_utc', 0),
                        'subreddit': subreddit_name
                    })
            
            print(f"✅ {json_file} üzerinden {len(children)} gönderi yüklendi.")
        except Exception as e:
            print(f"❌ {json_file} okuma hatası: {e}")
    
    print(f"\n🎯 Toplam {len(all_posts)} gönderi yüklendi.")
    return all_posts

def get_reddit_posts():
    """Reddit'ten popüler gönderileri çek - Önce data/ klasörünü kontrol eder (GitHub Actions)
    
    Sıralama:
    1. data/ klasöründeki JSON dosyalarını kullan (GitHub Actions tarafından indirilmiş)
    2. Eğer yoksa wget ile dene
    3. Eğer o da başarısız olursa mock data kullan
    """
    # Önce GitHub Actions tarafından indirilen verileri kontrol et
    all_posts = load_reddit_from_data_folder()
    
    if all_posts:
        return all_posts
    
    # Eğer data/ klasöründe veri yoksa, wget ile dene
    print("\n[Reddit Veri Kaynağı - wget ile JSON]")
    for sub in SUBREDDITS:
        if download_reddit_json(sub):
            posts = parse_reddit_json()
            if posts:
                print(f"✅ Başarılı! r/{sub} üzerinden {len(posts)} gönderi alındı.")
                all_posts.extend(posts)
                break  # İlk başarılı olandan devam et
            else:
                print(f"⚠️  r/{sub} boş veya geçerli veri yok.")
        else:
            print(f"⚠️  r/{sub} erişilemedi.")
    
    if all_posts:
        print(f"\n🎯 Toplam {len(all_posts)} gönderi başarıyla çekildi.")
        return all_posts
    
    # Eğer hiç gönderi çekilemediyse, örnek mock data kullan
    print("⚠️  Reddit'ten veri çekilemedi, örnek veriler kullanılıyor...")
    all_posts = [
        {
            'title': "Herkes bu filmi beğendi, o halde bu film kesinlikle en iyi filmdir.",
            'text': "Tüm arkadaşlarım bu filmi çok beğendi. Demek ki bu film tarihin en iyi filmi olmalı. Herkesin aynı fikirde olması, filmin kalitesinin kanıtıdır.",
            'url': "#",
            'score': 150,
            'author': "example_user",
            'created_utc': datetime.now().timestamp(),
            'subreddit': "fallacy"
        },
        {
            'title': "Ya bizimlesiniz ya da düşmanımızsınız",
            'text': "Bu konuda ya tamamen benimle hemfikirsiniz ya da tamamen yanılıyorsunuz. Orta yol yok. Eğer benim argümanımı desteklemiyorsanız, düşmanlarımdan birisiniz demektir.",
            'url': "#",
            'score': 89,
            'author': "debate_master",
            'created_utc': datetime.now().timestamp(),
            'subreddit': "philosophy"
        },
        {
            'title': "Doktor dedi, öyleyse doğrudur",
            'text': "Dr. Smith bu ilacı önerdi. O bir doktor olduğu için bu ilacın işe yarayacağı kesinlikle doğrudur. Doktorların her söylediği doğru olmalıdır.",
            'url': "#",
            'score': 234,
            'author': "health_guru",
            'created_utc': datetime.now().timestamp(),
            'subreddit': "science"
        },
        {
            'title': "Bundan sonra bu oldu, demek ki bundan dolayı oldu",
            'text': "Dün vitamin takviyesi almaya başladım ve bugün kendimi daha iyi hissediyorum. Demek ki vitamin takviyesi beni iyileştirdi. Bundan sonra her hasta vit almalı.",
            'url': "#",
            'score': 67,
            'author': "wellness_fan",
            'created_utc': datetime.now().timestamp(),
            'subreddit': "todayilearned"
        },
        {
            'title': "Plastik poşetleri yasaklarsak yakında her şeyi yasaklayacaklar",
            'text': "Önce plastik poşetleri yasakladılar. Sonra pipetleri. Yakında araba kullanmayı, et yemeyi, hatta nefes almayı bile yasaklayacaklar! Bu kaygan zeminde ilerliyoruz.",
            'url': "#",
            'score': 312,
            'author': "freedom_fighter",
            'created_utc': datetime.now().timestamp(),
            'subreddit': "changemyview"
        }
    ]
    print(f"✅ {len(all_posts)} örnek veri yüklendi.")
    
    return all_posts

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
            model=ANALYSIS_MODEL,
            max_new_tokens=250,
            temperature=0.3
        )
        
        # JSON'u temizle ve parse et
        clean_response = response.strip()
        if '```json' in clean_response:
            clean_response = clean_response.split('```json')[1]
        if '```' in clean_response:
            clean_response = clean_response.split('```')[0]
        clean_response = clean_response.strip()
        
        # JSON bulmaya çalış (bazen model ekstra metin ekleyebilir)
        start_idx = clean_response.find('{')
        end_idx = clean_response.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            clean_response = clean_response[start_idx:end_idx]
        
        result = json.loads(clean_response)
        return result
    except Exception as e:
        print(f"Analysis error: {e}")
        return {"fallacy_type": None, "confidence": 0, "explanation": "Analiz edilemedi", "quote": ""}

def generate_tarot_image(fallacy_type, output_path):
    """Tarot kartı görseli oluştur - Sabit stil, değişken konu"""
    # Fallacy tipine göre anahtar kelimeyi al, yoksa varsayılan kullan
    keyword = FALLACY_KEYWORDS.get(fallacy_type, "a mysterious symbol of logical error")
    
    # Sabit prompt ile değişken kısmı birleştir
    full_prompt = BASE_IMAGE_PROMPT + keyword
    
    try:
        image = client.text_to_image(full_prompt, model=IMAGE_MODEL)
        image.save(output_path)
        print(f"🎨 '{fallacy_type}' için tarot kartı çizildi: {output_path}")
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
