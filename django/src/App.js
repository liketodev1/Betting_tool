import React from 'react';
import logo from './logo.svg';
import './App.css';
import {
  BrowserRouter,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";


//  Components

import Header from './Components/Header/Header'
import Main from './Components/Main/Main'
import Footer from './Components/Footer/Footer'
import AboutUs from './Components/AboutUs/AboutUs';
import Prediction from './Components/Prediction/Prediction';
import TVInfo from './Components/TVInfo/TVInfo';
import Login from './Components/Login/Login';
import Register from './Components/Register/Register';
import Faq from './Components/FAQ/Faq';



function App() {

  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <div className="main">
          <Route path={`${process.env.PUBLIC_URL}/`} component={Main} />
          <Route path={`${process.env.PUBLIC_URL}/home`} component={Main} />
          <Route path={`${process.env.PUBLIC_URL}/about_us`} component={AboutUs}/>
          <Route path={`${process.env.PUBLIC_URL}/prediction`} component={Prediction} />
          <Route path={`${process.env.PUBLIC_URL}/tv_info`} component={TVInfo} />
          <Route path={`${process.env.PUBLIC_URL}/faq`} component={Faq} />
          <Route path={`${process.env.PUBLIC_URL}/login_in`} component={Login} />
          <Route path={`${process.env.PUBLIC_URL}/register`} component={Register} />
        </div>
        <Footer />
      </BrowserRouter>
    </div>
  );
}

export default App;
