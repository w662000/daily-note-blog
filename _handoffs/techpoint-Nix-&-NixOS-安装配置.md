---
layout: default
title: 技术点 · Nix & NixOS 安装配置
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Nix & NixOS 安装配置

> 来源：261010_Nix & NixOS 安装配置_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- title: "Nix & NixOS 安装配置"
- description: "使用 Nix 安装和部署 Hermes Agent——从快速 `nix run` 到完全声明式的 NixOS 模块（含容器模式）"
- | **`nix run` / `nix profile install`** | 任意 Nix 用户（macOS、Linux） | 包含所有依赖的预构建二进制文件——然后使用标准 CLI 工作流 |
- | **NixOS 模块（原生）** | NixOS 服务器部署 | 声明式配置、加固的 systemd 服务、托管密钥 |
- `curl | bash` 安装程序自行管理 Python、Node 及依赖项。Nix flake 替代了所有这些——每个 Python 依赖都是由 [uv2nix](https://github.com/pyproject-nix/uv2nix) 构建的 Nix derivation，运行时工具（Node.js、git、ripgrep、ffmpeg）已封装进二进制文件的 PATH 中。不需要运行时 pip，不需要激活 venv，不需要 `npm install`。
- **对于非 NixOS 用户**，这只影响安装步骤。之后的操作（`hermes setup`、`hermes gateway install`、编辑配置）与标准安装完全相同。
- **对于 NixOS 模块用户**，整个生命周期有所不同：配置存放在 `configuration.nix` 中，密钥通过 sops-nix/agenix 管理，服务是一个 systemd 单元，CLI 配置命令被屏蔽。管理 hermes 的方式与管理其他 NixOS 服务相同。
- **API 密钥**，用于你想使用的服务（至少需要一个 OpenRouter 或 Anthropic 密钥）
- ```
# 直接运行（首次使用时构建，之后使用缓存）
nix run github:NousResearch/hermes-agent -- setup
nix run github:NousResearch/hermes-agent -- chat

# 或持久化安装
nix profile install github:NousResearch/hermes-agent
hermes setup
hermes chat
```
- 执行 `nix profile install` 后，`hermes`、`hermes-agent` 和 `hermes-acp` 将出现在你的 PATH 中。之后的工作流与[标准安装](./installation.md)完全相同——`hermes setup` 引导你完成提供商选择，`hermes gateway install` 设置 launchd（macOS）或 systemd 用户服务，配置存放在 `~/.hermes/`。
- ```
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
nix build
./result/bin/hermes setup
```
- 该 flake 导出 `nixosModules.default`——一个完整的 NixOS 服务模块，以声明式方式管理用户创建、目录、配置生成、密钥、文档和服务生命周期。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）

## 6、部署状态
模块支持两种模式，由 `container.enable` 控制：

| | **原生**（默认） | **容器** |
|---|---|---|
| 运行方式 | 主机上加固的 systemd 服务 | 持久化 Ubuntu 容器，`/nix/store` 以只读方式绑定挂载 |
| 安全性 | `NoNewPrivileges`、`ProtectSystem=strict`、`PrivateTmp` | 容器隔离，内部以非特权用户运行 |
| Agent 可自行安装包 | 否——仅限 Nix 提供的 PATH 上的工具 | 是——`apt`、`pip`、`npm` 安装的包在重启后持久保留 |
| 配置界面 | 相同 | 相同 |
| 适用场景 | 标准部署、最高安全性、可重现性 | Agent 需要运行时安装包、可变环境、实验性工具 |

启用容器模式只需添加一行：

```nix
{
  services.hermes-agent = {
    enable = true;
    container.enable = true;
    # ... 其余配置相同
  };
}
```

:::info
容器模式通过 `mkDefault` 自动启用 `virtualisation.docker.enable`。如果你使用 Podman，请设置 `container.backend = "podman"` 并将 `virtualisation.docker.enable` 设为 `false`。
:::

---
