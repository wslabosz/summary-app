importScripts(
  "https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js"
);
importScripts(
  "https://www.gstatic.com/firebasejs/10.8.0/firebase-messaging-compat.js"
);

var FIREBASE_CONFIG = {
  apiKey: "AIzaSyDN5IKHN9V5WWCPcHNWyscI2JP3463IcSo",
  authDomain: "summaryai-fcdaa.firebaseapp.com",
  projectId: "summaryai-fcdaa",
  storageBucket: "summaryai-fcdaa.appspot.com",
  messagingSenderId: "220311930178",
  appId: "1:220311930178:web:9e24cb9d571785c49fb4db",
};

// Initialize Firebase
firebase.initializeApp(FIREBASE_CONFIG);
const messaging = firebase.messaging();

messaging.onBackgroundMessage(async (payload) => {
  console.log(
    "[firebase-messaging-sw.js] Received background message ",
    payload
  );
  // Customize notification here
  const notificationTitle = "Background Message Title";
  const notificationOptions = {
    body: "Background Message body.",
    // when deployed it doesn't work
    icon: "/pwa-192x192.png",
  };

  self.registration.showNotification(
    payload.notification.title ?? "Random notification",
    {
      body: payload.notification.body ?? "Random notification body",
      icon: notificationOptions.icon,
    }
  );
});
