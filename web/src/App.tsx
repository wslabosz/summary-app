import { getDatabase, ref, set } from "firebase/database";
import { getMessaging, getToken } from "firebase/messaging";
import { Outlet } from "react-router-dom";
import "./App.css";
import { AppBar } from "./components/AppBar";
import { app } from "./firebase";

export async function Loader() {
  const db = getDatabase(app);
  if (Notification.permission !== "granted") {
    const permission = await Notification.requestPermission();
    if (permission !== "granted") {
      alert("You need to grant notification permission to use this app.");
    }
  }

  const messaging = getMessaging();
  const token = await getToken(messaging, {
    vapidKey: import.meta.env.VITE_FIREBASE_VAPID_KEY,
  });
  set(ref(db, `tokens/${token}`), {
    token,
  });
  return null;
}

function App() {
  return (
    <>
      <AppBar />
      <main className="App">
        <img src="/favicon.svg" alt="PWA Logo" width="60" height="60" />
        <h1 className="Home-title">AI Summary</h1>
        <Outlet />
      </main>
    </>
  );
}

export default App;
