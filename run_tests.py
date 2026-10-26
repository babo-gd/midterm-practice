"""로컬 채점기: py run_tests.py [테스트파일.json]

각 테스트를 별도 프로세스에서 돌려서 10초 넘게 걸리면 시간 초과로 표시합니다.
(실제 채점 기준: 10초 안에 안 끝나면 0점)
"""
import json
import multiprocessing as mp
import sys
import time

TIME_LIMIT = 10


def run_case(case, queue):
    from solution import StudentManager  # 문제지의 클래스 이름으로 바꾸기

    obj = StudentManager()
    results = []
    for step in case["steps"]:
        try:
            got = getattr(obj, step["call"])(*step["args"])
        except Exception as e:  # noqa: BLE001
            got = f"ERROR: {type(e).__name__}: {e}"
        results.append((step, got))
    queue.put(results)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "sample_test.json"
    with open(path, encoding="utf-8") as f:
        cases = json.load(f)

    passed = 0
    for i, case in enumerate(cases, 1):
        q = mp.Queue()
        p = mp.Process(target=run_case, args=(case, q))
        start = time.time()
        p.start()
        p.join(TIME_LIMIT)
        elapsed = time.time() - start
        if p.is_alive():
            p.terminate()
            print(f"[{i}] ⏰ 시간 초과 ({TIME_LIMIT}초) - {case['name']}")
            continue
        results = q.get()
        bad = [(s, g) for s, g in results if g != s["expected"]]
        if bad:
            print(f"[{i}] ❌ 실패 - {case['name']}")
            for s, g in bad:
                print(f"     {s['call']}{tuple(s['args'])} 기대={s['expected']!r} 실제={g!r}")
        else:
            passed += 1
            print(f"[{i}] ✅ 통과 - {case['name']} ({elapsed:.2f}초)")

    print(f"\n결과: {passed}/{len(cases)} 통과")


if __name__ == "__main__":
    main()
