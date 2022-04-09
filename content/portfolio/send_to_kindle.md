Title: Send To Kindle
Date: 2010-12-03 10:20
Modified: 2010-12-05 19:30
Category: Portfolio
Tags: python, microservices, flask
Slug: send-to-kindle
Authors: Phil Nicholls
Summary: gRPC microservices to convert and send webpages to a Kindle
Cover: /photos/send_to_kindle/send-to-kindle1.jpg
Features: Microservice architecture built with gRPC,Built with Docker,Kubernetes ready,Uses PyTest monkeypatch to prevent email sending in test,Generates a bookmarklet during the registration process which includes a token for API authentification,Well commented and conforming to PEP8 and detailed docstrings
Links: https://github.com/philjnicholls/sendtokindle|Source Code
Gallery: {photo}send_to_kindle/

Simple Flask REST API with beautifully crafted gRPC microservice architecture that takes the URL of a web page, finds the main article text, converts it to an ebook, and emails to a Kindle email address. I created endpoints to accept a URL or the actual HTML to send to the Kindle. The later endpoint supports sites with logins, popups or attempts to catch scraping tools and integrates Readability JS to identify main page content.
