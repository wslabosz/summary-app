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

// TODO: add on message to focus window
messaging.onBackgroundMessage(async (payload) => {
  const [videoId, notificationBody] = payload.notification.body.split("|");

  self.registration.showNotification(
    payload.notification.title ?? "Notification title",
    {
      body: notificationBody ?? "Notification body",
      icon: payload.notification.icon ?? "/pwa-192x192.png",
      data: {
        videoId,
      },
    }
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();

  const videoId = event.notification.data.videoId;
  // This looks to see if the current is already open and
  // focuses if it is
  event.waitUntil(
    clients
      .matchAll({
        type: "window",
        includeUncontrolled: true,
      })
      .then((clientList) => {
        for (const client of clientList) {
          if (
            client.url === `${self.location.origin}/video/${videoId}` &&
            "navigate" in client
          ) {
            client.focus();
            return client.navigate(`${self.location.origin}/video/${videoId}`);
          }
        }
        if (clients.openWindow)
          return clients
            .openWindow(`${self.location.origin}/video/${event.data.videoId}`)
            .then((client) => (client ? client.focus() : null));
      })
  );
});
