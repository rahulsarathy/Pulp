import React from 'react';
import ReactDOM from 'react-dom';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import $ from 'jquery';
// const stripe = Stripe('pk_test_9DUWDnI9T5YJWmLRhNn6nHtS')
// const stripe = require('stripe')('pk_test_9DUWDnI9T5YJWmLRhNn6nHtS')

var src = 'https://js.stripe.com/v3/';
var tag = document.createElement('script');
tag.async = false;
tag.src = src;
document.getElementsByTagName('script')[0].appendChild(tag);
const stripe = Stripe('pk_test_9DUWDnI9T5YJWmLRhNn6nHtS');

export default class Payment_Pane extends React.Component {

	constructor(props) {
		super(props);
		// this.setStripeScript();
		this.createSession = this.createSession.bind(this);
		this.state = {
			paid: false
		};
	}

	componentDidMount() {
		this.checkPaymentStatus();
	}

	setStripeScript() {
		
	}

	checkPaymentStatus(){
		$.ajax({
			url: '../api/payments/payment_status',
			type: 'GET',
			success: function(data, statusText, xhr) {
				console.log(xhr)
				if (xhr.status == 208) {
					this.setState({
						paid: true
					});
				}
			}.bind(this)
		});
	}

	createSession(){
		$.ajax({
			url: '../api/payments/create_session',
			type: 'GET',
			success: function(data, statusText, xhr) {
				if (xhr.status == 208){
					this.setState({
						paid: true
					});
				}
				var id = data.id;
				this.startPayment(id);
			}.bind(this)
		});
	}

	startPayment(id) {
		console.log("starting stripe payment")
		stripe.redirectToCheckout({
        // Make the id field from the Checkout Session creation API response
        // available to this file, so you can provide it as parameter here
        // instead of the {{CHECKOUT_SESSION_ID}} placeholder.
        sessionId: id
    }).then(function (result) {
    	// If `redirectToCheckout` fails due to a browser or network
    	// error, display the localized error message to your customer
    	// using `result.error.message`.
    	console.log(result.error.message)
    });
}

	render () {
		return (
			<div >
				<h3>Magazines are $15.00/Month.</h3>
				<button onClick={this.createSession}>Get Pulp</button>
			</div>
    	);
  }
}