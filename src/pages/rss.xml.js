import { getCollection } from 'astro:content';

function escapeXml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

export async function GET(context) {
  const posts = await getCollection('posts', ({ data }) => !data.draft);
  posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

  const site = context.site?.toString() ?? 'https://www.feilong.eu.org';
  const items = posts
    .map((post) => {
      const url = new URL(`/posts/${post.slug}/`, site).toString();
      const description = escapeXml(post.data.description ?? '');
      const title = escapeXml(post.data.title);
      const pubDate = post.data.date.toUTCString();
      return [
        '    <item>',
        `      <title>${title}</title>`,
        `      <link>${url}</link>`,
        `      <guid>${url}</guid>`,
        `      <pubDate>${pubDate}</pubDate>`,
        `      <description>${description}</description>`,
        '    </item>',
      ].join('\n');
    })
    .join('\n');

  const xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<rss version="2.0">',
    '  <channel>',
    '    <title>飞龙</title>',
    '    <description>飞龙博客最新文章</description>',
    `    <link>${site}</link>`,
    '    <language>zh-CN</language>',
    items,
    '  </channel>',
    '</rss>',
  ].join('\n');

  return new Response(xml, {
    headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' },
  });
}
