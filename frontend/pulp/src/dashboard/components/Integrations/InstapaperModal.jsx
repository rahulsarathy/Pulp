import React from 'react'
import { connect } from 'react-redux'
import { Modal, Button } from 'react-bootstrap'
import PulpButton from '../../../components/PulpButton'
import { integrateInstapaper, removeInstapaper } from '../../actions/InstapaperActions'

import './InstapaperModal.scss'

const image_url = "/static/images/"

function PocketModal({ text, integrationStatus, integrateWithInstapaper, removeInstapaperIntegration }) {
    const [show, setShow] = React.useState(false)

    const handleHide = (e) => {
        if (e) { e.preventDefault() }
        setShow(false)
    }
    const handleShow = (e) => {
        if (e) { e.preventDefault() }
        setShow(true)
    }

    function handleRemoveInstapaper(e) {
        if (e) { e.preventDefault() }
        removeInstapaperIntegration()
        handleHide()
    }

    function handleIntegrateInstapaper(e) {
        if (e) { e.preventDefault() }
        integrateWithInstapaper()
        handleHide()
    }

    var modal;
    if (integrationStatus.integrated) {
        modal = (
            <Modal show={show} onHide={handleHide}>
                <Modal.Header>
                    <Modal.Title>
                        Instapaper is integrated with Pulp
                    </Modal.Title>
                </Modal.Header>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleHide}>Close</Button>
                    <Button variant="primary" onClick={handleRemoveInstapaper}>Remove Instapaper integration</Button>
                </Modal.Footer>
            </Modal>
        )
    } else {
        modal = (
            <Modal show={show} onHide={handleHide}>
                <Modal.Header>
                    <Modal.Title>
                        Sign into Instapaper
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <form onSubmit={handleIntegrateInstapaper}>
                        <label htmlFor="username">Instapaper Username:</label>
                        <input type="text" name="username" />
                        <label htmlFor="password">Instapaper Password:</label>
                        <input type="password" name="password" />
                    </form>
                    {/* TODO */}
                    {integrationStatus.invalidPassword && <p>Invalid password or username</p>}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleHide}>Close</Button>
                    <Button variant="primary" onClick={handleIntegrateInstapaper}>Import from Instapaper</Button>
                </Modal.Footer>
            </Modal>
        )
    }

    var activator;
    if (!text) {
        activator = (
            <PulpButton className="instapaper-button" onClick={handleShow}>
                <img className="instapaper-logo" src={image_url + "instapaper_logo.png"} />
            </PulpButton>
        )
    } else {
        activator = (
            <a href="" onClick={handleShow}>{text}</a>
        )
    }

    return (
        <React.Fragment>
            {activator}
            {modal}
        </React.Fragment>
    )
}

function mapStateToProps(state) {
    return {
        integrationStatus: {
            integrated: state.integrations.instapaper.integrated,
            invalidPassword: false, // TODO
        }
    }
}

function mapDispatchToProps(dispatch) {
    return {
        integrateWithPocket: () => dispatch(integrateInstapaper()),
        removePocketIntegration: () => dispatch(removeInstapaper()),
    }
}

PocketModal = connect(mapStateToProps, mapDispatchToProps)(PocketModal)

export default PocketModal
