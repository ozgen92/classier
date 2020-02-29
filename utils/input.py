def get_yes_no(text: str="") -> bool:
    answer = get_limited_options(["y", "n"], text)
    return answer == "y"


def get_limited_options(limited_options, text=""):
    limited_options = list(map(str, list(limited_options)))
    answer = input(f"{text} ({'/'.join(limited_options)})")
    while answer.lower() not in limited_options:
        print("Wrong input. Please enter one of: {{', '.join(limited_options)}} (case insensitive)")
        answer = input(f"{text}")
    return answer.lower()
