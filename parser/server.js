"use strict";
const Mercury = require("@postlight/mercury-parser");
const express = require("express");
var bodyParser = require("body-parser");

// Constants
const PORT = 3000;
const HOST = "0.0.0.0";

// App
const app = express();
app.use(bodyParser.json()); // to support JSON-encoded bodies
app.use(
	express.urlencoded({
		extended: true
	})
); // to support URL-encoded bodies

app.get("/", (req, res) => {
	res.send("Parser Is up and running\n");
});

app.post("/api/mercury", function(req, res) {
	var url = req.body.url;

	Mercury.parse(url)
		.then(function(result) {
			res.send(result);
		})
		.catch(error => res.status(400).send(error.message));
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);
