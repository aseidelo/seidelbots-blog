import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const posts = defineCollection({
  // The folder is the language: src/content/posts/<en|pt>/<slug>.md. Two files
  // with the same slug are translations of each other and share one page.
  loader: glob({
    pattern: "**/*.md",
    base: "./src/content/posts",
    generateId: ({ entry }) => entry.replace(/\.md$/, ""),
  }),
  schema: z.object({
    title: z.string(),
    dek: z.string(),
    pubDate: z.coerce.date(),
    category: z.enum(["Essay", "Note"]).default("Essay"),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    /** What this post's icon should show. Defaults to the category. */
    icon: z.string().optional(),
    /** Name of a project in src/data/projects.ts — renders the "Built on this" card. */
    project: z.string().optional(),
  }),
});

export const collections = { posts };
