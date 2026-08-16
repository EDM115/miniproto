import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { docsSchema } from '@astrojs/starlight/schema';

const documentationLanguage = z.enum(['python', 'telegram', 'rust']);
const documentationKind = z.enum([
  'alias',
  'attribute',
  'class',
  'constant',
  'constructor',
  'crate',
  'enum',
  'error',
  'field',
  'file',
  'function',
  'index',
  'macro',
  'method',
  'module',
  'property',
  'struct',
  'trait',
  'type',
  'variant',
]);

const sourcePath = z
  .string()
  .min(1)
  .refine((value) => !value.startsWith('/') && !value.includes('\\') && !value.split('/').includes('..'), {
    message: 'source_path must be a non-empty, repository-relative POSIX path.',
  });

const generatedMetadata = z
  .object({
    generated: z.boolean().default(false),
    editUrl: z.union([z.string().min(1), z.literal(false)]).optional(),
    language: documentationLanguage.optional(),
    kind: documentationKind.optional(),
    qualified_name: z.string().min(1).optional(),
    source_path: sourcePath.optional(),
    source_url: z.url().optional(),
    aliases: z.array(z.string().min(1)).default([]),
    module: z.string().min(1).optional(),
    namespace: z.string().min(1).optional(),
    layer: z.number().int().positive().optional(),
    schema_source: z.string().min(1).optional(),
    constructor_id: z.string().regex(/^0x[0-9a-f]{8}$/i).optional(),
    crate: z.string().min(1).optional(),
    python_visible: z.boolean().optional(),
  })
  .superRefine((data, context) => {
    if (!data.generated) return;

    for (const field of ['language', 'kind', 'qualified_name', 'source_path', 'source_url'] as const) {
      if (data[field] === undefined) {
        context.addIssue({
          code: 'custom',
          path: [field],
          message: `Generated documentation requires ${field}.`,
        });
      }
    }

    if (data.editUrl !== false) {
      context.addIssue({
        code: 'custom',
        path: ['editUrl'],
        message: 'Generated documentation must set editUrl to false.',
      });
    }

    if (data.language === 'python' && data.module === undefined) {
      context.addIssue({
        code: 'custom',
        path: ['module'],
        message: 'Generated Python documentation requires module.',
      });
    }

    if (data.language === 'telegram') {
      if (data.layer === undefined) {
        context.addIssue({
          code: 'custom',
          path: ['layer'],
          message: 'Generated Telegram documentation requires layer.',
        });
      }

      if (data.schema_source === undefined) {
        context.addIssue({
          code: 'custom',
          path: ['schema_source'],
          message: 'Generated Telegram documentation requires schema_source.',
        });
      }
    }

    if (data.language === 'rust' && data.crate === undefined) {
      context.addIssue({
        code: 'custom',
        path: ['crate'],
        message: 'Generated Rust documentation requires crate.',
      });
    }
  });

const docs = defineCollection({
  loader: glob({
    base: '../docs',
    pattern: ['**/*.md', '!THOUGHTS.md', '!reference-manifest.json'],
  }),
  schema: docsSchema({ extend: generatedMetadata }),
});

export const collections = { docs };
