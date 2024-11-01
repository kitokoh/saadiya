import os
import platform
import subprocess
import re

class ScheduledTaskChecker:
    def __init__(self, program_name):
        self.program_name = program_name

    def check_windows_task(self):
        """Vérifie les tâches planifiées sur Windows."""
        command = 'schtasks /query /fo LIST /v'
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            output = result.stdout.strip()

            if self.program_name in output:
                next_run_time = re.search(r'Next Run Time:\s+(.*)', output)
                if next_run_time:
                    return next_run_time.group(1)
                else:
                    return "Pas de prochaine exécution trouvée."
            else:
                return f"Aucune tâche trouvée pour '{self.program_name}'."
        except Exception as e:
            return str(e)

    def check_macos_launchd(self):
        """Vérifie les programmes lancés avec launchd sur macOS."""
        command = f"launchctl list | grep '{self.program_name}'"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        if result.stdout:
            command_plist = f"cat ~/Library/LaunchAgents/{self.program_name}.plist"
            plist_result = subprocess.run(command_plist, capture_output=True, text=True, shell=True)

            if plist_result.stdout:
                matches = re.findall(r'<key>StartCalendarInterval</key>\s*<dict>.*?<key>Hour</key>\s*<integer>(\d+)</integer>.*?<key>Minute</key>\s*<integer>(\d+)</integer>', plist_result.stdout, re.DOTALL)
                if matches:
                    next_run_times = [f"{hour}:{minute}" for hour, minute in matches]
                    return "Prochaines exécutions: " + ", ".join(next_run_times)
                else:
                    return "Pas de prochaines exécutions trouvées."
            else:
                return "Aucune information trouvée dans launchctl."
        else:
            return f"Aucun programme trouvé pour '{self.program_name}'."

    def check_task(self):
        """Vérifie le système d'exploitation et appelle la méthode appropriée."""
        if platform.system() == "Windows":
            return self.check_windows_task()
        elif platform.system() == "Darwin":  # macOS
            return self.check_macos_launchd()
        else:
            return "Système d'exploitation non pris en charge."


def main():
    program_name = input("Entrez le nom de la tâche/programme à vérifier : ")
    task_checker = ScheduledTaskChecker(program_name)
    next_run = task_checker.check_task()
    print(next_run)


if __name__ == "__main__":
    main()
