import argparse
import json
import os
import fnmatch
import sys
import asyncio
import signal
import subprocess
import time
import inspect
from typing import Any, Dict, List, Optional, Tuple
from openai import AsyncOpenAI, OpenAI
import httpx

from prompts import SYSTEM_PROMPT

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- LLM Configuration ---
LLM_CONFIG = {
    "title": "deepseek-v3",
    "provider": "openai",
    "model": "deepseek-v3",
    "apiKey": "sk-P4rnO5obBI6YoaAkZdn5gw",
    "apiBase": "http://172.21.3.106:80/v1"
}

# In-memory storage for plan sessions.
PLAN_SESSIONS = {}

# --- Plan State Persistence ---
FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')
STATE_DIR = os.path.join(FILES_DIR, '.state')
os.makedirs(STATE_DIR, exist_ok=True)

def get_state_path(plan_id: str) -> str:
    """Gets the path for a plan's state file."""
    return os.path.join(STATE_DIR, f"{plan_id}.state.json")

def load_plan_state(plan_id: str) -> dict:
    """Loads the execution state of a plan from its state file."""
    state_path = get_state_path(plan_id)
    if os.path.exists(state_path):
        try:
            with open(state_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If state file is corrupted, start from scratch
            return {"current_step": 0}
    return {"current_step": 0} # Default state if no file exists

def save_plan_state(plan_id: str, state: dict):
    """Saves the execution state of a plan to its state file."""
    state_path = get_state_path(plan_id)
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=4)


def kill_process_on_port(port):
    """Find and kill a process listening on a specific port."""
    sys.stderr.write(f"Checking for and attempting to kill process on port {port}...\n")
    if sys.platform == "win32":
        command = f"Get-Process -Id (Get-NetTCPConnection -LocalPort {port} -State Listen).OwningProcess | Stop-Process -Force"
        try:
            subprocess.run(["powershell", "-Command", command], check=False, capture_output=True, text=True, creationflags=0x08000000)
            sys.stderr.write(f"Attempted to kill process on port {port} via PowerShell.\n")
            time.sleep(1)
        except Exception as e:
            sys.stderr.write(f"Could not execute PowerShell command (is it in PATH?): {e}\n")
    else: # For linux, darwin, etc.
        try:
            # More robust command for Linux/macOS
            command = f"lsof -ti tcp:{port} | xargs kill -9"
            subprocess.run(command, shell=True, check=False, capture_output=True, text=True)
            sys.stderr.write(f"Attempted to kill process on port {port}.\n")
            time.sleep(1)
        except Exception as e:
            sys.stderr.write(f"Error finding/killing process on port {port}: {e}\n")
    sys.stderr.flush()


def search_files(search_path: str, file_patterns: list, keywords: list, output_filename: str) -> None:
    """
    Searches for files matching patterns and keywords, sorts them by size, and saves the paths.
    """
    matched_files = []
    output_dir = resource_path('files')
    os.makedirs(output_dir, exist_ok=True)
    print(f"Searching in '{search_path}' for patterns '{file_patterns}' with keywords '{keywords}'...")

    for root, _, files in os.walk(search_path):
        if os.path.abspath(root).startswith(os.path.abspath(output_dir)):
            continue
        for pattern in file_patterns:
            for filename in fnmatch.filter(files, pattern):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if all(keyword.lower() in content.lower() for keyword in keywords):
                            abs_path = os.path.abspath(filepath)
                            file_size = os.path.getsize(filepath)
                            matched_files.append((abs_path, file_size))
                except Exception:
                    pass

    matched_files.sort(key=lambda x: x[1])
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        for filepath, _ in matched_files:
            f.write(filepath + ' |\n')
    print(f"Found {len(matched_files)} files. Results saved to {output_path}")


async def get_structured_query(client: AsyncOpenAI, query: str) -> Optional[dict]:
    """
    Calls the LLM to convert a natural language query into a structured JSON object.
    """
    try:
        response = await client.chat.completions.create(
            model=LLM_CONFIG["model"],
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        if content:
            return json.loads(content)
        return None
    except Exception as e:
        sys.stderr.write(f"Error calling LLM or parsing JSON: {e}\n")
        return None


async def create_plan(query: str) -> str:
    """
    High-level function to process a natural language query, generate a plan file,
    and return the name of the file.
    """
    try:
        client = AsyncOpenAI(api_key=LLM_CONFIG["apiKey"], base_url=LLM_CONFIG["apiBase"])
    except Exception as e:
        return f"Error: Failed to initialize OpenAI client: {e}"

    structured_query = await get_structured_query(client, query)
    if not structured_query:
        return "Error: Failed to get structured query from LLM."

    output_filename = structured_query.get('output_filename', 'search_results.txt')
    try:
        search_files(
            search_path=structured_query.get('search_path', '.'),
            file_patterns=structured_query.get('file_patterns', ['*']),
            keywords=structured_query.get('keywords', []),
            output_filename=output_filename
        )
        
        # Load plan into session
        plan_path = os.path.join(resource_path('files'), output_filename)
        with open(plan_path, 'r', encoding='utf-8') as f:
            steps = [line.strip() for line in f if line.strip()]
        
        PLAN_SESSIONS[output_filename] = {
            "steps": steps,
            "current_step": 0
        }
        # Create initial state file
        save_plan_state(output_filename, {"current_step": 0})
        
        return f"Plan created and loaded: {output_filename}. Total steps: {len(steps)}"
    except Exception as e:
        return f"Error: Failed to execute search or load plan: {e}"


def add_instruction(plan_id: str, instruction: str) -> str:
    """Appends a natural language instruction to each line of a plan file."""
    plan_path = os.path.join(resource_path('files'), plan_id)
    if not os.path.exists(plan_path):
        return f"Error: Plan file not found at '{plan_path}'"
    try:
        with open(plan_path, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            f.seek(0)
            f.truncate()
            for line in lines:
                base_part = line.split('|', 1)[0].strip()
                f.write(f"{base_part} | {instruction.strip()}\n")
        
        # Reload plan in session if it exists and reset progress
        if plan_id in PLAN_SESSIONS:
            with open(plan_path, 'r', encoding='utf-8') as f:
                steps = [line.strip() for line in f if line.strip()]
            PLAN_SESSIONS[plan_id]['steps'] = steps
            PLAN_SESSIONS[plan_id]['current_step'] = 0 # Reset progress
            sys.stderr.write(f"Reloaded and reset plan '{plan_id}' in active session.\n")

        # Reset persistent state as well
        save_plan_state(plan_id, {"current_step": 0})

        return f"Successfully appended instruction to '{plan_id}'. Plan progress has been reset."
    except IOError as e:
        return f"Error updating plan file '{plan_path}': {e}"


def get_next_step(plan_id: str) -> str:
    """
    Executes the next step of a given plan. Progress is persisted and survives restarts.
    """
    if plan_id not in PLAN_SESSIONS:
        sys.stderr.write(f"Session for '{plan_id}' not found. Loading from disk.\n")
        file_path = os.path.join(resource_path('files'), plan_id)
        if not os.path.exists(file_path):
            return f"Error: Plan file '{plan_id}' not found."
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                steps = [line.strip() for line in f if line.strip()]
            
            state = load_plan_state(plan_id)
            
            PLAN_SESSIONS[plan_id] = {
                "steps": steps,
                "current_step": state.get("current_step", 0)
            }
            sys.stderr.write(f"Loaded plan '{plan_id}'. Resuming from step {PLAN_SESSIONS[plan_id]['current_step'] + 1}.\n")
        except Exception as e:
            return f"Error loading plan file or state for '{plan_id}': {e}"

    session = PLAN_SESSIONS[plan_id]
    current_step_index = session["current_step"]
    
    if current_step_index < len(session["steps"]):
        next_step = session["steps"][current_step_index]
        session["current_step"] += 1
        
        # Save the new state
        save_plan_state(plan_id, {"current_step": session["current_step"]})
        
        return f"Step {current_step_index + 1}/{len(session['steps'])}: {next_step}"
    else:
        return "Plan finished. All steps have been executed."


def reset_plan(plan_id: str) -> str:
    """Resets the execution progress of a given plan, both in memory and on disk."""
    file_path = os.path.join(resource_path('files'), plan_id)
    if not os.path.exists(file_path):
        return f"Error: Plan '{plan_id}' not found, cannot reset."
        
    # Reset in-memory session if it exists
    if plan_id in PLAN_SESSIONS:
        PLAN_SESSIONS[plan_id]["current_step"] = 0
    
    # Reset persistent state
    save_plan_state(plan_id, {"current_step": 0})
    
    return f"Plan '{plan_id}' has been reset to the beginning."


def get_plan_status(plan_id: str) -> str:
    """Gets the current execution status of a given plan."""
    if plan_id not in PLAN_SESSIONS:
        file_path = os.path.join(resource_path('files'), plan_id)
        if os.path.exists(file_path):
            return f"Plan '{plan_id}' exists but has not been started. Call get_next_step to begin execution."
        return f"Error: Plan '{plan_id}' not found."

    session = PLAN_SESSIONS[plan_id]
    total_steps = len(session["steps"])
    current_step_index = session["current_step"]

    if current_step_index < total_steps:
        next_step_to_execute = session["steps"][current_step_index]
        return f"Plan '{plan_id}': On step {current_step_index + 1} of {total_steps}. Next step to execute is: '{next_step_to_execute}'"
    else:
        return f"Plan '{plan_id}': Finished. All {total_steps} steps have been executed."


class NL2FindMCPServer:
    """A TCP server that handles MCP requests for the NL2Find tool."""
    
    def __init__(self, name: str = "NL2Find MCP Server"):
        self.name = name
        self.version = "1.0.0"
        self.tools = {}
        self.PLAN_SESSIONS = {}
        
        # Create a custom httpx client that explicitly disables proxies
        httpx_client = httpx.AsyncClient(proxies=None)

        # Pass the custom client to OpenAI
        self.llm_client = AsyncOpenAI(
            api_key=LLM_CONFIG["apiKey"], 
            base_url=LLM_CONFIG["apiBase"],
            http_client=httpx_client
        )
        self._register_tools()

    def _register_tools(self):
        self.add_tool(
            "create_plan", 
            "Create a plan from a natural language query.", 
            {"query": {"type": "string", "description": "Natural language query for finding files."}}, 
            self.create_plan
        )
        self.add_tool(
            "add_instruction", 
            "Append an instruction to a plan.", 
            {"plan_id": {"type": "string", "description": "The plan file to modify."}, "instruction": {"type": "string", "description": "The instruction to add."}}, 
            self.add_instruction
        )
        self.add_tool(
            "get_next_step", 
            "Executes the next step of a given plan.", 
            {"plan_id": {"type": "string", "description": "The name of the plan file to execute."}}, 
            self.get_next_step
        )
        self.add_tool(
            "reset_plan", 
            "Resets the execution progress of a given plan to the beginning.", 
            {"plan_id": {"type": "string", "description": "The name of a plan file to reset."}},
            self.reset_plan
        )
        self.add_tool(
            "get_plan_status", 
            "Gets the current execution status of a given plan.", 
            {"plan_id": {"type": "string", "description": "The name of the plan file to check."}}, 
            self.get_plan_status
        )

    def add_tool(self, name: str, description: str, parameters: Dict[str, Any], func):
        self.tools[name] = {
            "description": description,
            "inputSchema": {"type": "object", "properties": parameters, "required": list(parameters.keys())},
            "function": func
        }

    async def _call_function(self, func, args):
        if asyncio.iscoroutinefunction(func):
            return await func(**args)
        return func(**args)

    async def handle_request(self, req: Dict[str, Any]) -> Dict[str, Any]:
        method, params, req_id = req.get("method"), req.get("params", {}), req.get("id")
        try:
            if method == "initialize":
                return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": self.name, "version": self.version}, "capabilities": {"tools": {"listChanged": True}}}}
            if method == "tools/list":
                return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [{"name": n, "description": t["description"], "inputSchema": t["inputSchema"]} for n, t in self.tools.items()]}}
            if method == "tools/call":
                tool_name, args = params.get("name"), params.get("arguments", {})
                if tool_name not in self.tools: raise Exception(f"Tool '{tool_name}' not found")
                result = await self._call_function(self.tools[tool_name]["function"], args)
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": str(result)}]}}
            raise Exception(f"Unknown method: {method}")
        except Exception as e:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": str(e)}}

    async def handle_client(self, reader, writer):
        try:
            data = await reader.read(8192)
            if data:
                request_text = data.decode('utf-8')
                header_end = request_text.find('\r\n\r\n')
                if header_end != -1:
                    body = request_text[header_end + 4:]
                    response = await self.handle_request(json.loads(body))
                    response_body = json.dumps(response).encode('utf-8')
                    http_response = (f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(response_body)}\r\nConnection: close\r\n\r\n").encode('utf-8') + response_body
                    writer.write(http_response)
                    await writer.drain()
        except Exception as e:
            sys.stderr.write(f"Client handling error: {e}\n")
        finally:
            writer.close()
            await writer.wait_closed()

    async def run(self, host='127.0.0.1', port=5001):
        server = await asyncio.start_server(self.handle_client, host, port)
        sys.stderr.write(f"Serving on {', '.join(str(sock.getsockname()) for sock in server.sockets)}\n")
        async with server:
            await server.serve_forever()

    async def create_plan(self, query: str) -> str:
        """
        High-level function to process a natural language query, generate a plan file,
        and return the name of the file.
        """
        try:
            structured_query = await self._get_structured_query(query)
            if not structured_query:
                return "Error: Failed to get structured query from LLM."

            output_filename = structured_query.get('output_filename', 'search_results.txt')
            try:
                search_files(
                    search_path=structured_query.get('search_path', '.'),
                    file_patterns=structured_query.get('file_patterns', ['*']),
                    keywords=structured_query.get('keywords', []),
                    output_filename=output_filename
                )
                
                # Load plan into session
                plan_path = os.path.join(resource_path('files'), output_filename)
                with open(plan_path, 'r', encoding='utf-8') as f:
                    steps = [line.strip() for line in f if line.strip()]
                
                self.PLAN_SESSIONS[output_filename] = {
                    "steps": steps,
                    "current_step": 0
                }
                # Create initial state file
                save_plan_state(output_filename, {"current_step": 0})
                
                return f"Plan created and loaded: {output_filename}. Total steps: {len(steps)}"
            except Exception as e:
                return f"Error: Failed to execute search or load plan: {e}"
        except Exception as e:
            return f"Error: Failed to get structured query from LLM: {e}"

    async def _get_structured_query(self, query: str) -> Dict[str, Any]:
        """Uses LLM to convert a natural language query into a structured format."""
        try:
            response = await self.llm_client.chat.completions.create(
                model=LLM_CONFIG["model"],
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": query}
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            if content:
                return json.loads(content)
            return None
        except Exception as e:
            sys.stderr.write(f"Error calling LLM or parsing JSON: {e}\n")
            return None

    async def add_instruction(self, plan_id: str, instruction: str) -> str:
        """Appends a natural language instruction to each line of a plan file."""
        plan_path = os.path.join(resource_path('files'), plan_id)
        if not os.path.exists(plan_path):
            return f"Error: Plan file not found at '{plan_path}'"
        try:
            with open(plan_path, 'r+', encoding='utf-8') as f:
                lines = f.readlines()
                f.seek(0)
                f.truncate()
                for line in lines:
                    base_part = line.split('|', 1)[0].strip()
                    f.write(f"{base_part} | {instruction.strip()}\n")
            
            # Reload plan in session if it exists and reset progress
            if plan_id in self.PLAN_SESSIONS:
                with open(plan_path, 'r', encoding='utf-8') as f:
                    steps = [line.strip() for line in f if line.strip()]
                self.PLAN_SESSIONS[plan_id]['steps'] = steps
                self.PLAN_SESSIONS[plan_id]['current_step'] = 0 # Reset progress
                sys.stderr.write(f"Reloaded and reset plan '{plan_id}' in active session.\n")

            # Reset persistent state as well
            save_plan_state(plan_id, {"current_step": 0})

            return f"Successfully appended instruction to '{plan_id}'. Plan progress has been reset."
        except IOError as e:
            return f"Error updating plan file '{plan_path}': {e}"

    async def get_next_step(self, plan_id: str) -> str:
        """
        Executes the next step of a given plan. Progress is persisted and survives restarts.
        """
        if plan_id not in self.PLAN_SESSIONS:
            sys.stderr.write(f"Session for '{plan_id}' not found. Loading from disk.\n")
            file_path = os.path.join(resource_path('files'), plan_id)
            if not os.path.exists(file_path):
                return f"Error: Plan file '{plan_id}' not found."
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    steps = [line.strip() for line in f if line.strip()]
                
                state = load_plan_state(plan_id)
                
                self.PLAN_SESSIONS[plan_id] = {
                    "steps": steps,
                    "current_step": state.get("current_step", 0)
                }
                sys.stderr.write(f"Loaded plan '{plan_id}'. Resuming from step {self.PLAN_SESSIONS[plan_id]['current_step'] + 1}.\n")
            except Exception as e:
                return f"Error loading plan file or state for '{plan_id}': {e}"

        session = self.PLAN_SESSIONS[plan_id]
        current_step_index = session["current_step"]
        
        if current_step_index < len(session["steps"]):
            next_step = session["steps"][current_step_index]
            session["current_step"] += 1
            
            # Save the new state
            save_plan_state(plan_id, {"current_step": session["current_step"]})
            
            return f"Step {current_step_index + 1}/{len(session['steps'])}: {next_step}"
        else:
            return "Plan finished. All steps have been executed."

    async def reset_plan(self, plan_id: str) -> str:
        """Resets the execution progress of a given plan, both in memory and on disk."""
        file_path = os.path.join(resource_path('files'), plan_id)
        if not os.path.exists(file_path):
            return f"Error: Plan '{plan_id}' not found, cannot reset."
        
        # Reset in-memory session if it exists
        if plan_id in self.PLAN_SESSIONS:
            self.PLAN_SESSIONS[plan_id]["current_step"] = 0
        
        # Reset persistent state
        save_plan_state(plan_id, {"current_step": 0})
        
        return f"Plan '{plan_id}' has been reset to the beginning."

    async def get_plan_status(self, plan_id: str) -> str:
        """Gets the current execution status of a given plan."""
        if plan_id not in self.PLAN_SESSIONS:
            file_path = os.path.join(resource_path('files'), plan_id)
            if os.path.exists(file_path):
                return f"Plan '{plan_id}' exists but has not been started. Call get_next_step to begin execution."
            return f"Error: Plan '{plan_id}' not found."

        session = self.PLAN_SESSIONS[plan_id]
        total_steps = len(session["steps"])
        current_step_index = session["current_step"]

        if current_step_index < total_steps:
            next_step_to_execute = session["steps"][current_step_index]
            return f"Plan '{plan_id}': On step {current_step_index + 1} of {total_steps}. Next step to execute is: '{next_step_to_execute}'"
        else:
            return f"Plan '{plan_id}': Finished. All {total_steps} steps have been executed."

async def main():
    parser = argparse.ArgumentParser(description="NL2Find Tool", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--server', action='store_true', help='Run as MCP server.')
    parser.add_argument('params', nargs='*', help='''
CLI Usage:
- Create plan: "your query"
- Append instruction: <plan.txt> "instruction"
- Get next step: <plan.txt> getnextstep
    ''')
    args = parser.parse_args()

    if args.server:
        kill_process_on_port(5001)
        server = NL2FindMCPServer()
        await server.run()
    else:
        if not args.params:
            parser.print_help()
            return
        
        if len(args.params) == 1:
            result = asyncio.run(server.create_plan(query=args.params[0]))
            print(result)
        elif len(args.params) == 2:
            if args.params[1].lower() == 'getnextstep':
                print(asyncio.run(server.get_next_step(plan_id=args.params[0])))
            else:
                print(asyncio.run(server.add_instruction(plan_id=args.params[0], instruction=args.params[1])))
        else:
            parser.print_help()

if __name__ == "__main__":
    asyncio.run(main()) 