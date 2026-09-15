// zai_openai_proxy.mjs — OpenAI-compatible proxy -> z-ai-web-dev-sdk.
//
// Recreates the M17 AI-Scientist wiring (research/ai_scientist_trial/
// README.md) so SakanaAI/AI-Scientist v1 runs on the local backend with
// no external API keys:
//
//   bun zai_openai_proxy.mjs [port]          # default 8787
//   OPENAI_API_KEY=any OPENAI_BASE_URL=http://127.0.0.1:8787/v1 \
//     python ai_scientist/generate_ideas.py --experiment bioelectric_fidelity
//
// Needs the SDK resolvable from this directory:
//   scripts/node_modules/z-ai-web-dev-sdk -> the bun global install
// (see scripts/bootstrap_sdk.sh; falls back to the global path below).
//
// Endpoints: POST /v1/chat/completions (stream + non-stream),
// GET /v1/models. Retries 4x with backoff on SDK errors.
import http from "node:http";
import ZAI from "z-ai-web-dev-sdk";

const PORT = Number(process.argv[2] || process.env.PORT || 8787);
const MAX_RETRIES = Number(process.env.PROXY_RETRIES || 6);
// Pacing: minimum gap between SDK calls (the backend 429s under
// rapid consecutive requests; ~43% of the AI-Scientist's idea calls
// were lost before this landed).
const MIN_GAP_MS = Number(process.env.PROXY_MIN_GAP_MS || 2500);

let zai = null;
let nextAllowed = 0;
const gate = (ms) => new Promise((r) => setTimeout(r, ms));

async function sdk() {
  if (!zai) zai = await ZAI.create();
  return zai;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function complete(messages, temperature) {
  let lastErr;
  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
      const wait = nextAllowed - Date.now();
      if (wait > 0) await gate(wait);
      nextAllowed = Date.now() + MIN_GAP_MS;
      const c = await (await sdk()).chat.completions.create({
        messages,
        thinking: { type: "disabled" },
        ...(temperature != null ? { temperature } : {}),
      });
      const text = c.choices?.[0]?.message?.content;
      if (typeof text !== "string" || !text.trim()) {
        throw new Error("empty completion");
      }
      return text;
    } catch (e) {
      lastErr = e;
      const is429 = /429|Too many|rate/i.test(String(e.message));
      const backoff = is429 ? 8000 * attempt : 1500 * attempt;
      console.error(`[proxy] attempt ${attempt}/${MAX_RETRIES} failed `
        + `(${is429 ? "rate" : "err"}), backoff ${backoff}ms: `
        + `${e.message}`);
      if (attempt < MAX_RETRIES) await sleep(backoff);
    }
  }
  throw lastErr;
}

function sseChunks(model, text) {
  const id = `chatcmpl-${Date.now()}`;
  const created = Math.floor(Date.now() / 1000);
  const frames = [];
  frames.push(`data: ${JSON.stringify({
    id, object: "chat.completion.chunk", created, model,
    choices: [{ index: 0, delta: { role: "assistant", content: "" }, finish_reason: null }],
  })}\n\n`);
  // chunk the text so streaming clients see progress
  const CH = 160;
  for (let i = 0; i < text.length; i += CH) {
    frames.push(`data: ${JSON.stringify({
      id, object: "chat.completion.chunk", created, model,
      choices: [{ index: 0, delta: { content: text.slice(i, i + CH) }, finish_reason: null }],
    })}\n\n`);
  }
  frames.push(`data: ${JSON.stringify({
    id, object: "chat.completion.chunk", created, model,
    choices: [{ index: 0, delta: {}, finish_reason: "stop" }],
  })}\n\n`);
  frames.push("data: [DONE]\n\n");
  return frames.join("");
}

const server = http.createServer(async (req, res) => {
  if (req.method === "GET" && (req.url === "/v1/models" || req.url === "/models")) {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({
      object: "list",
      data: [{ id: "zai-gpt-4o-proxy", object: "model", owned_by: "zai" }],
    }));
    return;
  }
  if (req.method === "POST" && /\/v1\/chat\/completions$/.test(req.url)) {
    let body = "";
    for await (const chunk of req) body += chunk;
    let spec;
    try {
      spec = JSON.parse(body);
    } catch {
      res.writeHead(400, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: { message: "invalid JSON" } }));
      return;
    }
    const model = spec.model || "zai-proxy";
    const messages = Array.isArray(spec.messages) ? spec.messages : [];
    try {
      const text = await complete(messages, spec.temperature);
      if (spec.stream) {
        res.writeHead(200, {
          "Content-Type": "text/event-stream",
          "Cache-Control": "no-cache",
          Connection: "keep-alive",
        });
        res.end(sseChunks(model, text));
      } else {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({
          id: `chatcmpl-${Date.now()}`,
          object: "chat.completion",
          created: Math.floor(Date.now() / 1000),
          model,
          choices: [{
            index: 0,
            message: { role: "assistant", content: text },
            finish_reason: "stop",
          }],
          usage: {
            prompt_tokens: Math.ceil(JSON.stringify(messages).length / 4),
            completion_tokens: Math.ceil(text.length / 4),
            total_tokens: Math.ceil((JSON.stringify(messages).length + text.length) / 4),
          },
        }));
      }
    } catch (e) {
      console.error(`[proxy] request failed: ${e.message}`);
      res.writeHead(502, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: { message: e.message, type: "proxy_error" } }));
    }
    return;
  }
  res.writeHead(404, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ error: { message: `no route: ${req.method} ${req.url}` } }));
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`[proxy] z-ai OpenAI-compatible proxy on http://127.0.0.1:${PORT}/v1`);
});
