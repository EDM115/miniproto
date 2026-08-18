# syntax=docker/dockerfile:1.7

FROM node:26.7.0-alpine3.24 AS dependencies

ENV PNPM_HOME=/pnpm
ENV PATH=${PNPM_HOME}:${PATH}
WORKDIR /workspace

RUN npm install --global pnpm@11.22.0

COPY docs-site/package.json docs-site/pnpm-lock.yaml docs-site/pnpm-workspace.yaml ./docs-site/
RUN --mount=type=cache,id=miniproto-docs-pnpm,target=/pnpm/store pnpm config set store-dir /pnpm/store && pnpm --dir docs-site install --frozen-lockfile

FROM dependencies AS builder

ARG MINIPROTO_DOCS_SITE=http://localhost
ENV MINIPROTO_DOCS_SITE=${MINIPROTO_DOCS_SITE}
ENV MINIPROTO_DOCS_BASE=/
ENV NODE_OPTIONS=--max-old-space-size=1536
ENV ASTRO_TELEMETRY_DISABLED=1

COPY docs/ ./docs/
COPY docs-site/ ./docs-site/
RUN pnpm --dir docs-site build

FROM alpine:3.24 AS artifact

WORKDIR /site
COPY docs-site/dist/ ./
RUN test -f index.html && test -f start/installation/index.html && test -f pagefind/pagefind.js && ! grep -q 'href="/miniproto/' index.html

FROM nginxinc/nginx-unprivileged:1.31.3-alpine3.24 AS runtime-base

LABEL org.opencontainers.image.source="https://github.com/EDM115/miniproto"
LABEL org.opencontainers.image.description="Root-hosted miniproto documentation"

COPY docs-site/nginx.conf /etc/nginx/conf.d/default.conf

USER 101
EXPOSE 8080
STOPSIGNAL SIGQUIT
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD wget -q -O /dev/null http://127.0.0.1:8080/ || exit 1

CMD ["nginx", "-g", "daemon off;"]

FROM runtime-base AS source-runtime

COPY --from=builder --chown=101:101 /workspace/docs-site/dist/ /usr/share/nginx/html/

FROM runtime-base AS runtime

COPY --from=artifact --chown=101:101 /site/ /usr/share/nginx/html/
