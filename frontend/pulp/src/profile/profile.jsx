import React from "react";
import ReactDOM from "react-dom";
import "bootstrap/dist/css/bootstrap.css";
import $ from "jquery";
import shortid from "shortid";
import classnames from "classnames";
import { Row, Col } from "react-bootstrap";
import {
  Address_Pane,
  Header,
  Instapaper,
  Pocket,
  SubscribePane
} from "./components.jsx";

class SubHeader extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div>
        <h2>{this.props.title}</h2>
        <hr></hr>
      </div>
    );
  }
}

export default class Profile extends React.Component {
  constructor(props) {
    super(props);
    this.cancelPayment = this.cancelPayment.bind(this);
    this.handleCheck = this.handleCheck.bind(this);
    this.handleSelector = this.handleSelector.bind(this);
    this.updateSettings = this.updateSettings.bind(this);
    this.getEmail = this.getEmail.bind(this);
    this.state = {
      email: "",
      archive_links: false,
      paid: false,
      sortby: "oldest",
      invite_codes: []
    };
  }

  componentDidMount() {
    this.checkPaymentStatus();
    this.getSettings();
    this.getEmail();
  }

  updateSettings() {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    let data = {
      archive_links: this.state.archive_links,
      sortby: this.state.sortby,
      csrfmiddlewaretoken: csrftoken
    };
    $.ajax({
      url: "../api/users/set_settings/",
      type: "POST",
      data: data,
      success: function(data) {
        this.setState({
          changed: false
        });
      }.bind(this)
    });
  }

  getEmail() {
    $.ajax({
      url: "../api/users/get_email",
      type: "GET",
      success: function(data) {
        this.setState({
          email: data
        });
      }.bind(this)
    });
  }

  getSettings() {
    $.ajax({
      url: "../api/users/get_settings",
      type: "GET",
      success: function(data) {
        let deliver_oldest;
        if (data.deliver_oldest) {
          deliver_oldest = "oldest";
        } else {
          deliver_oldest = "newest";
        }
        this.setState({
          archive_links: data.archive_links,
          sortby: deliver_oldest
        });
      }.bind(this)
    });
  }

  checkPaymentStatus() {
    $.ajax({
      url: "../api/payments/payment_status",
      type: "GET",
      success: function(data, statusText, xhr) {
        if (xhr.status == 208) {
          this.setState({ paid: true });
        } else {
          this.setState({ paid: false });
        }
      }.bind(this)
    });
  }

  cancelPayment() {
    $.ajax({
      url: "../api/payments/cancel_payment",
      type: "GET",
      success: function(data, statusText, xhr) {
        this.setState({ paid: false });
      }.bind(this)
    });
  }

  handleCheck(e) {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    const name = target.name;
    this.setState({ [name]: value, changed: true });
  }

  handleSelector(e) {
    let name = e.target.name;
    this.setState({
      [name]: e.target.value,
      changed: true
    });
  }

  render() {
    return (
      <div className="profile-container">
        <h1>Settings</h1>
        <hr className="divider"></hr>
        <div id="contact" className="subsection">
          <SubHeader title="Contact Info" />
          <label>
            <b>{"Email: "}</b>
            {this.state.email}
          </label>
        </div>
        <div id="subscription" className="subsection">
          <SubHeader title="Subscription Info" />
          <SubscribePane
            unsubscribe={this.props.unsubscribe}
            email={this.state.email}
            paid={this.props.paid}
          />
        </div>
        <div id="import" className="subsection">
          <SubHeader title="Import Articles" />
          <Instapaper
            syncInstapaper={this.props.syncInstapaper}
            instapaper={this.props.instapaper}
            removeInstapaper={this.props.removeInstapaper}
          />
          <Pocket
            syncPocket={this.props.syncPocket}
            pocket={this.props.pocket}
            removePocket={this.props.removePocket}
          />
        </div>
        <div id="address" className="subsection">
          <SubHeader title="Delivery Info" />
          <Address_Pane />
        </div>
        <div id="delivery" className="subsection">
          <SubHeader title="Delivery Settings" />
          <div id="archive_links">
            <label>
              -{" "}
              <input
                name="archive_links"
                type="checkbox"
                checked={this.state.archive_links}
                onChange={this.handleCheck}
              />
              Archive links once they are delivered
            </label>
          </div>
          <div id="sortby">
            <label>Deliver</label>
            <select
              name="sortby"
              value={this.state.sortby}
              onChange={this.handleSelector}
            >
              <option value="oldest">oldest</option>
              <option value="newest">newest</option>
            </select>
            <label>articles first</label>
          </div>
          {this.state.changed ? (
            <div>
              <button onClick={this.updateSettings}>Apply changes</button>
            </div>
          ) : (
            <div></div>
          )}
        </div>
        <div id="password" className="subsection">
          <SubHeader title="Security" />
          <a href="../accounts/password/change">Change Password</a>
        </div>
      </div>
    );
  }
}

// ReactDOM.render(<Profile/>, document.getElementById('profile'))
