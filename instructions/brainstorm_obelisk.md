# Brainstorm — Project Obelisk

Resumo prático e passos para transformar a ideia "Jarvis local" em um projeto seguro e operacional.

## Objetivo
Criar um agente multimodal para Windows com:
- Visão computacional (captura de tela, OCR, detecção de UI);
- Interação com aplicações (mouse, teclado, automações, integração PowerShell/Win32);
- Capacidade de receber comandos de alto nível ("faça isso:") e decompor em tarefas executáveis;
- Fluxo controlado de auto-update com assinatura e revisão humana.

## Componentes principais
- Percepção: captura de tela, OCR (Tesseract / serviço), CV (OpenCV, detectors), heurísticas Win32/UIA.
- NLU & Planner: LLM para decomposição de comandos + planejador simbólico para ações atômicas.
- Executor: camada de automação (PyAutoGUI, win32api, PowerShell); modos: dry-run, sandbox, execução controlada.
- Updater: pipeline com builds assinados, testes automáticos e aprovação humana.
- Observabilidade: logs imutáveis, telemetria opcional e histórico versionado.

## Segurança e governança
- Sempre pedir confirmação para ações destrutivas.
- Whitelist de aplicativos e diretórios para acesso automatizado.
- Roles: `user`, `admin`, `dev` com permissões diferentes.
- Logs auditáveis com hashes e timestamps.

## Roadmap (MVP)
1. Especificação de segurança e políticas.
2. Protótipo que recebe "faça isso:" e gera um plano (sem executar).
3. Executor não-privilegiado com dry-run e simulações em VM/sandbox.
4. Fluxo de update com assinatura e revisão humana.
5. Expansão: visão avançada, integração com apps locais e melhorias de planner.

## Riscos e mitigação
- Atualizações automáticas sem controle → mitigação: assinatura + revisão humana.
- Escalada de privilégios/mal-uso remoto → mitigação: regras de rede, feature flags, desvincular execução privilegiada.
- Comandos ambíguos → mitigação: decomposição iterativa e confirmação do usuário.

## Entregáveis imediatos
- `instructions/brainstorm_obelisk.md` (este arquivo)
- Templates: `doc_policy.json`, `doc_roles.json`, `doc_update_flow.json`
- Protótipo CLI (modo dry-run) — sugerido como próximo artefato.

---
