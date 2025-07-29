import { Heart, Github, Twitter, Mail } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About */}
          <div className="col-span-1 md:col-span-2">
            <h3 className="text-lg font-semibold mb-4">Know Your Fallacy</h3>
            <p className="text-gray-300 mb-4 leading-relaxed">
              AI destekli mantık hatası tespit sistemi ile eleştirel düşünme becerilerinizi geliştirin. 
              Metinlerdeki mantık hatalarını tespit edin ve daha güçlü argümanlar oluşturun.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <Github className="h-5 w-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <Twitter className="h-5 w-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <Mail className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-md font-semibold mb-4">Hızlı Erişim</h4>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-gray-300 hover:text-white transition-colors">
                  Ana Sayfa
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-300 hover:text-white transition-colors">
                  Mantık Hataları
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-300 hover:text-white transition-colors">
                  Nasıl Çalışır?
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-300 hover:text-white transition-colors">
                  API Dokümantasyonu
                </a>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="text-md font-semibold mb-4">Kaynaklar</h4>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-gray-300 hover:text-white transition-colors">
                  Eleştirel Düşünme Rehberi
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-300 hover:text-white transition-colors">
                  Mantık Hataları Sözlüğü
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-300 hover:text-white transition-colors">
                  Örnekler ve Alıştırmalar
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-300 hover:text-white transition-colors">
                  Blog
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-gray-400 text-sm mb-4 md:mb-0">
              © 2024 Know Your Fallacy. Tüm hakları saklıdır.
            </div>
            <div className="flex items-center text-gray-400 text-sm">
              <span>Made with</span>
              <Heart className="h-4 w-4 mx-1 text-red-500" />
              <span>for critical thinking</span>
            </div>
          </div>
          
          <div className="flex flex-col md:flex-row justify-center items-center mt-4 space-y-2 md:space-y-0 md:space-x-6">
            <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors">
              Gizlilik Politikası
            </a>
            <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors">
              Kullanım Şartları
            </a>
            <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors">
              Çerez Politikası
            </a>
            <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors">
              İletişim
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer

