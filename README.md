# Fallacy Hunter - Automated Tarot Archive

Bu proje, sosyal medya gönderilerini (Reddit) tarayarak mantık hatalarını (fallacies) tespit eder, bunları mistik bir tarot kartı stiline dönüştürür ve GitHub Pages üzerinde sergiler. Tamamen ücretsizdir ve GitHub Actions ile otomatize edilmiştir.

## Özellikler

- **Tam Otomasyon:** GitHub Actions ile günde 4 kez otomatik çalışır.
- **Mantık Hatası Tespiti:** Hugging Face ücretsiz API (Mistral-7B) kullanılarak metinler analiz edilir.
- **Tarot Kartı Görselleştirme:** Her mantık hatası için özel bir tarot kartı ismi ve görseli oluşturulur.
- **Arşiv Sistemi:** Geçmiş tespitler `data/archive.json` dosyasında saklanır.
- **İnteraktif Arayüz:** 
  - Sağ/Sol kaydırma ile gezinme.
  - Sıralama: En Yeni (New), En Çok Oy alan (Hot), En Güvenilir (Best).
  - Oylama sistemi (Client-side demo).
- **0 Maliyet:** Reddit API (ücretsiz erişim), Hugging Face Inference API (ücretsiz katman) ve GitHub Pages kullanılır.

## Kurulum

### 1. Repository'yi Forklayın veya Klonlayın

### 2. GitHub Secrets Ayarları
Projenizin `Settings` > `Secrets and variables` > `Actions` bölümünden aşağıdaki secret'ları ekleyin:

- `HF_TOKEN`: Hugging Face API Token ([Buradan alın](https://huggingface.co/settings/tokens))
- `REDDIT_CLIENT_ID`: Reddit API Client ID (Opsiyonel, anonim erişim de çalışır)
- `REDDIT_CLIENT_SECRET`: Reddit API Secret (Opsiyonel)

*Not: Reddit API kimlik bilgileri olmadan da script çalışabilir, ancak daha düşük limitlere tabi olur.*

### 3. GitHub Pages'i Aktifleştirin
- `Settings` > `Pages` bölümüne gidin.
- Source olarak `Deploy from a branch` seçin.
- Branch olarak `main` (veya `master`) ve folder olarak `/docs` seçin.
- Kaydedin. Site birkaç dakika içinde yayında olacaktır.

### 4. Manuel Tetikleme (İsteğe Bağlı)
Otomasyonu beklemek istemiyorsanız:
- `Actions` sekmesine gidin.
- "Fallacy Hunter Automation" workflow'unu seçin.
- "Run workflow" butonuna tıklayın.

## Yapı

```
.
├── .github/workflows/
│   └── fallacy_hunter.yml    # Otomasyon workflow'u
├── scripts/
│   └── analyze.py            # Analiz ve görsel oluşturma scripti
├── data/
│   └── archive.json          # Tespit edilen fallacy arşivi
├── docs/
│   ├── index.html            # Frontend arayüzü
│   └── assets/               # Oluşturulan tarot kartları
└── README.md
```

## Mantık Hataları ve Tarot İsimleri

| Mantık Hatası | Tarot İsmi | Açıklama |
| :--- | :--- | :--- |
| Ad Hominem | The Betrayer | Kişiye saldırma |
| Straw Man | The Illusionist | Argümanı çarpıtma |
| Appeal to Authority | The High Priest | Otoriteye dayandırma |
| False Dilemma | The Forked Path | Yanlış ikilem |
| Slippery Slope | The Avalanche | Kaygan zemin |
| Circular Reasoning | The Ouroboros | Döngüsel mantık |
| Hasty Generalization | The Blind Seer | Aceleci genelleme |
| Red Herring | The Distractor | Konuyu saptırma |
| Tu Quoque | The Mirror | Sen de öylesin |
| No True Scotsman | The Gatekeeper | Gerçek İskoçyalı yok |

## Notlar

- **Oylama Sistemi:** Statik bir site olduğu için oylamalar tarayıcıda geçici olarak tutulur. Kalıcı oylama için bir backend veya GitHub API entegrasyonu gerekir.
- **Görseller:** Şu an basit geometrik şekillerle temsil edilmektedir. Daha gelişmiş görseller için DALL-E veya Stable Diffusion API'leri entegre edilebilir (bu maliyetli olabilir).
- **Sıklık:** GitHub Actions free tier limitlerine takılmamak için günde 4 kez çalışacak şekilde ayarlanmıştır.

## Lisans
MIT
