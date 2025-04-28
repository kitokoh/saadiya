export type User = {
    id: string;
    name: string;
    avatar: string;
    lastSeen?: string;
    isOnline?: boolean;
  };
  
  export type MediaType = 'image' | 'video';
  
  export type MediaCategory = 'personal' | 'work' | 'family' | 'travel' | 'other';
  
  export type MediaItem = {
    id: string;
    type: MediaType;
    uri: string;
    description: string;
    category: MediaCategory;
    timestamp: number;
    sent: boolean;
  };
  
  export type Message = {
    id: string;
    text: string;
    timestamp: number;
    isReceived: boolean;
    media?: MediaItem[];
  };
  
  export type Chat = {
    id: string;
    user: User;
    messages: Message[];
    unreadCount: number;
    lastMessageTimestamp: number;
  };
  
  export type UtilityLink = {
    id: string;
    title: string;
    url: string;
    description: string;
    icon: string;
    category: string;
  };