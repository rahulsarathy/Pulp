import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';
import shortid from 'shortid';
import {CSSTransition, TransitionGroup} from "react-transition-group";
import {Row, Col, Modal} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import {Header, ReadingListView, ReadingListItem, Archive, Profile} from './components.jsx';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useHistory,
  useLocation,
  useParams,
  withRouter,
} from "react-router-dom";

class MenuItem extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let className;
    let image_url = '/static/icons/' + this.props.value + '.svg'
    this.props.location.pathname.split('/')[1] === this.props.value
      ? className = 'menu-item-selected'
      : className = "menu-item"

    return (<div className={className} onClick={this.props.onClick}>
      {
        this.props.value === 'reading_list'
          ? (<div className="unread">
            <div className="number">{this.props.unread}</div>
          </div>)
          : (<img className="icon" src={image_url}/>)
      }
      {this.props.text}
    </div>);
  }
}

export default class Switcher extends React.Component {

  constructor(props) {
    super(props);
    this.changeSelected = this.changeSelected.bind(this);
    this.state = {
      value: "",
      reading_list: [],
      invalid_url: false,
      article_data: {},
      selected: 'unread'
    };

  }

  changeSelected(value) {
    this.setState({selected: value});
  }

  render() {
    const RouterMenuItem = withRouter(MenuItem);

    return (<Router>
      <div>
        <Row className="readinglist-container">
          <Col className="sidebar">
            <Link to={'/reading_list'}>
              <RouterMenuItem onClick={() => this.changeSelected("reading_list")} unread={this.state.reading_list.length} selected={this.state.selected} value="reading_list" text={"Unread"}/>
            </Link>
            <Link to={'/archive'}>
              <RouterMenuItem onClick={() => this.changeSelected("archive")} selected={this.state.selected} value="archive" text={"Archive"}/>
            </Link>
            <Link to={'/settings'}>
              <RouterMenuItem onClick={() => this.changeSelected("settings")} selected={this.state.selected} value="settings" text={"Settings"}/>
            </Link>
          </Col>
          <Col className="readinglist">
            <Route path='/reading_list' component={ReadingListView}/>
            <Route path='/archive' component={Archive}/>
            <Route path='/settings' component={Profile}/>
          </Col>
        </Row>
      </div>
    </Router>);
  }
}

ReactDOM.render(<Switcher/>, document.getElementById('reading_list'))
