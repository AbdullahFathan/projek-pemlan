import "../index.css";
import { ref, get } from "firebase/database";
import { db } from "../firebase";
import { useState, useEffect } from "react";

const UserQueue = ({ inputValue }) => {
  const [yourQueue, setYourQueue] = useState([]);

  const getYourQueue = async () => {
    try {
      const snapshot = await get(ref(db, "/pasien"));
      if (snapshot.exists()) {
        const pasienData = snapshot.val();
        // Filter data berdasarkan inputValue
        const filteredData = Object.values(pasienData).filter(
          (data) => data.id === inputValue
        );
        setYourQueue(filteredData);
      } else {
        console.log("Data tidak ditemukan");
      }
    } catch (error) {
      console.error("Error fetching data: ", error);
    }
  };

  useEffect(() => {
    // Memanggil fungsi saat komponen pertama kali dimuat
    getYourQueue();
  }, [inputValue]); // Memastikan useEffect dipanggil hanya jika inputValue berubah

  return (
    <>
      {yourQueue.length > 0 ? (
        <>
          <p className="subtitle">Antrian Anda</p>
          <p className="title">{yourQueue[0].index}</p>
          <p className="body-medium">Nama: {yourQueue[0].name}</p>
        </>
      ) : (
        <p>Data tidak ditemukan</p>
      )}
    </>
  );
};

export default UserQueue;
