import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent } from '@/components/ui/card'
import { Brain, Search, Lightbulb } from 'lucide-react'

const HeroSection = ({ onAnalyze }) => {
  const [text, setText] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const handleAnalyze = async () => {
    if (!text.trim()) return
    
    setIsAnalyzing(true)
    try {
      // Call the backend API
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text.trim() })
      })
      
      if (!response.ok) {
        throw new Error('Analysis failed')
      }
      
      const result = await response.json()
      await onAnalyze(result)
    } catch (error) {
      console.error('Analysis error:', error)
      // Fallback to mock data if API fails
      const mockResults = {
        fallacies: [
          {
            name: "API Bağlantı Hatası",
            description: "Backend API'ye bağlanırken bir hata oluştu. Lütfen daha sonra tekrar deneyin.",
            example: "Bağlantı hatası",
            severity: "high",
            confidence: 100
          }
        ],
        summary: "API bağlantısında sorun yaşandı. Demo veriler gösteriliyor."
      }
      await onAnalyze(mockResults)
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Metninizi Analiz Edin,{' '}
            <span className="text-blue-600">Mantık Hatalarını</span> Keşfedin
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            AI destekli sistemimiz ile metinlerdeki mantık hatalarını tespit edin, 
            eleştirel düşünme becerilerinizi geliştirin ve daha güçlü argümanlar oluşturun.
          </p>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <Card className="text-center">
            <CardContent className="pt-6">
              <Brain className="h-12 w-12 text-blue-600 mx-auto mb-4" />
              <h3 className="font-semibold text-lg mb-2">AI Destekli Analiz</h3>
              <p className="text-gray-600 text-sm">
                Gelişmiş yapay zeka ile metinlerdeki mantık hatalarını otomatik tespit
              </p>
            </CardContent>
          </Card>
          
          <Card className="text-center">
            <CardContent className="pt-6">
              <Search className="h-12 w-12 text-blue-600 mx-auto mb-4" />
              <h3 className="font-semibold text-lg mb-2">Detaylı Açıklamalar</h3>
              <p className="text-gray-600 text-sm">
                Her mantık hatası için örnekler ve açıklamalar ile öğrenin
              </p>
            </CardContent>
          </Card>
          
          <Card className="text-center">
            <CardContent className="pt-6">
              <Lightbulb className="h-12 w-12 text-blue-600 mx-auto mb-4" />
              <h3 className="font-semibold text-lg mb-2">Eleştirel Düşünme</h3>
              <p className="text-gray-600 text-sm">
                Mantık hatalarını tanıyarak eleştirel düşünme becerinizi geliştirin
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Text Analysis Section */}
        <Card className="max-w-3xl mx-auto">
          <CardContent className="p-6">
            <div className="space-y-4">
              <div>
                <label htmlFor="text-input" className="block text-sm font-medium text-gray-700 mb-2">
                  Analiz edilecek metni girin:
                </label>
                <Textarea
                  id="text-input"
                  placeholder="Buraya analiz etmek istediğiniz metni yazın... (makale, konuşma metni, sosyal medya gönderisi vb.)"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  className="min-h-[150px] resize-none"
                />
              </div>
              
              <div className="flex justify-center">
                <Button 
                  onClick={handleAnalyze}
                  disabled={!text.trim() || isAnalyzing}
                  size="lg"
                  className="px-8"
                >
                  {isAnalyzing ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Analiz Ediliyor...
                    </>
                  ) : (
                    'Analiz Et'
                  )}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </section>
  )
}

export default HeroSection

