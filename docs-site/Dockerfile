FROM node:26-alpine AS dependencies

ENV PNPM_HOME=/pnpm
ENV PATH="${PNPM_HOME}:${PNPM_HOME}/bin:/workspace/docs-site/node_modules/.bin:${PATH}"
WORKDIR /workspace

RUN wget -qO- https://get.pnpm.io/install.sh | ENV="$HOME/.shrc" SHELL="$(which sh)" sh -

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

FROM alpine:3 AS artifact

WORKDIR /site
COPY docs-site/dist/ ./
RUN test -f index.html && test -f start/installation/index.html && test -f pagefind/pagefind.js && ! grep -q 'href="/miniproto/' index.html

FROM nginxinc/nginx-unprivileged:stable-alpine AS runtime-base

LABEL org.opencontainers.image.authors="EDM115 <docker@edm115.dev>"
LABEL org.opencontainers.image.base.name="nginxinc/nginx-unprivileged:stable-alpine"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/EDM115/miniproto.git"
LABEL org.opencontainers.image.title="miniproto documentation"
LABEL org.opencontainers.image.url="https://miniproto.edm115.dev"

COPY docs-site/nginx.conf /etc/nginx/conf.d/default.conf

USER 101
EXPOSE 6743
STOPSIGNAL SIGQUIT
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD wget -q -O /dev/null http://127.0.0.1:6743/ || exit 1

CMD ["nginx", "-g", "daemon off;"]

FROM runtime-base AS source-runtime

COPY --from=builder --chown=101:101 /workspace/docs-site/dist/ /usr/share/nginx/html/

FROM runtime-base AS runtime

COPY --from=artifact --chown=101:101 /site/ /usr/share/nginx/html/
