import React from 'react';
import ReactDOM from 'react-dom';
import 'bootstrap/dist/css/bootstrap.css';
import shortid from 'shortid';

export default class Header extends React.Component {

	constructor(props) {
		super(props);
		
		this.state = {

		};
	}

	render () {
    return (
    	<div className="header">
            <div className="links">
                <p><a href="/auth/login">Login</a></p>  
                <p><a href="/api/users/signup">Sign up</a></p>  
            </div>
    	</div>
    	);
  }
}

