from flask import Blueprint, request, jsonify
import openai
import os
import json

fallacy_bp = Blueprint('fallacy', __name__)

# OpenAI client configuration
client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_API_BASE')
)

@fallacy_bp.route('/analyze', methods=['POST'])
def analyze_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        # AI prompt for fallacy detection
        prompt = f"""
        Aşağıdaki metni analiz et ve içindeki mantık hatalarını (logical fallacies) tespit et. 
        Her tespit edilen mantık hatası için şu bilgileri ver:
        
        1. Mantık hatasının adı (Türkçe)
        2. Kısa açıklama
        3. Metinden örnek cümle
        4. Güven seviyesi (0-100)
        5. Önem derecesi (low, medium, high)
        
        Analiz edilecek metin:
        "{text}"
        
        Lütfen yanıtını JSON formatında ver:
        {{
            "fallacies": [
                {{
                    "name": "Mantık Hatası Adı",
                    "description": "Açıklama",
                    "example": "Metinden örnek",
                    "confidence": 85,
                    "severity": "medium"
                }}
            ],
            "summary": "Genel analiz özeti"
        }}
        
        Eğer hiç mantık hatası bulamazsan, fallacies dizisini boş bırak.
        """
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sen mantık hataları konusunda uzman bir analiz sistemisin. Metinlerdeki mantık hatalarını tespit etmek ve açıklamak konusunda çok iyisin."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        # Parse the response
        ai_response = response.choices[0].message.content
        
        # Try to extract JSON from the response
        try:
            # Find JSON in the response
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = ai_response[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                # Fallback if JSON parsing fails
                result = {
                    "fallacies": [],
                    "summary": "Analiz tamamlandı ancak sonuçlar beklenilen formatta değil."
                }
        except json.JSONDecodeError:
            # Fallback response
            result = {
                "fallacies": [],
                "summary": "Analiz tamamlandı ancak sonuçlar işlenirken bir hata oluştu."
            }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in analyze_text: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@fallacy_bp.route('/fallacy-types', methods=['GET'])
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
        },
        {
            "name": "Kaygan Zemin",
            "english_name": "Slippery Slope",
            "description": "Küçük bir değişikliğin aşırı sonuçlara yol açacağını iddia etme",
            "example": "Plastik poşetleri yasaklarsak, yakında her şeyi yasaklarız"
        },
        {
            "name": "Çember İçi Akıl Yürütme",
            "english_name": "Circular Reasoning",
            "description": "Sonucu kanıt olarak kullanma",
            "example": "Bu kitap en iyisidir çünkü en iyi kitaplar listesinde"
        },
        {
            "name": "Kırmızı Ringa Balığı",
            "english_name": "Red Herring",
            "description": "Dikkati asıl konudan uzaklaştırma",
            "example": "İklim değişikliği önemli ama ekonomi daha önemli"
        }
    ]
    
    return jsonify({"fallacy_types": fallacy_types})

