import React, { useState, useRef } from 'react';
import { 
  View, 
  TextInput, 
  StyleSheet, 
  TouchableOpacity, 
  Keyboard,
  Platform,
  Animated,
} from 'react-native';
import { 
  Mic, 
  Camera, 
  Image as ImageIcon, 
  Send, 
  Plus, 
  X 
} from 'lucide-react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Haptics from 'expo-haptics';
import Colors from '@/constants/colors';
import { MediaItem, MediaCategory } from '@/types';

interface ChatInputProps {
  onSendMessage: (text: string, media?: MediaItem[]) => void;
  getDefaultDescription: (type: 'image' | 'video', category: MediaCategory) => string;
}

export default function ChatInput({ onSendMessage, getDefaultDescription }: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);
  const [selectedMedia, setSelectedMedia] = useState<MediaItem[]>([]);
  const expandAnimation = useRef(new Animated.Value(0)).current;
  
  const toggleExpand = () => {
    if (Platform.OS !== 'web') {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
    
    const toValue = isExpanded ? 0 : 1;
    
    Animated.spring(expandAnimation, {
      toValue,
      friction: 7,
      tension: 40,
      useNativeDriver: false,
    }).start();
    
    setIsExpanded(!isExpanded);
  };
  
  const expandedHeight = expandAnimation.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 100],
  });
  
  const handleSend = () => {
    if (message.trim() || selectedMedia.length > 0) {
      onSendMessage(message, selectedMedia.length > 0 ? selectedMedia : undefined);
      setMessage('');
      setSelectedMedia([]);
    }
  };
  
  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      allowsEditing: true,
      quality: 1,
    });
    
    if (!result.canceled && result.assets && result.assets.length > 0) {
      const asset = result.assets[0];
      const isVideo = asset.uri.endsWith('.mp4') || asset.uri.endsWith('.mov') || asset.type === 'video';
      
      const newMedia: MediaItem = {
        id: Date.now().toString(),
        type: isVideo ? 'video' : 'image',
        uri: asset.uri,
        description: message.trim() || getDefaultDescription(isVideo ? 'video' : 'image', 'personal'),
        category: 'personal',
        timestamp: Date.now(),
        sent: false,
      };
      
      setSelectedMedia([...selectedMedia, newMedia]);
      if (Platform.OS !== 'web') {
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      }
    }
  };
  
  const takePhoto = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    
    if (status === 'granted') {
      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.All,
        allowsEditing: true,
        quality: 1,
      });
      
      if (!result.canceled && result.assets && result.assets.length > 0) {
        const asset = result.assets[0];
        const isVideo = asset.uri.endsWith('.mp4') || asset.uri.endsWith('.mov') || asset.type === 'video';
        
        const newMedia: MediaItem = {
          id: Date.now().toString(),
          type: isVideo ? 'video' : 'image',
          uri: asset.uri,
          description: message.trim() || getDefaultDescription(isVideo ? 'video' : 'image', 'personal'),
          category: 'personal',
          timestamp: Date.now(),
          sent: false,
        };
        
        setSelectedMedia([...selectedMedia, newMedia]);
        if (Platform.OS !== 'web') {
          Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
        }
      }
    }
  };
  
  const removeMedia = (id: string) => {
    setSelectedMedia(selectedMedia.filter(media => media.id !== id));
  };
  
  return (
    <View style={styles.container}>
      {selectedMedia.length > 0 && (
        <View style={styles.selectedMediaContainer}>
          {selectedMedia.map(media => (
            <View key={media.id} style={styles.selectedMediaItem}>
              <TouchableOpacity 
                style={styles.removeMediaButton}
                onPress={() => removeMedia(media.id)}
              >
                <X size={16} color="#FFFFFF" />
              </TouchableOpacity>
              {media.type === 'image' ? (
                <ImageIcon size={24} color={Colors.primary} />
              ) : (
                <Camera size={24} color={Colors.primary} />
              )}
            </View>
          ))}
        </View>
      )}
      
      <Animated.View style={[styles.expandedContainer, { height: expandedHeight }]}>
        <TouchableOpacity style={styles.expandedButton} onPress={pickImage}>
          <ImageIcon size={24} color={Colors.primary} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.expandedButton} onPress={takePhoto}>
          <Camera size={24} color={Colors.primary} />
        </TouchableOpacity>
      </Animated.View>
      
      <View style={styles.inputContainer}>
        <TouchableOpacity style={styles.iconButton} onPress={toggleExpand}>
          {isExpanded ? (
            <X size={24} color={Colors.primary} />
          ) : (
            <Plus size={24} color={Colors.primary} />
          )}
        </TouchableOpacity>
        
        <TextInput
          style={styles.input}
          placeholder="Type a message"
          value={message}
          onChangeText={setMessage}
          multiline
        />
        
        {message.trim() || selectedMedia.length > 0 ? (
          <TouchableOpacity style={styles.sendButton} onPress={handleSend}>
            <Send size={24} color="#FFFFFF" />
          </TouchableOpacity>
        ) : (
          <TouchableOpacity style={styles.iconButton}>
            <Mic size={24} color={Colors.primary} />
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    borderTopWidth: 1,
    borderTopColor: Colors.separator,
    backgroundColor: Colors.background,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 8,
    paddingVertical: 8,
  },
  iconButton: {
    padding: 8,
  },
  input: {
    flex: 1,
    backgroundColor: '#F0F2F5',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 8,
    maxHeight: 100,
    fontSize: 16,
  },
  sendButton: {
    backgroundColor: Colors.primary,
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 8,
  },
  expandedContainer: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    overflow: 'hidden',
  },
  expandedButton: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#F0F2F5',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
    marginVertical: 16,
  },
  selectedMediaContainer: {
    flexDirection: 'row',
    padding: 8,
    flexWrap: 'wrap',
  },
  selectedMediaItem: {
    width: 60,
    height: 60,
    borderRadius: 8,
    backgroundColor: '#F0F2F5',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
    marginBottom: 8,
    position: 'relative',
  },
  removeMediaButton: {
    position: 'absolute',
    top: -5,
    right: -5,
    backgroundColor: Colors.primary,
    width: 20,
    height: 20,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1,
  },
});