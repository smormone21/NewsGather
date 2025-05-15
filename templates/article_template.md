
---
title: "{{ title }}"
date: "{{ date }}"
lang: "{{ lang }}"
original_urls:
{% for url in urls %}
  - "{{ url }}"
{% endfor %}
slug: "{{ slug }}"
draft: false
---
{{ body }}
