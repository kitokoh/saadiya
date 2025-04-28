import React, { useEffect, useState, useRef } from 'react';
import { 
  View, 
  StyleSheet, 
  FlatList, 
  KeyboardAvoidingView, 
  Platform,
  ActivityIndicator,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Stack, useRouter, useLocalSearchParams } from 'expo-router';
import { useChatStore } from '@/store/chat-store';
import ChatHeader from '@/components/ChatHeader';
import MessageBubble from '@/components/MessageBubble';
import ChatInput from '@/components/ChatInput';
import MediaPreview from '@/components/MediaPreview';
import { MediaItem } from '@/types';
import Colors from '@/constants/colors';

export default function ChatDetailScreen() {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const flatListRef = useRef<FlatList>(null);
  const [previewMedia, setPreviewMedia] = useState<MediaItem | null>(null);
  const [showPreview, setShowPreview] = useState(false);
  
  const { 
    sendMessage, 
    getChat,
    setActiveChat,
    getDefaultDescriptionForMedia
  } = useChatStore();
  
  const currentChat = id ? getChat(id) : null;
  
  useEffect(() => {
    if (id) {
      setActiveChat(id);
    }
  }, [id]);
  
  useEffect(() => {
    // Scroll to bottom when messages change
    if (currentChat?.messages.length && flatListRef.current) {
      setTimeout(() => {
        flatListRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }
  }, [currentChat?.messages.length]);
  
  const handleSendMessage = (text: string, media?: MediaItem[]) => {
    if (id) {
      sendMessage(id, text, media);
    }
  };
  
  const handleMediaPress = (messageIndex: number, mediaIndex: number) => {
    if (currentChat?.messages[messageIndex]?.media?.[mediaIndex]) {
      setPreviewMedia(currentChat.messages[messageIndex].media![mediaIndex]);
      setShowPreview(true);
    }
  };
  
  const handleUpdateMedia = (updatedMedia: MediaItem) => {
    setShowPreview(false);
    setPreviewMedia(null);
    // In a real app, you would update the media in the store
  };
  
  const handleBackPress = () => {
    router.back();
  };
  
  if (!currentChat) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={Colors.primary} />
      </View>
    );
  }
  
  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
    >
      <Stack.Screen
        options={{
          headerShown: false,
        }}
      />
      
      <ChatHeader 
        user={currentChat.user} 
        onBackPress={handleBackPress}
      />
      
      <FlatList
        ref={flatListRef}
        style={styles.messagesList}
        data={currentChat.messages}
        keyExtractor={(item) => item.id}
        renderItem={({ item, index }) => (
          <MessageBubble 
            message={item} 
            onMediaPress={
              item.media && item.media.length > 0
                ? (mediaIndex) => handleMediaPress(index, mediaIndex)
                : undefined
            }
          />
        )}
        contentContainerStyle={[
          styles.messagesContent,
          { paddingBottom: insets.bottom + 10 }
        ]}
      />
      
      <ChatInput 
        onSendMessage={handleSendMessage}
        getDefaultDescription={getDefaultDescriptionForMedia}
      />
      
      <MediaPreview
        visible={showPreview}
        media={previewMedia}
        onClose={() => setShowPreview(false)}
        onSave={handleUpdateMedia}
      />
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ECE5DD', // WhatsApp chat background
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Colors.background,
  },
  messagesList: {
    flex: 1,
  },
  messagesContent: {
    paddingVertical: 10,
  },
});