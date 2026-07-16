import React, { useState, useContext } from 'react';
import { Search, RotateCcw } from 'lucide-react';
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
    setError('');
  };

  return (
    <div className="max-w-5xl mx-auto animate-fade-in-up">
      {/* Header */}
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
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">

          {/* ── Left: Image Preview ── */}
          <div className="glass-card overflow-hidden p-3">
            <div className="relative w-full rounded-xl overflow-hidden bg-slate-900 border border-slate-700/50" style={{ aspectRatio: '1/1' }}>
              <img
                src={preview}
                alt="Leaf preview"
                className="w-full h-full object-cover"
              />

              {/* Scanner overlay while loading */}
              {loading && (
                <>
                  <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" />
                  <div
                    className="absolute top-0 left-0 w-full h-1 bg-green-400 z-20"
                    style={{
                      boxShadow: '0 0 15px #4ade80',
                      animation: 'scan 2s linear infinite',
                    }}
                  />
                  <div className="absolute inset-0 flex flex-col items-center justify-center z-30">
                    <div className="spinner mb-4 border-t-green-400 w-12 h-12" />
                    <div className="text-green-400 font-bold tracking-widest uppercase text-sm animate-pulse">
                      {t('detection.analyzing')}
                    </div>
                  </div>
                </>
              )}

              {/* Confidence badge after result */}
              {!loading && result && (
                <div className="absolute bottom-3 left-3 right-3 bg-slate-900/85 backdrop-blur-md border border-slate-700 rounded-lg px-4 py-2 flex justify-between items-center">
                  <span className="text-sm font-semibold text-slate-300">Confidence</span>
                  <span className="text-green-400 font-bold text-lg">
                    {(result.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              )}
            </div>

            {/* Action buttons below image */}
            {!result && !loading && (
              <div className="mt-4 flex gap-3">
                <button onClick={reset} className="btn-secondary flex-1 py-3">
                  {t('common.cancel')}
                </button>
                <button onClick={handleAnalyze} className="btn-primary flex-1 justify-center py-3">
                  <Search size={18} />
                  {t('detection.analyze_btn')}
                </button>
              </div>
            )}

            {result && (
              <div className="mt-4">
                <button onClick={reset} className="btn-secondary w-full py-3 flex items-center justify-center gap-2">
                  <RotateCcw size={16} />
                  Analyze Another Image
                </button>
              </div>
            )}
          </div>

          {/* ── Right: Results Panel ── */}
          <div className="flex flex-col gap-4">
            {/* Error */}
            {error && (
              <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 shadow-lg">
                {error}
              </div>
            )}

            {/* Idle state */}
            {!result && !loading && !error && (
              <div className="glass-card p-8 flex flex-col justify-center min-h-[300px]">
                <div className="w-16 h-16 rounded-2xl bg-green-500/10 border border-green-500/20 flex items-center justify-center mb-6">
                  <Search size={28} className="text-green-400" />
                </div>
                <h3 className="text-xl font-bold mb-3">Ready to Analyze</h3>
                <p className="text-slate-400 leading-relaxed">
                  Our AI model will process this image to identify diseases, assess severity, and provide detailed treatment recommendations.
                </p>
              </div>
            )}

            {/* Loading state */}
            {loading && (
              <div className="glass-card p-8 flex flex-col items-center justify-center min-h-[300px]">
                <div className="spinner border-t-green-400 w-14 h-14 mb-6" />
                <p className="text-green-400 font-bold tracking-widest uppercase text-sm animate-pulse">
                  {t('detection.analyzing')}
                </p>
                <p className="text-slate-500 text-sm mt-2">Running AI inference...</p>
              </div>
            )}

            {/* Results */}
            {result && !loading && (
              <div className="animate-fade-in-up">
                <div className="glass-card shadow-2xl shadow-green-500/5">
                  <PredictionCard result={result} />
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
