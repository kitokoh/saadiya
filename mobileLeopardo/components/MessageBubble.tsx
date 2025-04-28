import React from 'react';
import { View, Text, StyleSheet, Dimensions, TouchableOpacity } from 'react-native';
import { Image } from 'expo-image';
import { Check, CheckCheck, Play } from 'lucide-react-native';
import Colors from '@/constants/colors';
import { Message } from '@/types';

interface MessageBubbleProps {
  message: Message;
  onMediaPress?: (mediaIndex: number) => void;
}

const { width } = Dimensions.get('window');
const MAX_BUBBLE_WIDTH = width * 0.75;

export default function MessageBubble({ message, onMediaPress }: MessageBubbleProps) {
  const formattedTime = new Date(message.timestamp).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });
  
  return (
    <View style={[
      styles.container,
      message.isReceived ? styles.receivedContainer : styles.sentContainer
    ]}>
      <View style={[
        styles.bubble,
        message.isReceived ? styles.receivedBubble : styles.sentBubble
      ]}>
        {message.media && message.media.length > 0 && (
          <View style={styles.mediaContainer}>
            {message.media.map((media, index) => (
              <TouchableOpacity 
                key={media.id} 
                style={styles.mediaItem}
                onPress={() => onMediaPress && onMediaPress(index)}
              >
                {media.type === 'image' ? (
                  <Image 
                    source={{ uri: media.uri }} 
                    style={styles.mediaImage}
                    contentFit="cover"
                  />
                ) : (
                  <View style={styles.videoContainer}>
                    <Image 
                      source={{ uri: media.uri }} 
                      style={styles.mediaImage}
                      contentFit="cover"
                    />
                    <View style={styles.playButton}>
                      <Play size={24} color="#FFFFFF" />
                    </View>
                  </View>
                )}
                <Text style={styles.mediaDescription} numberOfLines={1}>
                  {media.description}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        )}
        
        {message.text ? (
          <Text style={styles.messageText}>{message.text}</Text>
        ) : null}
        
        <View style={styles.timeContainer}>
          <Text style={styles.timeText}>{formattedTime}</Text>
          {!message.isReceived && (
            <View style={styles.statusIcon}>
              <CheckCheck size={14} color={Colors.secondaryText} />
            </View>
          )}
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 2,
    paddingHorizontal: 10,
    width: '100%',
  },
  sentContainer: {
    alignItems: 'flex-end',
  },
  receivedContainer: {
    alignItems: 'flex-start',
  },
  bubble: {
    maxWidth: MAX_BUBBLE_WIDTH,
    borderRadius: 12,
    paddingHorizontal: 12,
    paddingTop: 8,
    paddingBottom: 6,
  },
  sentBubble: {
    backgroundColor: Colors.chatBubble.sent,
    borderTopRightRadius: 2,
  },
  receivedBubble: {
    backgroundColor: Colors.chatBubble.received,
    borderTopLeftRadius: 2,
  },
  messageText: {
    fontSize: 16,
    color: Colors.text,
    marginBottom: 4,
  },
  timeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-end',
    marginTop: 2,
  },
  timeText: {
    fontSize: 11,
    color: Colors.secondaryText,
    marginRight: 2,
  },
  statusIcon: {
    marginLeft: 2,
  },
  mediaContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 6,
  },
  mediaItem: {
    width: '100%',
    marginBottom: 4,
    borderRadius: 8,
    overflow: 'hidden',
  },
  mediaImage: {
    width: '100%',
    height: 180,
    borderRadius: 8,
  },
  mediaDescription: {
    fontSize: 14,
    color: Colors.text,
    marginTop: 4,
  },
  videoContainer: {
    position: 'relative',
  },
  playButton: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: [{ translateX: -20 }, { translateY: -20 }],
    backgroundColor: 'rgba(0,0,0,0.5)',
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
});