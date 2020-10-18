{
    "type": "wasm",
    "name": "limit-visualization",
    "bid":  1,
    "subtask_timeout": "00:10:00",
    "timeout": "00:10:00",
    "options": {
        "js_name": "micropython.js",
        "wasm_name": "micropython.wasm",
        "input_dir": ".",
        "output_dir": ".",
        "subtasks": {
            "render": {
                "exec_args": ["plot.py"],
                "output_file_paths": ["out.txt"]
            }
        }
    }
}