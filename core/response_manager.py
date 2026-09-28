import time


class ResponseManager:
    def __init__(self, state, router, command_engine, knowledge_core, llm_engine, logger, tts_manager=None, ui=None):
        self.state = state
        self.router = router
        self.command_engine = command_engine
        self.knowledge_core = knowledge_core
        self.llm_engine = llm_engine
        self.logger = logger
        self.tts_manager = tts_manager
        self.ui = ui

    def process(self, raw_text: str) -> dict:
        start = time.time()
        route = self.router.classify(raw_text)
        intent = route.get("intent", "UNKNOWN")
        source = route.get("source", "SYSTEM")

        if intent in {"SYSTEM_DIAGNOSTIC", "SHOW_TELEMETRY", "ACTIVATE_REACTOR", "DEFENSE_MODE", "SHOW_COMMAND_HISTORY", "GENERATE_MISSION_REPORT", "PROTOCOL_OMEGA", "HELP", "TIME", "CLEAR", "RESET", "ABOUT", "UNKNOWN"}:
            result = self.command_engine.run(intent, raw_text)
        elif intent == "KNOWLEDGE_QUERY":
            result = self._knowledge_or_llm(raw_text)
            source = result.get("source", "KNOWLEDGE_CORE")
        else:
            result = self.command_engine.run(intent, raw_text)

        latency = time.time() - start

        self.state.last_intent = intent
        self.state.last_response = result.get("response", "")
        if self.ui is not None:
            self.ui.append_terminal(result.get("response", ""))
            self.ui.set_hud_state(self.state.hud_state)

        if self.tts_manager is not None and result.get("status") == "SUCCESS":
            short = self._shorten(result.get("response", ""))
            self.tts_manager.speak_async(short)

        self.logger.log_event(
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            user_input=raw_text,
            intent=intent,
            response_source=source,
            latency=latency,
            system_state=self.state.get_snapshot(),
            status=result.get("status", "SUCCESS"),
        )

        return {"intent": intent, "source": source, "result": result, "latency": latency}

    def _knowledge_or_llm(self, question: str) -> dict:
        if self.llm_engine and self.llm_engine.is_available():
            answer = self.llm_engine.answer(question)
            if answer:
                return {"response": answer, "source": "LLM", "status": "SUCCESS"}
        answer = self.knowledge_core.answer(question)
        return {"response": answer, "source": "KNOWLEDGE_CORE", "status": "SUCCESS"}

    @staticmethod
    def _shorten(text: str, limit: int = 120) -> str:
        cleaned = " ".join((text or "").split())
        if len(cleaned) <= limit:
            return cleaned
        return cleaned[: limit - 3].rstrip() + "..."
