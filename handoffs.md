---
layout: default
title: AI 项目组
permalink: /handoffs/
---
<h2 class="section">AI 项目组</h2>
<ul class="post-list">
{% assign hs = site.handoffs | sort: "date" | reverse %}
{% for p in hs %}
  <li>
    <span class="post-date">{{ p.date | date: "%Y-%m-%d" }}</span>
    <a href="{{ p.url | relative_url }}">{{ p.title }}</a>
  </li>
{% endfor %}
</ul>
