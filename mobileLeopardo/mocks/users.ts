import { User } from '@/types';

export const users: User[] = [
  {
    id: 'leopardo',
    name: 'Leopardo',
    avatar: 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    isOnline: true,
  },
  {
    id: 'user1',
    name: 'Sarah Johnson',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    lastSeen: '2 hours ago',
  },
  {
    id: 'user2',
    name: 'Michael Chen',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    isOnline: true,
  },
  {
    id: 'user3',
    name: 'Olivia Rodriguez',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    lastSeen: 'Yesterday',
  },
  {
    id: 'user4',
    name: 'James Wilson',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    lastSeen: '3 days ago',
  },
  {
    id: 'user5',
    name: 'Emma Thompson',
    avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    isOnline: true,
  },
];

export const getLeopardo = () => users.find(user => user.id === 'leopardo')!;