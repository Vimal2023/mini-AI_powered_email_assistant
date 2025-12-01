from typing import Literal, TypedDict

IntentType = Literal["READ", "REPLY", "SEND", "DELETE", "HELP", "UNKNOWN"]

class ParsedCommand(TypedDict):
    intent: IntentType
    emailIndex: int | None
    subjectKeyword: str | None
    sender: str | None
    additionalMessage: str | None

def parse_command(message: str) -> ParsedCommand:
    text = message.lower().strip()
    result: ParsedCommand = {
        "intent": "UNKNOWN",
        "emailIndex": None,
        "subjectKeyword": None,
        "sender": None,
        "additionalMessage": None,
    }

    if "read" in text and "email" in text:
        result["intent"] = "READ"
    elif "reply" in text:
        result["intent"] = "REPLY"
    elif "send" in text and "reply" in text:
        result["intent"] = "SEND"
    elif "delete" in text:
        result["intent"] = "DELETE"
    elif "help" in text:
        result["intent"] = "HELP"

    # simple index parsing: "email 2" etc.
    for token in text.split():
        if token.isdigit():
            result["emailIndex"] = int(token)
            break

    return result
