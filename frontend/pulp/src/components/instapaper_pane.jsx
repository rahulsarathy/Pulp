import React from "react";
import ReactDOM from "react-dom";
import "bootstrap/dist/css/bootstrap.css";
import $ from "jquery";
import shortid from "shortid";
import classnames from "classnames";
import { Modal, Button } from "react-bootstrap";
import {} from "./components.jsx";

const static_url = "../static/images/";

export default class Instapaper_Pane extends React.Component {
  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this);
    this.authenticateInstapaper = this.authenticateInstapaper.bind(this);

    this.showModal = this.showModal.bind(this);
    this.hideModal = this.hideModal.bind(this);
    this.state = {
      username: "",
      password: "",
      invalid: false,
      loading: false,
      success: false,
      instapaper: false
    };
  }

  showModal(service) {
    this.setState({ [service]: true });
  }

  hideModal(service) {
    this.setState({ [service]: false });
  }

  handleChange(e) {
    var field = e.target.id;
    this.setState({ [field]: e.target.value });
  }

  authenticateInstapaper(username, password) {
    this.setState({ loading: true });
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    let data = {
      username: username,
      password: password,
      csrfmiddlewaretoken: csrftoken
    };
    $.ajax({
      url: "../api/instapaper/authenticate_instapaper",
      data: data,
      type: "POST",
      success: function(data) {
        this.setState({ loading: false, success: true, invalid: false });
        // this.updateReadingList(data);
      }.bind(this),
      error: function(data) {
        if (data.status === 401) {
          this.setState({ invalid: true, loading: false });
        }
      }.bind(this)
    });
  }

  defaultModal() {
    return (
      <Modal
        id="instapaper-modal"
        show={this.state.instapaper}
        onHide={() => this.hideModal("instapaper")}
      >
        <h2>Sign into Instapaper</h2>
        Username
        <input id="username" onChange={this.handleChange}></input>
        Password
        <input
          type="password"
          id="password"
          onChange={this.handleChange}
        ></input>
        <Modal.Footer>
          {this.state.invalid ? (
            <div className="invalid">Invalid username or password</div>
          ) : (
            <div></div>
          )}
          {this.state.loading ? (
            <div className="loading">Loading...</div>
          ) : (
            <div></div>
          )}
          {this.state.success ? (
            <div className="success">
              Your articles will be imported over the next half hour.
            </div>
          ) : (
            <div></div>
          )}
          <Button
            onClick={() =>
              this.authenticateInstapaper(
                this.state.username,
                this.state.password
              )
            }
          >
            Import from Instapaper
          </Button>
          <Button
            variant="secondary"
            onClick={() => this.hideModal("instapaper")}
          >
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    );
  }

  removeModal() {
    return (
      <Modal
        id="instapaper-modal"
        show={this.state.instapaper}
        onHide={() => this.hideModal("instapaper")}
      >
        <p>Instapaper is integrated with Pulp</p>
        <Modal.Footer>
          <Button onClick={this.props.removeInstapaper}>
            Remove Instapaper integration
          </Button>
          <Button
            variant="secondary"
            onClick={() => this.hideModal("instapaper")}
          >
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    );
  }

  render() {
    return (
      <div className="service-container">
        <button
          onClick={() => this.showModal("instapaper")}
          className="integration-button instapaper"
        >
          <img
            className="instapaper-image"
            src={static_url + "instapaper_logo.png"}
          />
          Instapaper
        </button>
        {this.props.signed_in ? this.removeModal() : this.defaultModal()}
      </div>
    );
  }
}
