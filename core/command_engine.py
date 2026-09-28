import datetime as dt


class CommandEngine:
    def __init__(self, state, session_manager, logger, report_generator) -> None:
        self.state = state
        self.session_manager = session_manager
        self.logger = logger
        self.report_generator = report_generator

    def run(self, intent: str, raw: str) -> dict:
        if intent == "SYSTEM_DIAGNOSTIC":
            self.state.set_hud("DIAGNOSTIC", 1.7)
            result = "SYSTEM DIAGNOSTIC\nCOMMAND ENGINE ........ NOMINAL\nHUD ENGINE ............ NOMINAL\nTELEMETRY ENGINE ...... NOMINAL\nDATA ENGINE ........... NOMINAL\nVOICE ENGINE .......... ONLINE\nKNOWLEDGE CORE ........ NOMINAL\nGENERATIVE CORE ....... READY / STANDBY\n\nDIAGNOSTIC COMPLETE\nSYSTEMS NOMINAL"
            self.state.set_hud("COMPLETE", 1.2)
            return {"response": result, "source": "SYSTEM", "status": "SUCCESS"}

        if intent == "SHOW_TELEMETRY":
            self.state.set_hud("TELEMETRY", 1.3)
            summary = self.logger.summary()
            result = (
                "TELEMETRY REPORT\n"
                f"TOTAL INTERACTIONS: {summary.get('total_interactions', 0)}\n"
                f"SYSTEM COMMANDS: {summary.get('system_commands', 0)}\n"
                f"AI QUERIES: {summary.get('ai_queries', 0)}\n"
                f"KNOWLEDGE CORE RESPONSES: {summary.get('knowledge_responses', 0)}\n"
                f"LLM RESPONSES: {summary.get('llm_responses', 0)}\n"
                f"SUCCESS RATE: {summary.get('success_rate', 0)}%\n"
                f"AVERAGE LATENCY: {summary.get('avg_latency', 0.0):.2f}s\n"
                f"FASTEST RESPONSE: {summary.get('fastest_response', 0.0):.2f}s\n"
                f"SLOWEST RESPONSE: {summary.get('slowest_response', 0.0):.2f}s\n"
                f"SESSION DURATION: {summary.get('session_duration', 0.0):.2f}s"
            )
            return {"response": result, "source": "SYSTEM", "status": "SUCCESS"}

        if intent == "ACTIVATE_REACTOR":
            self.state.set_hud("PROCESSING", 1.8)
            return {"response": "REACTOR ACTIVATED. SYSTEMS ARE RUNNING AT OPTIMUM VISUALIZATION.", "source": "SYSTEM", "status": "SUCCESS"}

        if intent == "DEFENSE_MODE":
            self.state.set_hud("TACTICAL", 2.2)
            self.state.protocol_mode = "DEFENSE"
            return {"response": "TACTICAL MODE ENGAGED. REACTOR ACTIVITY INCREASED. SYSTEM STATUS: STABLE.", "source": "SYSTEM", "status": "SUCCESS"}

        if intent == "SHOW_COMMAND_HISTORY":
            history = self.session_manager.command_history(limit=8)
            return {"response": history, "source": "SYSTEM", "status": "SUCCESS"}

        if intent == "GENERATE_MISSION_REPORT":
            self.state.set_hud("COMPLETE", 1.5)
            report = self.report_generator.generate_report(self.logger.events)
            return {"response": report, "source": "SYSTEM", "status": "SUCCESS"}

        if intent == "PROTOCOL_OMEGA":
            self.state.set_hud("TACTICAL", 2.6)
            self.state.protocol_mode = "OMEGA"
            return {"response": "PROTOCOL OMEGA INITIALIZING...\nCORE SYNCHRONIZATION COMPLETE\nHUD SYNCHRONIZATION COMPLETE\nTELEMETRY SYNCHRONIZATION COMPLETE\nSYSTEM STATUS: MAXIMUM PERFORMANCE VISUALIZATION", "source": "SYSTEM", "status": "SUCCESS"}

        if intent == "HELP":
            from config import HELP_TEXT
            return {"response": HELP_TEXT, "source": "SYSTEM", "status": "SUCCESS"}

        if intent == "TIME":
            return {"response": f"CURRENT SYSTEM TIME: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "source": "SYSTEM", "status": "SUCCESS"}

        if intent == "CLEAR":
            return {"response": "TERMINAL MEMORY CLEARED.", "source": "SYSTEM", "status": "SUCCESS"}

        if intent == "RESET":
            self.state.set_hud("IDLE", 0.8)
            return {"response": "SYSTEM STATE RESET TO IDLE.", "source": "SYSTEM", "status": "SUCCESS"}

        if intent == "ABOUT":
            return {"response": "J.A.R.V.I.S. IS A MODULAR OFFLINE AI-INSPIRED COMMAND PLATFORM WITH AN OPTIONAL GENERATIVE INTELLIGENCE LAYER.", "source": "SYSTEM", "status": "SUCCESS"}

        if intent == "UNKNOWN":
            return {"response": "COMMAND NOT RECOGNIZED.\nAVAILABLE COMMAND CATEGORIES:\nSYSTEM\nTELEMETRY\nHUD\nDATA\nUTILITY", "source": "SYSTEM", "status": "ERROR"}

        return {"response": "SYSTEM COMMAND EXECUTED.", "source": "SYSTEM", "status": "SUCCESS"}
