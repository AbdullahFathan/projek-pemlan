import "../index.css";
import { ref, onValue, off } from "firebase/database";
import { db } from "../firebase";
import { useState, useEffect } from "react";

const CurrentQueue = () => {
  const [currentQueueIndex, setCurrentQueueIndex] = useState("");

  // Mendapatkan data kedua dari Firebase secara real-time
  useEffect(() => {
    const currentQueueRef = ref(db, "/pasien");

    const updateCurrentQueue = (snapshot) => {
      const pasienData = snapshot.val();
      if (pasienData) {
        const firstPasienKey = Object.keys(pasienData)[0];
        const firstPasien = pasienData[firstPasienKey];
        setCurrentQueueIndex(firstPasien.index);
      } else {
        // Handle jika data kosong
        setCurrentQueueIndex("Data tidak tersedia");
      }
    };

    onValue(currentQueueRef, updateCurrentQueue);

    // Membersihkan listener saat komponen dibongkar
    return () => {
      off(currentQueueRef, "value", updateCurrentQueue);
    };
  }, []); // Membuat efek hanya dijalankan saat komponen pertama kali dimuat

  return (
    <>
      <p className="body-medium">Antrian Saat ini</p>
      <p className="current-queue">{currentQueueIndex}</p>
    </>
  );
};

export default CurrentQueue;
