import React from "react";
import ReactDOM from "react-dom";
import $ from "jquery";
import shortid from "shortid";
import "bootstrap/dist/css/bootstrap.css";

const icon_url = "../static/icons/";

class CheckBox extends React.Component {
	constructor(props) {
		super(props);

		this.state = {};
	}

	render() {
		let className;
		let image;
		if (this.props.checked) {
			className = "selected";
			image = <img src={icon_url + "checkmark.svg"} />;
		} else {
			className = "unselected";
		}
		return (
			<div
				onClick={this.props.onChange}
				className={"checkbox " + className + " center"}
			>
				{image}
			</div>
		);
	}
}

class OverflowBox extends React.Component {
	constructor(props) {
		super(props);

		this.state = {};
	}

	render() {
		let style = {
			borderColor: "red"
		};
		return <div style={style} className="checkbox unselected center"></div>;
	}
}

export { OverflowBox, CheckBox };
