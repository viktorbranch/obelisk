# 🪨 Project Obelisk

[![Status](https://img.shields.io/badge/status-alpha-orange)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()
[![Language](https://img.shields.io/badge/lang-Python%20%7C%20PowerShell-green)]()

> **Project Obelisk** — agente IA multimodal com visão de tela, controle de mouse/teclado via macros e capacidade de auto-atualização. Interface inicial baseada em texto. Projetado para ser modular, auditável e extensível.

---

## Sumário

- [Visão geral](#visão-geral)
- [Escopo & objetivos](#escopo--objetivos)
- [Funcionalidades (MVP)](#funcionalidades-mvp)
- [Arquitetura](#arquitetura)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Instalação & Execução](#instalação--execução)
- [Configuração](#configuração)
- [Uso básico](#uso-básico)
- [Segurança, ética e privacidade](#segurança-ética-e-privacidade)
- [Testes & CI](#testes--ci)
- [Contribuição](#contribuição)
- [Roadmap](#roadmap)
- [Licença](#licença)
- [Contato](#contato)

---

## Visão geral

Project Obelisk é um agente IA projetado para _ver_ o que acontece na tela do Windows, tomar decisões e executar ações reais usando macros de mouse/teclado. O agente suporta atualizações autônomas controladas e possui uma UI inicial por texto para entrada de comandos.

Objetivos principais:

- Automação assistida por visão (screen understanding).
- Interação com ambiente Windows (input control).
- Atualização segura automatizada.
- Observabilidade e auditabilidade.

---

## Escopo & objetivos

**Não** é objetivo inicial:

- Fazer reconhecimento biométrico sem consentimento.
- Controlar dispositivos em redes externas sem autorização.
- Tornar-se um agente completamente autônomo sem limites humanos.

**Escopo (v1 — MVP)**:

- Captura de tela periódica / por demanda.
- OCR + detecção simples de UI (buttons, campos).
- Macros seguras para executar cliques, digitação e atalhos.
- Mecanismo de auto-update com assinatura/verificação.
- Console/terminal + UI de texto para enviar instruções.

---

## Funcionalidades (MVP)

- 📸 Captura de tela e pipeline básico de visão.
- 🖱️ Macros de mouse (move, click, drag).
- ⌨️ Macros de teclado (send keys, shortcuts).
- 🔁 Auto-update com verificação de integridade.
- 💬 Entrada via terminal/CLI (pronto para extender a GUI).
- 📄 Logs detalhados e arquivo `instructions/doc_index.csv` explicando documentação.

---

## Arquitetura

```mermaid
flowchart LR
  User["Usuário (CLI / Texto)"] -->|comando| Core[Core Agent]
  Core --> Vision[Visão (captura + OCR + CV)]
  Core --> Planner[Planejador de Ações]
  Planner --> Actuator[Atuadores (Macros Mouse/Teclado)]
  Core --> Updater[Auto-Updater (verificação)]
  Core --> Logs[Logs / Telemetria]
  Vision --> Knowledge[Knowledge Base / Heurísticas]
```
