import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import test from 'node:test';
import assert from 'node:assert/strict';

const repoRoot = resolve(import.meta.dirname, '..');

test('rss and sitemap entrypoints exist', () => {
  assert.equal(existsSync(resolve(repoRoot, 'src/pages/rss.xml.js')), true);
  assert.equal(existsSync(resolve(repoRoot, 'src/pages/sitemap-index.xml.js')), true);
  assert.equal(existsSync(resolve(repoRoot, 'src/pages/sitemap-0.xml.js')), true);
});

test('layout exposes rss navigation link', () => {
  const layout = readFileSync(resolve(repoRoot, 'src/layouts/Layout.astro'), 'utf8');
  assert.match(layout, /href="\/rss\.xml"/);
});

test('sitemap endpoint references the generated sitemap page', () => {
  const sitemapIndex = readFileSync(resolve(repoRoot, 'src/pages/sitemap-index.xml.js'), 'utf8');
  assert.match(sitemapIndex, /sitemap-0\.xml/);
});

test('built rss and sitemap files exist after build', () => {
  assert.equal(existsSync(resolve(repoRoot, 'dist/rss.xml')), true);
  assert.equal(existsSync(resolve(repoRoot, 'dist/sitemap-index.xml')), true);
  assert.equal(existsSync(resolve(repoRoot, 'dist/sitemap-0.xml')), true);
});
