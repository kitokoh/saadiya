import React, { useState } from 'react';
import { 
  View, 
  StyleSheet, 
  FlatList, 
  TextInput,
  TouchableOpacity,
  Text,
} from 'react-native';
import { Stack } from 'expo-router';
import { Search, X } from 'lucide-react-native';
import { useChatStore } from '@/store/chat-store';
import { users } from '@/mocks/users';
import UserListItem from '@/components/UserListItem';
import Colors from '@/constants/colors';
import { User } from '@/types';

export default function ContactsScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const { chats, addChat } = useChatStore();
  
  const filteredUsers = users.filter(user => 
    user.name.toLowerCase().includes(searchQuery.toLowerCase())
  );
  
  const handleSelectUser = (user: User) => {
    addChat(user);
  };
  
  const getLastMessageInfo = (userId: string) => {
    const chat = chats.find(c => c.id === userId);
    if (!chat || chat.messages.length === 0) return null;
    
    const lastMessage = chat.messages[chat.messages.length - 1];
    const formattedTime = new Date(lastMessage.timestamp).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });
    
    return {
      text: lastMessage.text,
      time: formattedTime,
      unreadCount: chat.unreadCount,
    };
  };
  
  return (
    <View style={styles.container}>
      <Stack.Screen
        options={{
          title: 'Contacts',
        }}
      />
      
      <View style={styles.searchContainer}>
        <Search size={20} color={Colors.secondaryText} style={styles.searchIcon} />
        <TextInput
          style={styles.searchInput}
          placeholder="Search contacts"
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
        {searchQuery.length > 0 && (
          <TouchableOpacity onPress={() => setSearchQuery('')} style={styles.clearButton}>
            <X size={20} color={Colors.secondaryText} />
          </TouchableOpacity>
        )}
      </View>
      
      <FlatList
        data={filteredUsers}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => {
          const lastMessageInfo = getLastMessageInfo(item.id);
          
          return (
            <UserListItem
              user={item}
              onPress={handleSelectUser}
              hasUnread={!!lastMessageInfo?.unreadCount}
              unreadCount={lastMessageInfo?.unreadCount || 0}
              lastMessage={lastMessageInfo?.text || ''}
              lastMessageTime={lastMessageInfo?.time || ''}
            />
          );
        }}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>No contacts found</Text>
          </View>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F0F2F5',
    borderRadius: 8,
    margin: 16,
    paddingHorizontal: 12,
  },
  searchIcon: {
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    height: 40,
    fontSize: 16,
  },
  clearButton: {
    padding: 8,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    marginTop: 50,
  },
  emptyText: {
    fontSize: 16,
    color: Colors.secondaryText,
    textAlign: 'center',
  },
});