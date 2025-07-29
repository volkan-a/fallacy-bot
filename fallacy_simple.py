from flask import Blueprint, request, jsonify
import json
import re

fallacy_simple_bp = Blueprint('fallacy_simple', __name__)

# Predefined fallacy patterns for simple detection
FALLACY_PATTERNS = {
    "Ad Hominem": {
        "patterns": [
            r"çünkü.*?(başarısız|kötü|güvenilmez|yetersiz)",
            r"bunu söyleyen.*?(kişi|adam|kadın).*?(başarısız|kötü)",
            r"(o|bu kişi|şu adam).*?(geçmişte|daha önce).*?(başarısız|hata)"
        ],
        "description": "Argümanın kendisi yerine, argümanı öne süren kişi hedef alınmıştır. Bu, mantıklı tartışmanın temel ilkelerinden birinin ihlalidir.",
        "severity": "high"
    },
    "Hatalı Genelleme": {
        "patterns": [
            r"(tüm|bütün|hep|her zaman).*?(kaba|kötü|başarısız)",
            r"(bir|tek).*?(deneyim|olay).*?(tüm|bütün|hep)",
            r"demek ki.*?(tüm|bütün|hep|her)"
        ],
        "description": "Yetersiz örneklerden geniş sonuçlar çıkarılmıştır. Bu mantık hatası, sınırlı gözlemlerden tüm bir grup hakkında genelleme yapılması durumunda ortaya çıkar.",
        "severity": "medium"
    },
    "Yanlış İkilem": {
        "patterns": [
            r"ya.*?ya da",
            r"(desteklersin|kabul edersin).*?ya da.*?(karşısın|reddersin|mahvet)",
            r"(iki seçenek|sadece iki|ya bu ya o)"
        ],
        "description": "Sadece iki seçenek olduğu varsayılmış ve diğer olasılıklar göz ardı edilmiştir.",
        "severity": "medium"
    },
    "Post Hoc": {
        "patterns": [
            r"(sonra|ardından).*?(neden|sebep)",
            r"(içtikten|yedikten|yaptıktan) sonra.*?(ağrı|sorun|hastalık)",
            r"(bundan dolayı|bu yüzden).*?(oldu|gerçekleşti)"
        ],
        "description": "Bir olayın başka bir olaydan sonra gerçekleşmesi, onun nedeni olduğu anlamına gelmez.",
        "severity": "medium"
    }
}

def detect_fallacies(text):
    """Simple pattern-based fallacy detection"""
    detected_fallacies = []
    text_lower = text.lower()
    
    for fallacy_name, fallacy_data in FALLACY_PATTERNS.items():
        for pattern in fallacy_data["patterns"]:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                # Find the actual text that matched
                match_obj = re.search(pattern, text, re.IGNORECASE)
                if match_obj:
                    example_text = match_obj.group(0)
                    
                    detected_fallacies.append({
                        "name": fallacy_name,
                        "description": fallacy_data["description"],
                        "example": example_text,
                        "severity": fallacy_data["severity"],
                        "confidence": 85  # Fixed confidence for pattern matching
                    })
                break  # Only detect once per fallacy type
    
    return detected_fallacies

@fallacy_simple_bp.route('/analyze', methods=['POST'])
def analyze_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        # Detect fallacies using pattern matching
        detected_fallacies = detect_fallacies(text)
        
        # Generate summary
        if detected_fallacies:
            fallacy_count = len(detected_fallacies)
            high_severity_count = len([f for f in detected_fallacies if f['severity'] == 'high'])
            
            if high_severity_count > 0:
                summary = f"Analiz edilen metinde {fallacy_count} adet mantık hatası tespit edilmiştir. {high_severity_count} tanesi yüksek önem seviyesindedir. Metninizi gözden geçirerek bu hataları düzeltebilirsiniz."
            else:
                summary = f"Analiz edilen metinde {fallacy_count} adet mantık hatası tespit edilmiştir. Bu hataları düzelterek argümanınızı güçlendirebilirsiniz."
        else:
            summary = "Analiz edilen metinde belirgin bir mantık hatası tespit edilmedi. Metniniz mantıksal açıdan tutarlı görünüyor."
        
        result = {
            "fallacies": detected_fallacies,
            "summary": summary
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in analyze_text: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@fallacy_simple_bp.route('/fallacy-types', methods=['GET'])
def get_fallacy_types():
    """Return common fallacy types for reference"""
    fallacy_types = [
        {
            "name": "Hatalı Genelleme",
            "english_name": "Hasty Generalization",
            "description": "Yetersiz örneklerden geniş sonuçlar çıkarma",
            "example": "Bir restorandaki kötü deneyimden tüm şehirdeki restoranları kötü olarak değerlendirme"
        },
        {
            "name": "Ad Hominem",
            "english_name": "Personal Attack",
            "description": "Argüman yerine kişiyi hedef alma",
            "example": "Bir fikri, onu söyleyen kişinin geçmişine bakarak reddetme"
        },
        {
            "name": "Yanlış İkilem",
            "english_name": "False Dilemma",
            "description": "Sadece iki seçenek varmış gibi gösterme",
            "example": "Ya benimle hemfikirsin ya da tamamen yanılıyorsun"
        },
        {
            "name": "Post Hoc",
            "english_name": "False Cause",
            "description": "Ardışıklığı nedensellik olarak görme",
            "example": "Limonata içtikten sonra başım ağrıdı, limonata baş ağrısına neden oluyor"
        }
    ]
    
    return jsonify({"fallacy_types": fallacy_types})

