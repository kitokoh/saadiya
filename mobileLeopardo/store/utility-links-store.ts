import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { UtilityLink } from '@/types';
import { utilityLinks as mockLinks } from '@/mocks/utility-links';

interface UtilityLinksState {
  links: UtilityLink[];
  categories: string[];
  isLoading: boolean;
  lastUpdated: number | null;
  error: string | null;
  
  // Actions
  fetchLinks: () => Promise<void>;
  refreshLinks: () => Promise<void>;
  getLinksByCategory: (category: string) => UtilityLink[];
}

// Simulate API fetch with a delay
const fetchLinksFromAPI = async (): Promise<UtilityLink[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(mockLinks);
    }, 800);
  });
};

// Extract unique categories from links
const getUniqueCategories = (links: UtilityLink[]): string[] => {
  const categories = links.map(link => link.category);
  return [...new Set(categories)];
};

export const useUtilityLinksStore = create<UtilityLinksState>()(
  persist(
    (set, get) => ({
      links: [],
      categories: [],
      isLoading: false,
      lastUpdated: null,
      error: null,
      
      fetchLinks: async () => {
        // Skip if we already have links and they were updated recently (within 1 hour)
        const lastUpdated = get().lastUpdated;
        const oneHourAgo = Date.now() - 3600000;
        
        if (get().links.length > 0 && lastUpdated && lastUpdated > oneHourAgo) {
          return;
        }
        
        set({ isLoading: true, error: null });
        
        try {
          const links = await fetchLinksFromAPI();
          const categories = getUniqueCategories(links);
          
          set({
            links,
            categories,
            isLoading: false,
            lastUpdated: Date.now(),
          });
        } catch (error) {
          set({
            isLoading: false,
            error: 'Failed to fetch utility links',
          });
        }
      },
      
      refreshLinks: async () => {
        set({ isLoading: true, error: null });
        
        try {
          const links = await fetchLinksFromAPI();
          const categories = getUniqueCategories(links);
          
          set({
            links,
            categories,
            isLoading: false,
            lastUpdated: Date.now(),
          });
        } catch (error) {
          set({
            isLoading: false,
            error: 'Failed to refresh utility links',
          });
        }
      },
      
      getLinksByCategory: (category) => {
        return get().links.filter(link => link.category === category);
      },
    }),
    {
      name: 'leopardo-utility-links-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);