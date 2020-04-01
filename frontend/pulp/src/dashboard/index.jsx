import React from 'react'
import ReactDOM from 'react-dom'
import $ from 'jquery'
import { createStore, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { Provider } from 'react-redux'

import Dashboard from './components/Dashboard'
import reducer from './reducer'

const store = createStore(reducer, applyMiddleware(thunk))

function populateEmail(dispatch) {
    // TODO this doesn't use the csrf token!!!
    return $.ajax({
        url: "/api/users/get_email",
        type: "GET",
    }).then(
        (response) => dispatch({ type: "SET_EMAIL", data: response }),
        (error) => console.log(error)
    )
}

function populateReadingList(dispatch) {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    let data = {
      csrfmiddlewaretoken: csrftoken
    };

    dispatch({ type: "LOADING_ARTICLES" })

    return $.ajax({
      url: "/api/reading_list/get_reading",
      data: data,
      type: "GET"
    }).then(
        (response) => dispatch({ type: "LOADED_ARTICLES", articles: response }),
        (error) => console.log(error)
    )
}

function populateInitialState() {
    return function(dispatch) {
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();

        return Promise.all([
            populateEmail(dispatch),
            populateReadingList(dispatch),

        ])
    }
}

store.dispatch(populateInitialState())

ReactDOM.render(
    <Provider store={store}>
        <Dashboard />
    </Provider>,
    document.getElementById("root")
)