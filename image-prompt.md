# Image Prompt for Memories From URLs Repository

## Primary Prompt (Architecture Illustration)

```
A modern tech illustration showing a data pipeline architecture for news/article extraction. 
The image should depict: on the left side, multiple RSS feed icons and URL links flowing into 
a central processing hub; in the middle, a stylized server or cloud icon with gears representing 
content cleaning and readability extraction (removing ads, scripts, navigation); on the right 
side, clean text blocks being delivered as output. Use a professional color scheme with blues, 
teals, and whites. Include subtle visual elements like code brackets, network nodes, and data 
streams. The overall style should be clean, minimal, and tech-oriented — suitable for a GitHub 
repository hero image. No text or labels in the image.
```

## Alternative Prompt (Abstract/Artistic)

```
An abstract digital illustration representing web content extraction and processing. Show flowing 
lines of complex, cluttered data (with scattered symbols representing ads, scripts, navigation 
elements) entering a filter or funnel in the center, and clean, organized text streams emerging 
from the other side. Use a gradient color palette transitioning from dark/chaotic on the left to 
bright/orderly on the right. Modern flat design style with subtle geometric patterns. Professional 
and minimalist aesthetic for a developer tool.
```

---

## Usage Tips

| Tool | Additional Parameters |
|------|----------------------|
| DALL-E 3 | Use primary prompt as-is |
| Midjourney | Add `--ar 16:9 --v 6` for high-quality landscape |
| Stable Diffusion | Add negative prompts: "text, watermark, blurry, low quality" |

---

## About This Project

**Memories From URLs** is a hybrid news pipeline that:
- Extracts article content from RSS feeds and direct URLs
- Cleans HTML (removes scripts, styles, ads, navigation)
- Uses Mozilla Readability (Node.js) or Scrapling (Python) for content extraction
- Sends processed text to a callback/webhook endpoint
- Supports both batch and streaming processing modes

### Tech Stack
- **Node.js**: Express + Axios + JSDOM + @mozilla/readability
- **Python**: FastAPI + Pydantic + Feedparser + Scrapling + httpx + Uvicorn
