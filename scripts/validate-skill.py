#!/usr/bin/env python3
"""Static package checks only; run gate behavior is tested separately. --demo-check adds a local build."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
# Codex loads the team skill from this path on the current host. Keep an
# explicit --install-root override for other hosts or CI packaging checks.
DEFAULT_INSTALL=Path.home()/'.codex/skills/yb-mobile-design'
MANAGED={'references','agents','scripts','tests','evals','docs','assets','demo'}
EXCLUDED={'node_modules','dist','dist-ssr','.vite','__pycache__','.git','.vercel'}
REQUIRED=['references/tool-adaptation-contract.md','references/capture-and-validation.md','SKILL.md','agents/openai.yaml','references/index.md','references/yuanbao-mobile-configuration.md','references/input-routing.md',
 'references/prd-design-contract.md','references/live-component-resolution.md','references/evidence-contract.md',
 'references/orchestration-and-completion-gates.md','references/run-record-format.md','references/adaptive-execution-profiles.md','references/layout-quality-gate.md','references/capability-preflight.md',
 'references/interaction-validation.md','references/review-checklist.md','references/missing-component-creation.md',
 'references/component-instance-safety.md','references/state-and-fallback.md','references/design-guidelines.md','references/team-font-configuration.md',
 'references/ai-canvas-and-references.md','references/interaction-patterns.md','references/conversation-content-domain.md',
 'references/mode-existing-design-review.md','references/mode-independent-review.md','references/mode-generation.md','references/mode-iteration.md',
 'references/canvas-organization.md','references/web-demo-delivery.md','references/device-and-canvas-scan.md','references/foundations/index.md',
 'references/experience/experience-decision-contract.md','references/experience/product-experience-model.md','references/experience/task-experience-patterns.md',
 'references/experience/experience-case-contract.md','references/experience/task-simulation-review.md',
 'demo/README.md','docs/usage-guide.md','scripts/validate-run.py','scripts/scaffold-demo.mjs',
 'assets/standalone-web-template/package.json','assets/standalone-web-template/vite.config.ts',
 'assets/standalone-web-template/src/App.tsx','tests/test_run_gate.py','evals/workflow-scenarios.md','evals/experience-quality-scenarios.md']
LINK_RE=re.compile(r'\[[^\]]+\]\(([^)]+)\)')
CJK=re.compile(r'[\u4e00-\u9fff]')
BANNED=re.compile(r'\b(Knot|Coze|Dify|FigmaPartner)\b',re.I)


def managed_files(root):
    return sorted(p.relative_to(root) for p in root.rglob('*') if p.is_file()
                  and not (EXCLUDED & set(p.relative_to(root).parts))
                  and p.name not in {'.DS_Store','code-connect-docs.json','.figma-token','.figma-token.json'}
                  and p.name != '.env' and not p.name.startswith('.env.')
                  and p.suffix not in {'.pyc','.log','.tsbuildinfo'}
                  and not p.is_symlink()
                  and (p.relative_to(root)==Path('SKILL.md') or p.relative_to(root).parts[0] in MANAGED))


def validate(root):
    errors=[]
    for name in REQUIRED:
        if not (root/name).is_file():errors.append('Missing '+name)
    if not (root/'SKILL.md').is_file():return errors
    try:
        font_root=root/'assets/fonts'
        manifest=json.loads((font_root/'manifest.json').read_text())
        expected={'PingFangSC-Regular.otf','PingFangSC-Medium.otf','PingFangSC-Semibold.otf','dinpro_medium.otf'}
        entries=manifest['fonts']
        if len(entries)!=len(expected) or {f['file'] for f in entries}!=expected:
            errors.append('Font manifest file set differs')
        for f in entries:
            if Path(f['file']).name!=f['file']:
                errors.append('Invalid font path');continue
            data=(font_root/f['file']).read_bytes()
            if len(data)!=f['bytes'] or hashlib.sha256(data).hexdigest()!=f['sha256']:
                errors.append('Font checksum mismatch: '+f['file'])
    except (OSError,ValueError,KeyError,TypeError) as e:
        errors.append('Invalid font bundle: '+str(e))
    entry=(root/'SKILL.md').read_text()
    frontmatter=re.match(r'^---\n(.*?)\n---\n',entry,re.S)
    if not frontmatter:errors.append('Invalid frontmatter')
    else:
        block=frontmatter.group(1)
        if not re.search(r'^name: yb-mobile-design$',block,re.M):errors.append('Frontmatter name mismatch')
        if not re.search(r'^description: .+',block,re.M):errors.append('Frontmatter description missing')
    if len(entry.splitlines())>140:errors.append('Entrypoint exceeds 140 lines')
    for p in sorted((root/'references').rglob('*.md')):
        rel=str(p.relative_to(root))
        if rel not in REQUIRED:errors.append('Unlisted reference: '+rel)
    files=[root/'SKILL.md',*sorted((root/'references').rglob('*.md'))]
    graph={}
    for p in files:
        text=p.read_text();graph[p.resolve()]=set()
        if not CJK.search(next((l for l in text.splitlines() if l.startswith('# ')),'')):errors.append(f'Chinese heading missing: {p.name}')
        for raw in LINK_RE.findall(text):
            target=raw.split('#')[0]
            if not target or '://' in target:continue
            dest=(p.parent/target).resolve()
            if not dest.exists():errors.append(f'Broken link: {p.name} -> {raw}')
            graph[p.resolve()].add(dest)
        if re.search(r'(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])',text,re.I):errors.append(f'Component key recipe in {p.name}')
        if re.search(r'(?<![\w])#[0-9a-f]{6}(?:[0-9a-f]{2})?(?![\w])',text,re.I):errors.append(f'Color recipe in {p.name}')
        if re.search(r'P0/P1\s*(?:清零|已完成)',text):errors.append(f'Obsolete completion threshold: {p.name}')
        if BANNED.search(text):errors.append(f'Obsolete workflow platform reference in {p.name}')
    seen=set();pending=[(root/'SKILL.md').resolve()]
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);pending.extend(graph.get(p,()))
    for p in files:
        if p.resolve() not in seen:errors.append(f'Unreachable reference: {p.name}')
    # Maintenance docs and evaluation links also travel with the team package.
    for folder in ['docs','evals']:
        for p in (root/folder).rglob('*.md'):
            for raw in LINK_RE.findall(p.read_text()):
                target=raw.split('#')[0]
                if target and '://' not in target and not (p.parent/target).exists():
                    errors.append(f'Broken link: {p.name} -> {raw}')
    for p in (root/'references').glob('mode-*.md'):
        for heading in ['## 触发','## 允许写入','## 禁止','## 确认点','## 停止']:
            if heading not in p.read_text():errors.append(f'Mode section missing: {p.name}: {heading}')
    ux_eval=root/'evals/experience-quality-scenarios.md'
    if not ux_eval.is_file(): errors.append('Missing evals/experience-quality-scenarios.md')
    elif 'Pairwise' not in ux_eval.read_text() or 'humanPreference' not in ux_eval.read_text():
        errors.append('Experience quality evals must document pairwise human preference data')
    text=(root/'evals/workflow-scenarios.md').read_text()
    numbers=[int(x) for x in re.findall(r'^## (\d+)\.',text,re.M)]
    if len(numbers)<26 or numbers!=list(range(1,len(numbers)+1)):errors.append('Evaluation cases missing or nonsequential')
    routing=(root/'references/input-routing.md').read_text()
    if 'deliverableDecision' not in routing or 'web-demo' not in routing:
        errors.append('Input routing must document deliverableDecision and the web-demo default')
    manifest=(root/'agents/openai.yaml').read_text()
    for field in ['display_name:','short_description:','default_prompt:']:
        if field not in manifest:errors.append('openai.yaml missing interface field: '+field.rstrip(':'))
    if 'dependencies:' not in manifest or 'tools:' not in manifest:
        errors.append('openai.yaml must declare dependencies.tools for the Figma MCP toolchain')
    for tool in ['get_libraries','list_file_components_for_code_connect','search_design_system','get_design_context','get_screenshot']:
        if tool not in manifest:errors.append('openai.yaml missing MCP tool: '+tool)
    demo_readme=(root/'demo/README.md').read_text()
    for raw in LINK_RE.findall(demo_readme):
        target=raw.split('#')[0]
        if target and '://' not in target and not (root/'demo'/target).exists():
            errors.append(f'Broken link: demo/README.md -> {raw}')
    tokens=(root/'demo/src/tokens.css').read_text()
    actual=len(set(re.findall(r'^\s*(--[A-Za-z0-9-]+)\s*:',tokens,re.M)))
    match=re.search(r'(\d+)\s*个本地 CSS token',demo_readme)
    if not match:errors.append('demo/README.md must state the local CSS token count')
    elif int(match.group(1))!=actual:errors.append(f'Token count drift: demo/README.md says {match.group(1)}, tokens.css has {actual}')
    demo_package=json.loads((root/'demo/package.json').read_text())
    for script in ['dev','generate','typecheck','lint','build','preview']:
        if script not in demo_package.get('scripts',{}):errors.append('demo/package.json missing script: '+script)
        if f'npm run {script}' not in demo_readme and script!='preview':errors.append('demo/README.md missing command: npm run '+script)
    template=root/'assets/standalone-web-template'
    for name in ['package.json','vite.config.ts','tsconfig.json','index.html','src/main.tsx','src/App.tsx','src/screens/example-page.tsx']:
        if not (template/name).is_file():errors.append('Missing standalone template file: '+name)
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-install',action='store_true')
    parser.add_argument('--demo-check',action='store_true')
    parser.add_argument('--install-root',type=Path,default=DEFAULT_INSTALL)
    args=parser.parse_args();errors=validate(ROOT)
    if args.demo_check:
        demo=ROOT/'demo'; tracked=['src/.generated-assets-manifest.json','src/generated/assets.ts','src/generated/components.tsx','src/generated/index.ts','code-connect-mappings.json']
        before={p:hashlib.sha256((demo/p).read_bytes()).hexdigest() for p in tracked}
        generated=subprocess.run(['npm','run','generate'],cwd=demo,capture_output=True,text=True)
        if generated.returncode!=0:errors.append('demo npm run generate failed:\n'+(generated.stdout+generated.stderr)[-2000:])
        after={p:hashlib.sha256((demo/p).read_bytes()).hexdigest() for p in tracked}
        if before!=after:errors.append('demo npm run generate is not deterministic: generated files changed on rerun')
        if not (demo/'node_modules').is_dir():errors.append('demo-check requires demo/node_modules; run npm ci in demo/ first')
        else:
            for script in ('typecheck','build','test:strict-render'):
                result=subprocess.run(['npm','run',script],cwd=demo,capture_output=True,text=True)
                if result.returncode!=0:errors.append(f'demo npm run {script} failed:\n'+(result.stdout+result.stderr)[-2000:])
        with tempfile.TemporaryDirectory(prefix='yb-scaffold-check-') as tmp:
            result=subprocess.run(['node','scripts/scaffold-demo.mjs','smoke-test','--run-dir',tmp],cwd=ROOT,capture_output=True,text=True)
            if result.returncode!=0:errors.append('scaffold-demo smoke test failed:\n'+(result.stdout+result.stderr)[-2000:])
            else:
                target=Path(tmp)/'standalone-web'/'smoke-test'
                for name in ['package.json','vite.config.ts','tsconfig.json','index.html','src/main.tsx','src/App.tsx','src/screens/smoke-test.tsx']:
                    if not (target/name).is_file():errors.append('scaffold-demo missing output: '+name)
                if (target/'package.json').is_file() and json.loads((target/'package.json').read_text()).get('name')!='standalone-web-smoke-test':
                    errors.append('scaffold-demo did not replace slug in package.json')
                if (target/'vite.config.ts').is_file() and str((ROOT/'demo').resolve()) not in (target/'vite.config.ts').read_text():
                    errors.append('scaffold-demo did not bind the installed demo root')
                screen=target/'src/screens/smoke-test.tsx'
                if screen.is_file() and 'export function SmokeTestScreen' not in screen.read_text():
                    errors.append('scaffold-demo screen export is not a valid PascalCase identifier')
            rejected=subprocess.run(['node','scripts/scaffold-demo.mjs','1','--run-dir',tmp],cwd=ROOT,capture_output=True,text=True)
            if rejected.returncode==0:errors.append('scaffold-demo accepted a digit-leading slug (invalid component identifier)')
    if args.check_install:
        installed=args.install_root
        if not installed.is_dir():errors.append(f'Install missing: {installed}')
        else:
            a=set(managed_files(ROOT));b=set(managed_files(installed))
            for p in sorted(a^b):errors.append(f'Install file set differs: {p}')
            for p in sorted(a&b):
                if (ROOT/p).read_bytes()!=(installed/p).read_bytes():errors.append(f'Install drift: {p}')
    if errors:
        print('FAILED\n'+'\n'.join('- '+e for e in errors));return 1
    print(f'OK: {len(managed_files(ROOT))} managed files; static structure/links only.')
    if args.check_install:print(f'Install identical: {args.install_root}')
    return 0

if __name__=='__main__':sys.exit(main())
