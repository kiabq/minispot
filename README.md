# minispot
A miniature API for retrieving Spotify status.

## Purpose
This was made because the first version of my personal site is using Astro, a static site generator, to build. This is a problem for me (partially due to poor planning) because I wanted to retrieve my Spotify status and display it on my personal site.

I solved this by making a small API in Python using FastAPI and deploying it on Vercel. On my site, I make an API call to this API on a set interval to get varying data from Spotify.

## Setup
If you want to use this API yourself, follow these steps:

- Clone repo with `git clone git@github.com:kiabq/minispot.git`
- Obtain your Spotify client_id, client_secret and refresh_token. Here's a [useful tutorial](https://leerob.io/blog/spotify-api-nextjs) for doing so.
- Fill in environment variables and deploy wherever you want
