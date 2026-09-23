import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import { SITE } from "../config";

export async function GET(context) {
  const posts = await getCollection("posts", ({ data }) => !data.draft);
  return rss({
    title: SITE.title,
    description: SITE.description,
    site: context.site ?? SITE.url,
    items: posts
      .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf())
      .map((post) => ({
        title: post.data.title,
        description: post.data.dek,
        pubDate: post.data.pubDate,
        link: `/writing/${post.id}/`,
      })),
  });
}
