import { useState } from 'react'
import Header from './components/Header'
import HeroSection from './components/HeroSection'
import ResultsSection from './components/ResultsSection'
import FallacyCategories from './components/FallacyCategories'
import Footer from './components/Footer'
import './App.css'

function App() {
  const [analysisResults, setAnalysisResults] = useState(null)
  const [showResults, setShowResults] = useState(false)

  // Handle analysis results from backend
  const handleAnalyze = async (result) => {
    setAnalysisResults(result)
    setShowResults(true)
  }

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <HeroSection onAnalyze={handleAnalyze} />
      <ResultsSection results={analysisResults} isVisible={showResults} />
      <FallacyCategories />
      <Footer />
    </div>
  )
}

export default App
