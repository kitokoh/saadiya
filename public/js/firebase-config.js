
// Configuration Firebase
const firebaseConfig = {
    apiKey: "AIzaSyDMEs2f8IBooNo-rWVZ_fEZYPEpPvnyNC4",
    authDomain: "leopardo-ai.firebaseapp.com",
    databaseURL: "https://leopardo-ai-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "leopardo-ai",
    storageBucket: "leopardo-ai.firebasestorage.app",
    messagingSenderId: "838044402284",
    appId: "1:838044402284:web:3e8c53eb13fdac6b6e4e49",
    measurementId: "G-4NFRX042CB"
};

// Initialiser Firebase
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
const database = firebase.database();
const analytics = firebase.analytics();