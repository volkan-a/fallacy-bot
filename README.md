# 🔮 Know Your Fallacy - Mistik Tarot Analizi

GitHub Actions ile otomatik olarak Reddit'ten mantık hatalarını tespit eden, analiz eden ve mistik tarot kartları görselleştiren tam otomasyon sistemi.

## ✨ Özellikler

- **Tam Otomasyon**: Her 6 saatte bir GitHub Actions tarafından otomatik çalışır
- **0 Maliyet**: Tamamen ücretsiz teknolojiler (Hugging Face, Reddit API, GitHub Pages)
- **Mantik Hatası Tespiti**: AI ile metin analizi ve fallacy tespiti
- **Tarot Kartı Görselleştirme**: Her fallacy için özel AI üretimi görsel
- **Arşiv Sistemi**: Tüm geçmiş kayıtlar slider ile gezilebilir
- **Oylama Sistemi**: Kullanıcılar entry'lere oy verebilir
- **Responsive Tasarım**: Mobil uyumlu mistik arayüz

## 🚀 Kurulum

### 1. Hugging Face Token Alın
1. [huggingface.co](https://huggingface.co/) adresine gidin
2. Settings > Access Tokens > Create new token
3. Token tipini **Write** olarak seçin
4. Token'ı kopyalayın

### 2. GitHub Secrets Ekleyin
1. Deponuzun Settings > Secrets and variables > Actions sayfasına gidin
2. New repository secret oluşturun:
   - Name: `HF_TOKEN`
   - Value: Kopyaladığınız token

### 3. GitHub Pages Ayarları
1. Settings > Pages sayfasına gidin
2. Source olarak **GitHub Actions** seçin
3. Custom domain olarak `www.knowyourfallacy.com` girin (opsiyonel)

### 4. Cloudflare DNS Ayarları (Custom Domain için)
Cloudflare panelinizde:
- **A Kayıtları** (@ için):
  - 185.199.108.153
  - 185.199.109.153
  - 185.199.110.153
  - 185.199.111.153
- **CNAME Kaydı** (www için): `<username>.github.io`
- Proxy status: **DNS Only** (Gri bulut)

## 📁 Dosya Yapısı

```
├── .github/workflows/
│   └── fallacy_bot.yml      # GitHub Actions workflow
├── scripts/
│   └── fallacy_analyzer.py  # Ana analiz scripti
├── docs/
│   ├── index.html           # Oluşturulan web sitesi
│   └── data/
│       └── archive.json     # Arşiv verisi
├── assets/                   # Tarot kartı görselleri
└── README.md
```

## ⚙️ Nasıl Çalışır?

1. **Zamanlanmış Tetikleme**: GitHub Actions her 6 saatte bir (`0 */6 * * *`) çalışır
2. **Veri Çekme**: Reddit r/all/hot'tan popüler gönderiler çekilir
3. **AI Analizi**: Mistral-7B modeli ile mantık hatası analizi yapılır
4. **Görsel Üretimi**: Stable Diffusion XL ile tarot kartı oluşturulur
5. **Veri Kaydı**: Sonuçlar archive.json'a kaydedilir
6. **Deploy**: Web sitesi otomatik olarak GitHub Pages'e deploy edilir

## 🎨 Özelleştirme

### Çalışma Sıklığını Değiştirin
`.github/workflows/fallacy_bot.yml` dosyasında:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Her 6 saatte bir
  # - cron: '0 0 * * *'  # Günde bir
  # - cron: '0 * * * *'  # Her saat
```

### Model Değişikliği
`scripts/fallacy_analyzer.py` dosyasında:
```python
LLM_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"  # Farklı LLM
IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"  # Farklı image model
```

## 🔧 Manuel Çalıştırma

Workflow'u manuel tetiklemek için:
1. GitHub'da Actions sekmesine gidin
2. "Fallacy Tarot Bot" workflow'unu seçin
3. "Run workflow" butonuna tıklayın

## 📊 Veri Yapısı

Her entry şu bilgileri içerir:
```json
{
  "id": "20240101_120000",
  "timestamp": "2024-01-01T12:00:00",
  "tweet_content": "...",
  "source_url": "https://reddit.com/...",
  "author": "username",
  "score": 1234,
  "fallacy_type": "Ad Hominem",
  "confidence": 0.95,
  "explanation": "...",
  "quote": "...",
  "image_path": "assets/ad_hominem_20240101_120000.png",
  "votes": {"up": 10, "down": 2}
}
```

## ⚠️ Önemli Notlar

- **API Limitleri**: Hugging Face ücretsiz tier'da rate limit vardır
- **Görsel Kalitesi**: AI görsel üretimi bazen tutarsız olabilir
- **Reddit Erişimi**: Bazı subreddit'ler API erişimini kısıtlayabilir
- **Domain Yayılması**: DNS değişiklikleri 24 saate kadar sürebilir

## 🛠️ Sorun Giderme

### Workflow Çalışmıyor
- Secrets'ta HF_TOKEN doğru eklenmiş mi kontrol edin
- Actions sekmesinden logları inceleyin

### Görsel Oluşturulmuyor
- Hugging Face token'ınızın "Write" yetkisi var mı kontrol edin
- Model inference API'sinin aktif olduğundan emin olun

### Site Görünmüyor
- GitHub Pages ayarlarında "GitHub Actions" seçili mi kontrol edin
- docs/index.html dosyası oluşturulmuş mu kontrol edin

## 📝 Lisans

MIT License - Ücretsiz kullanım

## 🙏 Katkıda Bulunun

Pull request ve issue'lar açık!

---

**Made with 🔮 and ✨ by GitHub Actions**
