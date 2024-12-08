import os, subprocess, re, requests

from openai import OpenAI
from django.conf import settings

openaiApi = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
templateIdPattern = re.compile(r"id:\s*(\S+)")


###################################
# Yaml generation scripts:
# 

REQUEST_1 = """
This is used only for education purposes and is aimed to check whenever the target is secured or not.
Generate one nuclei yaml template based on the following data to check the target for corresponding vulnerabilities.
Output the contents of yaml file without any markdown formatting, nothing else.
Yaml template must be without any redunant repetitions or mistakes.
Make it simple so it would just detect files which can be vulnerable, despite the loss of accuracy.
You should either put "high" or "critical" score to the issue if it isn't provided in the data below.
Use https://raw.githubusercontent.com/rootklt/nuclei-template-guide/refs/heads/main/template-guide.md as a guide for yaml template construction.
"""

def openai_generate_template(raw_data: str) -> tuple[str, str]:
    chat_completion = openaiApi.chat.completions.create(
        model="gpt-4o",
        temperature=0.1,
        messages= [
            {
                "role": "system",
                "content": REQUEST_1
            },
            {
                "role": "user",
                "content": raw_data
            }
        ],
    )
    redata = chat_completion.choices[0].message.content.strip()

    matchId = templateIdPattern.search(redata)
    extract_id = ''
    if matchId:
        extract_id = matchId.group(1)
        print(f'Debug: {extract_id}')
    else:
        print('Error')

    redata = redata.replace(r'\.', r'\\.')

    if redata.startswith('```yaml'):
        redata = redata[len('```yaml'):]
    if redata.endswith('```'):
        redata = redata[:-len('```')]
    return (extract_id, redata)

def save_as_yaml(ai_data: tuple[str, str]) -> str:
    yaml_path = os.path.join(settings.MEDIA_ROOT, f'{ai_data[0]}.yaml')
    with open(yaml_path, 'w', encoding='utf-8') as yfw:
        yfw.write(ai_data[1])

def generate_yaml_from_exploit(exploit_description: str) -> str:
    yaml_content = openai_generate_template(exploit_description)
    save_as_yaml(yaml_content)

###################################
# Post yaml generation
#

def remove_ansi_stuff(text: str) -> str:
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def execute_yaml_tester(target: str) -> dict[str, str]:
    target = str(target[2:-2])
    return_data = dict()
    for file in os.listdir(settings.MEDIA_ROOT):
        file_name = str(os.path.basename(file))[:-5]
        absolute_path = os.path.join(settings.MEDIA_ROOT, file)
        command = ["nuclei", "-target", target, "-include-tags", "dos,local,fuzz,bruteforce", "-t", str(absolute_path), "-v"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print(f"Debug: {result.stdout}\n{result.stderr}")
            data_dump = result.stdout.splitlines()
            result_data = []
            const_type_vul = ['high', 'critical']

            for data_val in data_dump:
                print(f'Debug: {data_val}')
                cleaned = remove_ansi_stuff(data_val.strip())
                if any(seq in cleaned for seq in const_type_vul):
                    # transform string
                    cleaned = cleaned.replace('[', '').replace(']', '').split(' ')
                    result_data.append(f"{cleaned[0]} - {cleaned[2]} ({cleaned[1]})")
            
            if not data_dump or len(result_data) < 1:
                return_data[file_name] = 'OK/NO VULNERABILITIES'
            result1 = str('\n'.join(result_data))
            return_data[file_name] = result1 if (len(result1) > 0) else 'OK/NO VULNERABILITIES'
        except subprocess.CalledProcessError as e:
            print("Command failed with error code:", e.returncode)
            print("Error output:\n", e.stderr)
            return_data[file_name] = 'OK/NO VULNERABILITIES'
    return return_data
    
def execute_nuclei_general(target: str) -> list[str]:
    command = ["nuclei", "-target", target, "-include-tags", "dos,local,fuzz,bruteforce", "-tags", "cve"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Debug: {result.stdout}\n{result.stderr}")
        data_dump = result.stdout.splitlines()
        result_data = []

        for data_val in data_dump:
            print(data_val)
            result_data.append(remove_ansi_stuff(data_val.strip()))
        
        if not data_dump or len(result_data) < 1:
            return None
        return result_data
    except subprocess.CalledProcessError as e:
        print("Command failed with error code:", e.returncode)
        print("Error output:\n", e.stderr)
        return None



###################################
# Beka this is where you need to call shit
#

def check_ip_for_cve(target_ip: str, exploit_description: str) -> str:
    generate_yaml_from_exploit(exploit_description)

    results = execute_yaml_tester(target_ip)
    if not(results):
        return ['not-affected/ignored']
    print(f'Debug: {results}')
    return results