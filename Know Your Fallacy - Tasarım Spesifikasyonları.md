# Know Your Fallacy - Tasarım Spesifikasyonları

## Proje Genel Bakış
knowyourfallacy.com için AI destekli mantık hatası tespit sistemi. Kullanıcılar metin girişi yaparak mantık hatalarını tespit edebilir ve görsel açıklamalar alabilir.

## Renk Paleti
- **Ana Mavi**: #4A90A4 (Logo ve ana vurgular)
- **Koyu Mavi**: #2C5F7A (Başlıklar ve navigasyon)
- **Açık Gri**: #F8F9FA (Arka plan)
- **Orta Gri**: #6C757D (İkincil metin)
- **Beyaz**: #FFFFFF (Kartlar ve ana içerik alanları)
- **Vurgu Rengi**: #28A745 (Başarı durumları)
- **Uyarı Rengi**: #DC3545 (Hata durumları)

## Tipografi
- **Ana Font**: Inter, sans-serif
- **Başlık Boyutları**: 
  - H1: 2.5rem (40px)
  - H2: 2rem (32px)
  - H3: 1.5rem (24px)
- **Gövde Metni**: 1rem (16px)
- **Küçük Metin**: 0.875rem (14px)

## Ana Bileşenler

### 1. Header
- Logo (sol taraf)
- Navigasyon menüsü (sağ taraf): Ana Sayfa, Hakkında, İletişim
- Responsive hamburger menü (mobil)

### 2. Hero Section
- Ana başlık: "Metninizi Analiz Edin, Mantık Hatalarını Keşfedin"
- Alt başlık: Kısa açıklama
- Büyük metin input alanı
- "Analiz Et" butonu

### 3. Sonuçlar Bölümü
- Tespit edilen mantık hataları kartları
- Her kart için:
  - Mantık hatası adı
  - Kısa açıklama
  - Görsel ikon
  - Detaylı açıklama linki

### 4. Yan Panel (Sidebar)
- Mantık hatası kategorileri
- Popüler mantık hataları listesi
- Hızlı erişim linkleri

### 5. Footer
- Telif hakkı bilgisi
- Sosyal medya linkleri
- Gizlilik politikası

## Kullanıcı Deneyimi Akışı

1. **Giriş**: Kullanıcı ana sayfaya gelir
2. **Metin Girişi**: Analiz edilecek metni yazar
3. **Analiz**: AI sistemi metni analiz eder
4. **Sonuçlar**: Tespit edilen mantık hataları görüntülenir
5. **Detay**: Kullanıcı her mantık hatası hakkında detaylı bilgi alabilir

## Responsive Tasarım
- **Desktop**: 1200px+ (3 sütun layout)
- **Tablet**: 768px-1199px (2 sütun layout)
- **Mobil**: <768px (1 sütun layout)

## Animasyonlar ve Etkileşimler
- Hover efektleri (butonlar ve kartlar)
- Smooth scroll
- Fade-in animasyonları
- Loading spinner (analiz sırasında)
- Tooltip'ler (mantık hatası açıklamaları için)

## Erişilebilirlik
- WCAG 2.1 AA standartlarına uyum
- Klavye navigasyonu desteği
- Screen reader uyumluluğu
- Yeterli renk kontrastı
- Alt text'ler tüm görseller için

## Performans Hedefleri
- Sayfa yükleme süresi: <3 saniye
- First Contentful Paint: <1.5 saniye
- Lighthouse skoru: 90+
- Mobil optimizasyon

## Teknik Gereksinimler
- React.js frontend
- Responsive CSS (Tailwind CSS)
- AI entegrasyonu (OpenAI API)
- Modern browser desteği
- SEO optimizasyonu

