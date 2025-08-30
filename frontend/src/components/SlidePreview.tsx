'use client';

import { useState } from 'react';
import { Eye, EyeOff, ExternalLink } from 'lucide-react';

interface SlidePreviewProps {
  slidesHtml: string;
  showPreview: boolean;
  onTogglePreview: () => void;
}

export default function SlidePreview({
  slidesHtml,
  showPreview,
  onTogglePreview,
}: SlidePreviewProps) {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const openInNewTab = () => {
    if (typeof window === 'undefined') return;
    
    const blob = new Blob([slidesHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    window.open(url, '_blank');

    // Clean up the URL after a delay
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };

  return (
    <div className="mt-4">
      <div className="flex items-center justify-between mb-3">
        <button
          onClick={onTogglePreview}
          className="flex items-center gap-2 text-sm font-medium text-gray-200 hover:text-white"
        >
          {showPreview ? <EyeOff size={16} /> : <Eye size={16} />}
          {showPreview ? 'Hide Preview' : 'Show Preview'}
        </button>

        <button
          onClick={openInNewTab}
          className="flex items-center gap-2 text-sm text-blue-400 hover:text-blue-300"
        >
          <ExternalLink size={14} />
          Open in New Tab
        </button>
      </div>

      {showPreview && (
        <div className="border border-gray-600 rounded-lg overflow-hidden">
          <iframe
            srcDoc={slidesHtml}
            className="w-full h-96 border-0"
            title="Slide Preview"
          />
        </div>
      )}
    </div>
  );
}
