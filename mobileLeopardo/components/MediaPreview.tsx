import React from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  Modal, 
  TouchableOpacity, 
  Dimensions,
  TextInput,
  ScrollView,
  Platform,
} from 'react-native';
import { Image } from 'expo-image';
import { X, Check, Tag } from 'lucide-react-native';
import Colors from '@/constants/colors';
import { MediaItem, MediaCategory } from '@/types';

interface MediaPreviewProps {
  visible: boolean;
  media: MediaItem | null;
  onClose: () => void;
  onSave: (updatedMedia: MediaItem) => void;
}

const { width, height } = Dimensions.get('window');

const categories: MediaCategory[] = ['personal', 'work', 'family', 'travel', 'other'];

export default function MediaPreview({ visible, media, onClose, onSave }: MediaPreviewProps) {
  const [description, setDescription] = React.useState('');
  const [category, setCategory] = React.useState<MediaCategory>('personal');
  
  React.useEffect(() => {
    if (media) {
      setDescription(media.description);
      setCategory(media.category);
    }
  }, [media]);
  
  if (!media) return null;
  
  const handleSave = () => {
    onSave({
      ...media,
      description,
      category,
    });
  };
  
  return (
    <Modal
      visible={visible}
      animationType="slide"
      transparent={false}
      onRequestClose={onClose}
    >
      <View style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={onClose} style={styles.closeButton}>
            <X size={24} color={Colors.text} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>
            {media.type === 'image' ? 'Image Preview' : 'Video Preview'}
          </Text>
          <TouchableOpacity onPress={handleSave} style={styles.saveButton}>
            <Check size={24} color={Colors.primary} />
          </TouchableOpacity>
        </View>
        
        <ScrollView style={styles.content}>
          <View style={styles.mediaContainer}>
            <Image
              source={{ uri: media.uri }}
              style={styles.mediaImage}
              contentFit="contain"
            />
          </View>
          
          <View style={styles.formContainer}>
            <Text style={styles.label}>Description</Text>
            <TextInput
              style={styles.input}
              value={description}
              onChangeText={setDescription}
              placeholder="Add a description..."
              multiline
            />
            
            <Text style={styles.label}>Category</Text>
            <View style={styles.categoriesContainer}>
              {categories.map((cat) => (
                <TouchableOpacity
                  key={cat}
                  style={[
                    styles.categoryButton,
                    category === cat && styles.categoryButtonActive,
                  ]}
                  onPress={() => setCategory(cat)}
                >
                  <Tag 
                    size={16} 
                    color={category === cat ? '#FFFFFF' : Colors.text} 
                  />
                  <Text 
                    style={[
                      styles.categoryText,
                      category === cat && styles.categoryTextActive,
                    ]}
                  >
                    {cat.charAt(0).toUpperCase() + cat.slice(1)}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
        </ScrollView>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: Colors.separator,
  },
  closeButton: {
    padding: 8,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: Colors.text,
  },
  saveButton: {
    padding: 8,
  },
  content: {
    flex: 1,
  },
  mediaContainer: {
    width: width,
    height: width,
    backgroundColor: '#000',
    justifyContent: 'center',
    alignItems: 'center',
  },
  mediaImage: {
    width: '100%',
    height: '100%',
  },
  formContainer: {
    padding: 16,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.text,
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#F0F2F5',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    marginBottom: 16,
    minHeight: 100,
  },
  categoriesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 16,
  },
  categoryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F0F2F5',
    borderRadius: 20,
    paddingHorizontal: 12,
    paddingVertical: 8,
    marginRight: 8,
    marginBottom: 8,
  },
  categoryButtonActive: {
    backgroundColor: Colors.primary,
  },
  categoryText: {
    fontSize: 14,
    color: Colors.text,
    marginLeft: 4,
  },
  categoryTextActive: {
    color: '#FFFFFF',
  },
});