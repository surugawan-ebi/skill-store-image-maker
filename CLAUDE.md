# Claude Code Instructions

<!-- BEGIN managed:initialize-managed-repo:claude -->
<!-- version: 1; body-sha256: 49180cc3acf371a0c35f477e828d29f1670836956973c509878dec749f6b7a34 -->
作業開始前に、このrepoの`AGENTS.md`を全文読み、上位workspaceの`AGENTS.md`がある場合は併用する。

- プロジェクト固有の正本、既存差分、秘密情報、本番保護を優先する。
- 最上位モデル、サブエージェント委譲、Codexとのcross-review、Git公開依頼の詳細規約は`AGENTS.md`を正本とする。
- 実質的な変更では、可能かつ安全ならCodexへ独立レビューを依頼し、結果を自身でも検証する。
- pushだけの依頼へ無断でPRを追加せず、commit、push、PR、release、deployは明示された範囲だけ実行する。
<!-- END managed:initialize-managed-repo:claude -->

<!-- BEGIN managed:github-access-policy-bridge:v1 -->
## GitHub access bridge

GitHubのclone／fetch／pull／push、PR操作、認証fallbackでは、`AGENTS.md`の「GitHubアクセスの標準経路」を必ず適用する。Claude CodeでもGit transportはSSH、PR操作は認証済み`gh`を標準とし、connector失敗時にHTTPS credentialを場当たり的に変更しない。
<!-- END managed:github-access-policy-bridge:v1 -->
