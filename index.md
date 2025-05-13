---
layout: default
title: Home
---

# Astronomy Observation Log

Welcome to my astro logbook. Each entry below documents an observing session.

<ul>
  {% for post in site.posts %}
    <li><a href="{{ site.baseurl }}{{ post.url }}">{{ post.date | date: "%Y-%m-%d" }} - {{ post.title }}</a></li>
  {% endfor %}
</ul>