import rss from "@astrojs/rss";
import { getListedPosts, postHref } from "../lib/posts";
import { SITE } from "../config";

export async function GET(context) {
  const posts = await getListedPosts();
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
        link: postHref(post),
      })),
  });
}
