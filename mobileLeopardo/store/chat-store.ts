import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Chat, Message, MediaItem, User, MediaCategory } from '@/types';
import { getLeopardo, users } from '@/mocks/users';

interface ChatState {
  chats: Chat[];
  activeChat: string | null;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setActiveChat: (chatId: string) => void;
  sendMessage: (chatId: string, text: string, media?: MediaItem[]) => void;
  receiveMessage: (chatId: string, text: string) => void;
  addChat: (user: User) => void;
  getChat: (chatId: string) => Chat | undefined;
  getDefaultDescriptionForMedia: (type: 'image' | 'video', category: MediaCategory) => string;
}

// Generate default descriptions based on media type and category
const getDefaultDescription = (type: 'image' | 'video', category: MediaCategory): string => {
  const descriptions = {
    image: {
      personal: "A personal photo I wanted to share",
      work: "Work-related image for your reference",
      family: "A family moment captured in this photo",
      travel: "A beautiful scene from my travels",
      other: "An image I thought you might find interesting"
    },
    video: {
      personal: "A personal video I wanted to share with you",
      work: "Work-related video for your reference",
      family: "A special family moment captured on video",
      travel: "Video footage from my recent travels",
      other: "A video I thought you might find interesting"
    }
  };
  
  return descriptions[type][category];
};

// Initialize with Leopardo chat
const initialChats: Chat[] = [
  {
    id: 'leopardo',
    user: getLeopardo(),
    messages: [
      {
        id: '1',
        text: "Hello! I'm Leopardo. Send me your media and I'll help you share it.",
        timestamp: Date.now() - 86400000, // 1 day ago
        isReceived: true,
      }
    ],
    unreadCount: 0,
    lastMessageTimestamp: Date.now() - 86400000,
  }
];

export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      chats: initialChats,
      activeChat: 'leopardo',
      isLoading: false,
      error: null,
      
      setActiveChat: (chatId) => set({ activeChat: chatId }),
      
      sendMessage: (chatId, text, media) => {
        const newMessage: Message = {
          id: Date.now().toString(),
          text,
          timestamp: Date.now(),
          isReceived: false,
          media,
        };
        
        set((state) => {
          const updatedChats = state.chats.map((chat) => {
            if (chat.id === chatId) {
              return {
                ...chat,
                messages: [...chat.messages, newMessage],
                lastMessageTimestamp: newMessage.timestamp,
              };
            }
            return chat;
          });
          
          return { chats: updatedChats };
        });
        
        // Auto-reply from Leopardo after a short delay
        if (chatId === 'leopardo') {
          setTimeout(() => {
            get().receiveMessage(chatId, media 
              ? "I've received your media. Thank you for sharing!"
              : "Message received. How can I help you today?");
          }, 1000);
        }
      },
      
      receiveMessage: (chatId, text) => {
        const newMessage: Message = {
          id: Date.now().toString(),
          text,
          timestamp: Date.now(),
          isReceived: true,
        };
        
        set((state) => {
          const updatedChats = state.chats.map((chat) => {
            if (chat.id === chatId) {
              return {
                ...chat,
                messages: [...chat.messages, newMessage],
                lastMessageTimestamp: newMessage.timestamp,
                unreadCount: state.activeChat === chatId ? 0 : chat.unreadCount + 1,
              };
            }
            return chat;
          });
          
          return { chats: updatedChats };
        });
      },
      
      addChat: (user) => {
        const chatExists = get().chats.some(chat => chat.id === user.id);
        
        if (!chatExists) {
          const newChat: Chat = {
            id: user.id,
            user,
            messages: [],
            unreadCount: 0,
            lastMessageTimestamp: Date.now(),
          };
          
          set((state) => ({
            chats: [...state.chats, newChat],
          }));
        }
        
        set({ activeChat: user.id });
      },
      
      getChat: (chatId) => {
        return get().chats.find(chat => chat.id === chatId);
      },
      
      getDefaultDescriptionForMedia: getDefaultDescription,
    }),
    {
      name: 'leopardo-chat-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);