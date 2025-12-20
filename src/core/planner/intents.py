def match_intent(user_input: str) -> str | None:
    text = user_input.lower()

    if "setup" in text and "project" in text:
        return "start_project"

    if "open" in text and "project" in text:
        return "open_project"

    if "prepare" in text and "work" in text:
        return "prepare_work_environment"
    
    if "open copied path" in text:
        return "open_copied_path"

    return None
