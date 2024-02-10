import { initializeApp } from "firebase/app";

const firebaseConfig = {
  apiKey: "AIzaSyDN5IKHN9V5WWCPcHNWyscI2JP3463IcSo",
  authDomain: "summaryai-fcdaa.firebaseapp.com",
  projectId: "summaryai-fcdaa",
  storageBucket: "summaryai-fcdaa.appspot.com",
  messagingSenderId: "220311930178",
  appId: "1:220311930178:web:9e24cb9d571785c49fb4db",
  databaseURL:
    "https://summaryai-fcdaa-default-rtdb.europe-west1.firebasedatabase.app/",
};

export const app = initializeApp(firebaseConfig);
