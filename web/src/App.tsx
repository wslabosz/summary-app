import { Outlet } from "react-router-dom";
import "./App.css";
import { AppBar } from "./components/AppBar";

export async function Loader() {
  if (Notification.permission !== "granted") {
    const permission = await Notification.requestPermission();
    if (permission !== "granted") {
      alert("You need to grant notification permission to use this app.");
    }
  }
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
