# DOWNLOAD CHECKLIST

Use this to track which files you've downloaded. All 32 files are available.

## 📋 Guide Files (Download First) - 3 files

- [ ] `START_HERE.md` ⭐⭐⭐ (Read this first!)
- [ ] `FILE_REORGANIZATION_GUIDE.md` ⭐⭐ (Instructions for organizing files)
- [ ] `FILE_MANIFEST.md` ⭐ (Description of each file)

## 📚 Documentation Files - 5 files

- [ ] `PROJECT_OVERVIEW.md` (Architecture overview)
- [ ] `QUICKSTART.md` (5-minute setup guide)
- [ ] `README.md` (Main user guide)
- [ ] `docs__SLASH__PRD.md` → `docs/PRD.md` (Technical deep dive)
- [ ] `LICENSE` (MIT License)

## ⚙️ Configuration Files - 4 files

- [ ] `DOT_env.example` → `.env.example` (Environment variables template)
- [ ] `DOT_gitignore` → `.gitignore` (Git exclusions)
- [ ] `agent__SLASH__config.yaml` → `agent/config.yaml` (All settings)
- [ ] `requirements.txt` (Python dependencies)

## 🎯 Core Files - 2 files

- [ ] `agent__SLASH__main.py` → `agent/main.py` (CLI entry point)
- [ ] `verify_setup.py` (Setup verification script)

## 📦 Package Init Files - 6 files

- [ ] `agent__SLASH____init__.py` → `agent/__init__.py`
- [ ] `agent__SLASH__collectors__SLASH____init__.py` → `agent/collectors/__init__.py`
- [ ] `agent__SLASH__signals__SLASH____init__.py` → `agent/signals/__init__.py`
- [ ] `agent__SLASH__narratives__SLASH____init__.py` → `agent/narratives/__init__.py`
- [ ] `agent__SLASH__llm__SLASH____init__.py` → `agent/llm/__init__.py`
- [ ] `agent__SLASH__reports__SLASH__README.md` → `agent/reports/README.md`

## 📡 Collector Files - 3 files

- [ ] `agent__SLASH__collectors__SLASH__onchain.py` → `agent/collectors/onchain.py`
- [ ] `agent__SLASH__collectors__SLASH__github.py` → `agent/collectors/github.py`
- [ ] `agent__SLASH__collectors__SLASH__social.py` → `agent/collectors/social.py`

## ⚡ Signal Processing Files - 3 files

- [ ] `agent__SLASH__signals__SLASH__normalize.py` → `agent/signals/normalize.py`
- [ ] `agent__SLASH__signals__SLASH__momentum.py` → `agent/signals/momentum.py`
- [ ] `agent__SLASH__signals__SLASH__clustering.py` → `agent/signals/clustering.py`

## 🎯 Narrative Logic Files - 3 files

- [ ] `agent__SLASH__narratives__SLASH__detect.py` → `agent/narratives/detect.py`
- [ ] `agent__SLASH__narratives__SLASH__explain.py` → `agent/narratives/explain.py`
- [ ] `agent__SLASH__narratives__SLASH__ideas.py` → `agent/narratives/ideas.py`

## 🤖 LLM Layer Files - 3 files

- [ ] `agent__SLASH__llm__SLASH__base.py` → `agent/llm/base.py`
- [ ] `agent__SLASH__llm__SLASH__openai.py` → `agent/llm/openai.py`
- [ ] `agent__SLASH__llm__SLASH__local.py` → `agent/llm/local.py`

---

## Quick Count

- Guide files: 3
- Documentation: 5
- Configuration: 4
- Core files: 2
- Init files: 6
- Collectors: 3
- Signals: 3
- Narratives: 3
- LLM: 3

**Total: 32 files**

## After Download

Once you have all files:

1. ✅ Run `FILE_REORGANIZATION_GUIDE.md` instructions
2. ✅ Create empty directories: `data/raw`, `data/processed`, `reports`
3. ✅ Run `python3 verify_setup.py`
4. ✅ Follow `QUICKSTART.md` to run the agent

---

**All files are in `/outputs` folder. Happy building! 🚀**
