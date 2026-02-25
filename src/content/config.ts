import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).optional().default([]),
    description: z.string().optional(),
    draft: z.boolean().optional().default(false),
  }),
});

const links = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    url: z.string().url(),
    date: z.coerce.date(),
    type: z.enum(['article', 'link']).default('link'),
    image: z.string().optional(),
    description: z.string().optional(),
  }),
});

export const collections = { posts, links };
