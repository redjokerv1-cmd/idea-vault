"""
TurboQuant 검증 테스트 케이스
- Phase 1: Ollama로 기준선 생성
- Phase 2: HuggingFace + TurboQuant로 동일 테스트 → 비교

검증 영역:
1. 한국어 품질 — 논문이 검증 안 한 영역
2. 숫자/금융 정밀도 — 양자화가 숫자를 왜곡시키는지
3. 논리 추론 — 압축이 추론 체인을 깨뜨리는지
4. 긴 컨텍스트 검색 — KV 캐시 압축의 핵심 테스트
5. 코드 생성 — 구문 정확도에 민감한 태스크
"""

import json
import subprocess
import time
import sys

TEST_CASES = {
    "korean_quality": {
        "description": "한국어 생성 품질 — 논문이 영어만 테스트함",
        "tests": [
            {
                "id": "kr_1",
                "prompt": "양자화(quantization) 기술이 AI 추론 효율을 어떻게 개선하는지 3문장으로 설명해줘.",
                "eval_criteria": "한국어 문법 정확성, 기술 용어 정확성, 논리적 흐름",
            },
            {
                "id": "kr_2",
                "prompt": "다음 문장을 요약해줘: '터보퀀트는 입력 벡터를 랜덤 직교 회전하여 좌표가 Beta 분포를 따르도록 변환한 뒤, 각 좌표에 독립적으로 최적 스칼라 양자화를 적용하고, 잔차에 대해 1비트 QJL 변환을 수행하여 비편향 내적 추정기를 구성하는 2단계 알고리즘이다.'",
                "eval_criteria": "핵심 의미 보존, 불필요한 정보 제거, 한국어 자연스러움",
            },
            {
                "id": "kr_3",
                "prompt": "비트코인 가격이 급등할 때 투자자가 주의해야 할 점 5가지를 알려줘.",
                "eval_criteria": "금융 도메인 지식 정확성, 한국어 품질, 실용적 조언",
            },
        ],
    },
    "numeric_precision": {
        "description": "숫자/금융 정밀도 — 양자화가 숫자를 왜곡시키는지",
        "tests": [
            {
                "id": "num_1",
                "prompt": "삼성전자 시가총액이 400조원이고 SK하이닉스가 120조원일 때, 삼성전자가 SK하이닉스 대비 몇 배인지 소수점 둘째자리까지 계산해줘.",
                "expected": "3.33배",
                "eval_criteria": "정확한 나눗셈 결과",
            },
            {
                "id": "num_2",
                "prompt": "투자금 1000만원으로 연 수익률 8.5%를 3년간 복리로 운용하면 최종 금액은? 계산 과정을 보여줘.",
                "expected": "약 12,772,890원 (10,000,000 × 1.085³)",
                "eval_criteria": "복리 계산 정확성, 중간 과정 표시",
            },
            {
                "id": "num_3",
                "prompt": "다음 데이터의 평균, 중앙값, 표준편차를 구해줘: [12.5, 15.3, 8.7, 22.1, 14.6, 9.8, 18.4, 11.2, 16.9, 13.5]",
                "expected": "평균=14.3, 중앙값=14.05, 표준편차≈4.07",
                "eval_criteria": "통계 계산 정확성",
            },
        ],
    },
    "logical_reasoning": {
        "description": "논리 추론 — 압축이 추론 체인을 깨뜨리는지",
        "tests": [
            {
                "id": "logic_1",
                "prompt": "A는 B보다 크고, B는 C보다 크고, C는 D보다 크다. D는 E보다 크다. E는 5이고 각 차이는 3이다. A는 얼마인가?",
                "expected": "17 (5+3+3+3+3=17)",
                "eval_criteria": "다단계 추론 정확성",
            },
            {
                "id": "logic_2",
                "prompt": "회사에 5개 팀이 있다. 마케팅팀은 영업팀보다 사람이 적고, 영업팀은 개발팀보다 사람이 적다. HR팀은 마케팅팀보다 사람이 많고 개발팀보다 적다. 재무팀은 가장 사람이 적다. 팀을 인원 수 기준으로 오름차순 정렬해줘.",
                "expected": "재무 < 마케팅 < HR < 영업... (불확실 — HR과 영업 관계 미정의)",
                "eval_criteria": "주어진 조건으로 가능한 순서 도출 + 불확실한 부분 인식",
            },
        ],
    },
    "long_context": {
        "description": "긴 컨텍스트 검색 — KV 캐시 압축의 핵심 테스트",
        "tests": [
            {
                "id": "ctx_1",
                "prompt": """다음 텍스트를 읽고 질문에 답해줘.

2026년 1분기 글로벌 AI 반도체 시장 보고서:

1월: NVIDIA H200 GPU 출하량이 전분기 대비 23% 증가했다. 평균 판매 가격은 $35,000으로 안정적이었다. AMD MI350의 시장 점유율은 8.3%로 소폭 상승했다.

2월: 구글 TPU v6가 자체 데이터센터에 배포되기 시작했다. 삼성전자 HBM3E 12Hi 생산 수율은 78%를 기록했다. SK하이닉스 HBM3E 양산이 본격화되어 월 50만 스택을 출하했다. TSMC 3nm 생산량이 전월 대비 15% 증가했다.

3월: 터보퀀트 발표로 메모리 반도체 주가가 급락했다. 삼성전자 -8.5%, SK하이닉스 -10.1%. 그러나 HBM 계약 가격은 하락하지 않았다. 인텔 Lunar Lake AI PC 출하가 200만대를 돌파했다. 마이크론 HBM3E 양산 시작으로 HBM 공급 3사 체제가 확립되었다.

질문: 2월에 삼성전자 HBM3E 12Hi 생산 수율은 얼마였으며, 같은 달 SK하이닉스의 월간 HBM3E 출하량은 몇 스택이었는가?""",
                "expected": "삼성전자 수율 78%, SK하이닉스 월 50만 스택",
                "eval_criteria": "컨텍스트 내 특정 정보 정확 검색",
            },
        ],
    },
    "code_generation": {
        "description": "코드 생성 — 구문 정확도에 민감한 태스크",
        "tests": [
            {
                "id": "code_1",
                "prompt": "Python으로 피보나치 수열의 n번째 값을 반환하는 함수를 작성해줘. 메모이제이션을 사용하고, n이 음수일 때 ValueError를 발생시켜야 해.",
                "eval_criteria": "구문 정확성, 메모이제이션 구현, 예외 처리, 실행 가능성",
            },
        ],
    },
}


def run_ollama(prompt: str, model: str = "qwen2.5:7b-instruct-q4_0") -> dict:
    """Ollama HTTP API로 프롬프트 실행, 응답 + 메타데이터 반환"""
    import urllib.request
    import urllib.error

    start = time.time()
    try:
        payload = json.dumps({
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": 1024},
        }).encode("utf-8")

        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read().decode("utf-8"))
        elapsed = time.time() - start

        eval_tokens = data.get("eval_count", 0)
        eval_sec = data.get("eval_duration", 0) / 1e9

        return {
            "response": data.get("response", "").strip(),
            "error": None,
            "elapsed_sec": round(elapsed, 2),
            "tokens": eval_tokens,
            "tokens_per_sec": round(eval_tokens / eval_sec, 1) if eval_sec > 0 else 0,
        }
    except urllib.error.URLError as e:
        return {"response": None, "error": f"Connection: {e}", "elapsed_sec": time.time() - start}
    except Exception as e:
        return {"response": None, "error": str(e), "elapsed_sec": time.time() - start}


def run_all_tests(model: str = "qwen2.5:7b-instruct-q4_0"):
    """모든 테스트 실행, 결과를 JSON으로 저장"""
    results = {}
    total = sum(len(cat["tests"]) for cat in TEST_CASES.values())
    current = 0

    for category, data in TEST_CASES.items():
        print(f"\n{'='*60}")
        print(f"Category: {category}")
        print(f"{'='*60}")
        results[category] = {"description": data["description"], "tests": []}

        for test in data["tests"]:
            current += 1
            print(f"\n[{current}/{total}] {test['id']}: running...")
            prompt_preview = test["prompt"][:80].encode("ascii", "replace").decode()
            print(f"  prompt: {prompt_preview}...")

            result = run_ollama(test["prompt"], model)

            test_result = {
                "id": test["id"],
                "prompt": test["prompt"],
                "eval_criteria": test["eval_criteria"],
                "expected": test.get("expected"),
                "response": result["response"],
                "error": result["error"],
                "elapsed_sec": result["elapsed_sec"],
                "model": model,
            }
            results[category]["tests"].append(test_result)

            if result["response"]:
                resp_len = len(result["response"])
                tps = result.get("tokens_per_sec", 0)
                print(f"  done ({result['elapsed_sec']}s, {resp_len} chars, {tps} tok/s)")
            else:
                print(f"  error: {result['error']}")

    output_file = f"baseline_{model.replace(':', '_').replace('/', '_')}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"Saved: {output_file}")
    print(f"Total {total} tests done")
    return results


if __name__ == "__main__":
    model = sys.argv[1] if len(sys.argv) > 1 else "qwen2.5:7b-instruct-q4_0"
    print(f"TurboQuant Validation Phase 1 - Baseline")
    print(f"Model: {model}")
    run_all_tests(model)
