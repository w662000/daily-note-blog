---
layout: default
title: 交接文档 · Domestic Tech Research
date: 2026-10-13 23:30:00 +0800
---

# Domestic Tech Research

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\domestic-tech-research\SKILL.md

---
name: domestic-tech-research
category: research
description: Research and analysis of AI/ML content on Chinese domestic tech platforms, with focus on emerging AI frameworks and tools like Hermes Agent.
---

# Domestic Tech Research

Research and analysis of AI/ML content on Chinese domestic tech platforms, with focus on emerging AI frameworks and tools like Hermes Agent.

## Trigger Conditions
- User asks to search/research content on Chinese domestic tech platforms (CSDN, 掘金, 知乎, B站, etc.)
- User wants to understand AI tool adoption and usage patterns in Chinese tech community
- User needs comprehensive analysis of specific AI frameworks across multiple platforms
- User wants to identify popular tutorials, projects, and learning resources

## Workflow

### 1. Platform Research Planning
- Identify relevant Chinese domestic tech platforms
- Understand each platform's API/research limitations
- Plan search strategy to maximize data collection

### 2. Multi-Platform Search Execution
- Create search scripts targeting multiple platforms
- Handle API restrictions and anti-bot measures
- Collect structured data from successful searches

### 3. Data Processing and Analysis
- Parse large JSON datasets from platforms
- Extract key metrics (view counts, author info, publication dates)
- Identify common themes and application patterns

### 4. Content Categorization
- Separate tutorials from opinion pieces
- Identify practical projects vs theoretical discussions
- Categorize by skill level (beginner vs advanced)

### 5. Recommendation Generation
- Filter and rank content by popularity and relevance
- Create learning paths for different user types
- Generate actionable recommendations

## Key Techniques

### Search Script Creation
```python
# Multi-platform search script structure
def search_platform(keyword, platform_func):
    """Generic platform search wrapper"""
    try:
        result = platform_func(keyword)
        if result:
            return process_result(result)
        else:
            return {"error": f"Search failed for {platform}"}
    except Exception as e:
        return {"error": str(e)}
```

### Handling Platform Restrictions
- **CSDN**: Use official API with proper headers
- **掘金**: Use search API with rate limiting
- **知乎**: API often blocked, need alternative approaches
- **B站**: Strict anti-bot measures, limited data access
- **GitHub**: Use search API with language filters
- **小红书**: Service frequently returns 500 errors

### Data Analysis Pipeline
1. **JSON Parsing**: Handle large datasets efficiently
2. **Metrics Extraction**: Extract view counts, author info, dates
3. **Theme Identification**: Use keyword frequency analysis
4. **Popularity Scoring**: Weight by views, likes, downloads

### Recommendation Filtering
- **Quality Score**: Based on engagement metrics
- **Relevance**: Match to user's specific needs
- **Freshness**: Prioritize recent content
- **Accessibility**: Consider implementation complexity

## Pitfalls

### Platform Limitations
- **CSDN**: API rate limiting, commercial content mixed with free content
- **掘金**: Search results often empty or limited
- **知乎**: Strong anti-bot measures, API frequently blocked
- **B站**: 412 errors for automated searches
- **GitHub**: SSL errors can occur, need retry logic
- **小红书**: Consistent 500 server errors

### Data Quality Issues
- Duplicate content across platforms
- Inconsistent metadata formats
- Missing publication dates
- Author information may be incomplete
- View counts may be inflated or unreliable

### Analysis Challenges
- Chinese text requires proper encoding handling
- Platform-specific HTML tags need cleaning
- Date formats vary between platforms
- Some platforms return empty results for technical terms

## References

See `references/chinese-tech-research-methodology.md` for detailed platform-specific research techniques and data processing patterns.

## Templates

- `templates/search_script.py` - Multi-platform search script template
- `templates/data_parser.py` - JSON data processing template
- `templates/recommendation_generator.py` - Content recommendation template

## Scripts

- `scripts/analyze_search_results.py` - Analyze collected search data
- `scripts/generate_report.py` - Generate comprehensive research reports
- `scripts/filter_content.py` - Filter and rank content by quality
