#from globals import subprocess, time, timeit
import subprocess

#mylist = ["cue_cards", "mindmap", "tasks"]
x = 2   #int(input("which script number?"))

var_scripts = {
    "1": "./discord_bot/v2024/disbot3.py",
    "2": "./mindmap.py",
    "3": "./imgur.py",
    "4": "./tasks3.py",
    "5": "./cuecards.py",
    "6": "./globals.py",
    "7": "./troal.py",
}

print(f"About to run {var_scripts[f'{x}']}")

#start_time = time.time()
y = subprocess.run(["python3", str(var_scripts[f"{x}"])])
#y = subprocess.run(["python3", str(f'./{x}/program.py')])
#end_time = time.time()

#execution_time = round((end_time - start_time), 2)

#program_time = timeit.timeit('y', globals=globals(), number=1)
#print(f"Successfuly ran {var_scripts[f'{x}']}\nProgram time: {round((program_time * (10 ** 6)), 2)} μs\nExecution time: {execution_time} s")
