// gta6-meme-x-01 — entrypoint for "Post a GTA 6 meme on X".
//
// The entry itself is the X post: this program just carries the post's
// address (POST.json) into the kit's output directory, unchanged, so the
// grader can read it. The meme image (meme.png) and the script that drew
// its captions (compose_meme.py) live beside this file in the repo.
//
// The post this entry names is the @jajbavn post of the GTA VI launch-day
// sick-day meme: the whole office called in sick, the make.fun ghost
// stayed at its desk playing in Vice City. The program refuses to run
// when POST.json does not name a real X status URL, so a placeholder can
// never be entered by mistake.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const postPath = join(botDir, "POST.json");
const raw = readFileSync(postPath, "utf8");
const post = JSON.parse(raw) as { url?: unknown };

if (typeof post.url !== "string") {
  throw new Error('POST.json must name the X post under its "url" field');
}
const address = new URL(post.url);
const isXPost =
  (address.hostname === "x.com" || address.hostname === "twitter.com") &&
  /^\/[^/]+\/status\/\d+$/.test(address.pathname);
if (!isXPost) {
  throw new Error(`POST.json does not name an X status URL: ${post.url}`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "POST.json"), raw);
console.log(`entry post: ${post.url}`);
