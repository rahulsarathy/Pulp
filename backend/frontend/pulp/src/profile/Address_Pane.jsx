import React from 'react';
import ReactDOM from 'react-dom';
import 'bootstrap/dist/css/bootstrap.css';
import $ from 'jquery';
import { Modal } from 'react-bootstrap';
import {Address_Modal} from './Components.jsx'


var componentForm = {
  street_number: 'short_name',
  route: 'long_name',
  locality: 'long_name',
  administrative_area_level_1: 'short_name',
  country: 'long_name',
  postal_code: 'short_name'
};

export default class Address_Pane extends React.Component {

	constructor(props) {
		super(props);

		this.handleChange = this.handleChange.bind(this);
		this.setAddress = this.setAddress.bind(this);
		this.getAddress = this.getAddress.bind(this);
		this.showModal = this.showModal.bind(this);
		this.closeModal = this.closeModal.bind(this);

		this.state = {
			address: '',
			line_1: '',
			line_2: '',
			city: '',
			state: '',
			zip: '',
			country: '',
			show: false
		};
	}

	componentDidMount() {
		this.getAddress()
	}

	handleChange(e){
		var field = e.target.id;
		this.setState({
			[field]: e.target.value
		});
	}

	setAddress()
	{
		var csrftoken = $("[name=csrfmiddlewaretoken]").val();
		var address_json = {
			line_1: this.state.line_1,
			line_2: this.state.line_2,
			city: this.state.city,
			state: this.state.state,
			zip: this.state.zip,
			country: this.state.country,
		}
		var data = {
			address_json: JSON.stringify(address_json),
			csrfmiddlewaretoken: csrftoken,
		}

		$.ajax(
			{
				type: 'POST',
				data: data,
				url: '../api/users/set_address/',
				success: function(data)
					{
						this.setState(
							{
								address: data,
							});
					}.bind(this),
				error: function (request, status, error) {
				}
			});
	}

	getAddress() {
		$.ajax({
			type: 'GET',
			url: '../api/users/get_address/',
			success: function(data) {
				this.setState({
					address: data
				});
			}.bind(this)
		});
	}

	closeModal (e) {
		this.setState({
			show: false
		});
	}

	showModal(e) {
		this.setState({
			show: true
		});
	}

	render () {
		// const addresses = this.createAddresses()
		const no_address = (
			<div>
				<h3>You have not yet set a delivery address</h3>
				<Address_Modal set={true} handleChange={this.handleChange} setAddress={this.setAddress} />
			</div>
			);
		const address = (
			<div>
				<p>Your magazine will be delivered to <span className="highlighted">{this.state.address.line_1}</span> </p>
				<Address_Modal set={false} handleChange={this.handleChange} setAddress={this.setAddress}/>
			</div>
			);
		return (
			<div className="address_pane">
				{this.state.address == '' ? no_address : address}
			</div>
    	);
  }
}
