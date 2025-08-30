'use client';

import { SlideTheme } from '@/types';
import { Palette, Loader2 } from 'lucide-react';

interface ThemeSelectorProps {
  themes: Record<string, SlideTheme>;
  selectedTheme: string;
  onThemeChange: (themeKey: string) => void;
  isLoading: boolean;
}

export default function ThemeSelector({
  themes,
  selectedTheme,
  onThemeChange,
  isLoading,
}: ThemeSelectorProps) {
  return (
    <div className="mb-4">
      <h3 className="text-sm font-medium text-gray-200 mb-2 flex items-center gap-2">
        <Palette size={16} className="text-purple-400" />
        Choose Theme
      </h3>

      <div className="grid grid-cols-1 gap-2">
        {Object.entries(themes).map(([key, theme]) => (
          <button
            key={key}
            onClick={() => onThemeChange(key)}
            disabled={isLoading}
            className={`p-3 rounded-lg border text-left transition-all ${
              selectedTheme === key
                ? 'border-blue-400 bg-gray-600'
                : 'border-gray-600 hover:border-gray-500 bg-gray-700'
            } ${isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:shadow-sm'}`}
          >
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-sm text-white">{theme.name}</div>
                <div className="text-xs text-gray-300 mt-1">{theme.description}</div>
              </div>

              <div className="flex items-center gap-2">
                {isLoading && selectedTheme === key && (
                  <Loader2 size={14} className="animate-spin text-blue-400" />
                )}
                <div className="flex gap-1">
                  <div
                    className="w-3 h-3 rounded-full border border-gray-500"
                    style={{ backgroundColor: theme.primary_color }}
                  />
                  <div
                    className="w-3 h-3 rounded-full border border-gray-500"
                    style={{ backgroundColor: theme.secondary_color }}
                  />
                </div>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
