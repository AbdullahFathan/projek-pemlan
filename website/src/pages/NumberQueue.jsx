import "../index.css";
import { useLocation } from "react-router-dom";
import CurrentQueue from "../components/CurrentQueue";
import UserQueue from "../components/UserQueue";

const NumberQueue = () => {
  const location = useLocation();
  const inputValue = location.state ? location.state.inputValue : "";

  return (
    <section className="center-screen">
      <div className="box">
        <UserQueue inputValue={inputValue} />
        <CurrentQueue />
        <p>Harap Sabar menunggu</p>
      </div>
    </section>
  );
};

export default NumberQueue;
