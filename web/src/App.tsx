import { Outlet } from "react-router-dom";
import "./App.css";
import { getModels } from "./api/models";
import { AppBar } from "./components/AppBar";

export async function Loader() {
  if (Notification.permission !== "granted") {
    const permission = await Notification.requestPermission();
    if (permission !== "granted") {
      alert("You need to grant notification permission to use this app.");
    }
  }

  const modelsResponse = await getModels();
  return modelsResponse?.models;
}

function App() {
  return (
    <>
      <AppBar />
      <main className="App">
        <Outlet />
      </main>
    </>
  );
}

export default App;
