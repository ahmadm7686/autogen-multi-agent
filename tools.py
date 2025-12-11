# tools.py
"""
FetchDataTool: أداة بسيطة تجيب بيانات "محاكاة" حسب الموضوع.
If AutoGen is available we register it as an autogen function; otherwise it's a plain callable.
"""

try:
    # try to import AutoGen's register_function (API may differ by version)
    from autogen import register_function  # type: ignore

    @register_function
    def fetch_live_data(topic: str) -> str:
        fake_db = {
            "AI Stock Trends": "AI stocks increased 12% today, led by OpenAI and Anthropic.",
            "Tech News": "New AI chips announced with 40% speed improvement.",
            "Climate": "Unusual warm spell recorded across Mediterranean this week."
        }
        return fake_db.get(topic, f"No data available for '{topic}'")

    USING_AUTOGEN_TOOL = True

except Exception:
    # Fallback: plain python function if AutoGen isn't installed
    def fetch_live_data(topic: str) -> str:
        fake_db = {
            "AI Stock Trends": "AI stocks increased 12% today, led by OpenAI and Anthropic.",
            "Tech News": "New AI chips announced with 40% speed improvement.",
            "Climate": "Unusual warm spell recorded across Mediterranean this week."
        }
        return fake_db.get(topic, f"No data available for '{topic}'")

    USING_AUTOGEN_TOOL = False
