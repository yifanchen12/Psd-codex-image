# Security Policy / 安全政策

## English

### Supported versions

Security fixes are provided for the latest version on the default branch. Older snapshots may not receive fixes.

### Reporting a vulnerability

Please do not disclose credentials, private artwork, or an unpatched vulnerability in a public issue. If GitHub private vulnerability reporting is enabled for this repository, use it. Otherwise, contact the repository maintainers privately through GitHub and include a concise reproduction, affected file/version, impact, and any suggested mitigation. Do not include passwords, API keys, access tokens, or unrelated personal data in the report.

There is no guaranteed response-time SLA. We will acknowledge reports when practical, investigate reproducible issues, and coordinate public disclosure after a fix or mitigation is available.

### Safe use and data handling

- The bundled builder runs locally and does not make network requests. It reads image paths named in the manifest and writes only to the explicitly supplied output/preview paths.
- Review manifests and image sources before running them. A manifest can reference any local path available to the user account; do not run manifests from untrusted sources without checking those paths.
- Do not commit passwords, API keys, access tokens, private user data, or confidential source artwork.
- Keep Python and Pillow up to date, and only use image files you are authorized to process.
- Image-generation prompts and outputs may be sent to the provider configured by the active Codex runtime. Do not include confidential information unless that provider and workflow are approved for it.

## 中文

### 支持范围

安全修复面向默认分支上的最新版本。较旧快照不保证获得修复。

### 漏洞报告

请勿在公开 issue 中披露凭据、私人作品或尚未修复的漏洞。如果本仓库启用了 GitHub 私密漏洞报告，请使用该入口；否则请通过 GitHub 私下联系维护者，并提供简明复现步骤、受影响文件/版本、影响范围和可能的缓解办法。报告中不要附带密码、API 密钥、访问令牌或无关个人信息。

本项目不承诺固定响应时限。维护者会在可行时确认收到报告、调查可复现问题，并在修复或缓解方案可用后协调公开披露。

### 安全使用与数据处理

- 附带的构建脚本在本机运行，不主动发起网络请求；它读取清单中指定的图像路径，并只写入命令行明确指定的 PSD/预览路径。
- 运行前检查清单和图像来源。清单可以引用当前账户有权访问的任意本地路径；对来源不可信的清单，先审阅路径再运行。
- 不要提交密码、API 密钥、访问令牌、私人用户数据或保密源素材。
- 保持 Python 与 Pillow 更新，并只处理你有权使用的图像文件。
- 图像生成提示词和生成结果可能会发送至当前 Codex 运行环境配置的服务提供方。未经授权，不要放入保密信息。
