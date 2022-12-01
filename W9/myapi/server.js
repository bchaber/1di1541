const express = require('express');
const cors = require('cors');
const app = express();
const { expressjwt } = require('express-jwt');

const port = process.env.PORT || 8080;
const secret = process.env.JWT_SECRET;
const tasks = {} // sub => task list

const json = express.json()
const jwt = expressjwt({
  secret: secret,
  audience: 'http://localhost:3001',
  algorithms: ['HS256'],
  issuer: 'https://bach.eu.auth0.com/'
});

app.use(jwt);
app.use(json);
app.use(cors({ origin: "http://localhost:3000" }))

app.get('/tasks', function (req, res) {
  let user = req.auth.sub
  return res.status(200).send(tasks[user] || [])  
});

app.post('/tasks', function (req, res) {
  let user = req.auth.sub
  let task = req.body
  tasks[user] = tasks[user] || []
  tasks[user].push(task)
  return res.status(200).send(tasks[user])
});

process.on('SIGINT', function() {
    process.exit();
});

app.listen(port);
console.log('Running on port ', port);
