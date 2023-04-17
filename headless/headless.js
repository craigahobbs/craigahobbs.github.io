// Licensed under the MIT License
// https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

/* eslint-disable no-console */

import http from 'http';
import puppeteer from 'puppeteer';
import {parse as urlParse} from 'url';


// Main entry point
async function main() {
    // Environment variables
    // eslint-disable-next-line no-undef
    const port = process.env.PORT || 3000;

    // Launch a new headless browser instance
    const browser = await puppeteer.launch();

    // Create an HTTP server to handle incoming requests
    const server = http.createServer(async (req, res) => {
        // Parse the request URL and its query parameters
        const {pathname, query} = urlParse(req.url, true);

        // Handle requests
        if (pathname === '/render') {
            await render(req, res, query, browser);
        } else {
            res.writeHead(404, {'Content-Type': 'text/plain'});
            res.end('Not Found');
        }
    });

    // Start the server
    server.listen({port}, () => {
        console.log(`Server is running on port ${port}`);
    });

    // Add an event listener to close the browser instance when the application exits
    // eslint-disable-next-line no-undef
    process.on('exit', async () => {
        console.log('Closing headless browser');
        await browser.close();
        await server.close();
    });
}


// Headlessly render a web page and respond with its rendered HTML content
async function render(req, res, query, browser) {
    // Validate query string arguments
    const {url} = query;
    if (!url) {
        res.writeHead(400, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({'error': 'Missing URL parameter'}));
        return;
    }

    try {
        // Headlessly render the web page
        const page = await browser.newPage();
        await page.goto(url, {'waitUntil': 'networkidle2'});
        const content = await page.content();

        // Respond with the rendered HTML text
        res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
        res.end(content);
    } catch (error) {
        res.writeHead(500, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({'error': 'Failed to render the URL', 'details': error.message}));
    }
}


// Start the application
main();
