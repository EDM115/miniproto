# AI Agents guidelines

- `miniproto` is in heavy alpha development. What is referred to as "v1" so far will be the first publicly released version, likely as `0.1.0`. In this regard, breaking changes are accepted and even expected, as long as they're precised.
- Performance is the absolute key in this project, speedups are the primary goal
- The main developer (`EDM115`) might be wrong. AI Agents might be wrong. Authoritative sources are either official Telegram documentations or other referenced projects.
- Do not wrap commands whose live output or running session may need to be polled with RTK. Invoke `uv`, `cargo`, and `pnpm` directly, keep RTK for bounded commands such as `rg`, `curl`, `git` and PowerShell scriptlets.
