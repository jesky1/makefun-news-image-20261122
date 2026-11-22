// news-image-20261122 — entry program (Node 22).
// Copies the pre-rendered entry.png shipped in this repository to the
// output directory, after validating it is a real PNG within the size
// limit. No network access; the output is byte-identical on every run.
import {
  closeSync,
  copyFileSync,
  existsSync,
  mkdirSync,
  openSync,
  readSync,
  statSync,
} from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC: readonly number[] = [0x89, 0x50, 0x4e, 0x47];
const MAX_BYTES = 1024 * 1024;

function fail(message: string): never {
  console.error(`error: ${message}`);
  process.exit(1);
}

function checkPng(path: string, label: string): number {
  if (!existsSync(path)) {
    fail(`${label} not found: ${path}`);
  }
  const size = statSync(path).size;
  if (size <= 0 || size > MAX_BYTES) {
    fail(`${label} size ${size} is outside 1..${MAX_BYTES} bytes`);
  }
  const head = new Uint8Array(4);
  const fd = openSync(path, "r");
  try {
    const read = readSync(fd, head, 0, 4, 0);
    if (read !== 4) {
      fail(`${label} is too short to be a PNG`);
    }
  } finally {
    closeSync(fd);
  }
  for (let i = 0; i < 4; i++) {
    if (head[i] !== PNG_MAGIC[i]) {
      fail(`${label} does not start with the PNG signature`);
    }
  }
  return size;
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = resolve(here, "entry.png");
  const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
  const target = join(outDir, "entry.png");

  const size = checkPng(source, "entry.png");
  mkdirSync(outDir, { recursive: true });
  copyFileSync(source, target);
  const written = checkPng(target, "output entry.png");
  if (written !== size) {
    fail(`output size ${written} differs from source size ${size}`);
  }
  console.log(`wrote ${target} (${written} bytes)`);
}

main();
