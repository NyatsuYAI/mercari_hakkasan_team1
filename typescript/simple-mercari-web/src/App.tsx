import { useState } from "react";
import "./App.css";
import {
  BrowserRouter,
  Routes,
  Route,
  RouteProps,
  Navigate,
  useNavigate,
} from "react-router-dom";
import { Header } from "./components/toppage/Header/Header";
import { TabItems } from "./components/toppage/TabItems/TabItems";
import { Login } from "./components/logingpage/Login";
import { ItemList } from "./components/ItemList";
import { Listing } from "./components/Listingpage/Listing";
import AuthUserProvider, {
  useAuthUser,
} from "./components/Hooks/AuthUserContext";

function RequireAuth({ children }: { children: JSX.Element }) {
  const authUser = useAuthUser();
  !authUser ?? <Navigate to="/Login" />;
  return children;
}

function App() {
  return (
    <AuthUserProvider>
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={
              <RequireAuth>
                <Header />
              </RequireAuth>
            }
          />
          <Route path="/login" element={<Login />} />
          <Route path="/listing" element={<Listing />} />
        </Routes>
      </BrowserRouter>
    </AuthUserProvider>
  );
}

export default App;
