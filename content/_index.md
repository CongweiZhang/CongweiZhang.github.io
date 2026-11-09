---
title: ""
date: 2026-11-09
type: landing
sections:
  - block: resume-biography-3
    content:
      username: me
      headings:
        about: ""
        education: ""
        interests: ""
    design:
      name:
        size: md
      avatar:
        size: medium
        shape: circle
      show_status: false
  - block: markdown
    id: research-overview
    content:
      title: "Research"
      text: |
        My research focuses on **networked systems, edge intelligence, and efficient large language model systems**. I am interested in building efficient, scalable, and resource-aware systems that connect machine learning with computer systems and networks.

        Current interests include efficient LLM inference at the edge, resource-aware scheduling, load balancing, and distributed intelligence.
    design:
      columns: "1"
  - block: markdown
    id: selected-research
    content:
      title: "Selected Research"
      text: |
        <div class="research-list">
          <article class="research-item">
            <div class="research-cover"><strong>CRISP</strong><small>MoE inference at the edge</small></div>
            <div class="research-body">
              <div class="research-meta"><span>ACM MobiCom 2026</span><span>Published</span></div>
              <h3>CRISP</h3>
              <p class="research-authors">Congwei Zhang et al.</p>
              <p>An efficient MoE inference system for edge servers. CRISP jointly considers expert pruning and scheduling to reduce inference overhead and improve system throughput.</p>
              <details><summary>Read more</summary><p>This work studies the systems challenges of deploying mixture-of-experts language models on resource-constrained edge servers, combining model-side and system-side optimizations.</p></details>
              <div class="research-links">Paper link to be added</div>
            </div>
          </article>
          <article class="research-item">
            <div class="research-cover"><strong>Power of<br>Imbalance</strong><small>Networked systems</small></div>
            <div class="research-body">
              <div class="research-meta"><span>arXiv Preprint</span><span>Preprint</span></div>
              <h3>Power of Imbalance</h3>
              <p class="research-authors">Congwei Zhang et al.</p>
              <p>A research project investigating the role of imbalance in networked and distributed systems.</p>
              <details><summary>Read more</summary><p>This work is presented as an arXiv preprint, not as an accepted conference or journal publication. Full bibliographic details will be added after verification.</p></details>
              <div class="research-links">arXiv link to be added</div>
            </div>
          </article>
        </div>
        <p class="section-footnote">Selected works are manually curated and ordered. Each paper has an independent folder in the repository.</p>
    design:
      columns: "1"
  - block: content-collection
    id: recent-news
    content:
      title: "News"
      page_type: news
      count: 5
      sort_by: Date
      order: desc
    design:
      view: list
      columns: 1
      show_date: true
      show_read_more: false
  - block: content-collection
    id: research-projects
    content:
      title: "Research Projects"
      page_type: projects
      count: 4
      sort_by: Date
      order: desc
    design:
      view: card
      columns: 2
      show_date: false
      show_read_more: true
---
