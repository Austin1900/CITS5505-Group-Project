const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const db = mysql.createConnection({
    host: 'localhost',
    user: 'username',
    password: 'password',
    database: 'movie_forum'
});

app.post('/comment', (req, res) => {
    const { movieId, commentText } = req.body;
    const sql = 'INSERT INTO comments (movie_id, comment_text) VALUES (?, ?)';
    db.query(sql, [movieId, commentText], (err, result) => {
        if (err) throw err;
        console.log('Comment added:', result);
        res.send('Comment added successfully');
    });
});

app.post('/like', (req, res) => {
    const { movieId } = req.body;
    const sql = 'INSERT INTO likes (movie_id) VALUES (?)';
    db.query(sql, [movieId], (err, result) => {
        if (err) throw err;
        console.log('Like added:', result);
        res.send('Like added successfully');
    });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
