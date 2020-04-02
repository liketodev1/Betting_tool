import React from "react"
// import { PageHeader, Button, Avatar, Descriptions } from 'antd';
import {
  Link
} from "react-router-dom";

import classes from './Header.module.css'
import './Header.module.css'
import './Header.css'
import Logo from '../../Images/LogoSmall.svg'
import Login from '../../Images/login.svg'
import Register from '../../Images/register.svg'
import {
    Navbar,
    NavbarBrand,
    NavbarToggle,
    NavbarCollapse,
    Nav,
    NavLink,
    NavDropdown,
    NavDropdownItem,
    Container 
}  from 'react-bootstrap'


const Header = () => {
    return (
        <div className="header">
            <Navbar className={` ${classes.headerContainer } `} expand="lg">
            <Container>
                <Navbar.Brand href="#home" className="navbar-logo">
                    <img src={Logo} alt="LOGOSMALL"/>
                    <div className="logo-title ml-2">
                        <span className="font-16">COMPANY</span>
                        <span className="font-20">LOGO</span>
                    </div>
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav" className="">
                    <Nav className="justify-content-center w-75" >
                        <Nav.Item className="mx-2">
                            <Nav.Link>
                                <Link to="/home" className="text-white">Home</Link>
                            </Nav.Link>
                        </Nav.Item>
                        <Nav.Item className="mx-2">
                            <Nav.Link>
                                <Link to="/about_us" className="font-16 text-white " >About Us</Link>
                            </Nav.Link>
                        </Nav.Item>
                        <Nav.Item className="mx-2">
                            <Nav.Link>
                                <Link to="/prediction" className="font-16 text-white" >Prediction</Link>
                            </Nav.Link>
                        </Nav.Item>
                        <Nav.Item className="mx-2">
                            <Nav.Link>
                                <Link to="/tv_info" className="font-16 text-white" >TV Info</Link>
                            </Nav.Link>
                        </Nav.Item>
                        <Nav.Item className="mx-2">
                            <Nav.Link>
                                <Link to="/faq" className="font-16 text-white" >FAQ</Link>
                            </Nav.Link>
                        </Nav.Item>
                    </Nav>
                    <Nav className="justify-content-end w-25">
                        <Nav.Link className="mx-2">
                            <Link to="/login_in" className="text-white">
                                <img src={Login} alt="LOGIN"/>
                                <span className="font-16 text-white ml-2">Log In</span>
                            </Link>
                        </Nav.Link>
                        <Nav.Link className="mx-2">
                            <Link to="/register" className="text-white">
                                <img src={Register} alt="REGISTER"/>
                                <span className="font-16 text-white ml-2">Register</span>
                            </Link>
                        </Nav.Link>
                    </Nav>
                </Navbar.Collapse>
                </Container>
            </Navbar>
        </div>
    )
}


export default Header