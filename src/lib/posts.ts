import { getCollection, type CollectionEntry } from "astro:content";

export const LANGS = ["en", "pt"] as const;
export type Lang = (typeof LANGS)[number];

/** Shown on the toggle. */
export const LANG_LABEL: Record<Lang, string> = { en: "EN", pt: "PT" };

/** What a post opens in when it exists in both languages. */
export const DEFAULT_LANG: Lang = "en";

export type PostEntry = CollectionEntry<"posts">;

export type PostGroup = {
  /** Shared slug — also the URL, since both languages live on one page. */
  slug: string;
  /** Languages this post was actually written in, in LANGS order. */
  langs: Lang[];
  versions: Partial<Record<Lang, PostEntry>>;
  /** The version list pages and metadata read from. */
  primary: PostEntry;
};

const isLang = (value: string): value is Lang => (LANGS as readonly string[]).includes(value);

/** Splits "en/how-this-shop-works" into its language and slug. */
export function parsePostId(id: string): { lang: Lang; slug: string } {
  const [folder, ...rest] = id.split("/");
  if (!isLang(folder) || rest.length === 0) {
    throw new Error(
      `Post "${id}" isn't in a language folder. Move it to src/content/posts/en/ or src/content/posts/pt/.`
    );
  }
  return { lang: folder, slug: rest.join("/") };
}

/** Both languages share a URL, so the language folder drops out of the path. */
export const postHref = (post: PostEntry) => `/writing/${parsePostId(post.id).slug}/`;

/** Published posts, one group per slug, newest first. */
export async function getPostGroups(): Promise<PostGroup[]> {
  const posts = await getCollection("posts", ({ data }) => !data.draft);

  const bySlug = new Map<string, PostGroup>();
  for (const post of posts) {
    const { lang, slug } = parsePostId(post.id);
    const group = bySlug.get(slug) ?? { slug, langs: [], versions: {}, primary: post };
    if (group.versions[lang]) {
      throw new Error(`Two ${lang} posts claim the slug "${slug}".`);
    }
    group.versions[lang] = post;
    bySlug.set(slug, group);
  }

  for (const group of bySlug.values()) {
    group.langs = LANGS.filter((lang) => group.versions[lang]);
    group.primary = group.versions[DEFAULT_LANG] ?? group.versions[group.langs[0]!]!;
  }

  return [...bySlug.values()].sort(
    (a, b) => b.primary.data.pubDate.valueOf() - a.primary.data.pubDate.valueOf()
  );
}

/** The list-page view: one entry per post, in its primary language. */
export async function getListedPosts(): Promise<PostEntry[]> {
  return (await getPostGroups()).map((group) => group.primary);
}
