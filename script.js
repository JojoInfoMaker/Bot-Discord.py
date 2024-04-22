const express = require('express');
const ytdl = require('ytdl-core');

const app = express();
const PORT = 3000;

app.get('/play', async (req, res) => {
    const url = req.query.url;
    if (!url) {
        return res.status(400).send('URL is required');
    }

    try {
        const info = await ytdl.getInfo(url);
        const audioURL = ytdl.chooseFormat(info.formats, { filter: 'audioonly' }).url;
        return res.send(audioURL);
    } catch (error) {
        console.error('Error:', error);
        return res.status(500).send('Error fetching audio URL');
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
