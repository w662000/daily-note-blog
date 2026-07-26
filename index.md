---
layout: default
title: AI 工作流
is_home: true
---
<div class="home-nav">
  <a href="{{ '/dailylog/' | relative_url }}">AI 每日工作日志</a>
  <a href="{{ '/handoffs/' | relative_url }}">AI 项目组</a>
</div>

<h2 class="section">最新日志</h2>
<ul class="post-list">
{% assign logs = site.dailylog | sort: "date" | reverse %}
{% for p in logs limit:10 %}
  <li>
    <span class="post-date">{{ p.date | date: "%Y-%m-%d" }}</span>
    <a href="{{ p.url | relative_url }}">{{ p.title }}</a>
  </li>
{% endfor %}
</ul>
<p class="more"><a href="{{ '/dailylog/' | relative_url }}">查看全部日志 →</a></p>

<h2 class="section">项目交接</h2>
<ul class="post-list">
{% assign hs = site.handoffs | sort: "date" | reverse %}
{% for p in hs limit:10 %}
  <li>
    <span class="post-date">{{ p.date | date: "%Y-%m-%d" }}</span>
    <a href="{{ p.url | relative_url }}">{{ p.title }}</a>
  </li>
{% endfor %}
</ul>
<p class="more"><a href="{{ '/handoffs/' | relative_url }}">查看全部项目 →</a></p>
