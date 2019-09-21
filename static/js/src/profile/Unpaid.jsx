import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';
import shortid from 'shortid';

const stripe = Stripe(stripe_public_key);

export default class Unpaid extends React.Component {

	constructor(props) {
		super(props);

        this.createSession = this.createSession.bind(this);

		this.state = {
		};
	} 

    createSession(){
        console.log("create session called");
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
        sessionId: id,

    }).then(function (result) {
        // If `redirectToCheckout` fails due to a browser or network
        // error, display the localized error message to your customer
        // using `result.error.message`.
        console.log(result.error.message)
    });
}

	render () {
        return (
            <div className="unpaid">
                <div className="pay-card">
                    <div className="title">
                        <p>Pulp</p>
                    </div>
                    <div className="description">
                        <p>1 new magazine every month</p>
                        <p>$9.99 a month</p>
                        <button onClick={this.createSession} className="getpulp">Get Pulp</button>
                    </div>

                </div> 
            </div>
            );
    }
}