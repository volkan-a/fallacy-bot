# 🔮 Fallacy Tarot - Mistik Mantık Analizi

Reddit'teki popüler gönderilerdeki mantık hatalarını tespit eden, her hata için mistik tarot kartı görseli oluşturan ve bunları güzel bir arayüzde sunan tam otomasyon sistemi.

## ✨ Özellikler

- **Otomatik Veri Toplama**: Reddit API ile popüler gönderileri çeker
- **AI Destekli Analiz**: Hugging Face LLM modelleri ile mantık hatası tespiti
- **Tarot Kartı Görselleştirme**: Her mantık hatası için Stable Diffusion ile özel görsel üretimi
- **Mistik Arayüz**: Tarot temalı, slider navigasyonlu modern web arayüzü
- **Oylama Sistemi**: Reddit tarzı upvote/downvote ile "Hot", "Best", "Newest" sıralama
- **Tam Otomasyon**: GitHub Actions ile günde 4 kez otomatik çalışma
- **0 Maliyet**: Tamamen ücretsiz teknolojiler

## 🚀 Kurulum

### 1. Hugging Face Token Alın

1. [huggingface.co](https://huggingface.co/) adresine gidin
2. Hesap oluşturun veya giriş yapın
3. Settings > Access Tokens > Create new token
4. İsim: `fallacy-bot`, Tip: **Write** seçin
5. Token'ı kopyalayın

### 2. GitHub Secrets'e Token Ekleyin

1. Depo ayarlarına gidin (Settings)
2. Secrets and variables > Actions
3. New repository secret
4. Name: `HF_TOKEN`, Secret: [kopyaladığınız token]

### 3. GitHub Pages Ayarları

1. Settings > Pages
2. Source: **GitHub Actions** seçin
3. Custom domain: `www.knowyourfallacy.com` girin (opsiyonel)
4. Enforce HTTPS işaretleyin

### 4. Cloudflare DNS Ayarları (Domain kullanıyorsanız)

Cloudflare panelinde:
- **A Kayıtları** (@ için):
  - 185.199.108.153
  - 185.199.109.153
  - 185.199.110.153
  - 185.199.111.153
- **CNAME Kaydı** (www için): `<kullaniciadi>.github.io`
- Proxy durumunu **Gri Bulut (DNS Only)** yapın

## 📁 Dosya Yapısı

```
├── .github/workflows/
│   └── fallacy_automation.yml    # GitHub Actions workflow
├── src/
│   └── fallacy_analyzer.py       # Ana analiz scripti
├── docs/
│   ├── index.html                # Web arayüzü
│   ├── data/
│   │   └── fallacies.json        # Analiz sonuçları
│   └── assets/                   # Tarot kartı görselleri
└── README.md
```

## ⏰ Otomasyon Zamanlaması

Workflow her 6 saatte bir otomatik çalışır (UTC):
- 00:00
- 06:00
- 12:00
- 18:00

Manuel tetikleme için: Actions > Fallacy Tarot Automation > Run workflow

## 🔮 Mantık Hatası Türleri

Sistem şu mantık hatalarını tespit edebilir:
- Ad Hominem (Kişiye Saldırı)
- Straw Man (Korkuluk Saçma)
- Appeal to Authority (Otoriteye Başvuru)
- False Dilemma (Yanlış İkilem)
- Slippery Slope (Kaygan Eğim)
- Circular Reasoning (Döngüsel Mantık)
- Hasty Generalization (Acelemci Genelleme)
- Red Herring (Konu Sapıtma)
- Tu Quoque (Sen de Öyle)
- Appeal to Emotion (Duyguya Başvuru)

## 🛠️ Teknolojiler

- **Veri Kaynağı**: Reddit API (ücretsiz)
- **LLM Analiz**: Hugging Face Mistral-7B-Instruct
- **Görsel Üretim**: Stable Diffusion XL
- **Otomasyon**: GitHub Actions
- **Hosting**: GitHub Pages
- **Frontend**: HTML/CSS/JavaScript (vanilla)

## 📝 Notlar

- İlk çalıştırmada örnek veri oluşturulur
- Görsel üretimi başarısız olursa placeholder kart oluşturulur
- Oylama verileri localStorage'da tutulur (gerçek uygulamada backend gerekir)
- Domain yayına alınması 15 dakika - 24 saat sürebilir

## 🎯 Kullanım

1. Workflow otomatik çalışır veya manuel tetiklenir
2. Reddit'ten popüler gönderiler çekilir
3. Her gönderi mantık hatası açısından analiz edilir
4. Tespit edilen hatalar için tarot kartı görselleri oluşturulur
5. Sonuçlar `docs/data/fallacies.json` dosyasına kaydedilir
6. GitHub Pages otomatik deploy edilir
7. Ziyaretçiler `knowyourfallacy.com` üzerinden sonuçları görüntüler

## 📄 Lisans

MIT License
