from openai import OpenAI
client = OpenAI()  # expects OPENAI_API_KEY in env

def analyze_with_llm(ticker: str, snapshot: dict, headlines: list, model="gpt-4o-mini"):
    # Build headlines block
    if headlines:
        head_str = "\n".join([f'- "{h["title"]}" ({h.get("url","")})' for h in headlines])
    else:
        head_str = "- (no recent headlines found)"

    user_prompt = USER_TEMPLATE.format(
        ticker=ticker.upper(),
        snapshot_json=json.dumps(snapshot),
        headlines_bulleted=head_str
    )

    # Responses API with JSON object output
    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": [{"type":"text", "text": SYSTEM_PROMPT}]},
            {"role": "user", "content": [{"type":"text", "text": FEW_SHOT_USER}]},
            {"role": "assistant", "content": [{"type":"text", "text": FEW_SHOT_ASSISTANT}]},
            {"role": "user", "content": [{"type":"text", "text": user_prompt}]}
        ],
        response_format={"type": "json_object"}
    )
    # Extract text from the first output
    raw = resp.output[0].content[0].text  # structure per Responses API
    return json.loads(raw)