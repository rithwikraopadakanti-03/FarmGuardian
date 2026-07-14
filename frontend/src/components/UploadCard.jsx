import React from 'react';
import { UploadCloud, Camera } from 'lucide-react';

const UploadCard = ({ onFileUpload, isMultiple = false, title, subtitle }) => {
  const fileInputRef = React.useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    e.currentTarget.classList.add('drag-over');
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove('drag-over');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove('drag-over');
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      if (isMultiple) {
        onFileUpload(Array.from(e.dataTransfer.files));
      } else {
        onFileUpload(e.dataTransfer.files[0]);
      }
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      if (isMultiple) {
        onFileUpload(Array.from(e.target.files));
      } else {
        onFileUpload(e.target.files[0]);
      }
    }
  };

  return (
    <div className="glass-card p-1 relative overflow-hidden">
      {/* Decorative overlapping elements */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-green-500/10 rounded-full blur-2xl -mr-10 -mt-10"></div>
      <div className="absolute bottom-0 left-0 w-32 h-32 bg-blue-500/10 rounded-full blur-2xl -ml-10 -mb-10"></div>
      
      <div className="relative z-10 bg-slate-900/60 p-8 sm:p-12 rounded-2xl border border-slate-700/50 backdrop-blur-xl">
        <div className="text-center mb-8">
          <h3 className="text-2xl font-bold font-heading mb-2 text-white">{title}</h3>
          <p className="text-slate-400">{subtitle}</p>
        </div>

        <div 
          className="upload-zone group relative overflow-hidden bg-slate-800/30 border-2 border-dashed border-slate-600 hover:border-green-500/50 rounded-2xl p-10 flex flex-col items-center justify-center cursor-pointer transition-all duration-300"
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          {/* Animated glow on hover */}
          <div className="absolute inset-0 bg-gradient-to-b from-green-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          
          <div className="relative z-10 w-20 h-20 rounded-full bg-slate-900/80 border border-slate-700 flex items-center justify-center text-green-400 mb-6 group-hover:scale-110 group-hover:shadow-[0_0_30px_rgba(34,197,94,0.2)] transition-all duration-300">
            <UploadCloud size={36} />
          </div>
          <p className="relative z-10 text-lg font-medium text-slate-200 mb-2 group-hover:text-white transition-colors">
            Click or drag & drop to upload
          </p>
          <p className="relative z-10 text-sm text-slate-500">
            Supports JPG, PNG (Max 5MB)
          </p>
          <input 
            type="file" 
            className="hidden" 
            ref={fileInputRef} 
            onChange={handleFileChange}
            accept="image/jpeg, image/png"
            multiple={isMultiple}
          />
        </div>

        {!isMultiple && (
          <div className="mt-8 flex flex-col items-center">
            <div className="flex items-center gap-4 w-full max-w-xs mb-6">
              <div className="h-px bg-slate-700 flex-1"></div>
              <span className="text-slate-500 text-xs font-semibold uppercase tracking-wider">OR</span>
              <div className="h-px bg-slate-700 flex-1"></div>
            </div>
            <button className="w-full max-w-xs btn-secondary flex justify-center py-3">
              <Camera size={18} />
              <span>Use Mobile Camera</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadCard;
