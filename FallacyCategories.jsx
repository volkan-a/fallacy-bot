import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Users, 
  Target, 
  TrendingDown, 
  RotateCcw, 
  Zap, 
  ArrowRight,
  BookOpen
} from 'lucide-react'

const FallacyCategories = () => {
  const fallacyTypes = [
    {
      name: "Hatalı Genelleme",
      englishName: "Hasty Generalization",
      icon: <TrendingDown className="h-6 w-6" />,
      description: "Yetersiz örneklerden geniş sonuçlar çıkarma",
      example: "Bir restorandaki kötü deneyimden tüm şehirdeki restoranları kötü olarak değerlendirme",
      color: "bg-red-50 border-red-200"
    },
    {
      name: "Ad Hominem",
      englishName: "Personal Attack",
      icon: <Users className="h-6 w-6" />,
      description: "Argüman yerine kişiyi hedef alma",
      example: "Bir fikri, onu söyleyen kişinin geçmişine bakarak reddetme",
      color: "bg-orange-50 border-orange-200"
    },
    {
      name: "Yanlış İkilem",
      englishName: "False Dilemma",
      icon: <Target className="h-6 w-6" />,
      description: "Sadece iki seçenek varmış gibi gösterme",
      example: "Ya benimle hemfikirsin ya da tamamen yanılıyorsun",
      color: "bg-yellow-50 border-yellow-200"
    },
    {
      name: "Post Hoc",
      englishName: "False Cause",
      icon: <ArrowRight className="h-6 w-6" />,
      description: "Ardışıklığı nedensellik olarak görme",
      example: "Limonata içtikten sonra başım ağrıdı, limonata baş ağrısına neden oluyor",
      color: "bg-green-50 border-green-200"
    },
    {
      name: "Kaygan Zemin",
      englishName: "Slippery Slope",
      icon: <TrendingDown className="h-6 w-6" />,
      description: "Küçük bir değişikliğin aşırı sonuçlara yol açacağını iddia etme",
      example: "Plastik poşetleri yasaklarsak, yakında her şeyi yasaklarız",
      color: "bg-blue-50 border-blue-200"
    },
    {
      name: "Çember İçi Akıl Yürütme",
      englishName: "Circular Reasoning",
      icon: <RotateCcw className="h-6 w-6" />,
      description: "Sonucu kanıt olarak kullanma",
      example: "Bu kitap en iyisidir çünkü en iyi kitaplar listesinde",
      color: "bg-purple-50 border-purple-200"
    },
    {
      name: "Kırmızı Ringa Balığı",
      englishName: "Red Herring",
      icon: <Zap className="h-6 w-6" />,
      description: "Dikkati asıl konudan uzaklaştırma",
      example: "İklim değişikliği önemli ama ekonomi daha önemli",
      color: "bg-pink-50 border-pink-200"
    }
  ]

  return (
    <section className="py-16 bg-white">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Yaygın Mantık Hataları
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            En sık karşılaşılan mantık hatalarını tanıyın ve eleştirel düşünme becerilerinizi geliştirin
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {fallacyTypes.map((fallacy, index) => (
            <Card key={index} className={`${fallacy.color} hover:shadow-lg transition-all duration-300 cursor-pointer group`}>
              <CardHeader className="pb-3">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-white rounded-lg shadow-sm group-hover:shadow-md transition-shadow">
                    {fallacy.icon}
                  </div>
                  <div>
                    <CardTitle className="text-lg text-gray-900">{fallacy.name}</CardTitle>
                    <p className="text-sm text-gray-600">{fallacy.englishName}</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 mb-4 text-sm leading-relaxed">
                  {fallacy.description}
                </p>
                
                <div className="bg-white/70 p-3 rounded-md mb-4">
                  <p className="text-xs font-medium text-gray-600 mb-1">Örnek:</p>
                  <p className="text-sm text-gray-700 italic">"{fallacy.example}"</p>
                </div>
                
                <div className="flex items-center justify-between">
                  <Badge variant="secondary" className="text-xs">
                    Yaygın
                  </Badge>
                  <div className="flex items-center text-blue-600 text-sm font-medium group-hover:text-blue-700">
                    <BookOpen className="h-4 w-4 mr-1" />
                    Detaylar
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="text-center mt-12">
          <p className="text-gray-600 mb-4">
            Daha fazla mantık hatası türü ve detaylı açıklamalar için
          </p>
          <Badge variant="outline" className="text-blue-600 border-blue-600">
            Tüm Mantık Hataları Rehberi
          </Badge>
        </div>
      </div>
    </section>
  )
}

export default FallacyCategories

