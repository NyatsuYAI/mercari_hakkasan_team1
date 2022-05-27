import { useState } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route, RouteProps, Navigate } from 'react-router-dom';
import { Header } from './components/toppage/Header/Header'
import { TabItems } from './components/toppage/TabItems/TabItems';
import { Login } from './components/logingpage/Login'
import { ItemList } from './components/ItemList';
import { Listing } from './components/Listingpage/Listing';
import AuthUserProvider, { useAuthUser } from './components/Hooks/AuthUserContext';

const PrivateRoute: React.VFC<RouteProps> = ({ ...props }) => {
    const authUser = useAuthUser()
    const isAuthenticated = authUser != null
    if (isAuthenticated) {
        return <Route {...props} />
    } else {
        console.log(isAuthenticated)
        return <Navigate to="/Login" replace />
    }
};

// const UnAuthRoute: React.FC<RouteProps> = ({ ...props }) => {
//   const User = getUser()
//   if (User) {
//     return <Redirect to="/" />
//   } else {
//     return <Route {...props} />
//   }
// };


function App() {
    // reload ItemList after Listing complete
    //   const [reload, setReload] = useState(true);
    return (
        <AuthUserProvider>
            <BrowserRouter>
                <Routes>
                        <Route element={<PrivateRoute />}>
                            <Route path="/" element={<Header />} />
                        </Route>
                        <Route path="/login" element={<Login />} />
                        <Route path="/listing" element={<Listing />} />
                </Routes>
            </BrowserRouter>
        </AuthUserProvider>
    )
}

export default App;