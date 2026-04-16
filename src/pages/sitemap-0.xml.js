import { getCollection } from 'astro:content';

function xmlEscape(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

const site = 'https://www.feilong.eu.org';

export async function GET() {
  const posts = await getCollection('posts', ({ data }) => !data.draft);
  posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

  const staticUrls = ['/', '/about/', '/links/', '/tags/'];
  const tagUrls = Array.from(new Set(posts.flatMap((post) => post.data.tags ?? [])))
    .sort((a, b) => a.localeCompare(b, 'zh-CN'))
    .map((tag) => `/tags/${encodeURIComponent(tag)}/`);
  const postUrls = posts.map((post) => `/posts/${post.slug}/`);

  const urls = [...staticUrls, ...tagUrls, ...postUrls];
  const xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ...urls.map((path) => [
      '  <url>',
      `    <loc>${xmlEscape(new URL(path, site).toString())}</loc>`,
      '  </url>',
    ].join('\n')),
    '</urlset>',
  ].join('\n');

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
}
