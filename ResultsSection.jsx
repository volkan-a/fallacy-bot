import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { AlertTriangle, Info, CheckCircle, ExternalLink } from 'lucide-react'

const ResultsSection = ({ results, isVisible }) => {
  if (!isVisible || !results) return null

  const getFallacyIcon = (severity) => {
    switch (severity) {
      case 'high':
        return <AlertTriangle className="h-5 w-5 text-red-500" />
      case 'medium':
        return <Info className="h-5 w-5 text-yellow-500" />
      case 'low':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      default:
        return <Info className="h-5 w-5 text-blue-500" />
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 text-red-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'low':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-blue-100 text-blue-800'
    }
  }

  return (
    <section className="py-12 bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Analiz Sonuçları</h2>
          <p className="text-gray-600">
            Metninizde tespit edilen mantık hataları ve açıklamaları
          </p>
        </div>

        {results.fallacies && results.fallacies.length > 0 ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {results.fallacies.map((fallacy, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-2">
                      {getFallacyIcon(fallacy.severity)}
                      <CardTitle className="text-lg">{fallacy.name}</CardTitle>
                    </div>
                    <Badge className={getSeverityColor(fallacy.severity)}>
                      {fallacy.severity === 'high' ? 'Yüksek' : 
                       fallacy.severity === 'medium' ? 'Orta' : 'Düşük'}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 mb-4 text-sm leading-relaxed">
                    {fallacy.description}
                  </p>
                  
                  {fallacy.example && (
                    <div className="bg-gray-100 p-3 rounded-md mb-4">
                      <p className="text-sm font-medium text-gray-700 mb-1">Metninizden örnek:</p>
                      <p className="text-sm text-gray-600 italic">"{fallacy.example}"</p>
                    </div>
                  )}
                  
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-gray-500">
                      Güven: %{fallacy.confidence || 85}
                    </span>
                    <Button variant="outline" size="sm">
                      <ExternalLink className="h-3 w-3 mr-1" />
                      Detay
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="max-w-2xl mx-auto text-center">
            <CardContent className="py-12">
              <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Tebrikler! Mantık Hatası Bulunamadı
              </h3>
              <p className="text-gray-600">
                Analiz edilen metinde belirgin bir mantık hatası tespit edilmedi. 
                Metniniz mantıksal açıdan tutarlı görünüyor.
              </p>
            </CardContent>
          </Card>
        )}

        {/* Summary */}
        {results.summary && (
          <Card className="mt-8 max-w-4xl mx-auto">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Info className="h-5 w-5 mr-2" />
                Analiz Özeti
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 leading-relaxed">{results.summary}</p>
            </CardContent>
          </Card>
        )}
      </div>
    </section>
  )
}

export default ResultsSection

