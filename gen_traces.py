import os
import sys
import subprocess
import shutil
import glob
import argparse

TRACER_TOOL_PATH = "./util/tracer_nvbit/tracer_tool/tracer_tool.so"
POST_PROCESSING_TOOL_PATH = "./util/tracer_nvbit/tracer_tool/traces-processing/post-traces-processing"

def parse_args():
    parser = argparse.ArgumentParser(description="Generate NVBit traces for CUDA applications")
    parser.add_argument("--app", required=True, help="Path to CUDA executable")
    parser.add_argument("--args", nargs=argparse.REMAINDER, help="Arguments passed to the CUDA executable.", default=[])
    parsed_args = parser.parse_args()

    if not os.path.isfile(parsed_args.app):
        print(f"ERROR: CUDA Executable does not exist: {executable}")
        sys.exit(1)
    
    return parsed_args

def run_traced_executable(executable, exec_args):
    tracer_path = os.path.abspath(TRACER_TOOL_PATH)

    if not os.path.isfile(tracer_path):
        print(f"ERROR: tracer_tool.so not found at {tracer_path}")
        sys.exit(1)

    cmd = f"LD_PRELOAD={tracer_path} {executable} {' '.join(exec_args)}"
    print(f"Running executable with NVBit tracer:")
    subprocess.run(cmd, shell=True, check=True)

def move_traces(executable, exec_args):
    src = os.path.abspath("./traces")
    if not os.path.isdir(src):
        print("ERROR: No traces/ folder found after running the executable.")
        sys.exit(1)

    parent_dir = os.path.dirname(os.path.abspath(executable))
    exe_name = os.path.basename(executable)

    safe_args = "_".join(arg.replace("/", "_") for arg in exec_args)
    unique_folder = f"{exe_name}_{safe_args}" if safe_args else exe_name

    dest = os.path.join(parent_dir, unique_folder, "traces")
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    print(f"Moving traces to: {dest}")
    shutil.move(src, dest)

    return dest

def run_post_processing(traces_dir):
    post_proc = os.path.abspath(POST_PROCESSING_TOOL_PATH)
    kernel_list = glob.glob(os.path.join(traces_dir, "kernelslist_ctx_*"))

    if not kernel_list:
        print("ERROR: No kernelslist_ctx_* file found in traces directory.")
        sys.exit(1)

    kernel_list_file = kernel_list[0]
    print(f"Running post-traces-processing on: {kernel_list_file}")

    subprocess.run([post_proc, kernel_list_file], check=True)

def main():
    parsed_args = parse_args()
    executable = parsed_args.app
    exec_args = parsed_args.args

    run_traced_executable(executable, exec_args)
    traces_dir = move_traces(executable, exec_args)
    run_post_processing(traces_dir)

    print("Traces generated and processed successfully")

if __name__ == "__main__":
    main()
