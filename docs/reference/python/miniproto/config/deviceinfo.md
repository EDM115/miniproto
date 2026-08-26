---
title: "miniproto.config.DeviceInfo"
description: "Application and device identity sent when initializing a Telegram session."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.config.DeviceInfo"
source_path: "src/miniproto/config.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/config.py#L60"
aliases: ["miniproto.DeviceInfo"]
module: "miniproto.config"
---

## `miniproto.config.DeviceInfo`

```python
DeviceInfo(device_model: str = 'miniproto', system_version: str = 'unknown', app_version: str = '0.1.0', lang_code: str = 'en', system_lang_code: str = 'en') -> None
```

Application and device identity sent when initializing a Telegram session.

Defaults identify this library without probing the host system; callers may supply platform-specific values when Telegram-facing metadata must be customized.

**Attributes:**

- [**device_model**](#miniproto.config.DeviceInfo.device_model) (<code>[str](#str)</code>) – Human-readable device model sent in Telegram initialization, defaulting to ``"miniproto"``.
- [**system_version**](#miniproto.config.DeviceInfo.system_version) (<code>[str](#str)</code>) – Operating-system version label sent to Telegram, defaulting to ``"unknown"``.
- [**app_version**](#miniproto.config.DeviceInfo.app_version) (<code>[str](#str)</code>) – Application version label sent to Telegram, defaulting to ``"0.1.0"``.
- [**lang_code**](#miniproto.config.DeviceInfo.lang_code) (<code>[str](#str)</code>) – Preferred interface language code, defaulting to ``"en"``.
- [**system_lang_code**](#miniproto.config.DeviceInfo.system_lang_code) (<code>[str](#str)</code>) – Device system language code, defaulting to ``"en"``.
