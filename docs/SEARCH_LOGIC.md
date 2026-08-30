# Search and Selection Logic

## Objective

Return a small, useful set of creator-attributed Pixiv illustrations while balancing popularity, relevance, human authorship, content preferences, and visual diversity.

## Pipeline

1. **Expand the query.** Build Japanese, Simplified Chinese, Traditional Chinese, Korean, and English variants. Include official character names, common transliterations, series names, and canonical Pixiv tags.
2. **Use two discovery channels.** Query both `popular_d` and `date_d`. Popularity finds established work; recency prevents the result set from becoming permanently frozen around older posts.
3. **Deduplicate by artwork ID.** The same work often appears under several language variants.
4. **Read public details.** Retrieve bookmark, like, view, page-count, AI-declaration, and content-rating fields from the official artwork detail endpoint.
5. **Filter declared AI.** Exclude `aiType=2` by default. Treat historical or unspecified values as unknown, not proof of human authorship.
6. **Apply the content preference.** Preserve mature-rated candidates when requested and already visible to the current session. Never bypass Pixiv authentication or safety controls.
7. **Rank candidates.** Sort primarily by bookmark count, then likes and views. Engagement is a discovery signal, not a quality verdict.
8. **Preview a larger pool.** For ten final images, visually inspect roughly 20–40 candidates when practical.
9. **Remove probable unlabelled AI.** Look for inconsistent hands, ornaments, clothing seams, typography, repeated micro-textures, implausible reflections, and high-volume near-duplicate account behavior. Visual inference must be described as uncertain.
10. **Enforce style diversity.** Avoid returning ten similar glamour portraits. Prefer different rendering methods, compositions, skins, moods, eras, and degrees of finish.
11. **Return attribution.** Include title, creator, bookmark snapshot, style note, and official artwork URL.

## Ranking model

The code uses a transparent lexicographic ranking:

```text
bookmark_count descending
like_count descending
view_count descending
```

The agent then performs relevance and diversity selection over the ranked candidate pool. This separation keeps measurable popularity distinct from subjective visual judgment.

## Known limitations

- Popularity order can depend on Pixiv account or subscription state.
- Anonymous search may omit mature or age-gated work.
- Bookmark counts change over time.
- Pixiv's AI declaration is creator/platform metadata and may be absent or incorrect.
- Visual AI detection is probabilistic and should not be presented as a definitive accusation.
- Search endpoints and response fields may change without notice.
