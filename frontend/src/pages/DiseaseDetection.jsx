import React, { useState, useContext, useRef } from 'react';
import { Camera, Image as ImageIcon, Search } from 'lucide-react';
import UploadCard from '../components/UploadCard';
import PredictionCard from '../components/PredictionCard';
import { predictAPI } from '../services/api';
import { LanguageContext } from '../context/LanguageContext';

const DiseaseDetection = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  
  const { t, language } = useContext(LanguageContext);

  const handleFileUpload = (uploadedFile) => {
    setFile(uploadedFile);
    setPreview(URL.createObjectURL(uploadedFile));
    setResult(null);
    setError('');
  };

  const handleAnalyze = async () => {
    if (!file) return;
    
    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language);
    
    try {
      const response = await predictAPI.predictDisease(formData);
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError(t('common.error') + ': Failed to analyze image');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in-up">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold font-heading mb-2">{t('detection.title')}</h1>
        <p className="text-slate-400">{t('detection.subtitle')}</p>
      </div>

      {!file ? (
        <UploadCard 
          onFileUpload={handleFileUpload} 
          title={t('detection.upload_title')}
          subtitle={t('detection.upload_desc')}
        />
      ) : (
        <div className="flex flex-col lg:flex-row gap-6 relative">
          {/* Image Preview Side */}
          <div className="w-full lg:w-5/12 z-10">
            <div className="glass-card overflow-hidden p-2 sticky top-24">
              <div className="relative aspect-square w-full rounded-xl overflow-hidden bg-slate-900 border border-slate-700/50">
                <img 
                  src={preview} 
                  alt="Leaf preview" 
                  className="w-full h-full object-cover transition-transform duration-700 hover:scale-105"
                />
                
                {/* Animated Scanner Bar for Loading */}
                {loading && (
                  <>
                    <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm transition-all duration-300"></div>
                    <div className="absolute top-0 left-0 w-full h-1 bg-green-400 shadow-[0_0_15px_#4ade80] animate-[float_2s_ease-in-out_infinite] z-20" style={{animation: 'scan 2s linear infinite'}}></div>
                    <div className="absolute inset-0 flex flex-col items-center justify-center z-30">
                      <div className="spinner mb-4 border-t-green-400 w-12 h-12"></div>
                      <div className="text-green-400 font-bold tracking-widest uppercase text-sm animate-pulse">{t('detection.analyzing')}</div>
                    </div>
                  </>
                )}
                
                {!loading && result && (
                  <div className="absolute bottom-4 left-4 right-4 bg-slate-900/80 backdrop-blur-md border border-slate-700 rounded-lg p-3 flex justify-between items-center shadow-xl">
                    <span className="text-sm font-semibold text-slate-300">Confidence</span>
                    <span className="text-green-400 font-bold">{(result.confidence * 100).toFixed(1)}%</span>
                  </div>
                )}
              </div>
            </div>
          </div>
          
          {/* Results Side (Overlapping Desktop Layout) */}
          <div className="w-full lg:w-7/12 relative lg:-ml-12 lg:mt-8 z-20">
            {!result && !loading && (
              <div className="glass-card p-8 flex flex-col justify-center h-full min-h-[300px]">
                <h3 className="text-xl font-bold mb-6">Ready to Analyze</h3>
                <p className="text-slate-400 mb-8">Our AI model will process this image to identify diseases, assess severity, and provide treatment recommendations.</p>
                <div className="flex gap-4">
                  <button onClick={reset} className="btn-secondary flex-1 py-3">{t('common.cancel')}</button>
                  <button onClick={handleAnalyze} className="btn-primary flex-1 justify-center py-3">
                    <Search size={20} /> {t('detection.analyze_btn')}
                  </button>
                </div>
              </div>
            )}
            
            {error && (
              <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 mb-6 shadow-lg backdrop-blur-md">
                {error}
              </div>
            )}
            
            {result && (
              <div className="animate-fade-in-right">
                <div className="glass-card shadow-2xl shadow-green-500/5">
                  <PredictionCard result={result} />
                </div>
                
                <div className="mt-6 flex justify-end">
                  <button onClick={reset} className="btn-secondary px-6">
                    Analyze Another Image
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default DiseaseDetection;
