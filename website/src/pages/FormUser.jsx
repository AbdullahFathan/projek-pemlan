import { useState } from "react";
import { useNavigate } from "react-router-dom";

const FormUser = () => {
  const [inputValue, setInputValue] = useState("");
  const navigate = useNavigate();

  const hanldeSubmit = (e) => {
    e.preventDefault();
    navigate("/number", { state: { inputValue } });
  };
  return (
    <section className="center-screen">
      <div className="box">
        <h1>Selamat Datang</h1>
        <h4>
          Masukan ID yang diberikan oleh <br />
          Petugas klinik X
        </h4>

        <form className="form-user" onSubmit={hanldeSubmit}>
          <input
            type="text"
            placeholder="Input ID"
            value={inputValue}
            required
            onChange={(e) => setInputValue(e.target.value)}
          />
          <button type="submit">Submit</button>
        </form>
      </div>
    </section>
  );
};
export default FormUser;
