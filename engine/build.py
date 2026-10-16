"""並行繪製所有場景
python engine/build.py film1            # 全部
python engine/build.py film1 s2_roots   # 單個
--preview  只出平攤預覽圖到 out/preview/
"""
import os, sys, time, importlib
from multiprocessing import Pool

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
sys.path.insert(0, os.path.join(ROOT, "scenes"))
FILMS = {"film1": "film1_roots", "film2": "film2_seasons", "film3": "film3_seedvault", "film4": "film4_basin",
         "film5": "film5_sand", "film6": "film6_invention", "film7": "film7_footpath", "film8": "film8_blood",
         "film9": "film9_blackbox", "film10": "film10_carrot",
         "film11": "film11_mould", "film12": "film12_ladder", "film13": "film13_clan", "film14": "film14_station"}
ASSETS = os.path.join(ROOT, "web", "assets")
PREV = os.path.join(ROOT, "out", "preview")


def job(args):
    film, fn_name, preview = args
    mod = importlib.import_module(FILMS[film])
    t0 = time.time()
    try:
        s = getattr(mod, fn_name)()
    except Exception:
        import traceback
        return f"FAIL {film}/{fn_name}: " + traceback.format_exc()
    s.save(ASSETS)
    if preview:
        os.makedirs(PREV, exist_ok=True)
        s.preview(os.path.join(PREV, f"{film}_{s.name}.jpg"), 0.4)
    return f"{film}/{s.name} {time.time() - t0:.1f}s"


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    preview = "--preview" in sys.argv
    import os.path as _p
    films = [args[0]] if args else [f for f in FILMS if _p.exists(_p.join(ROOT, 'scenes', FILMS[f] + '.py'))]
    jobs = []
    for f in films:
        mod = importlib.import_module(FILMS[f])
        for fn in mod.ALL:
            if len(args) > 1 and fn.__name__ not in args[1:]:
                continue
            jobs.append((f, fn.__name__, preview))
    with Pool(min(len(jobs), max(1, os.cpu_count() - 2))) as p:
        for r in p.imap_unordered(job, jobs):
            print(r, flush=True)
