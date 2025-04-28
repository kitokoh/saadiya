import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Linking } from 'react-native';
import { ExternalLink } from 'lucide-react-native';
import Colors from '@/constants/colors';
import { UtilityLink } from '@/types';

interface UtilityLinkItemProps {
  link: UtilityLink;
}

export default function UtilityLinkItem({ link }: UtilityLinkItemProps) {
  const handlePress = async () => {
    const supported = await Linking.canOpenURL(link.url);
    
    if (supported) {
      await Linking.openURL(link.url);
    } else {
      console.error(`Cannot open URL: ${link.url}`);
    }
  };
  
  return (
    <TouchableOpacity
      style={styles.container}
      onPress={handlePress}
      activeOpacity={0.7}
    >
      <View style={styles.content}>
        <Text style={styles.title}>{link.title}</Text>
        <Text style={styles.description}>{link.description}</Text>
      </View>
      <ExternalLink size={20} color={Colors.primary} />
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    backgroundColor: Colors.background,
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  content: {
    flex: 1,
    marginRight: 12,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.text,
    marginBottom: 4,
  },
  description: {
    fontSize: 14,
    color: Colors.secondaryText,
  },
});