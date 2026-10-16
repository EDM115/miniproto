# AI Agents guidelines

- `miniproto` is in heavy alpha development. What has been referred to as "v1" so far will be the first publicly released version as `0.1.0`. In this regard, breaking changes are accepted and even expected, as long as they're specified.
- Performance is the absolute key in this project, speedups are the primary goal
- The main developer (`EDM115`) might be wrong. AI Agents might be wrong. Authoritative sources are either official Telegram documentations or to some extend other referenced projects.
- Do not add tests that validate something else than intended behavior, ex checking if a file contains exactly these words
- Group related tests in the existing files for their feature or component, do not create test files named after a review, finding number, or other temporary context, create a new file only when no existing file fits and give it a descriptive feature or category name
