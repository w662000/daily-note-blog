---
layout: default
title: AI 每日工作日志
permalink: /dailylog/
---
<h2 class="section">AI 每日工作日志</h2>
<ul class="post-list">
{% assign logs = site.dailylog | sort: "date" | reverse %}
{% for p in logs %}
  <li>
    <span class="post-date">{{ p.date | date: "%Y-%m-%d" }}</span>
    <a href="{{ p.url | relative_url }}">{{ p.title }}</a>
  </li>
{% endfor %}
</ul>
