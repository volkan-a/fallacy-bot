import os
import json
import requests
import random
from datetime import datetime

# Hugging Face API Configuration
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# Reddit API (Public, no auth needed for basic access)
REDDIT_URL = "https://www.reddit.com/r/all/hot.json?limit=100"

# Hugging Face Models
LLM_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"  # Mantık hatası analizi için
IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"  # Görsel üretimi için

def fetch_reddit_posts():
    """Reddit'den popüler gönderileri çek"""
    try:
        response = requests.get(REDDIT_URL, headers={'User-Agent': 'FallacyBot/1.0'})
        response.raise_for_status()
        data = response.json()
        posts = []
        for child in data['data']['children']:
            post = child['data']
            # Sadece metin içeren veya başlığı olan gönderileri al
            if post['selftext'] or post['title']:
                content = f"{post['title']}\n{post['selftext']}".strip()
                if len(content) > 50:  # Çok kısa içerikleri atla
                    posts.append({
                        'id': post['id'],
                        'content': content,
                        'score': post['score'],
                        'url': f"https://reddit.com{post['permalink']}",
                        'author': post['author'] if post['author'] else 'anonymous',
                        'created_utc': post['created_utc']
                    })
        return posts[:20]  # İlk 20 gönderiyi analiz et (API limitleri için)
    except Exception as e:
        print(f"Reddit fetch error: {e}")
        return []

def analyze_fallacy(text):
    """Metindeki mantık hatasını analiz et"""
    prompt = f"""Analyze the following text for logical fallacies. 
Return ONLY a JSON object with this exact structure:
{{
    "has_fallacy": true/false,
    "fallacy_type": "Name of fallacy (e.g., Ad Hominem, Straw Man, False Dilemma)",
    "confidence": 0.0-1.0,
    "explanation": "Brief explanation in Turkish",
    "quote": "The specific part of text containing the fallacy"
}}

Text to analyze:
{text}

Remember: Return ONLY valid JSON, no markdown, no extra text."""

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{LLM_MODEL}/v1/chat/completions",
            headers=HEADERS,
            json={
                "model": LLM_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
                "temperature": 0.3
            }
        )
        response.raise_for_status()
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # JSON'u temizle ve parse et
        content = content.replace('```json', '').replace('```', '').strip()
        analysis = json.loads(content)
        return analysis
    except Exception as e:
        print(f"Analysis error: {e}")
        return None

def generate_tarot_card(fallacy_type, explanation):
    """Mistik tarot kartı görseli oluştur"""
    prompt = f"""Mystical tarot card illustration representing the logical fallacy '{fallacy_type}'. 
Dark mystical background with cosmic stars, ancient symbols, and ethereal glow. 
The card should show abstract symbolism of deception, flawed reasoning, or intellectual trap. 
Art style: Art Nouveau, Alphonse Mucha inspired, gold borders, intricate details, mystical atmosphere.
Title text at bottom: '{fallacy_type}'
Color palette: Deep purples, gold, midnight blue, silver accents."""

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{IMAGE_MODEL}/diffusers",
            headers=HEADERS,
            json={"prompt": prompt},
            timeout=60
        )
        response.raise_for_status()
        
        # Görseli kaydet
        image_filename = f"assets/{fallacy_type.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        with open(image_filename, 'wb') as f:
            f.write(response.content)
        return image_filename
    except Exception as e:
        print(f"Image generation error: {e}")
        return None

def load_existing_data():
    """Mevcut arşivi yükle"""
    try:
        with open('docs/data/archive.json', 'r') as f:
            return json.load(f)
    except:
        return {"entries": []}

def save_data(data):
    """Veriyi kaydet"""
    os.makedirs('docs/data', exist_ok=True)
    with open('docs/data/archive.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    print("🔮 Fallacy Tarot Bot başlatılıyor...")
    
    # Reddit'ten gönderi çek
    posts = fetch_reddit_posts()
    if not posts:
        print("Hiç gönderi bulunamadı!")
        return
    
    print(f"📊 {len(posts)} gönderi analiz ediliyor...")
    
    # Her gönderiyi analiz et
    analyzed_posts = []
    for post in posts:
        print(f"Analiz ediliyor: {post['id']}")
        analysis = analyze_fallacy(post['content'])
        
        if analysis and analysis.get('has_fallacy'):
            post['analysis'] = analysis
            analyzed_posts.append(post)
    
    if not analyzed_posts:
        print("Bu turda mantık hatası bulunamadı.")
        return
    
    # En yüksek confidence skoruna sahip olanı seç
    best_post = max(analyzed_posts, key=lambda x: x['analysis'].get('confidence', 0))
    
    print(f"🎯 En yüksek skorlu fallacy: {best_post['analysis']['fallacy_type']}")
    
    # Tarot kartı oluştur
    image_path = generate_tarot_card(
        best_post['analysis']['fallacy_type'],
        best_post['analysis']['explanation']
    )
    
    # Mevcut veriyi yükle ve yeni entry ekle
    archive = load_existing_data()
    
    new_entry = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "timestamp": datetime.now().isoformat(),
        "tweet_content": best_post['content'],
        "source_url": best_post['url'],
        "author": best_post['author'],
        "score": best_post['score'],
        "fallacy_type": best_post['analysis']['fallacy_type'],
        "confidence": best_post['analysis']['confidence'],
        "explanation": best_post['analysis']['explanation'],
        "quote": best_post['analysis']['quote'],
        "image_path": image_path if image_path else "assets/default_tarot.png",
        "votes": {"up": 0, "down": 0},
        "category": "newest"
    }
    
    archive["entries"].insert(0, new_entry)  # En başa ekle
    
    # Sıralama kategorilerini güncelle
    # Hot: Son 24 saatteki en çok vote alanlar
    # Best: Tüm zamanların en çok vote alanları
    # Newest: En yeniler (zaten chronological)
    
    save_data(archive)
    
    # HTML'i güncelle (bir sonraki adımda yapılacak)
    print("✨ Veri kaydedildi! HTML güncelleniyor...")
    generate_html(archive)

def generate_html(archive):
    """Mistik tarot temalı HTML oluştur"""
    
    entries_html = ""
    for entry in archive["entries"]:
        entries_html += f"""
        <div class="tarot-card-slide" data-id="{entry['id']}">
            <div class="card-image">
                <img src="{entry['image_path']}" alt="{entry['fallacy_type']}">
                <div class="card-overlay">
                    <h3>{entry['fallacy_type']}</h3>
                    <span class="confidence">Güven: {entry['confidence']*100:.0f}%</span>
                </div>
            </div>
            <div class="card-content">
                <blockquote>"{entry['quote']}"</blockquote>
                <p class="full-text">{entry['tweet_content']}</p>
                <div class="explanation">
                    <strong>🔮 Açımlama:</strong>
                    <p>{entry['explanation']}</p>
                </div>
                <div class="source">
                    <a href="{entry['source_url']}" target="_blank">Kaynak: Reddit/u/{entry['author']}</a>
                    <span class="score">⬆️ {entry['score']}</span>
                </div>
                <div class="voting">
                    <button onclick="vote('{entry['id']}', 'up')" class="vote-btn up">⬆️ <span id="up-{entry['id']}">{entry['votes']['up']}</span></button>
                    <button onclick="vote('{entry['id']}', 'down')" class="vote-btn down">⬇️ <span id="down-{entry['id']}">{entry['votes']['down']}</span></button>
                </div>
            </div>
        </div>
        """
    
    html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Know Your Fallacy - Mistik Tarot Analizi</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #1a0a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e8d5b7;
            min-height: 100vh;
            overflow-x: hidden;
        }}
        
        .stars {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 3rem;
        }}
        
        h1 {{
            font-size: 3rem;
            color: #ffd700;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
            margin-bottom: 1rem;
        }}
        
        .subtitle {{
            font-size: 1.2rem;
            opacity: 0.8;
            font-style: italic;
        }}
        
        .navigation {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        
        .nav-btn {{
            background: rgba(255, 215, 0, 0.1);
            border: 2px solid #ffd700;
            color: #ffd700;
            padding: 0.8rem 1.5rem;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1rem;
        }}
        
        .nav-btn:hover, .nav-btn.active {{
            background: #ffd700;
            color: #1a0a2e;
            transform: translateY(-2px);
        }}
        
        .slider-container {{
            position: relative;
            overflow: hidden;
            padding: 2rem 0;
        }}
        
        .slider {{
            display: flex;
            transition: transform 0.5s ease;
            gap: 2rem;
        }}
        
        .tarot-card-slide {{
            min-width: 100%;
            background: rgba(26, 10, 46, 0.8);
            border: 3px solid #ffd700;
            border-radius: 20px;
            padding: 2rem;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            backdrop-filter: blur(10px);
        }}
        
        .card-image {{
            position: relative;
            border-radius: 15px;
            overflow: hidden;
            border: 2px solid #ffd700;
        }}
        
        .card-image img {{
            width: 100%;
            height: 400px;
            object-fit: cover;
        }}
        
        .card-overlay {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0,0,0,0.8));
            padding: 1rem;
            text-align: center;
        }}
        
        .card-overlay h3 {{
            color: #ffd700;
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .confidence {{
            background: rgba(255, 215, 0, 0.2);
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.9rem;
        }}
        
        .card-content {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        blockquote {{
            background: rgba(255, 215, 0, 0.1);
            border-left: 4px solid #ffd700;
            padding: 1rem;
            font-style: italic;
            border-radius: 0 10px 10px 0;
        }}
        
        .full-text {{
            opacity: 0.8;
            line-height: 1.6;
        }}
        
        .explanation {{
            background: rgba(0, 0, 0, 0.3);
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid rgba(255, 215, 0, 0.3);
        }}
        
        .source {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.9rem;
        }}
        
        .source a {{
            color: #ffd700;
            text-decoration: none;
        }}
        
        .voting {{
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .vote-btn {{
            flex: 1;
            padding: 0.8rem;
            border: 2px solid #ffd700;
            background: transparent;
            color: #ffd700;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1rem;
        }}
        
        .vote-btn:hover {{
            background: #ffd700;
            color: #1a0a2e;
        }}
        
        .vote-btn.up:hover {{
            background: #4caf50;
            border-color: #4caf50;
            color: white;
        }}
        
        .vote-btn.down:hover {{
            background: #f44336;
            border-color: #f44336;
            color: white;
        }}
        
        .controls {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
        }}
        
        .control-btn {{
            background: rgba(255, 215, 0, 0.2);
            border: 2px solid #ffd700;
            color: #ffd700;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.5rem;
            transition: all 0.3s ease;
        }}
        
        .control-btn:hover {{
            background: #ffd700;
            color: #1a0a2e;
            transform: scale(1.1);
        }}
        
        @media (max-width: 768px) {{
            .tarot-card-slide {{
                grid-template-columns: 1fr;
            }}
            
            .card-image img {{
                height: 300px;
            }}
            
            h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="stars"></div>
    
    <div class="container">
        <header>
            <h1>🔮 Know Your Fallacy</h1>
            <p class="subtitle">Mistik Tarot Kartlarıyla Mantık Hatalarını Keşfet</p>
        </header>
        
        <div class="navigation">
            <button class="nav-btn active" onclick="filterEntries('newest')">🆕 En Yeni</button>
            <button class="nav-btn" onclick="filterEntries('hot')">🔥 Popüler</button>
            <button class="nav-btn" onclick="filterEntries('best')">⭐ En İyi</button>
        </div>
        
        <div class="slider-container">
            <div class="slider" id="slider">
                {entries_html}
            </div>
        </div>
        
        <div class="controls">
            <button class="control-btn" onclick="slide(-1)">◀</button>
            <button class="control-btn" onclick="slide(1)">▶</button>
        </div>
    </div>
    
    <script>
        let currentIndex = 0;
        const slider = document.getElementById('slider');
        const slides = document.querySelectorAll('.tarot-card-slide');
        
        function slide(direction) {{
            currentIndex = Math.max(0, Math.min(currentIndex + direction, slides.length - 1));
            slider.style.transform = `translateX(-${{currentIndex * 100}}%)`;
        }}
        
        function filterEntries(category) {{
            // Basit filtreleme - gerçek uygulamada backend'den veri çekilmeli
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            // Burada normalde API'den filtrelenmiş veri çekilir
            alert(category + ' kategorisi yükleniyor... (Backend entegrasyonu gerekli)');
        }}
        
        function vote(id, type) {{
            // Oylama fonksiyonu - localStorage ile geçici çözüm
            const key = `vote_${{id}}_${{type}}`;
            if (!localStorage.getItem(key)) {{
                const span = document.getElementById(`${{type}}-${{id}}`);
                span.textContent = parseInt(span.textContent) + 1;
                localStorage.setItem(key, 'voted');
            }} else {{
                alert('Zaten oy verdiniz!');
            }}
        }}
        
        // Otomatik yıldız efekti
        function createStars() {{
            const starsContainer = document.querySelector('.stars');
            for (let i = 0; i < 100; i++) {{
                const star = document.createElement('div');
                star.style.cssText = `
                    position: absolute;
                    width: 2px;
                    height: 2px;
                    background: white;
                    border-radius: 50%;
                    top: ${{Math.random() * 100}}%;
                    left: ${{Math.random() * 100}}%;
                    animation: twinkle ${{2 + Math.random() * 3}}s infinite;
                    opacity: ${{0.3 + Math.random() * 0.7}};
                `;
                starsContainer.appendChild(star);
            }}
        }}
        
        createStars();
        
        // CSS animasyonu ekle
        const style = document.createElement('style');
        style.textContent = `
            @keyframes twinkle {{
                0%, 100% {{ opacity: 0.3; }}
                50% {{ opacity: 1; }}
            }}
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>"""
    
    os.makedirs('docs', exist_ok=True)
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("🌐 HTML sayfası oluşturuldu!")

if __name__ == "__main__":
    main()
