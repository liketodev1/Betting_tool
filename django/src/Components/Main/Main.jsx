import React from "react"
import Banner from "./Banner/Banner"
import List from "./Lists/List"
import LogoLarge from '../../Images/LogoLarge.svg'

import {
    Card,
    Tabs,
    Container
} from 'react-bootstrap'


const Main = () => {

    return (
        <div className="main-container py-5">
            <div className="d-flex justify-content-center">
                <img src={LogoLarge} alt="LOGOLARGE"/>
            </div>
            <Container >
                <Banner />
            </Container>
        </div>
    )

}

export default Main