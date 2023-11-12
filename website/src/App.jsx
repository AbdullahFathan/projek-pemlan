import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";

import FormUser from "./pages/FormUser";
import NumberQueue from "./pages/NumberQueue";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<FormUser />} />
        <Route path="/number" element={<NumberQueue />} />
      </Routes>
    </BrowserRouter>
  );
};
export default App;
