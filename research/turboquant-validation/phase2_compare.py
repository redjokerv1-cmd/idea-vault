"""
TurboQuant Phase 2: FP16 KV Cache vs TurboQuant KV Cache
- Same model (Qwen2.5-3B-Instruct), same prompts
- Compare: output quality, memory, speed at bits=3 and bits=4
"""

import json
import time
import gc
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from turboquant import TurboQuantCache

MODEL_ID = "Qwen/Qwen2.5-3B-Instruct"

PROMPTS = [
    {
        "id": "kr_1",
        "category": "korean",
        "prompt": "Quantization technology improves AI inference efficiency. Explain in 3 sentences in Korean.",
        "chat": [{"role": "user", "content": "양자화(quantization) 기술이 AI 추론 효율을 어떻게 개선하는지 3문장으로 설명해줘."}],
    },
    {
        "id": "num_1",
        "category": "numeric",
        "prompt": "Calculate 400/120 to 2 decimal places",
        "chat": [{"role": "user", "content": "삼성전자 시가총액이 400조원이고 SK하이닉스가 120조원일 때, 삼성전자가 SK하이닉스 대비 몇 배인지 소수점 둘째자리까지 계산해줘."}],
    },
    {
        "id": "num_2",
        "category": "numeric",
        "prompt": "Compound interest calculation",
        "chat": [{"role": "user", "content": "투자금 1000만원으로 연 수익률 8.5%를 3년간 복리로 운용하면 최종 금액은? 계산 과정을 보여줘."}],
    },
    {
        "id": "logic_1",
        "category": "logic",
        "prompt": "A>B>C>D>E chain reasoning",
        "chat": [{"role": "user", "content": "A는 B보다 크고, B는 C보다 크고, C는 D보다 크다. D는 E보다 크다. E는 5이고 각 차이는 3이다. A는 얼마인가?"}],
    },
    {
        "id": "ctx_1",
        "category": "context",
        "prompt": "Find specific facts in context",
        "chat": [{"role": "user", "content": """다음 텍스트를 읽고 질문에 답해줘.

2026년 1분기 글로벌 AI 반도체 시장 보고서:

1월: NVIDIA H200 GPU 출하량이 전분기 대비 23% 증가했다. 평균 판매 가격은 $35,000으로 안정적이었다. AMD MI350의 시장 점유율은 8.3%로 소폭 상승했다.

2월: 구글 TPU v6가 자체 데이터센터에 배포되기 시작했다. 삼성전자 HBM3E 12Hi 생산 수율은 78%를 기록했다. SK하이닉스 HBM3E 양산이 본격화되어 월 50만 스택을 출하했다. TSMC 3nm 생산량이 전월 대비 15% 증가했다.

3월: 터보퀀트 발표로 메모리 반도체 주가가 급락했다. 삼성전자 -8.5%, SK하이닉스 -10.1%. 그러나 HBM 계약 가격은 하락하지 않았다. 인텔 Lunar Lake AI PC 출하가 200만대를 돌파했다.

질문: 2월에 삼성전자 HBM3E 12Hi 생산 수율은 얼마였으며, 같은 달 SK하이닉스의 월간 HBM3E 출하량은 몇 스택이었는가?"""}],
    },
    {
        "id": "code_1",
        "category": "code",
        "prompt": "Fibonacci with memoization",
        "chat": [{"role": "user", "content": "Python으로 피보나치 수열의 n번째 값을 반환하는 함수를 작성해줘. 메모이제이션을 사용하고, n이 음수일 때 ValueError를 발생시켜야 해."}],
    },
]


def measure_gpu():
    """Return current GPU memory allocated in MB"""
    if torch.cuda.is_available():
        return torch.cuda.memory_allocated() / 1024 / 1024
    return 0


def run_generation(model, tokenizer, chat_messages, cache=None, max_tokens=512):
    """Run a single generation, return response + metrics"""
    text = tokenizer.apply_chat_template(chat_messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    input_len = inputs["input_ids"].shape[1]

    torch.cuda.reset_peak_memory_stats()
    mem_before = measure_gpu()

    start = time.time()
    with torch.no_grad():
        gen_kwargs = {
            "max_new_tokens": max_tokens,
            "do_sample": False,
            "use_cache": True,
        }
        if cache is not None:
            cache.reset()
            gen_kwargs["past_key_values"] = cache

        outputs = model.generate(**inputs, **gen_kwargs)

    elapsed = time.time() - start
    mem_peak = torch.cuda.max_memory_allocated() / 1024 / 1024

    new_tokens = outputs.shape[1] - input_len
    response = tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True)

    cache_mem = None
    if cache is not None and hasattr(cache, "memory_usage_bytes"):
        try:
            cache_info = cache.memory_usage_bytes()
            cache_mem = cache_info if isinstance(cache_info, dict) else {"total": cache_info}
        except Exception:
            pass

    return {
        "response": response.strip(),
        "new_tokens": new_tokens,
        "elapsed_sec": round(elapsed, 3),
        "tokens_per_sec": round(new_tokens / elapsed, 1) if elapsed > 0 else 0,
        "peak_vram_mb": round(mem_peak, 1),
        "cache_memory": cache_mem,
    }


def run_comparison():
    print("=" * 70)
    print("TurboQuant Phase 2: FP16 vs TurboQuant KV Cache Comparison")
    print(f"Model: {MODEL_ID}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    print("=" * 70)

    print("\nLoading model (FP16)...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    print(f"Model loaded. Base VRAM: {measure_gpu():.0f} MB")

    configs = [
        ("FP16 (baseline)", None),
        ("TurboQuant 4-bit", TurboQuantCache(bits=4)),
        ("TurboQuant 3-bit", TurboQuantCache(bits=3)),
    ]

    all_results = {}

    for config_name, cache in configs:
        print(f"\n{'='*70}")
        print(f"Config: {config_name}")
        print(f"{'='*70}")

        config_results = []
        for p in PROMPTS:
            print(f"  [{p['id']}] {p['prompt'][:50]}...", end=" ", flush=True)

            gc.collect()
            torch.cuda.empty_cache()

            try:
                result = run_generation(model, tokenizer, p["chat"], cache)
                result["id"] = p["id"]
                result["category"] = p["category"]
                config_results.append(result)

                resp_preview = result["response"][:80].replace("\n", " ")
                print(f"OK ({result['elapsed_sec']}s, {result['tokens_per_sec']} tok/s, {result['peak_vram_mb']}MB)")
            except Exception as e:
                print(f"ERROR: {e}")
                config_results.append({
                    "id": p["id"],
                    "category": p["category"],
                    "error": str(e),
                })

        all_results[config_name] = config_results

    output_file = "phase2_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"\n{'Test':<10} | {'Config':<20} | {'Tokens/s':>10} | {'Peak MB':>10} | {'Time':>8}")
    print("-" * 70)
    for config_name, results in all_results.items():
        for r in results:
            if "error" in r:
                print(f"{r['id']:<10} | {config_name:<20} | {'ERROR':>10} |")
            else:
                print(f"{r['id']:<10} | {config_name:<20} | {r['tokens_per_sec']:>10} | {r['peak_vram_mb']:>10} | {r['elapsed_sec']:>7}s")

    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    run_comparison()
