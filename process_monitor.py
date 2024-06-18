import os
import sys
import win32api
import win32con
import win32security
import wmi


def log_to_file(message):
    with open(file="process_monitor_log.csv", mode="a") as f:
        f.write(f"{message}\r\n")


def monitor():
    csv_header = "Command-Line, Time, Executable, Parent PID, PID, User, Privileges"
    log_to_file(message=csv_header)
    c = wmi.WMI()
    process_watcher = c.Win32_Process.watch_for('creation')  # start watch for process creation event

    while True:
        try:
            new_process = process_watcher()
            cmdline = new_process.CommandLine
            create_date = new_process.CreationDate
            executable = new_process.ExecutablePath
            parent_pid = new_process.ParentProcessId
            pid = new_process.ProcessId
            proc_owner = new_process.GetOwner()

            privileges = "N/A"
            process_log_message = f"{cmdline}, {create_date}, {executable}, {parent_pid}," \
                                  f"{pid}, {proc_owner}, {privileges}"
            # print(f"{process_log_message}\n")
            log_to_file(message=process_log_message)

            print("\n════════════════════════════════════════════════════════════════════════════")
            print(f"[1]: Command-Line    »» {cmdline}")
            print(f"[2]: Creation Date   »» {create_date}")
            print(f"[3]: Executable Path »» {executable}")
            print(f"[4]: Parent PID      »» {parent_pid}")
            print(f"[5]: PID             »» {pid}")
            print(f"[6]: Owner           »» {proc_owner}")
            print(f"[7]: Privileges      »» {privileges}")
            print("════════════════════════════════════════════════════════════════════════════\n")

        except KeyboardInterrupt:
            sys.exit(0)
        except Exception:
            pass


if __name__ == "__main__":
    monitor()
