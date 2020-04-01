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
                                <Link className=" font-16 text-white" to={{
                                    pathname: `${process.env.PUBLIC_URL}/home `
                                }}>Home
                                </Link >
                            </Nav.Link>
                        
                        </Nav.Item>
                        <Nav.Item className="mx-2">
                            <Nav.Link>
                                <Link className="font-16 text-white " to={{
                                    pathname: `${process.env.PUBLIC_URL}/about_us `
                                }}>About Us
                                </Link >
                            </Nav.Link>
                        </Nav.Item>
                        <Nav.Item className="mx-2">
                            <Nav.Link>
                                <Link className="font-16 text-white " to={{
                                pathname: `${process.env.PUBLIC_URL}/prediction`
                                }}>Prediction
                                </Link >
                            </Nav.Link>
                        </Nav.Item>
                        <Nav.Item className="mx-2">
                            <Nav.Link>
                                <Link className="font-16 text-white " to={{
                                pathname: `${process.env.PUBLIC_URL}/tv_info`
                                }}>TV Info
                                </Link >
                            </Nav.Link>
                        </Nav.Item>
                        <Nav.Item className="mx-2">
                            <Nav.Link>
                                <Link className="font-16 text-white " to={{
                                pathname: `${process.env.PUBLIC_URL}/faq`
                                }}>FAQ
                                </Link >
                            </Nav.Link>
                        </Nav.Item>
                    </Nav>
                    <Nav className="justify-content-end w-25">
                        <Nav.Link className="mx-2">
                            <Link className="text-white" to={{
                                pathname: `${process.env.PUBLIC_URL}/login_in` 
                                }}>
                                <img src={Login} alt="LOGIN"/>
                                <span className="font-16 text-white ml-2">Log </span>
                            </Link>
                        </Nav.Link>
                        <Nav.Link className="mx-2">
                            <Link className="text-white" to={{
                                pathname: `${process.env.PUBLIC_URL}/register` 
                                }}>
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