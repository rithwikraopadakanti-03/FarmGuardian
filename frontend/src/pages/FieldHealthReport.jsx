import React, { useState, useContext } from 'react';
import { FileText, Download, X } from 'lucide-react';
import UploadCard from '../components/UploadCard';
import HealthScoreCard from '../components/HealthScoreCard';
import { reportAPI } from '../services/api';
import { LanguageContext } from '../context/LanguageContext';

const FieldHealthReport = () => {
  const [files, setFiles] = useState([]);
  const [previews, setPreviews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState('');
  
  const { t, language } = useContext(LanguageContext);
  const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const handleFileUpload = (uploadedFiles) => {
    const newFiles = [...files, ...uploadedFiles];
    // Limit to 10 files for demo
    if (newFiles.length > 10) {
      setError('Maximum 10 images allowed per report');
      return;
    }
    setFiles(newFiles);
    
    const newPreviews = uploadedFiles.map(f => URL.createObjectURL(f));
    setPreviews([...previews, ...newPreviews]);
  };

  const removeFile = (index) => {
    const newFiles = files.filter((_, i) => i !== index);
    const newPreviews = previews.filter((_, i) => i !== index);
    setFiles(newFiles);
    setPreviews(newPreviews);
  };

  const handleGenerate = async () => {
    if (files.length === 0) return;
    
    setLoading(true);
    setError('');
    
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });
    formData.append('language', language);
    
    try {
      const response = await reportAPI.generateFieldReport(formData);
      setReport(response.data);
    } catch (err) {
      console.error(err);
      setError(t('common.error') + ': Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-fade-in-up">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold font-heading mb-2">{t('report.title')}</h1>
        <p className="text-slate-400">{t('report.subtitle')}</p>
      </div>

      {!report && (
        <div className="space-y-6">
          <UploadCard 
            onFileUpload={handleFileUpload} 
            isMultiple={true}
            title={t('report.upload_multiple')}
            subtitle="Upload up to 10 images from across your field"
          />
          
          {error && <div className="text-red-400 text-center">{error}</div>}
          
          {files.length > 0 && (
            <div className="glass-card p-6">
              <h3 className="font-semibold mb-4">Selected Images ({files.length})</h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4 mb-6">
                {previews.map((preview, idx) => (
                  <div key={idx} className="relative aspect-square rounded-xl overflow-hidden group">
                    <img src={preview} alt="preview" className="w-full h-full object-cover" />
                    <button 
                      onClick={() => removeFile(idx)}
                      className="absolute top-2 right-2 bg-red-500/80 p-1 rounded-full text-white opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <X size={14} />
                    </button>
                  </div>
                ))}
              </div>
              
              <button 
                onClick={handleGenerate} 
                disabled={loading}
                className="btn-primary w-full justify-center"
              >
                {loading ? (
                  <div className="flex items-center gap-2">
                    <div className="spinner w-5 h-5 border-2"></div>
                    {t('report.generating')}
                  </div>
                ) : (
                  <>
                    <FileText size={18} />
                    {t('report.generate_btn')}
                  </>
                )}
              </button>
            </div>
          )}
        </div>
      )}

      {report && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-1 space-y-6">
            <HealthScoreCard score={report.health_score} />
            
            <a 
              href={`${API_BASE}${report.pdf_url}`} 
              download
              target="_blank"
              rel="noreferrer"
              className="btn-primary w-full justify-center text-center"
            >
              <Download size={18} /> {t('report.export_pdf')}
            </a>
            
            <button 
              onClick={() => { setReport(null); setFiles([]); setPreviews([]); }} 
              className="btn-secondary w-full"
            >
              Start New Report
            </button>
          </div>
          
          <div className="md:col-span-2 space-y-6">
            <div className="glass-card p-6">
              <h3 className="text-xl font-bold font-heading mb-4">{t('report.diseases_found')}</h3>
              <div className="space-y-3">
                {Object.entries(report.disease_distribution).map(([disease, count]) => (
                  <div key={disease} className="flex justify-between items-center p-3 glass rounded-lg">
                    <span className="font-medium">{disease.replace(/_/g, ' ')}</span>
                    <span className="bg-slate-800 px-3 py-1 rounded-full text-sm">{count} images</span>
                  </div>
                ))}
              </div>
            </div>
            
            {report.recommendations?.immediate_actions?.length > 0 && (
              <div className="glass-card p-6 border-red-500/30">
                <h3 className="text-xl font-bold font-heading text-red-400 mb-4">{t('report.priority_actions')}</h3>
                <ul className="list-disc list-inside text-slate-300 space-y-2">
                  {report.recommendations.immediate_actions.map((act, i) => (
                    <li key={i}>{act}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default FieldHealthReport;
