import type { CollectionEntry } from "astro:content";

export const tagSlug = (tag: string) => tag.toLowerCase().replace(/\s+/g, "-");

/** Every tag in use, with its post count, busiest first. */
export function tagCounts(posts: CollectionEntry<"posts">[]) {
  const counts = new Map<string, number>();
  for (const post of posts) {
    for (const tag of post.data.tags) counts.set(tag, (counts.get(tag) ?? 0) + 1);
  }
  return [...counts.entries()]
    .map(([tag, count]) => ({ tag, count, slug: tagSlug(tag) }))
    .sort((a, b) => b.count - a.count || a.tag.localeCompare(b.tag));
}
